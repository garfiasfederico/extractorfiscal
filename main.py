
from typing import Union
from fastapi import FastAPI
import declaraciones
import constancias
import docopinion
import declaraciones_acuses
import declaraciones_pagadas
import declaraciones_mensuales
import descarga_declaraciones_mensuales
import declaraciones_mensuales_a
app = FastAPI()


@app.get("/")
def read_root():
    return {"App": "Extractor Fiscal V 1.0"}


@app.get("/extract/{rfc}/{req}/{anio_inicio}/{anio_fin}")
def get_results(rfc: str, req: str, anio_inicio: int = None, anio_fin: int = None):
    if(req.lower()=="da"):
        resultado =  declaraciones.getdeclaraanuales(rfc,anio_inicio,anio_fin)
    elif req.lower()=="csf" :
        resultado =  constancias.getcsf(rfc)
    elif req.lower()=="do":
        resultado =  docopinion.getdocopi(rfc)
    elif req.lower()=="daa":
        resultado =  declaraciones_acuses.getdeclaraanualesacuses(rfc,anio_inicio,anio_fin)   
    elif req.lower()=="dap":
        resultado =  declaraciones_pagadas.getdeclaraanualpagada(rfc,anio_inicio,anio_fin)   
    elif req.lower()=="dm":
        resultado =  declaraciones_mensuales.getdeclaramensuales(rfc,anio_inicio,anio_fin)   
    elif req.lower()=="dma":
        resultado =  declaraciones_mensuales_a.getdeclaramensualesa(rfc,anio_inicio,anio_fin)       
    elif req.lower()=="ddm":
        resultado =  descarga_declaraciones_mensuales.getfilesdm(rfc,anio_inicio,anio_fin,"DM")   
    elif req.lower()=="ddma":
        resultado =  descarga_declaraciones_mensuales.getfilesdm(rfc,anio_inicio,anio_fin,"DMA")   
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
