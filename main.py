
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/extract/{rfc}/{req}/{anio}")
def get_results(rfc: str, req: str, anio: int = None):
    return {
            "rfc": rfc, 
            "req": req, 
            "anio":anio,
            "result":"200",
            "message":"archivo generado satisfactoriamente",
            "pdf":""}
