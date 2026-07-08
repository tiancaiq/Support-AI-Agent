import os, hashlib
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader



def get_file_md5_hex(filepath:str): # get hex string
    if not os.path.exists(filepath):
        logger.error(f"{filepath} File does not exist")
        return
    if not os.path.isfile(filepath):
        logger.error(f"{filepath} is not a file")
        return

    md5_obj = hashlib.md5()
    chunk_size = 4096
    try:
        with open(filepath, "rb") as f:
            """
            :=
            chunk = f.read(chunk_size)
            while chunk:
                md5_obj.update(chunk)
                chunk = f.read(chunk_size)
            """
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)

            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"get_file_md5_hex Error: {e}")
        return None

def listdir_with_allowed_type(path: str , allowed_types: tuple[str]): #return file list of a dir
    files = []

    if not os.path.isdir(path):
        logger.error(f"{path} is not a directory")
        return allowed_types
    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path, f))
    return tuple(files)

def pdf_loader(filepath: str, passwd = None) -> list[Document]:
    return PyPDFLoader(filepath, passwd).load()


def txt_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath, encoding="utf-8").load()