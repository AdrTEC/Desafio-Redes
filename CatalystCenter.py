from flask import Flask, jsonify, request
import requests
import json
from pprint import pprint

# Disable SSL/TLS warnings
requests.packages.urllib3.disable_warnings()

# Constants variables
BASE_URL = "https://10.10.20.85"
USERNAME = "admin"
PASSWORD = "Cisco1234!"

app = Flask(__name__)

#=============================== Token Management

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

#=============================== Endpoint Functions

@app.route('/sites', methods=['GET'])
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
    return jsonify(JSON_RESP)




def createSite():
    """
    Crea un nuevo sitio en Cisco DNA Center.
    """
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
                "name": "TEST CREACION",
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
    return JSON_RESP

@app.route('/createSite', methods=['GET'])
def createSiteWrapper():
    """
    Endpoint de Flask para crear un nuevo sitio en Cisco DNA Center.
    Llama a la función createSite y devuelve el resultado.
    """
    # Llama a la función original que realiza el POST y crea el sitio
    response = createSite()

    # Devuelve la URL de estado de ejecución obtenida de la respuesta en JSON
    return response

@app.route('/confirmSiteCreation/<path:execution_url>', methods=['GET'])
def confirmSiteCreation(execution_url):
    URL = BASE_URL + execution_url
    TOKEN = getToken()
    HEADERS = {
        'X-Auth-Token': TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    RESPONSE = requests.get(URL, headers=HEADERS, verify=False)
    JSON_RESP = json.loads(RESPONSE.text)
    return jsonify(JSON_RESP)


def getUsers():
    API = '/dna/system/api/v1/user'
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

def updateUser():
    API = '/dna/system/api/v1/user'
    URL = BASE_URL + API
    TOKEN = getToken()
    HEADERS = {
        'X-Auth-Token': TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    PAYLOAD = {
        "firstName": "Anthony",
        "lastName": "Montero",
        "authSource": "internal",
        "passphraseUpdateTime": "1731368069345",
        "passphrase": None,
        "oldPassphrase": None,
        "roleList": [
            "6696f01aa04cae65c3c37b02"
        ],
        "userId": "6697740ae8e79474f717ab5a",
        "email": "",
        "username": "devnetuser"   
    }

    RESPONSE = requests.put(URL, headers=HEADERS, json=PAYLOAD, verify=False)
    JSON_RESP = json.loads(RESPONSE.text)
    return JSON_RESP['executionStatusUrl']

def getDevices():
    API = '/dna/intent/api/v1/network-device'
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


@app.route('/createDevice', methods=['POST'])
def createDevice():
    API = '/dna/intent/api/v1/network-device'
    URL = BASE_URL + API
    TOKEN = getToken()
    HEADERS = {
        'X-Auth-Token': TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json'}
    PAYLOAD = request.json or {
        "cliTransport": "ssh",
        "computeDevice": False,
        "enablePassword": "12345678",
        "extendedDiscoveryInfo": "DISCOVER_WITH_CANNED_DATA",
        "httpPassword": "12345678",
        "httpPort": "8080",
        "httpSecure": True,
        "httpUserName": "test",
        "ipAddress": ["10.10.20.189"],
        "merakiOrgId": ["your-meraki-org-id"],
        "netconfPort": "830",
        "password": "12345678",
        "serialNumber": "CML12345ROUT",
        "snmpAuthPassphrase": "auth_passphrase",
        "snmpAuthProtocol": "sha",
        "snmpMode": "authPriv",
        "snmpPrivPassphrase": "priv_passphrase",
        "snmpPrivProtocol": "AES128",
        "snmpROCommunity": "public",
        "snmpRWCommunity": "private",
        "snmpRetry": 3,
        "snmpTimeout": 5,
        "snmpUserName": "snmp_user",
        "snmpVersion": "v3",
        "type": "NETWORK_DEVICE",
        "updateMgmtIPaddressList": [
            {
                "existMgmtIpAddress": "10.10.20.178",
                "newMgmtIpAddress": "10.10.20.179"
            }
        ],
        "userName": "test"
    }
    RESPONSE = requests.post(URL, headers=HEADERS, json=PAYLOAD, verify=False)
    JSON_RESP = json.loads(RESPONSE.text)
    return jsonify(JSON_RESP)

@app.route('/confirmDeviceCreation/<path:execution_url>', methods=['GET'])
def confirmDeviceCreation(execution_url):
    URL = BASE_URL + execution_url
    TOKEN = getToken()
    HEADERS = {
        'X-Auth-Token': TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    RESPONSE = requests.get(URL, headers=HEADERS, verify=False)
    JSON_RESP = json.loads(RESPONSE.text)
    return jsonify(JSON_RESP)

@app.route('/getPhysicalTopology', methods=['GET'])
def getPhysicalTopology():
    API = "/dna/intent/api/v1/topology/physical-topology"
    URL = BASE_URL + API
    TOKEN = getToken()
    HEADERS = {
        'X-Auth-Token': TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    RESPONSE = requests.get(URL, headers=HEADERS, verify=False)
    JSON_RESP = json.loads(RESPONSE.text)
    return jsonify(JSON_RESP)

@app.route('/getSiteCount', methods=['GET'])
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
    return jsonify(JSON_RESP)

@app.route('/getSiteHealth', methods=['GET'])
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
    return jsonify(JSON_RESP)

@app.route('/assingLocationToDevice/<device_id>/<site_id>/<building_name>/<floor_name>', methods=['PUT'])
def assingLocationToDevice(device_id, site_id, building_name, floor_name):
    API = f'/dna/intent/api/v1/network-device/{device_id}/location'
    URL = BASE_URL + API
    TOKEN = getToken()
    HEADERS = {
        'X-Auth-Token': TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    PAYLOAD = {
        "location": {
            "siteId": site_id,
            "building": {
                "name": building_name
            },
            "floor": {
                "name": floor_name
            }
        }
    }
    RESPONSE = requests.put(URL, headers=HEADERS, json=PAYLOAD, verify=False)
    JSON_RESP = json.loads(RESPONSE.text)
    return jsonify(JSON_RESP)

#=============================== Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
