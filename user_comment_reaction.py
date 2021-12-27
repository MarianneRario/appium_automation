import threading
import time
import datetime
import uuid
from db_data import collection as collection
from db_data import col_time
from engagement_functions import search as search
from engagement_functions import login as login
from engagement_functions import user_comment as user_comment
from appium_init import device_serial as device_serial
from appium_init import thread as thread
from engagement_functions import user_react as user_react
from engagement_functions import thread_container
from user_engagement import add_user_engagement
from discord_webhook import public_url
from engagement_functions import keepAlive
import discord_webhook

lock = threading.BoundedSemaphore(thread)
args_arr = []
logged_devices = []
ctr = 0


def arr_append(argArr):
    args_arr.append(argArr)


def allowed_account(dev_name):
    allowed_acct = []
    try:
        acc_list = list(collection.find({"timestamp": {"$lt": datetime.datetime.now() - datetime.timedelta(minutes=10)}}))
        for key in range(len(acc_list)):
            if acc_list[key]["udid"] == dev_name:
                allowed_acct = acc_list[key]
                break

        if logged_devices:
            for x in logged_devices:
                if dev_name in x:
                    allowed_acct = []
    except Exception as err:
        print("ERROR: ", err)
    finally:
        return allowed_acct


def discord(webhook_url, worker_id):
    img_url = public_url + "/static/img/" + worker_id + ".png"
    webhook_url_extension = "/static/img/" + worker_id + ".png"
    discord_webhook.webhook(img_url, worker_id, webhook_url_extension, webhook_url)


def worker(_args_arr):
    global lock, logged_devices
    lock.acquire(True)
    # print(_args_arr)
    driver_no = _args_arr['driver_no']
    url = _args_arr['url']
    comment = _args_arr['comment']
    email = _args_arr["email"]
    password = _args_arr["password"]
    name = _args_arr["name"]
    reaction = _args_arr["reaction"]
    worker_id = _args_arr["worker_id"]
    webhook = _args_arr["webhook"]

    _logged_device = {email, driver_no}
    print("Worker id: ", worker_id, " is working...")
    print(name, " is logging in...")
    logged_devices.append(_logged_device)
    if search(driver_no, url):
        time.sleep(1)
        worker_login = login(driver_no, email, password)
        if worker_login <= 1:
            if reaction:
                worker_reaction = user_react(driver_no, reaction, worker_id)
                if worker_reaction:
                    print("DRIVER_NO: ", driver_no, ": LOCK RELEASE OF WORKER REACTION")
                    discord(webhook, worker_id)
                    lock.release()
                    print(name, " is logged out")
                    return
                else:
                    print("\033[2;31;40m DRIVER_NO: ", driver_no, ": IMMEDIATE LOCK RELEASE OF WORKER REACTION \x1b[0m")
                    lock.release()
                    return
            else:
                worker_comment = user_comment(driver_no, comment, worker_id, worker_login)
                if worker_comment:
                    print("DRIVER_NO: ", driver_no, ": LOCK RELEASE OF WORKER COMMENT")
                    discord(webhook, worker_id)
                    lock.release()
                    print(name, " is logged out")
                    return
                else:
                    print("\033[2;31;40m DRIVER_NO: ", driver_no, ": IMMEDIATE LOCK RELEASE OF WORKER COMMENT \x1b[0m")
                    lock.release()
        else:
            print("\033[2;31;40m DRIVER_NO: ", driver_no, ": IMMEDIATE LOCK RELEASE OF WORKER LOGIN \x1b[0m")
            lock.release()
    else:
        print("\033[2;31;40m DRIVER_NO: ", driver_no, ": IMMEDIATE LOCK RELEASE OF SEARCH \x1b[0m")
        lock.release()
        return


def update_database(email, url, time_now):
    # UPDATE URL
    collection.update_one({"email": email}, {"$set": {"url": url}})
    # UPDATE THE TIME
    collection.update_one({"email": email}, {"$set": {"timestamp": time_now}})


# def restart():
#     restart_time = list(col_time.find({"time": {"$lt": datetime.datetime.now() - datetime.timedelta(minutes=60)}}))
#     if restart_time:
#         col_time.update_one({}, {"$set": {"time": datetime.datetime.now()}})
#         return True
#     else:
#         return False

def _keep_alive(driver_no):
    global lock
    lock.acquire(True)
    keepAlive(driver_no)
    print("\033[2;32;40mDRIVER_NO: ", driver_no, ": KEEP ALIVE \x1b[0m")
    lock.release()


def reaction_functions(data):
    avail_accounts = list(
        collection.find({"timestamp": {"$lt": datetime.datetime.now() - datetime.timedelta(minutes=10)}}))
    for x in avail_accounts:
        arr_append(data)


def remove_device(_thread):
    if logged_devices:
        for x in logged_devices:
            if _thread in x:
                logged_devices.pop(logged_devices.index(x))


# for removal of killed accounts inside the logged_devices array
def remove_account():
    while True:
        if thread_container:
            print("THREAD CONTAINER: ", thread_container[0])
            remove_device(thread_container[0])
            thread_container.pop(0)


def run_thread():
    global ctr
    while True:
        if args_arr:
            allowed_acc = allowed_account(device_serial[ctr])
            if allowed_acc:
                args_list = {
                    "driver_no": ctr,
                    "url": args_arr[0]["url"],
                    "comment": args_arr[0]["comment"],
                    "reaction": args_arr[0]["reaction"],
                    "webhook": args_arr[0]["webhook"],
                    "email": allowed_acc["email"],
                    "password": allowed_acc["password"],
                    "name": allowed_acc["name"],
                    "udid": allowed_acc["udid"],
                    "worker_id": str(uuid.uuid4())[:8],
                }
                threading.Thread(target=worker, args=(args_list,)).start()
                ctr += 1
                if ctr == thread:
                    ctr = 0
                add_user_engagement(args_list["worker_id"], args_list["url"], args_list["email"],
                                    args_list["password"])
                update_database(args_list["email"], args_list["url"], datetime.datetime.now())
                args_arr.pop(0)
                time.sleep(1)
        else:
            threading.Thread(target=keepAlive, args=(ctr, )).start()
            ctr += 1
            if ctr == thread:
                ctr = 0


t = threading.Thread(target=run_thread)
t.setDaemon(True)
t.start()

t2 = threading.Thread(target=remove_account)
t2.setDaemon(True)
t2.start()
