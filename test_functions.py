from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from appium import webdriver
from db_data import locked_collection
from db_data import collection
import time
import uuid


desired_capabilities = {
    "deviceName": "5200c2c6b21cc457",
    "udid": "5200c2c6b21cc457",
    "automationName": "UiAutomator2",
    "systemPort	": 8201,
    "platformName": "Android",
    "newCommandTimeout": 500000

}

# CONNECT TO APPIUM
driver = webdriver.Remote("http://127.0.0.1:8201/wd/hub", desired_capabilities)
time.sleep(5)


def error_logs(id_name):
    page_source = driver.page_source
    write_page_source = open(f"error_logs/{id_name}.txt", "w", encoding="utf-8")
    write_page_source.write(page_source)
    write_page_source.close()


def hasXpath(xpath):
    driver.implicitly_wait(1)
    path = driver.find_elements_by_xpath(xpath)
    if len(path) != 0:
        return True
    else:
        return False


def update_locked_db(email, password):
    collection.delete_one({"email": email})
    locked_collection.insert_one({"email": email, "password": password})


def locked_account():
    if hasXpath("//android.widget.Button[@text = 'Get Started']"):
        print("LOCKED")
        return True
    else:
        return False


def search(url):
    id_name = str(uuid.uuid4())[:8] + "_search_error"
    driver.execute_script('mobile: shell', {'command': 'am start -n',
                                            'args': 'com.android.chrome/org.chromium.chrome.browser.incognito.'
                                                    'IncognitoTabLauncher'})
    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "com.android.chrome:id/url_bar"))).click()
        driver.execute_script('mobile: shell', {'command': 'input text', 'args': f'{url}'})
        driver.execute_script('mobile: shell', {'command': 'input', 'args': 'keyevent 66'})
        return True
    except Exception as err:
        print(f"\033[1;33;40mID: {id_name} - THREAD NO: ", " - FROM APPIUM (SEARCH ERR): ", err, "\x1b[0m")
        error_logs(id_name)
        logout()
        return False


def scroll_down(_driver, xpath):
    x = _driver.find_elements_by_xpath(xpath)
    if x:
        return True
    else:
        _driver.execute_script('mobile: shell', {'command': 'input swipe', 'args': '360 664 360 264 300'})
        return False


def scroll_up(_driver, xpath):
    x = _driver.find_elements_by_xpath(xpath)
    if x:
        return True
    else:
        _driver.execute_script('mobile: shell', {'command': 'input swipe', 'args': '300 300 300 800 500'})
        return False


def login(email, password):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@text = "Log In"]')))
        if hasXpath("//android.widget.Button[@text = 'Log In']"):
            print("THREAD: ", " LOGIN 1")
            _login = login1(email, password)
            return _login
        else:
            print("THREAD: ", " LOGIN 2")
            _login = login2(email, password)
            return _login
    except Exception as err:
        print("THREAD: ", " LOGIN 2 (FROM EXCEPTION ERROR): ", err)
        _login = login2(email, password)
        return _login


def login1(email, password):
    id_name = str(uuid.uuid4())[:8]
    try:
        # LOGIN
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@text = "Log In"]'))).click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//android.widget.EditText[@resource-id = 'm_login_email']"))).send_keys(email)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//android.widget.EditText[@resource-id = 'm_login_password']"))).send_keys(password)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//android.widget.Button[@text = 'Log In']"))).click()
        time.sleep(5)
        if locked_account:
            update_locked_db(email, password)
            time.sleep(2)
            logout()
            return 2
        return 0
    except Exception as err:
        print(f"\033[1;33;40mID: {id_name} - THREAD NO: ", " - FROM APPIUM (LOGIN 1 ERR): ", err, "\x1b[0m")
        _id_name = id_name + "_login1_error"
        error_logs(_id_name)
        logout()
        return 2


def login2(email, password):
    id_name = str(uuid.uuid4())[:8]
    # SCROLL
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, ".//*[contains(@text, 'Like')]")))
        driver.find_element_by_android_uiautomator(
            'new UiScrollable(new UiSelector().scrollable(true).instance(0)).'
            'scrollIntoView(new UiSelector().text("Like").instance(0));')
    except Exception as err:
        print(f"\033[1;33;40mID: {id_name} - THREAD NO: ", " - ERROR (INSIDE LOGIN 2 SCROLL): ", err, "\x1b[0m")
        _id_name = id_name + "_login2_scroll_error"
        error_logs(_id_name)
    finally:
        path = hasXpath(".//*[contains(@text, 'Like')]")
        if path:
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, ".//*[contains(@text, 'Like')]"))).click()
                # LOGIN
                WebDriverWait(driver, 20).until(EC.presence_of_element_located(
                    (By.XPATH, "//android.widget.EditText[@resource-id = 'm_login_email']"))).send_keys(email)
                WebDriverWait(driver, 20).until(EC.presence_of_element_located(
                    (By.XPATH, "//android.widget.EditText[@resource-id = 'm_login_password']"))).send_keys(password)
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//android.widget.Button[@text = 'Log In']"))).click()
                time.sleep(5)
                if locked_account:
                    update_locked_db(email, password)
                    time.sleep(2)
                    logout()
                    return 2
                return 1
            except Exception as err:
                print(f"\033[1;33;40mID: {id_name} - THREAD NO: ", " - LOGIN 2 ERROR: ", err, "\x1b[0m")
                _id_name = id_name + "_login2_error"
                error_logs(_id_name)
                logout()
                return 2
        else:
            _id_name = id_name + "_login2_path_not_found_error"
            error_logs(_id_name)
            logout()
            return 2


def user_react(reaction):
    id_name = str(uuid.uuid4())[:8]
    try:
        WebDriverWait(driver, 20).until(
            lambda x: scroll_down(driver, "//android.widget.ToggleButton[@text = 'Like, Off']"))
    except Exception as err:
        print(f"\033[1;33;40mID: {id_name} - THREAD NO: ", " - ERROR (INSIDE USER REACT SCROLL):  ", err, "\x1b[0m")
        _id_name = id_name + "_user_react_scroll"
        error_logs(_id_name)
    finally:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//android.widget.ToggleButton[@text = 'Like, Off']")))
        if hasXpath("//android.widget.ToggleButton[@text = 'Like, Off']"):
            # FIND THE REACTION BUTTON
            try:
                react = driver.find_element_by_xpath("//android.widget.ToggleButton[@text = 'Like, Off']")
                # LONG PRESS THE REACTION BUTTON
                actions = TouchAction(driver)
                actions.long_press(react)
                actions.perform()
                r = driver.find_element_by_xpath(f"//android.widget.Button[@text = '{reaction}']")
                r.click()
                time.sleep(2)
                logout()
                return True
            except Exception as err:
                print(f"\033[1;33;40mID: {id_name} - THREAD NO: ", " - FROM APPIUM (USER REACT ERR): ", err,
                      "\x1b[0m")
                _id_name = id_name + "_user_react_error"
                error_logs(_id_name)
                logout()
                return False
        else:
            print(f"\033[1;33;40mID: {id_name} - THREAD NO: ", " - FROM APPIUM (USER REACT ERR IN ELSE)", "\x1b[0m")
            _id_name = id_name + "_user_react_else"
            error_logs(_id_name)
            logout()
            return False


def logout():
    # EXIT FACEBOOK
    driver.execute_script('mobile: shell', {'command': 'am force-stop',
                                            'args': 'com.android.chrome'})
    time.sleep(1)
