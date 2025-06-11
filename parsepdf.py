import pathlib
import base64
from base64 import b64decode, b64encode

def pdf_to_base64(file):
    try:
        with open(file, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
            return encoded_string.decode("utf-8")  # Decode bytes to string
    except FileNotFoundError:
        print(f"Error: File not found at {file}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None