"""
Yealink configure script made for cool IT colleagues
Created Date: 28.01.2018
Written by artafo

abbreviations:
NR - (needs refactoring) indicator that a code needs refactoring
CS - (changed for security) indicator that insecure part of code was changed before publication
"""
from splinter import Browser
# THREADING import threading
from selenium import webdriver
# import getpass



# functions
#
def login_in_web(pas):
    if browser.is_element_present_by_name('username'):  # OPTIMIZ
        print("     Ok, we're on the login page")
    else:
        print("\n     It's not the login page...\nLogin in manually and press enter")
        input()
        return

    print("     Trying to login...")
    # pass_web_cur = getpass.getpass(prompt='\nInput web admin pass: ', stream=None)
    browser.find_by_name('username').first.fill(login_web)
    browser.find_by_name('pwd').first.fill(pas)
    browser.find_by_id('idConfirm').click()

    if browser.is_element_present_by_id('tdFirmware'):
        print("         Ok, we're inside...")
    else:
        print("\n     Fail! Login in manually and press enter")
        if browser.find_by_name('username').first:
            browser.find_by_name('username').first.fill(login_web)
        input()
        return


def br_init():
    global browser
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--hide-scrollbars')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument("--disable-logging")
    browser = Browser('chrome')

""" Not needed func while we are using while loop in Main part
def exit_script(exit_code, reboot_flag):
    print("\n\n==========  End  ==========")
    if reboot_flag:
        reboot_req = input("Reboot yealink? (y/n(or just enter)): ").lower()
        if reboot_req == "y":
            print("Rebooting...")
            browser.visit(yealink_web + "/servlet?p=settings-upgrade&q=load")
            browser.execute_script('document.getElementsByName("formAction")[0].action = "/servlet?p=settings-upgrade&q=reboot"')
            browser.execute_script('document.formAction.submit()')
    if browser:
        browser.quit()
    exit(exit_code)
"""

# var
#
yealink_web = ""
yealink_web_preset = "http://192.168.1" # CS
login_web = "admin"
pass_web_cur = "admin"
pass_web_new = ""
ntp_1 = "192.168.1.100" # CS 
ntp_2 = "192.168.1.100" # CS 



# ========== Main ==========
#
print("\n\nInit browser...")
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--hide-scrollbars')
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument("--disable-logging")
browser = Browser('chrome', chrome_options)
# THREADING br_init_th = threading.Thread(target=br_init)
# THREADING br_init_th.start()

while True:
    # ===== Gathering information =====
    print("\n\n\n\n* Gathering information")
    while True:
        yealink_web = input("      Enter yealink's IP ( 'c' for change ip preset ) " + yealink_web_preset)
        if yealink_web.lower() == 'c':
            yealink_web_preset = "http://" + input("            http://")
            continue
        break
    yealink_web = yealink_web_preset + yealink_web;
    username_yealink = input("      Enter Yealink's Username (ex: artafo): ")


    # ===== Login =====
    print("\n========== Begin ==========\n")
    # THREADING if br_init_th.is_alive():
    # THREADING     br_init_th.join()
    print("* Logging in")
    browser.visit(yealink_web.strip())
    login_in_web(pass_web_cur)


    # ===== Set Language =====
    print("\n* Changing language")
    browser.visit(yealink_web + "/servlet?p=settings-preference&q=load")
    browser.find_by_id('LanguageWebLang').select('Russian')
    browser.execute_script('doSubmit()')


    # ===== Set time =====
    print("\n* Setting Time:")
    browser.visit(yealink_web + "/servlet?p=settings-datetime&q=load")
    print("     Disabling Manual Time")
    browser.find_by_name('LocalTimeType').first.select('1')
    print("     Disabling DTS")
    browser.find_by_id('DST_Disabled').click()
    print("     Changing TimeZone")
    browser.find_by_id('iDTimeZoneName').select('+3')
    print("     Changing NTP servers")
    browser.find_by_name("LocalTimeServer1").first.fill(ntp_1)
    browser.find_by_name("LocalTimeServer2").first.fill(ntp_2)
    browser.execute_script('doSubmit()')


    # ===== Disable keyboard lock =====
    print("\n* Disabling keyboard lock")
    browser.visit(yealink_web + "/servlet?p=settings-phonelock&q=load")
    browser.find_by_name('ServerLockDisable').first.select('1')
    browser.execute_script('onNoticeOperator()')
    browser.execute_script('document.getElementsByName("formInput")[0].action = "/servlet?p=settings-phonelock&q=write&reboot=false"')
    browser.execute_script('document.formInput.submit()')


    # ===== Change admin password =====
    print("\n* Changing admin password")
    pass_web_new = "WhichPassWeUse"   # NR Should be more secure
    # pass_web_new = getpass.getpass(prompt='     Input web admin pass: ')
    browser.visit(yealink_web + "/servlet?p=security&q=load")
    browser.find_by_name('editOldPassword').first.fill(pass_web_cur)
    browser.find_by_name('editNewPassword').first.fill(pass_web_new)
    browser.find_by_name('editConfirmPassword').first.fill(pass_web_new)
    browser.execute_script('doSubmit()')
    browser.visit(yealink_web + "/servlet?p=security&q=load")
    if browser.is_element_not_present_by_name('editOldPassword', 1):
        print("     Need re-login...")
        login_in_web(pass_web_new)


    if not username_yealink:
        # exit_script(0, True)
        break
    # ==== Set hostname ====
    print("\n* Setting hostname")
    browser.visit(yealink_web + "/servlet?p=features-general&q=load")
    browser.find_by_name('DhcpHostnameValue').first.fill("SIP-T48G-" + username_yealink)
    browser.execute_script('onNoticeOperator()')
    browser.execute_script('document.getElementsByName("formInput")[0].action = "/servlet?p=features-general&q=write&reboot=false"')
    browser.execute_script('document.formInput.submit()')


    # ==== Set account ====
    print("\n* Setting account")
    browser.visit(yealink_web + "/servlet?p=account-register-lync&q=load&acc=0")
    browser.execute_script("doSubmit('signout')")
    browser.find_by_id('AccountLyncSignInType').select('1')
    browser.find_by_id("AccountLyncNtlmAddress").fill(username_yealink + "@mail.ru") # CS
    browser.find_by_id("AccountLyncNtlmUser").fill(username_yealink + "@int.mail.ru") # CS
    browser.find_by_id("AccountLyncNtlmPassword").fill("123")
    browser.execute_script("doSubmit('write')")

    # ==== Reboot request ====
    reboot_req = input("\n\nReboot yealink? (input 'y' if need)): ").lower()
    if reboot_req == "y":
        print("Rebooting...")
        browser.visit(yealink_web + "/servlet?p=settings-upgrade&q=load")
        browser.execute_script(
            'document.getElementsByName("formAction")[0].action = "/servlet?p=settings-upgrade&q=reboot"')
        browser.execute_script('document.formAction.submit()')

    print("\n\n==========  End  ==========\n\n")

# exit_script(0, True)
