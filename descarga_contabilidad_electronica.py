import parsepdf
import pathlib
import os
from clases.logs import Log

log = Log("logs/extractor.log")

def getfilescontabilidadelectronica(rfc,inicio,final,repo):    
    path_descarga = "/Library/WebServer/Documents/extractorfiscal/"+rfc+"/"+repo
    log.write("info",f" {rfc} - Descarga de archivos Declaraciones Provisionales "+repo)
    if(os.path.exists(path_descarga)):
        resultados = {}
        archivos = []
        anios = []
        for x in range(inicio,final+1):
            anios.append(x)
        
        resultados = {}
        for i in anios:
            resultados[str(i)] = []
            #comenzamos a procesar las metas generadas de los archivos
            path_meta = path_descarga+"/"+"meta"+str(i)+".txt"
            if(os.path.exists(path_meta)):
                #print(f"Si existe meta para este año: {i} {path_meta}")
                #procedemos con la lectura de la meta para ir obteniendo los archivos
                meta = open(path_meta)
                data = meta.read()
                folios = data.split("&")
                acuses_recepcion_archivos = []
                acuses_procesamiento = []
                acuses_zip = []
                acuses_sellos = []                
                for f in folios:
                    #procedemos al procesamiento de los folio recabados en la meta
                    f_m = f.split("|")
                    if(len(f_m)>1):
                        #print(f"Folio: {f_m[0]} Resultado: {f_m[1]}")

                        #obtenemos los pdf de acuses de recepcion
                        path_acuse_recepcion = path_descarga+"/"+f"AR_{f_m[0]}.pdf"
                        if(os.path.exists(path_acuse_recepcion)):
                            #print(f"El acuse de recepcion del folio: {f_m[0]}")                            
                            acuses_recepcion_archivos.append(parsepdf.pdf_to_base64(path_acuse_recepcion))
                        
                        #obtenemos los pdf de acuses de procesamiento
                        if(f_m[1]=="Aceptado"):
                            path_acuse_procesamiento = path_descarga+"/"+f"APA_{f_m[0]}.pdf"
                        else:
                            path_acuse_procesamiento = path_descarga+"/"+f"APR_{f_m[0]}.pdf"
                        
                        if(os.path.exists(path_acuse_procesamiento)):
                            acuses_procesamiento.append(parsepdf.pdf_to_base64(path_acuse_procesamiento))

                        #obtenemos los archivos de sello
                        path_acuse_sello = path_descarga+"/"+f"SelloDigital_{f_m[0]}.xml"
                        if(os.path.exists(path_acuse_sello)):
                            acuses_sellos.append(parsepdf.pdf_to_base64(path_acuse_sello))

                        #obtenemos los archivos zip
                        for zip_file in pathlib.Path(path_descarga).glob(f'{rfc}{str(i)}*.zip'):    
                            acuses_zip.append(parsepdf.pdf_to_base64(zip_file))
                        

                        #obtenemos     
                #print(acuses_recepcion_archivos)
                resultados[str(i)] ={
                    "acuses_recepcion":acuses_recepcion_archivos,
                    "acuses_procesamiento":acuses_procesamiento,
                    "acuses_zip":acuses_sellos,
                    "acuses_sellos":acuses_zip,
                } 

                    
                print("Esta meta tiene un total de: "+str(len(folios)))
            else:
                print(f"No existe meta para este año: {i} {path_meta}")
                  

            #for pdf_file in pathlib.Path(path_descarga).glob(f'*{str(i)}.pdf'):    
            #            archivos.append(parsepdf.pdf_to_base64(pdf_file))
            #resultados[str(i)] = archivos 
            #archivos = []       

        print(resultados)
        log.write("info",resultados)
        log.write("info",f" {rfc} - Procesamiento concluido satisfactoriamente "+repo)
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
            "files":None          
        } 
