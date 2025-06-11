#from clases.logs import Log
#import getdatacompany

#getdatacompany.getDataCompany("TRA1001211I3")
#if(getdatacompany.contribuyente==""):
#    print("Contribuyente no localizado")
#else:
#    print(f"Contribuyente localizado: {getdatacompany.contribuyente}")

#def pruebaFuncion():
#    return {
#        "result":"ok",
#        "message":"Proceso concluido"
#    }

#prueba = pruebaFuncion()
#log = Log("logs/log_declaraciones.log")
#log.write("info","Hola que tal")


import pathlib
import base64
from base64 import b64decode, b64encode
import getdatacompany

def pdf_to_base64(file):
    try:
        with open(file, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
            return encoded_string.decode("utf-8")  # Decode bytes to string
    except FileNotFoundError:
        print(f"Error: File not found at {file}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

archivos = []

#for pdf_file in pathlib.Path('E:\\SAT\\SAGF8705279C8').glob('*2019*.pdf'):    
#    archivos.append(pdf_to_base64(pdf_file))

#print(archivos)

getdatacompany.getDataCompany("SPG1010058K0")
print(getdatacompany.password_fiel)
