import uuid
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction
from appium_init import driver
from db_data import locked_collection
from db_data import collection

import time
import screenshot

thread_container = []


def hasXpath(_thread, xpath):
    driver[_thread].implicitly_wait(1)
    path = driver[_thread].find_elements_by_xpath(xpath)
    if len(path) != 0:
        return True
    else:
        return False


def update_locked_db(email, password):
    collection.delete_one({"email": email})
    locked_collection.insert_one({"email": email, "password": password})


def locked_account(_thread):
    time.sleep(1)
    if hasXpath(_thread, "//android.widget.Button[@text = 'Get Started']"):
        print("LOCKED")
        return True
    else:
        return False


def keepAlive(_thread):
    try:
        driver[_thread].orientation
    except Exception as err:
        print(err)


def search(_thread, url):
    try:
        driver[_thread].execute_script('mobile: shell', {'command': 'am start -n',
                                                         'args': 'com.android.chrome/org.chromium.chrome.browser.incognito.'
                                                                 'IncognitoTabLauncher'})
        WebDriverWait(driver[_thread], 20).until(
            EC.element_to_be_clickable((By.ID, "com.android.chrome:id/url_bar"))).click()
        driver[_thread].execute_script('mobile: shell', {'command': 'input text', 'args': f'{url}'})
        driver[_thread].execute_script('mobile: shell', {'command': 'input', 'args': 'keyevent 66'})
        return True
    except Exception as err:
        print(f"\033[1;33;40mTHREAD NO: ", _thread, " - FROM APPIUM (SEARCH ERR): ", err, "\x1b[0m")
        logout(_thread)
        return False


def scroll_down(_driver, xpath):
    try:
        x = _driver.find_elements_by_xpath(xpath)
        if x:
            return True
        else:
            _driver.execute_script('mobile: shell', {'command': 'input swipe', 'args': '360 664 360 264 300'})
            return False
    except Exception as err:
        print(f"\033[1;33;DRIVER NO: ", _driver, " - SCROLL DOWN ERROR", err,
              "\x1b[0m")
        logout(_driver)
        return False


def scroll_up(_driver, xpath):
    try:
        x = _driver.find_elements_by_xpath(xpath)
        if x:
            return True
        else:
            _driver.execute_script('mobile: shell', {'command': 'input swipe', 'args': '300 300 300 800 500'})
            return False
    except Exception as err:
        print(f"\033[1;33;DRIVER NO: ", _driver, " - SCROLL UP ERROR", err,
              "\x1b[0m")
        logout(_driver)
        return False


def user_react(_thread, reaction, filename):
    try:
        WebDriverWait(driver[_thread], 20).until(
            lambda x: scroll_down(driver[_thread], "//android.widget.ToggleButton[@text = 'Like, Off']"))
    except Exception as err:
        print(f"\033[1;33;40mTHREAD NO: ", _thread, " - ERROR (INSIDE USER REACT SCROLL):  ", err, "\x1b[0m")
        logout(_thread)
        return False
    finally:
        # FIND THE REACTION BUTTON
        try:
            WebDriverWait(driver[_thread], 20).until(
                EC.presence_of_element_located((By.XPATH, "//android.widget.ToggleButton[@text = 'Like, Off']")))
            if hasXpath(_thread, "//android.widget.ToggleButton[@text = 'Like, Off']"):
                react = driver[_thread].find_element_by_xpath("//android.widget.ToggleButton[@text = 'Like, Off']")
                # LONG PRESS THE REACTION BUTTON
                actions = TouchAction(driver[_thread])
                actions.long_press(react)
                actions.perform()
                r = driver[_thread].find_element_by_xpath(f"//android.widget.Button[@text = '{reaction}']")
                r.click()
                time.sleep(2)
                # SCREENSHOT
                ss = driver[_thread].get_screenshot_as_png()
                screenshot.get_screen(filename, ss)
                time.sleep(5)
                logout(_thread)
                return True
            else:
                print(f"\033[1;33;40m- THREAD NO: ", _thread,
                      " - FROM APPIUM (USER REACT ERR IN ELSE)", "\x1b[0m")
                logout(_thread)
                return False
        except Exception as err:
            print(f"\033[1;33;40mTHREAD NO: ", _thread, " - FROM APPIUM (USER REACT ERR): ", err,
                  "\x1b[0m")
            logout(_thread)
            return False


def write_comment(_thread, comment, filename):
    try:
        serialized_comment = comment.replace(" ", "\ ")
        for i in serialized_comment:
            driver[_thread].execute_script("mobile: shell", {"command": "input text", "args": i + " "})
            time.sleep(0.1)
        driver[_thread].execute_script('mobile: shell', {'command': 'input', 'args': 'keyevent 61'})
        time.sleep(0.2)
        driver[_thread].execute_script('mobile: shell', {'command': 'input', 'args': 'keyevent 66'})
        time.sleep(5)
        # SCREENSHOT
        ss = driver[_thread].get_screenshot_as_png()
        screenshot.get_screen(filename, ss)
        time.sleep(10)
        logout(_thread)
        return True
    except Exception as err:
        print(f"\033[1;33;40mTHREAD NO: ", _thread, " - FROM WRITE COMMENT: ", err, "\x1b[0m")
        logout(_thread)
        return False


