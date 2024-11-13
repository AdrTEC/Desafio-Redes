import requests
import json
from pprint import pprint

# Disable SSL/TLS warnings

requests.packages.urllib3.disable_warnings()

# Constants variables
BASE_URL = "https://10.10.20.85"
USERNAME = "admin"
PASSWORD = "Cisco1234!"

def getToken():
    API = '/dna/system/api/v1/auth/token'
    URL = BASE_URL + API
    HEADERS = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    JSON_RESPONSE = requests.post(URL, auth=(USERNAME, PASSWORD), headers=HEADERS, verify=False)
    JSON_RESP = json.loads(JSON_RESPONSE.text)
    return JSON_RESP['Token']

def getSite():
    API = '/dna/intent/api/v1/site'
    URL = BASE_URL + API
    TOKEN = getToken()
    HEADERS = {
        'X-Auth-Token': TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    RESPONSE = requests.get(URL, headers=HEADERS, verify=False)
    JSON_RESP = json.loads(RESPONSE.text)
    return JSON_RESP

def getSiteCount():
    API = '/dna/intent/api/v1/site/count'
    URL = BASE_URL + API
    TOKEN = getToken()
    HEADERS = {
        'X-Auth-Token': TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    RESPONSE = requests.get(URL, headers=HEADERS, verify=False)
    JSON_RESP = json.loads(RESPONSE.text)
    return JSON_RESP

def getSiteHealth():
    API = '/dna/intent/api/v1/site/site-health'
    URL = BASE_URL + API
    TOKEN = getToken()
    HEADERS = {
        'X-Auth-Token': TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    RESPONSE = requests.get(URL, headers=HEADERS, verify=False)
    JSON_RESP = json.loads(RESPONSE.text)
    return JSON_RESP

def createSite():
    API = '/dna/intent/api/v1/site'
    URL = BASE_URL + API
    TOKEN = getToken()
    HEADERS = {
        'X-Auth-Token': TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    PAYLOAD = {
        "type": "area",
        "site": {
            "area": {
                "name": "MARTE",
                "parentName": "Global"
            },
            "building": {
                "name": "MILK-WAY",
                "address": "NEAR THE SATURN",
                "parentName": "SOLAR SYSTEM",
                "latitude": 0,
                "longitude": 0,
                "country": "Peru"
            },
            "floor": {
                "name": "Far away",
                "parentName": "Beyond asteroid belt",
                "rfModel": "Space",
                "width": 0,
                "length": 0,
                "height": 0,
                "floorNumber": 0
            }
        }     
    }

    RESPONSE = requests.post(URL, headers=HEADERS, json=PAYLOAD, verify=False)
    print(RESPONSE.status_code)
    JSON_RESP = json.loads(RESPONSE.text)
    return JSON_RESP['executionStatusUrl']

def getSiteExecution():
    API = createSite()
    URL = BASE_URL + API
    print(URL)
    TOKEN = getToken()
    HEADERS = {
        'X-Auth-Token': TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    RESPONSE = requests.get(URL, headers=HEADERS, verify=False)
    JSON_RESP = json.loads(RESPONSE.text)
    return JSON_RESP

pprint(getSite(), indent=4)

