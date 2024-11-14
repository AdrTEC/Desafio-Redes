import requests
import json
from pprint import pprint

# Disable SSL/TLS warnings
requests.packages.urllib3.disable_warnings()

# Constants variables
BASE_URL = "https://10.10.20.85"
USERNAME = "admin"
PASSWORD = "Cisco1234!"

#===================================Manuel

def getToken():
    """
    Obtiene el token de autenticación para hacer solicitudes a la API de Cisco DNA Center.
    """
    API = '/dna/system/api/v1/auth/token'
    URL = BASE_URL + API
    HEADERS = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    JSON_RESPONSE = requests.post(URL, auth=(USERNAME, PASSWORD), headers=HEADERS, verify=False)
    JSON_RESP = json.loads(JSON_RESPONSE.text)
    return JSON_RESP['Token']

def assignLocationToDevice(device_id, site_id, building_name, floor_name):
    """
    Asigna una ubicación (sitio, edificio, piso) a un dispositivo de red.

    :param device_id: El ID del dispositivo al que se le asignará la ubicación.
    :param site_id: El ID del sitio al que se asignará el dispositivo.
    :param building_name: El nombre del edificio dentro del sitio.
    :param floor_name: El nombre del piso dentro del edificio.
    :return: Respuesta de la API con el resultado de la operación, o None si ocurre un error.
    """
    # URL para la asignación de ubicación
    API = f'/dna/intent/api/v1/network-device/{device_id}/location'
    URL = BASE_URL + API
    
    # Token de autenticación
    TOKEN = getToken()
    if not TOKEN:
        print("Error: No se pudo obtener el token de autenticación.")
        return None
    
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

    try:
        # Realiza la solicitud PUT para asignar la ubicación al dispositivo
        RESPONSE = requests.put(URL, headers=HEADERS, json=PAYLOAD, verify=False)
        
        # Verifica el código de estado de la respuesta
        if RESPONSE.status_code == 200:
            JSON_RESP = RESPONSE.json()
            print("Ubicación asignada correctamente:", JSON_RESP)
            return JSON_RESP
        else:
            print(f"Error al asignar la ubicación, código de estado: {RESPONSE.status_code}")
            print(RESPONSE.text)
            return None
    except requests.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return None


#==================================Adrián

def getSite():
    """
    Obtiene información sobre los sitios registrados en Cisco DNA Center.
    """
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

def confirmSiteCreation():
    """
    Obtiene el estado de ejecución de la creación del sitio.
    """
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






#===============================Antony

def createDevice():
    """
    Crea un dispositivo de red tipo router en Cisco DNA Center.
    """
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
    if RESPONSE.status_code == 202:
        JSON_RESP = json.loads(RESPONSE.text)
        print("Device creation initiated:", JSON_RESP)
        return JSON_RESP['response']["url"]  # Obtiene la URL de ejecución
    else:
        print(f"Failed to create device, status code: {RESPONSE.status_code}")
        print(RESPONSE.text)
        return None

def confirmDeviceCreation(execution_url):
    """
    Obtiene el estado de ejecución de la creación del dispositivo.
    """
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




#=============================== Gabriel
def getPhysicalTopology():
    """
    Obtiene la topología física de la red.
    """
    API = "/dna/intent/api/v1/topology/physical-topology"
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

def getSiteCount():
    """
    Obtiene el número de sitios registrados en Cisco DNA Center.
    """
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
    """
    Obtiene la salud de los sitios registrados en Cisco DNA Center.
    """
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



def main():
    # Un ejemplo de cómo llamar a las funciones
    #pprint(getSite())  # Imprime la lista de sitios
    #pprint(getSiteCount())  # Muestra el número de sitios
    #pprint(getSiteHealth())  # Muestra la salud de los sitios
    #pprint(getPhysicalTopology())  # Muestra la topología física de la red


    site_id= " a7d3d4a4-3dfa-4bd5-918b-2b562585e2f5"
    device_id="ab690aa1-a4c4-478b-9406-72ef0200517c"
    building_name="BEAV"
    floor_name="floor2"
# building name BEAV
    assignLocationToDevice(device_id,site_id,building_name, floor_name)
    # Crear un dispositivo router y luego consultar su estado
    #execution_url = createDevice()
    #if execution_url:
    #    pprint(confirmDeviceCreation(execution_url))


if __name__ == "__main__":
    main()
