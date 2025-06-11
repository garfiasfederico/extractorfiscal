
from typing import Union
from fastapi import FastAPI
import declaraciones

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/extract/{rfc}/{req}/{anio_inicio}/{anio_final}")
def get_results(rfc: str, req: str, anio_inicio: int = None, anio_final: int = None):
    resultado = declaraciones.getdeclaraanuales(rfc,anio_inicio,anio_final)
    return {
            "rfc": rfc, 
            "req": req, 
            "anio_inicio":anio_inicio,
            "anio_final":anio_final,
            "result":resultado["result"],
            "message":resultado["message"],
            }
