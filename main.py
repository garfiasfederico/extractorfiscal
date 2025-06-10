
from typing import Union
from fastapi import FastAPI
import declaraciones

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/extract/{rfc}/{req}/{anio}")
def get_results(rfc: str, req: str, anio: int = None):
    resultado = declaraciones.getdeclaraanuales(rfc,anio,anio)
    return {
            "rfc": rfc, 
            "req": req, 
            "anio":anio,
            "result":resultado["result"],
            "message":resultado["message"],
            }
