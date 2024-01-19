import requests

def get_from_fields()-> list[str]:
    res = requests.get("https://rest.uniprot.org/configure/idmapping/fields")
    return [i["name"] for i in res.json()["groups"][0]["items"] if i["from"]]

def get_to_fields()-> list[str]:
    res = requests.get("https://rest.uniprot.org/configure/idmapping/fields")
    return [i["name"] for i in res.json()["groups"][0]["items"] if i["to"]]
