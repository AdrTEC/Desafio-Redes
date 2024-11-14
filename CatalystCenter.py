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


def createRouterDevice():
    API = '/dna/intent/api/v1/network-device'
    URL = BASE_URL + API
    TOKEN = getToken()
    HEADERS = {
        'X-Auth-Token': TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    PAYLOAD = {
    "cliTransport": "ssh",
    "computeDevice": False,
    "enablePassword": "12345678",
    "extendedDiscoveryInfo": "DISCOVER_WITH_CANNED_DATA",
    "httpPassword": "12345678",
    "httpPort": "8080",
    "httpSecure": True,
    "httpUserName": "test",
    "ipAddress": [ "10.10.20.189" ],
    "merakiOrgId": [ "your-meraki-org-id" ],
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
    if RESPONSE.status_code == 202:
        JSON_RESP = json.loads(RESPONSE.text)
        print("Device creation initiated:", JSON_RESP)
        return JSON_RESP['response']["url"]  # Obtiene la URL de ejecución
    else:
        print(f"Failed to create device, status code: {RESPONSE.status_code}")
        print(RESPONSE.text)
        return None

def getDeviceExecutionStatus(execution_url):
    URL = BASE_URL + execution_url
    TOKEN = getToken()
    HEADERS = {
        'X-Auth-Token': TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    RESPONSE = requests.get(URL, headers=HEADERS, verify=False)
    if RESPONSE.status_code == 200:
        JSON_RESP = RESPONSE.json()
        pprint(JSON_RESP)
        return JSON_RESP
    else:
        print(f"Failed to retrieve execution status, status code: {RESPONSE.status_code}")
        print(RESPONSE.text)
        return None


def configDevice(): #para configurar los switches Antony
    print("hola")


def getPhysicalTopology(): # Gabriel
    print("hola")
    

def assingLocationToDevice(device_id, site_id, building_name, floor_name):
    """
    Asigna una ubicación (sitio, edificio, piso) a un dispositivo de red.

    :param device_id: El ID del dispositivo al que se le asignará la ubicación.
    :param site_id: El ID del sitio al que se asignará el dispositivo.
    :param building_name: El nombre del edificio dentro del sitio.
    :param floor_name: El nombre del piso dentro del edificio.
    :return: Respuesta de la API con el resultado de la operación.
    """
    # URL para la asignación de ubicación
    API = f'/dna/intent/api/v1/network-device/{device_id}/location'
    URL = BASE_URL + API
    
    # Token de autenticación
    TOKEN = getToken()
    
    # Encabezados para la solicitud
    HEADERS = {
        'X-Auth-Token': TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Cuerpo de la solicitud (payload) con la información de la ubicación
    PAYLOAD = {
        "location": {
            "siteId": site_id,  # ID del sitio
            "building": {
                "name": building_name  # Nombre del edificio
            },
            "floor": {
                "name": floor_name  # Nombre del piso
            }
        }
    }

    # Realiza la solicitud POST para asignar la ubicación al dispositivo
    RESPONSE = requests.put(URL, headers=HEADERS, json=PAYLOAD, verify=False)
    
    # Verifica el código de estado de la respuesta
    if RESPONSE.status_code == 200:
        JSON_RESP = json.loads(RESPONSE.text)
        print("Ubicación asignada correctamente:", JSON_RESP)
        return JSON_RESP
    else:
        print(f"Error al asignar la ubicación, código de estado: {RESPONSE.status_code}")
        print(RESPONSE.text)
        return None



def getNetworkDevices():
    
    API = '/dna/intent/api/v1/network-device'
    URL = BASE_URL + API
    TOKEN = getToken()
    HEADERS = {
        'X-Auth-Token': TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    RESPONSE = requests.get(URL, headers=HEADERS, verify=False)
    
    if RESPONSE.status_code == 200:
        JSON_RESP = json.loads(RESPONSE.text)
        pprint(JSON_RESP)  # Imprime el resultado en formato legible
        return JSON_RESP
    else:
        print(f"Failed to retrieve network devices, status code: {RESPONSE.status_code}")
        print(RESPONSE.text)
        return None

# Llama a la función para obtener la lista de dispositivos de red
#getNetworkDevices()

# Llama a la función para probar la creación de un dispositivo
execution_url = createRouterDevice()
pprint(execution_url)
getDeviceExecutionStatus(execution_url)

