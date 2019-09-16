from pymongo import MongoClient
import json, socket, tldextract
from netaddr import IPNetwork
client = MongoClient()
db = client['the-collector']
data_collection = db['data']

def add_data(data_list):
    f_data = []
    try:
        f_data = [json.loads(x) for x in data_list]
    except:
        for item in data_list:
            item_type = identify_type(item.strip())
            if (item_type == "subdomain"):
                extracted = tldextract.extract(item.strip())
                parent_asset = extracted.domain + extracted.suffix
            else:
                parent_asset = "N/A"
            obj = {"value": item.strip(), "type": item_type, "parent_asset": parent_asset}
    f_data = check_ip_cidrs(f_data)
    try:
        for value in f_data:
            if (data_collection.find({'value': value['value']}).count() == 0):
                data_collection.insert_one(value)
        print ('Data inserted')
    except Exception as e:
        print (e)


#FIX THIS - PRETTY MUCH I WANT TO UPDATE THE DB EVERY TIME AN ASSET IS ADDED TO ENSURE PARENT IDS ARE ACCURATE
def get_data():
    all_data = list(data_collection.find())
    for item in all_data:
        del item['_id']
    print ('All data pulled')
    return all_data

def check_ip_cidrs():
    list_of_cidrs = data_collection.find({'type': 'cidr'})
    all_ips = data_collection.find({'type': 'ipv4_address'})
    for cidr in list_of_cidrs:
        for item in all_ips:
            if (item['type'] == 'ipv4_address'):
                for ip in IPNetwork(cidr['value']):
                    if (item['value'] == str(ip)):
                        item['parent_asset'] = cidr['value']
                        print (item['value'])
                    elif ("parent_asset" not in item.keys()):
                        item['parent_asset'] = "N/A"

    return all_ips



def identify_type(item):
    asset_type = "Unknown"
    try:
        socket.inet_aton(item)
        asset_type = "ipv4_address"
    except:
        try:
            split_cidr = item.split('/')
            socket.inet_aton(split_cidr[0])
            if (int(split.cidr[1]) < 33 and int(split.cidr[1] > 0)):
                asset_type = "cidr"
        except:
            try:
                extracted_data = tldextract.extract(item)
                if (extracted_data.domain != ''):
                    if (extracted_data.subdomain != ''):
                        asset_type = "subdomain"
                    else:
                        asset_type = "domain"
            except:
                type = "unknown"
    return asset_type
