import os
import platform

def get_chrome_path(BASE_DIR=None):
    get_platform = platform.platform()
    chrome_driver_path = ""
    chrome_path = ""

    if "Linux" in get_platform:
            chrome_driver_path = os.path.join(BASE_DIR, "../../chromedriver/chromedriver")
            chrome_path = r'"/opt/google/chrome/chrome"'
            # Create an instance
    else:
        # Define the path where the chrome driver is installed on your computer
        chrome_driver_path = r"D:\Python\RoboWritely\ContentCreation\chromedriver\chromedriver.exe"
        # the sintax r'"..."' is required because the space in "Program Files"
        # in my chrome_path
        chrome_path = r'"C:\Program Files (x86)\Google\Chrome\Application\Chrome.exe"'

    return chrome_path, chrome_driver_path

def create_file(filename, content, directory_name="conversations"):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    with open(os.path.join(directory_name, filename), "a") as file:
        file.write(content)


def clean_chat_gpt_response(content, word_list, trim_comma=False):
     
    for i in word_list:
          content = content.replace(i, "")
    
    if content.startswith('"') and content.endswith('"'):
        content = content[1:-1]
    
    return content