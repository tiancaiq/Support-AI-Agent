from langchain_chroma import Chroma
from langchain_core.documents import Document

from utils.config_handler import  chroma_config
from model.factory import embedding_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from utils.path_tool import get_abs_path
from utils.logger_handler import logger
from utils.file_handler import  pdf_loader ,txt_loader, listdir_with_allowed_type, get_file_md5_hex


class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name = chroma_config["collection_name"],
            embedding_function = embedding_model,
            persist_directory = chroma_config["persist_directory"],
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_config["chunk_size"],
            chunk_overlap=chroma_config["chunk_overlap"],
            separators=chroma_config["separators"],
            length_function=len,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs ={"k": chroma_config["k"]})

    def load_document(self):


        """
        Load supported knowledge files into the vector store.

        MD5 hashes are used to avoid ingesting the same file more than once.

        :return:
        """
        def check_md5_hex(md5_for_check:str):
            if not os.path.exists(get_abs_path(chroma_config["md5_hex_store"])):
                open(get_abs_path(chroma_config["md5_hex_store"]), "w").close()
                return False
            with open(get_abs_path(chroma_config["md5_hex_store"]),"r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True

                return False

        def save_md5_hex(md5_for_check:str):
            with open(get_abs_path(chroma_config["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_for_check + "\n")

        def get_file_documents(read_path: str):
            if read_path.endswith("txt"):
                return txt_loader(read_path)
            if read_path.endswith("pdf"):
                return pdf_loader(read_path)

            return []

        allowed_files_path: list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_config["data_path"]),
            tuple(chroma_config["allow_knowledge_file_type"]),
        )

        for path in allowed_files_path:
            md5_hex = get_file_md5_hex(path)
            if check_md5_hex(md5_hex):
                logger.info(f"md5 hex already {path}")
                continue
            try:
                documents: list[Document] = get_file_documents(path)
                if not documents:
                    logger.warning(f"{path} no data skip")
                    continue
                split_document: list[Document] = self.spliter.split_documents(documents)

                if not split_document:
                    logger.warning(f"{path} no split document, skip")
                    continue

                # Save chunks to the vector store.
                self.vector_store.add_documents(split_document)
                # Save the file hash to avoid duplicate ingestion.
                save_md5_hex(md5_hex)
                logger.info(f"md5 hex saved {path}")
            except Exception as e:
                # exc_info=True records the full stack trace for ingestion failures.
                logger.error(f"{path} error {e}", exc_info=True )
                continue

if __name__ == '__main__':
    vs = VectorStoreService()
    vs.load_document()
    retriever = vs.get_retriever()
    res = retriever.invoke("system")
    for r in res:
        print(r.page_content)
