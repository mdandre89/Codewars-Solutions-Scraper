import requests
import sys
import os
from pprint import pprint

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

language_map = {
    "agda": "agda", "bf": "b", "c": "c", "cmlf": "cmfl","clojure": "clj", "cobol": "cob",
    "coffeescript": "coffee", "commonlisp": "lisp","coq": "coq", "cplusplus": "cpp", "crystal": "cr",
    "csharp": "cs","dart": "dart", "elixir": "ex", "elm": "elm", "erlang": "erl","factor": "factor",
    "forth": "fth", "fortran": "f", "fsharp": "fs","go": "go", "groovy": "groovy", "haskell": "hs",
    "haxe": "hx","idris": "idr", "java": "java", "javascript": "js", "julia": "jl","kotlin": "kt",
    "lean": "lean", "lua": "lua", "nasm": "nasm","nimrod": "nim", "objective": "m", "ocaml": "ml",
    "pascal": "pas","perl": "pl", "php": "php", "powershell": "ps1", "prolog": "pro",
    "purescript": "purs", "python": "py", "r": "r", "racket": "rkt","ruby": "rb", "rust": "rs",
    "scala": "scala", "shell": "sh","sql": "sql", "swift": "swift", "typescript": "ts", 
    "vb": "vb"
    }

def create_folder(name):
    parent_dir = os.path.abspath(os.getcwd())
    path = os.path.join(parent_dir, name)
    if not os.path.isdir(path):
        os.mkdir(path)
        print("Directory '% s' created" % name)

DRIVERFOLDER = os.getenv('DRIVERFOLDER')

codewars_username = sys.argv[1:][0]
github_username = sys.argv[1:][1]
github_pwd = sys.argv[1:][2]

def sign_codewars( driver, githubUsername, github_pwd):
    try:
        driver.get("https://www.codewars.com/users/sign_in")
        siginForm = driver.find_element(By.ID, "new_user")
        siginForm.find_element(By.TAG_NAME, "button").click()
        driver.find_element(By.ID, "login_field").send_keys(github_username)
        driver.find_element(By.ID, "password").send_keys(github_pwd)
        driver.find_element(By.NAME, "commit").click()
        time.sleep(3)
        otp_code = input("Enter OTP code(press Enter if not received any message): ")
        if(otp_code):
            time.sleep(3)
            # it logins authomatically if receving a 6 digit number
            driver.find_element(By.ID, "otp").send_keys(otp_code) 
        print("Logged in\n")
    except:
        print("Cannot Login\n")
        sys.exit(0)

# getting the completed katas
errors = []
new_data = []
not_downloaded = []
for i in range(10):
    URL = f'https://www.codewars.com/api/v1/users/{codewars_username}/code-challenges/completed?page='+str(i)
    new_data += requests.get(URL).json()['data']

number_of_solutions=0
for kata in new_data:
    for language in kata['completedLanguages']:
        number_of_solutions+=1
print(f"{number_of_solutions} Solutions to be downloaded\n")

## Setup chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")

# Set path to chromedriver as per your configuration
driver_folder= os.path.abspath(os.getcwd())+"/../chromedriver/stable/chromedriver" if DRIVERFOLDER else os.path.abspath(os.getcwd())+"/chromedriver/stable/chromedriver"
print("driver_folder", driver_folder)
webdriver_service = Service(driver_folder)
browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# login
sign_codewars(browser, github_username, github_pwd)

# Directory Creation
directory = "completed"
create_folder(directory)

for kata in new_data:
    for language in kata['completedLanguages']:
        if kata.get('slug', None):
            id = kata['id']
            slug = kata['slug']
            parent_dir = os.path.abspath(os.getcwd())
            create_folder(os.path.join(directory, slug))
            file_name = slug + "." + language_map.get(language, 'errorlanguage')

            save_path = os.path.join(parent_dir, os.path.join(directory, slug))
            complete_file_path = os.path.join(save_path, file_name)
            complete_readme_path = os.path.join(save_path, 'README.md')

            kata_info = {}
            try:
                URL_description = f'https://www.codewars.com/api/v1/code-challenges/{id}'
                kata_info = requests.get(URL_description, timeout=2).json()
            except:
                message = f'Error while retrieving kata info for {id}.\n'
                print(message)
                errors.append(message)

            URL = f'https://www.codewars.com/kata/{id}/solutions/{language}/me/newest'
            browser.get(URL)
            time.sleep(10)

            solutionCode = ""
            try:
                solutionsList = browser.find_element(By.ID, "solutions_list");
                solutionItem = solutionsList.find_element(By.TAG_NAME, "li");
                solutionCode = solutionItem.find_element(By.TAG_NAME, "pre").text;
            except:
                message = f'Error while scraping solutions for {id}, No DOM elements found.\n'
                print(message)
                errors.append(message)

            try:
                with open(complete_readme_path, 'w') as readme:
                    readme.write('# '+kata.get('name', 'no name found') + "\n\n")
                    readme.write(' - URL:'+ '[' + f'https://www.codewars.com/kata/{id}' + '](' + f'https://www.codewars.com/kata/{id}' + ')' + "\n")
                    readme.write(' - Id: '+ id + "\n")
                    readme.write(' - Language: '+ language + "\n")
                    readme.write(' - Completed on: '+kata.get('completedAt', 'no name found')+ "\n")
                    readme.write(' - Tags: ' + ','.join(kata_info.get('tags',[])) + "\n")
                    readme.write(' - Description:\n' + kata_info.get('description', 'N\A') + "\n")
            except:
                message = "Not able to write Readme for" + complete_readme_path + "\n"
                print(message)
                errors.append(message)

            try:
                if solutionCode:
                    with open(complete_file_path, "w") as solution_file:
                        solution_file.write(solutionCode)
                    print(f"Solution to {slug} downloaded.\n")
                else:
                    not_downloaded.append(slug)
            except:
                errors.append(slug)
                not_downloaded.append(slug)
                print("Not able to write" + complete_file_path + " \n")

            number_of_solutions-=1
            print(f"{number_of_solutions} Solutions left to be downloaded.\n")


print("All the solutions have been retrieved\n")
print('These were the errors\n', errors)
print('These are the katas not downloaded\n', not_downloaded)

time.sleep(10)
browser.quit()
