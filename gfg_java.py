from seleniumbase import Driver
from pynput import keyboard
import time
import psutil

# Function to close all existing Chrome processes
def close_existing_chrome_processes():
    for proc in psutil.process_iter():
        try:
            if "chrome" in proc.name().lower():
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

# Close existing Chrome windows
close_existing_chrome_processes()

driver = Driver(uc=True,user_data_dir="C:\\Users\\ADITYA\\AppData\\Local\\Google\\Chrome\\User Data",chromium_arg="--profile-directory=Default")

driver.maximize_window()

# Open the first webpage
driver.get('view-source:file:///D:/OneDrive/Documents/GFG_JAVA/gfg_java.txt')

# Read URLs from a text file
file_path = 'gfg_java.txt'
with open(file_path, 'r') as file:
    urls = file.readlines()
# Strip newline characters from each URL
urls = [url.strip() for url in urls]

# The last webpage
urls.append("https://www.geeksforgeeks.org/")

index = 0
shift_pressed = False
ctrl_pressed = False

# Function to insert new page
def insert_page():
    global index
    global urls
    driver.execute_script('''
        var url = prompt('Enter URL :');
        if(url!=null && url!='')
            alert(url+' is added successfully!');
        else 
            alert('Try again!');
    ''')
    alert = driver.switch_to.alert
    input_text = alert.text
    while input_text=='Enter URL :':
        input_text = alert.text
    input_text = input_text[:-23]
    if input_text:
        with open('gfg_java.txt', 'r') as file:
            lines = file.readlines()
            if(index==len(urls)-1):
                 lines[index-1] = lines[index-1].rstrip('\n') + '\n' + input_text + '\n'
            else:
                lines[index] = lines[index].rstrip('\n') + '\n' + input_text + '\n'
        with open('gfg_java.txt', 'w') as file:
            file.writelines(lines)
        if(index==len(urls)-1):
            urls = urls[:index] + [input_text] + urls[index:]
        else:
            urls = urls[:index+1] + [input_text] + urls[index+1:]

# Function to go to a page
def go_to_page():
    global index
    global ctrl_pressed
    driver.execute_script('''
        var page_no = prompt('Go To Page No :');
        var num = parseInt(page_no);
        if(Number.isInteger(num))
        {
            if(num.toString()==page_no && num>0)
                alert('Going to page ' + page_no);
            else
                alert('Try again!');  
        }
        else 
        {
            alert('Try again!');
        }
    ''')
    alert = driver.switch_to.alert
    input_text = alert.text
    while input_text=='Go To Page No :':
        input_text = alert.text
    input_text = input_text[14:]
    if input_text:
        try:
            index_to_go = int(input_text) - 1
            if index_to_go>=0 and index_to_go!=index and index_to_go<len(urls):
                index = index_to_go
                driver.get(urls[index])
            else:
                alert.accept()
        except:
            pass
    ctrl_pressed = False

# Function to navigate to the next and previous URL
def navigate(key):
    global index
    global shift_pressed
    global ctrl_pressed
    global urls
    if key == keyboard.Key.shift_l:
        shift_pressed = True
    if key == keyboard.Key.ctrl_l:
        ctrl_pressed = True
    if shift_pressed:
        if key == keyboard.Key.right and index!=len(urls) - 1:
            index = len(urls)-1
            driver.get(urls[index])
            shift_pressed = False
        elif key == keyboard.Key.left and index!=0:
            index = 0
            driver.get(urls[index])
            shift_pressed = False
    elif ctrl_pressed == True:
        if(key == keyboard.Key.right):
            go_to_page()
    else:
        if key == keyboard.Key.right and index < len(urls) - 1:
            index += 1
            driver.get(urls[index])  # Navigate forward
        elif key == keyboard.Key.left and index > 0:
            index -= 1
            driver.get(urls[index])  # Navigate backward
        elif key == keyboard.Key.insert:
            insert_page()

# Function to handle key release events
def on_release(key):
    global shift_pressed
    global ctrl_pressed
    if key == keyboard.Key.shift_l:
        shift_pressed = False
    if key == keyboard.Key.ctrl_l:
        ctrl_pressed = False

listener = keyboard.Listener(on_press=navigate, on_release=on_release)
listener.start()

# Keep the main thread running
while True:
    time.sleep(1)
