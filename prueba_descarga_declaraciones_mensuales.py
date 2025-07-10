import parsepdf
import pathlib
import os
from clases.logs import Log

log = Log("logs/extractor.log")

def getfilesdm(rfc,inicio,final):    
    path_descarga = "E:\\SAT\\"+rfc+"\\DP"
    log.write("info",f" {rfc} - Descarga de archivos Declaraciones Provisionales")
    if(os.path.exists(path_descarga)):
        resultados = {}
        archivos = []
        anios = []
        for x in range(inicio,final+1):
            anios.append(x)
        print(anios)
        for i in anios:
            for pdf_file in pathlib.Path(path_descarga).glob(f'*{str(i)}*.pdf'):    
                        archivos.append(parsepdf.pdf_to_base64(pdf_file))
            resultados[str(i)] = archivos        
        log.write("info",f" {rfc} - Procesamiento concluido satisfactoriamente")
        return {
            "rfc" : rfc,
            "result" : "success",
            "message" : "Proceso de descarga satisfactorio",
            "files" : archivos
        }
    else:
         log.write("info",f" {rfc} - El repositorio indicado no existe!")
         return {
            "rfc" : rfc,
            "result" : "error",
            "message" : f"El espositorio no existe {path_descarga}",            
        } 

print(getfilesdm("RIN0502285BA",2020,2025))