def vid_comment(_thread, comment, filename):
    try:
        if hasXpath(_thread, "//android.widget.EditText[@resource-id = 'composerInput']"):
            _comment = write_comment(_thread, comment, filename)
            return _comment
        else:
            WebDriverWait(driver[_thread], 20).until(
                lambda x: scroll_down(driver[_thread], ".//*[contains(@text, 'Comment')]"))
            WebDriverWait(driver[_thread], 5).until(
                EC.element_to_be_clickable((By.XPATH, ".//*[contains(@text, 'Comment')]"))).click()
            _comment = write_comment(_thread, comment, filename)
            return _comment
    except Exception as err:
        print(f"\033[1;33;40mTHREAD NO: ", _thread, " - ERROR (INSIDE VID COMMENT):  ", err, "\x1b[0m")
        logout(_thread)
        return False


def user_comment(_thread, comment, filename, log):
    try:
        WebDriverWait(driver[_thread], 120).until(
            lambda x: scroll_down(driver[_thread], ".//*[contains(@text, 'Comment')]"))
        if hasXpath(_thread, ".//*[contains(@text, 'Comment')]"):
            WebDriverWait(driver[_thread], 5).until(
                EC.presence_of_element_located((By.XPATH, ".//*[contains(@text, 'Comment')]"))).click()
            time.sleep(1)
            if log == 0:
                _comment = write_comment(_thread, comment, filename)
                return _comment
            else:
                _vid_comment = vid_comment(_thread, comment, filename)
                return _vid_comment
    except Exception as err:
        print(f"\033[1;33;40mTHREAD NO: ", _thread, " - ERROR (INSIDE USER COMMENT SCROLL):  ", err, "\x1b[0m")
        logout(_thread)
        return False


def login(_thread, email, password):
    try:
        WebDriverWait(driver[_thread], 10).until(
            EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@text = "Log In"]')))
        if hasXpath(_thread, "//android.widget.Button[@text = 'Log In']"):
            print("THREAD: ", _thread, " LOGIN 1")
            _login = login1(_thread, email, password)
            return _login
        else:
            print("THREAD: ", _thread, " LOGIN 2")
            _login = login2(_thread, email, password)
            return _login
    except Exception as err:
        print("THREAD: ", _thread, " LOGIN 2 (FROM EXCEPTION ERROR): ", err)
        _login = login2(_thread, email, password)
        return _login


def login1(_thread, email, password):
    try:
        # LOGIN
        WebDriverWait(driver[_thread], 20).until(
            EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@text = "Log In"]'))).click()
        WebDriverWait(driver[_thread], 20).until(EC.presence_of_element_located(
            (By.XPATH, "//android.widget.EditText[@resource-id = 'm_login_email']"))).send_keys(email)
        WebDriverWait(driver[_thread], 20).until(EC.presence_of_element_located(
            (By.XPATH, "//android.widget.EditText[@resource-id = 'm_login_password']"))).send_keys(password)
        WebDriverWait(driver[_thread], 20).until(
            EC.presence_of_element_located((By.XPATH, "//android.widget.Button[@text = 'Log In']"))).click()
        time.sleep(5)
        if locked_account(_thread):
            update_locked_db(email, password)
            time.sleep(2)
            logout(_thread)
            return 2
        return 0
    except Exception as err:
        print(f"\033[1;33;40mTHREAD NO: ", _thread, " - FROM APPIUM (LOGIN 1 ERR): ", err, "\x1b[0m")
        logout(_thread)
        return 2


def login2(_thread, email, password):
    # SCROLL
    try:
        WebDriverWait(driver[_thread], 20).until(
            EC.presence_of_element_located((By.XPATH, ".//*[contains(@text, 'Like')]")))
        driver[_thread].find_element_by_android_uiautomator(
            'new UiScrollable(new UiSelector().scrollable(true).instance(0)).'
            'scrollIntoView(new UiSelector().text("Like").instance(0));')
    except Exception as err:
        print(f"\033[1;33;40mTHREAD NO: ", _thread, " - ERROR (INSIDE LOGIN 2 SCROLL): ", err, "\x1b[0m")
        logout(_thread)
        return 2
    finally:
        path = hasXpath(_thread, ".//*[contains(@text, 'Like')]")
        if path:
            try:
                WebDriverWait(driver[_thread], 20).until(
                    EC.presence_of_element_located((By.XPATH, ".//*[contains(@text, 'Like')]"))).click()
                # LOGIN
                WebDriverWait(driver[_thread], 20).until(EC.presence_of_element_located(
                    (By.XPATH, "//android.widget.EditText[@resource-id = 'm_login_email']"))).send_keys(email)
                WebDriverWait(driver[_thread], 20).until(EC.presence_of_element_located(
                    (By.XPATH, "//android.widget.EditText[@resource-id = 'm_login_password']"))).send_keys(password)
                WebDriverWait(driver[_thread], 20).until(
                    EC.presence_of_element_located((By.XPATH, "//android.widget.Button[@text = 'Log In']"))).click()
                time.sleep(5)
                if locked_account(_thread):
                    update_locked_db(email, password)
                    time.sleep(2)
                    logout(_thread)
                    return 2
                return 1
            except Exception as err:
                print(f"\033[1;33;40mTHREAD NO: ", _thread, " - LOGIN 2 ERROR: ", err, "\x1b[0m")
                logout(_thread)
                return 2
        else:
            logout(_thread)
            return 2


def logout(_thread):
    # EXIT FACEBOOK
    driver[_thread].execute_script('mobile: shell', {'command': 'am force-stop',
                                                     'args': 'com.android.chrome'})
    if _thread not in thread_container:
        thread_container.append(_thread)
    time.sleep(1)
