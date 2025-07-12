import parsepdf
import pathlib
import os
from clases.logs import Log
import init

log = Log("logs/extractor.log")

def getfilesdm(rfc,inicio,final):    
    path_descarga = init.path_descarga

    log.write("info",f" {rfc} - Descarga de archivos Declaraciones Provisionales")
    if(os.path.exists(path_descarga)):
        resultados = {}
        archivos = []
        anios = []
        for x in range(inicio,final+1):
            anios.append(x)
        print(anios)
        for i in anios:
            for pdf_file in pathlib.Path(path_descarga).glob(f'*{str(i)}.pdf'):    
                        archivos.append(parsepdf.pdf_to_base64(pdf_file))
            resultados[str(i)] = archivos   
            archivos=[]     
        log.write("info",f" {rfc} - Procesamiento concluido satisfactoriamente")
        return {
            "rfc" : rfc,
            "result" : "success",
            "message" : "Proceso de descarga satisfactorio",
            "files" : resultados
        }
    else:
         log.write("info",f" {rfc} - El repositorio indicado no existe!")
         return {
            "rfc" : rfc,
            "result" : "error",
            "message" : f"El espositorio no existe {path_descarga}",            
        } 

print(getfilesdm("ACR140408T34",2024,2025))
