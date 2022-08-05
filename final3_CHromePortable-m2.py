import time
#import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service       # Useing as Service because of deprecated-Warning
from webdriver_manager.chrome import ChromeDriverManager     #AK-Note: to simplify management of binary drivers for different browsers.
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By             #Because OF: UserWarning: find_element_by_* commands are deprecated. Please use find_element() instead
import requests # to get image from the web
import shutil # to save it locally - AK: disabled, not requiered right now
from selenium.webdriver.common.action_chains import ActionChains
from pynput.keyboard import Key, Listener
import pyautogui


FILE_NAME_PROFILE = r'C:\Program Files_Portable\GoogleChromePortable_96\Data\profile' # read chrome-profiles
#C:\Program Files_Portable\GoogleChromePortable_96\Data\profile ---ORG Path to profile, asfter "install"

currency_list = []
dataframe_list = []
strategy_list = []
tsl_pairs_list = []

#curreny_file = open("Currencies _TOP 15.txt", "r")
curreny_file = open("Currencies.txt", "r")

lines = curreny_file.read().splitlines()

for line in lines:
    currency_list.append(line.strip())

print (currency_list)

dataframe_file = open("Dateframes.txt", "r")
lines = dataframe_file.read().splitlines()

for line in lines:
    dataframe_list.append(line.strip())

print (dataframe_list)

strategy_file = open("Strategies-Free.txt", "r")
lines = strategy_file.read().splitlines()

for line in lines:
    strategy_list.append(line.strip())

print (strategy_list)

tsl_pairs_file = open("TSL-pairs_TOP8.txt", "r")
lines = tsl_pairs_file.read().splitlines()

for line in lines:
    tsl_pairs_list.append(line.strip())

print (tsl_pairs_list)


option = Options()
option.add_argument("start-maximized")
#option.add_argument('--headless') # without GUI output
#option.add_argument('--no-sandbox')
option.add_argument('--no-default-browser-check')
option.add_argument('--no-first-run')
option.add_argument('--disable-extensions')
option.add_argument('--disable-default-apps')
option.add_argument('--disable-gpu') # to be safe while using VM
option.add_argument("user-data-dir=" + FILE_NAME_PROFILE) # SET/give Chrome-Profile dir
option.add_argument("profile-directory=Profile 1")          # Use Specific Chrome-Profile

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

 
main_url = 'https://www.cryptohopper.com/hoppers?set=11115d7&to=backtesting'
driver.get(main_url)
time.sleep(1)

#-------------------------------------------------------------------------IF redirected to LOGIN_START - autologin Captcha muss noch manuell gemacht werden 

# if driver.current_url == 'https://www.cryptohopper.com/login':  
if driver.current_url == 'https://www.cryptohopper.com/log-in':  
    #time.sleep(2)

    close_button = ""
    all_buttons = driver.find_elements_by_tag_name('button')
    for button in all_buttons:
        #print (button.text)
        if ("Cancel" in button.text):
            close_button = button
            break
        
    #close_button = driver.find_element_by_class_name('close')
    #driver.execute_script("arguments[0].click();", close_button) # throws error 
    time.sleep(1)

    #username = driver.find_element_by_id('username')
    username = driver.find_element(By.ID, 'username')

    username.send_keys('HansiMayer')
    #password = driver.find_element_by_id('password')
    password = driver.find_element(By.ID, 'password')
    password.send_keys(' ')

    #login_button = driver.find_element_by_id('submitOr2faButton')
    login_button = driver.find_element(By.ID, 'submitOr2faButton')
    driver.execute_script("arguments[0].click();", login_button)

    time.sleep(1)

    def show(key):
    
        print('\nYou Entered {0}'.format( key))
    
        if key == Key.enter:
            # Stop listener
            return False
    
    # Collect all event until released
    with Listener(on_press = show) as listener:   
        listener.join()
    print(driver.current_url)  
    time.sleep(1)
#-------------------------------------------------------------------------IF redirected to LOGIN_END


