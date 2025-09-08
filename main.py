
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
import declaraciones_mensuales_p
import descarga_contabilidad_electronica
import contabildad_electronica
import opinion_imss
from threading import Thread, Barrier
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
        resultado =   declaraciones_mensuales.getdeclaramensuales(rfc,anio_inicio,anio_fin)   
    elif req.lower()=="dma":
        resultado =  declaraciones_mensuales_a.getdeclaramensualesa(rfc,anio_inicio,anio_fin)       
    elif req.lower()=="dmp":
        resultado =  declaraciones_mensuales_p.getdeclaramensualesp(rfc,anio_inicio,anio_fin)       
    elif req.lower()=="dce":
        resultado =  contabildad_electronica.getcontabilidadelectronica(rfc,anio_inicio,anio_fin)       
    elif req.lower()=="ddm":
        resultado =  descarga_declaraciones_mensuales.getfilesdm(rfc,anio_inicio,anio_fin,"DM")   
    elif req.lower()=="ddma":
        resultado =  descarga_declaraciones_mensuales.getfilesdm(rfc,anio_inicio,anio_fin,"DMA")   
    elif req.lower()=="ddmp":
        resultado =  descarga_declaraciones_mensuales.getfilesdm(rfc,anio_inicio,anio_fin,"DMP")   
    elif req.lower()=="ddce":
        resultado =  descarga_contabilidad_electronica.getfilescontabilidadelectronica(rfc,anio_inicio,anio_fin,"CE")       
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

@app.get("/imss/extract/docopinion/{rfc}")
async def get_docs(rfc: str,req: str):
    if(req.lower()=="do"):
        data = {}
        #resultado =  opinion_imss.getopinionimss(data,rfc)
        #max_multitareas = 10
        #barri = Barrier(max_multitareas)
        #resultado_ = {}

        resultado = Thread(target=opinion_imss.getopinionimss,args=(data,rfc,))
        resultado.start() 
        resultado_ = resultado.join()        
    else:
        return{
            "message":f"El requerimiento {req} no existe en nuestro catálogo"
        }
    
    
    return data
    return {
            "rfc": rfc, 
            "req": req,             
            "result":resultado["result"],
            "message":resultado["message"],
            "doc":resultado["doc"]
            }