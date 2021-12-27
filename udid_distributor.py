from db_data import collection


def add_udid(device_serial):
    ctr = 0
    empty_udid = list(collection.find({'udid': ""}))

    for x in range(len(empty_udid)):
        collection.update_one({f"_id": empty_udid[x]['_id']}, {"$set": {"udid": device_serial[ctr]}})
        ctr += 1

        if ctr == len(device_serial):
            ctr = 0