index = 0
for currency_index in range(len(currency_list)):
    for dataframe_index in range(len(dataframe_list)):
        for strategy_index in range(len(strategy_list)):
            for tsl_pairs_index in range(len(tsl_pairs_list)):
                currency = currency_list[currency_index]
                dateframe = dataframe_list[dataframe_index]
                strategy  = strategy_list[strategy_index]
                trailing_stop_loss_percentage = tsl_pairs_list[tsl_pairs_index].strip().split("|")[0]
                arm_trailing_stop_loss_at = tsl_pairs_list[tsl_pairs_index].strip().split("|")[1]

                print ("iteration :", index+1)
                print ("currency :", currency)
                print ("dateframe :", dateframe)
                print ("strategy :", strategy)
                print ("trailing_stop_loss_percentage :", trailing_stop_loss_percentage)
                print ("arm_trailing_stop_loss_at :", arm_trailing_stop_loss_at)
                
                # currency test - select item id - coin_test -> select by value
                #select_currency_element = Select(driver.find_element_by_id('coin_test'))
                select_currency_element = Select(driver.find_element(By.ID, 'coin_test'))

                # select by value 
                select_currency_element.select_by_value(currency)


                #-----------------------------------Problem mit FOUND best Config bei Strategieauswahl
                #if  driver.find_element_by_class_name('best_config_div_test'):
                # strategy - select item id - strategy -> read each option and select
                # First find all options inside strategy select and find the appropriate value

                

                """ result_ul = driver.find_element_by_id('select2-results-1')
                for i in result_ul.find_elements_by_class_name('select2-result'):
                    print(i.text) """


                #search_input = driver.find_element_by_class_name('select2-search').find_element_by_tag_name('input')
                
                #search_input = driver.find_element(By.CLASS_NAME, 'select2-search').find_element(By.TAG_NAME, 'input')
                search_input = driver.find_element(By.XPATH, '//input[@id="s2id_autogen1_search"]')

                """   Wenn EXIISTS --> Current best configuration for ...""" 

                            
                strategy_element = driver.find_element_by_id('s2id_strategy')

                ac = ActionChains(driver)
                ac.move_to_element(strategy_element).click().perform()

                time.sleep(5)

                ##result_ul = driver.find_element_by_id('select2-results-1')
                ##for i in result_ul.find_elements_by_class_name('select2-result'):
                ##    print (i.text)

                search_input = driver.find_element_by_class_name('select2-search').find_element_by_tag_name('input')
                search_input.clear()
                search_input.send_keys(strategy)

                ##print ("After")
                ##result_ul = driver.find_element_by_id('select2-results-1')
                ##for i in result_ul.find_elements_by_class_name('select2-result'):
                ##    print (i.text)

                #select_btn = driver.find_element_by_class_name('select2-result-sub').find_element_by_tag_name('li')
                #print ("select_btn :", select_btn.text)
                #driver.execute_script("arguments[0].click();", select_btn)
                pyautogui.press('enter')
                
               
                ##print ("After")
                ##result_ul = driver.find_element_by_id('select2-results-1')
                ##for i in result_ul.find_elements_by_class_name('select2-result'):
                ##    print (i.text)

                #select_btn = driver.find_element_by_class_name('select2-result-sub').find_element_by_tag_name('li')
                #print ("select_btn :", select_btn.text)
                #driver.execute_script("arguments[0].click();", select_btn)
                pyautogui.press('enter')

                time.sleep(3)

                # div class=form-group wala 'Trailing stop-loss' text thiye nm span eka click karanna <- trading perc. buy add karana switch eka
                # div class=form-group wala 'Use trailing stop-loss only' text thiye nm span eka click karanna <- trading perc. buy add karana switch eka
                # 'Select period' text thiye nm span eka click karanna <- period eka danna
                if (index == 0):
                    all_form_group_divs = driver.find_elements_by_class_name('form-group')
                    for div in all_form_group_divs:
                        try:
                            label = div.find_element_by_tag_name("label").text
                            #print ("label : ", label)
                            if ('Trailing stop-loss' in label or 'Use trailing stop-loss only' in label or 'Select period' in label):
                                span = div.find_element_by_tag_name("span")
                                driver.execute_script("arguments[0].click();", span)
                        except:
                            continue

                # id - stop_loss_trailing_percentage_test
                # id - stop_loss_trailing_arm_test

                stop_loss_trailing_percentage_element = driver.find_element_by_id('stop_loss_trailing_percentage_test')
                stop_loss_trailing_percentage_element.clear()
                time.sleep(1)
                stop_loss_trailing_percentage_element.send_keys(trailing_stop_loss_percentage)

                arm_trailing_stop_loss_at_element = driver.find_element_by_id('stop_loss_trailing_arm_test')
                arm_trailing_stop_loss_at_element.clear()
                time.sleep(1)
                arm_trailing_stop_loss_at_element.send_keys(arm_trailing_stop_loss_at)

                # id - date_range_test
                date_range_test_element = driver.find_element_by_id('date_range_test')
                date_range_test_element.clear()
                time.sleep(1)
                date_range_test_element.send_keys(dateframe)

                time.sleep(2)

                # start btn id - submitConfigTest
                # stop button text - Stop backtest
                start_button = driver.find_element_by_id('submitConfigTest')
                driver.execute_script("arguments[0].click();", start_button)
                print ("start button clicked")
                time.sleep(5)
                while True:
                    is_stop_btn_exist = False
                    all_btns = driver.find_element_by_id('backtest-config').find_elements_by_tag_name('button')
                    for btn in all_btns:
                        if ("Stop backtest" in btn.text):
                            is_stop_btn_exist = True
                    if (is_stop_btn_exist == False):
                        break
                    time.sleep(4)
                index += 1
                print ("process is stopped")
