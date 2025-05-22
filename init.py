import xml.etree.ElementTree as ET
import os
import base64

config_path = "config/config.xml"
rfc = ""
razon_social = ""
path_cert = ""
path_key = ""
password = ""
path_descarga = ""

def existeconfig():
    if(os.path.exists(config_path)):
        return True
    else:
        return False
    
if(existeconfig()):
    
    xml = ET.parse("config/config.xml");
    root = xml.getroot()
    contribuyentes = len(root.findall("contribuyente"))    

    if(contribuyentes>0):        
        for contribuyente in root.findall("contribuyente"):
            rfc = contribuyente.attrib["rfc"]
            razon_social = contribuyente.attrib["nombre"]
            fiel = contribuyente.findall("firma")
            for firma in fiel:
                path_cert = firma.attrib["cert"]
                path_key = firma.attrib["key"]
                password = firma.attrib["password"]
            descarga = root.findall("descarga")
            for path_des in descarga:
                path_descarga = path_des.attrib["url"]
                   
    else:
        print("El archivo de configuración es incorrecto")    
else:
    print("No existe archivo de configuración")

