import requests
from src.Config.OpcConfig import OpcServer_API

def GetDataFromOpc():
    result = requests.get(OpcServer_API).json()
    return result

if __name__ == "__main__":
    GetDataFromOpc()

