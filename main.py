
from typing import Union
from fastapi import FastAPI
import declaraciones

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/extract/{rfc}/{req}/{anio_inicio}/{anio_fin}")
def get_results(rfc: str, req: str, anio_inicio: int = None, anio_fin: int = None):
    resultado = declaraciones.getdeclaraanuales(rfc,anio_inicio,anio_fin)
    return {
            "rfc": rfc, 
            "req": req, 
            "anio_inicio":anio_inicio,
            "anio_final":anio_fin,
            "result":resultado["result"],
            "message":resultado["message"],
            }
