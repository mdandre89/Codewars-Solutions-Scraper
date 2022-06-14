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
        print("jhelp")
    except:
        print("cannot navigate")
        sys.exit(0)

# getting the completed katas
new_data = []
for i in range(20):
    URL = f'https://www.codewars.com/api/v1/users/{codewars_username}/code-challenges/completed?page='+str(i)
    new_data += requests.get(URL).json()['data']

## Setup chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")

# Set path to chromedriver as per your configuration
webdriver_service = Service(os.path.abspath(os.getcwd())+"/scraper/chromedriver/stable/chromedriver")
browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# login
sign_codewars(browser, github_username, github_pwd)

# Directory Creation
directory = "Completed"
parent_dir = os.path.abspath(os.getcwd())
path = os.path.join(parent_dir, directory)
if not os.path.isdir(directory):
    os.mkdir(path)
    print("Directory '% s' created" % directory)

for kata in new_data:
    for language in kata['completedLanguages']:
        if i.get('slug', None):
            id = kata['id']
            slug = kata['slug']
            parent_dir = os.path.abspath(os.getcwd())
            save_path = os.path.join(parent_dir, directory)
            file_name = slug + "." + language_map.get(language, 'errorlanguage')
            complete_file_name = os.path.join(save_path, file_name)

            URL = f'https://www.codewars.com/kata/{id}/solutions/{language}/me/newest'
            browser.get(URL)
            time.sleep(10)

            solutionCode = ""
            try:
                solutionsList = browser.find_element(By.ID, "solutions_list");
            except:
                print("no solutionsList")

            try:
                solutionItem = solutionsList.find_element(By.TAG_NAME, "li");
            except:
                print("no solutionItem")

            try:
                solutionCode = solutionItem.find_element(By.TAG_NAME, "pre").text;
                print(solutionCode)
            except:
                print("no solutionCode")

            try:
                file = open(complete_file_name, "w")
                # file.write(URL.replace("/me/newest", "") + "\n")
                file.write(solutionCode)
                file.close()
            except:
                print("not able to write" + complete_file_name)


time.sleep(10)
browser.quit()
