from ppadb.client import Client as AdbClient
from appium import webdriver
from udid_distributor import add_udid as add_udid
import time
import subprocess

client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()

if len(devices) == 0:
    print('No devices')
    quit()

device_serial = []
thread = len(devices)
driver = []
port = 8210

desired_capabilities = {
    "platformName": "Android",
    "deviceName": "placeholder",
    "udid": "placeholder",
    "automationName": "UiAutomator2",
    "newCommandTimeout": 100000,
    "unicodeKeyboard": True
}


def appium_connect(device_name):
    dc = desired_capabilities
    dc['deviceName'] = device_name
    dc['udid'] = device_name
    return dc


def appium_server_start(port):
    cmd = '/home/ubuntu/.nvm/versions/node/v14.7.0/bin/appium -p ' + str(port) + ' --relaxed-security &'
    subprocess.Popen(cmd, shell=True, stdout=open('appium-logs-' + str(port) + '.log', 'a'), stderr=subprocess.STDOUT)
    time.sleep(10)


def adb_server():
    subprocess.Popen('adb kill-server', shell=True)
    time.sleep(3)
    subprocess.Popen('adb start-server', shell=True)


def appium():
    _port = 8210
    for x in range(thread):
        appium_server_start(_port)
        _port += 1

    for device in devices:
        try:
            time.sleep(5)
            connect = webdriver.Remote(f"http://0.0.0.0:{port}/wd/hub", appium_connect(device.serial))
            device_serial.append(device.serial)
            driver.append(connect)
        except Exception as err:
            print(err)
            break


try:
    print("RESTARTING ADB SERVER")
    adb_server()
except Exception as err:
    print("ADB ERROR: ", err)
time.sleep(5)
appium()
add_udid(device_serial)
