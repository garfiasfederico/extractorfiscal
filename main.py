
from typing import Union
from fastapi import FastAPI
import declaraciones
import constancias
import docopinion

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/extract/{rfc}/{req}/{anio_inicio}/{anio_fin}")
def get_results(rfc: str, req: str, anio_inicio: int = None, anio_fin: int = None):


    if(req.lower()=="da"):
        resultado = declaraciones.getdeclaraanuales(rfc,anio_inicio,anio_fin)
    elif req.lower()=="csf" :
        resultado = constancias.getcsf(rfc)
    elif req.lower()=="do"
        resultado = docopinion.getdocopi(rfc)
    else:
        return{
            "message":f"El requerimiento {req} no existe en nuestro catálogo"
        }

    return {
            "rfc": rfc, 
            "req": req, 
            "anio_inicio":anio_inicio,
            "anio_final":anio_fin,
            "result":resultado["result"],
            "message":resultado["message"],
            "files":resultado["files"]
            }
