
from typing import Union
from fastapi import FastAPI, File, UploadFile
import shutil
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
import pathlib
from pathlib import Path
import getdatacompany
app = FastAPI()



@app.get("/")
def read_root():
    return {"App": "Extractor Fiscal V 1.0"}


@app.get("/extract/{rfc}/{req}/{anio_inicio}/{anio_fin}")
async def get_results(rfc: str, req: str, anio_inicio: int = None, anio_fin: int = None):
    response = {}
    if(req.lower()=="da"):        
        #resultado =  declaraciones.getdeclaraanuales(rfc,anio_inicio,anio_fin)
        resultado = Thread(target=declaraciones.getdeclaraanuales,args=(rfc,anio_inicio,anio_fin,))
        resultado.start() 
        resultado.join() 
    elif req.lower()=="csf" :        
        #resultado =  constancias.getcsf(rfc)
        resultado = Thread(target=constancias.getcsf,args=(response,rfc,))
        resultado.start() 
        resultado.join() 
    elif req.lower()=="do":
        #resultado =  docopinion.getdocopi(rfc)
        resultado = Thread(target=docopinion.getdocopi,args=(rfc,))
        resultado.start() 
        resultado.join() 
    elif req.lower()=="daa":
        #resultado =  declaraciones_acuses.getdeclaraanualesacuses(rfc,anio_inicio,anio_fin)   
        resultado = Thread(target=declaraciones_acuses.getdeclaraanualesacuses,args=(rfc,anio_inicio,anio_fin,))
        resultado.start() 
        resultado.join() 
    elif req.lower()=="dap":
        #resultado =  declaraciones_pagadas.getdeclaraanualpagada(rfc,anio_inicio,anio_fin)   
        resultado = Thread(target=declaraciones_pagadas.getdeclaraanualpagada,args=(rfc,anio_inicio,anio_fin,))
        resultado.start() 
        resultado.join() 
    elif req.lower()=="dm":
        #resultado =   declaraciones_mensuales.getdeclaramensuales(rfc,anio_inicio,anio_fin)   
        resultado = Thread(target=declaraciones_mensuales.getdeclaramensuales,args=(rfc,anio_inicio,anio_fin,))
        resultado.start() 
        resultado.join() 
    elif req.lower()=="dma":
        #resultado =  declaraciones_mensuales_a.getdeclaramensualesa(rfc,anio_inicio,anio_fin) 
        resultado = Thread(target=declaraciones_mensuales_a.getdeclaramensualesa,args=(rfc,anio_inicio,anio_fin,))
        resultado.start() 
        resultado.join()       
    elif req.lower()=="dmp":
        #resultado =  declaraciones_mensuales_p.getdeclaramensualesp(rfc,anio_inicio,anio_fin)
        resultado = Thread(target=declaraciones_mensuales_p.getdeclaramensualesp,args=(rfc,anio_inicio,anio_fin,))
        resultado.start() 
        resultado.join()              
    elif req.lower()=="dce":
        #resultado =  contabildad_electronica.getcontabilidadelectronica(rfc,anio_inicio,anio_fin)  
        resultado = Thread(target=contabildad_electronica.getcontabilidadelectronica,args=(rfc,anio_inicio,anio_fin,))
        resultado.start() 
        resultado.join()     
    elif req.lower()=="ddm":
        #resultado =  descarga_declaraciones_mensuales.getfilesdm(rfc,anio_inicio,anio_fin,"DM") 
        resultado = Thread(target=descarga_declaraciones_mensuales.getfilesdm,args=(rfc,anio_inicio,anio_fin,"DM",))
        resultado.start() 
        resultado.join()  
    elif req.lower()=="ddma":
        #resultado =  descarga_declaraciones_mensuales.getfilesdm(rfc,anio_inicio,anio_fin,"DMA")   
        resultado = Thread(target=descarga_declaraciones_mensuales.getfilesdm,args=(rfc,anio_inicio,anio_fin,"DMA",))
        resultado.start() 
        resultado.join()
    elif req.lower()=="ddmp":
        #resultado =  descarga_declaraciones_mensuales.getfilesdm(rfc,anio_inicio,anio_fin,"DMP") 
        resultado = Thread(target=descarga_declaraciones_mensuales.getfilesdm,args=(rfc,anio_inicio,anio_fin,"DMP",))
        resultado.start() 
        resultado.join()  
    elif req.lower()=="ddce":
        #resultado =  descarga_contabilidad_electronica.getfilescontabilidadelectronica(rfc,anio_inicio,anio_fin,"CE") 
        resultado = Thread(target=descarga_contabilidad_electronica.getfilescontabilidadelectronica,args=(rfc,anio_inicio,anio_fin,"CE",))
        resultado.start() 
        resultado.join()        
    else:
        return{
            "message":f"El requerimiento {req} no existe en nuestro catálogo"
        }
    
    return_value = resultado.return_value

    return {
            "rfc": rfc, 
            "req": req, 
            "anio_inicio":anio_inicio,
            "anio_final":anio_fin,
            "result":return_value["result"],
            "message":return_value["message"],
            "files":return_value["files"]
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
        resultado.join()        
    else:
        return{
            "message":f"El requerimiento {req} no existe en nuestro catálogo"
        }
    
    
    return_value = resultado.return_value
    
    return {
            "rfc": rfc, 
            "req": req,             
            "result":return_value["result"],
            "message":return_value["message"],
            "doc":return_value["doc"]
            }

@app.post("/infonavit/uploadopinion")
async def upload_opinion(rfc:str,file_:UploadFile = File(...)):
    getdatacompany.getDataCompany(rfc)
    if(getdatacompany.contribuyente!=""):
        if file_.content_type == "application/pdf": #and len(file_)<1000:
            descarga = "/root/"+rfc+"/INFONAVIT"
            #descarga = "E:\\SAT\\"+rfc+"\\INFONAVIT"    
            folder_path = Path(descarga)
            folder_path.mkdir(parents=True, exist_ok=True)
            for file in pathlib.Path(descarga).glob('*.*'):
                try:
                    file.unlink()
                except:
                    pass
            try:
                with open(f"{descarga}/constancia_infonavit.pdf", "wb") as buffer:
                    shutil.copyfileobj(file_.file, buffer)
                return {"result":"success","filename" : file_.filename, "message" : "Archivo cargado satisfactoriamente", "Tipo archivo":file_.content_type}
            except Exception as ex:
                return {"result":"error","descripción" : str(ex)}
            
        else:
            return {"result":"error","filename" : file_.filename, "message" : "El archivo no corresponde a un documento PDF o es demasiado pesado.", "Tipo archivo":file_.content_type,"size":len(file_)}
    else:
        return {"result":"error","message" : "El rfc:" + rfc + " no se encuentra registrado en la base de datos"}

    