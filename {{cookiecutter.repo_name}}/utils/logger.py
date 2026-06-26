import logging
import os
from prefect import get_run_logger

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_directory = os.path.join(base_dir, 'logs')


class PrefectHandler(logging.Handler):

    def emit(self, record):

        try:
            prefect_logger = get_run_logger()

            mensaje = self.format(record)

            if record.levelno >= logging.ERROR:
                prefect_logger.error(mensaje)

            elif record.levelno >= logging.WARNING:
                prefect_logger.warning(mensaje)

            else:
                prefect_logger.info(mensaje)

        except Exception:
            pass


def get_logger(nombre="Unknow - def. Name"):

    #Validar existencia carpeta Log
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Definir nombre y nivel del Logger
    logger = logging.getLogger(nombre)
    logger.setLevel(logging.INFO)

    #Validar la existencia del objeto (Manejador/Gestor)
    if logger.handlers:
        return logger

    #Definir la estructura del Log
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s", datefmt='%d/%m/%Y %I:%M:%S %p')

    #Definir el destino del archivo log y almacenar datos
    log_path = os.path.join(log_directory, f'{nombre}.log')
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setFormatter(formatter)

    #Mostrar los log en la consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    #Enviar los logs al orquestador, en este caso Prefect
    prefect_handler = PrefectHandler()
    prefect_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.addHandler(prefect_handler)
    
    return logger
