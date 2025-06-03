import logging
class Log:
    filename = ""
    logger = ""
    def __init__(self,log):
        self.filename = log
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
        filename=self.filename,
        encoding="utf8",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s:%(message)s"
        )
    
    def write(self,tipo,mensaje):
        if(tipo=="info"):
            self.logger.info(mensaje)
        if(tipo=="warning"):
            self.logger.warning(mensaje)
        if(tipo=="error"):
            self.logger.error(mensaje)
        if(tipo=="debug"):
            self.logger.debug(mensaje)
        