"""
summarize
"""
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser

from rag.formatting import append_sources, build_context
from rag.vector_store import VectorStoreService
from utils.prompt_loader import  load_rag_prompts
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model
from utils.logger_handler import logger
from utils.observability import elapsed_ms, now_ms

class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model  = chat_model
        self.chain =self._init_chain()

    def _init_chain(self):
        chain = self.prompt_template | self.model | StrOutputParser()
        return chain

    def retriever_docs(self, query: str) -> list[Document]:
       start_ms = now_ms()
       docs = self.retriever.invoke(query)
       logger.info(
           "[rag_retrieval] query=%r docs=%s latency_ms=%.2f",
           query,
           len(docs),
           elapsed_ms(start_ms),
       )
       return docs

    def rag_summarize(self, query: str) -> str:
        start_ms = now_ms()
        context_docs = self.retriever_docs(query)
        context = build_context(context_docs)

        answer = self.chain.invoke({
            "input": query,
            "context": context,
            }
        )
        response = append_sources(answer, context_docs)
        logger.info(
            "[rag_answer] query=%r docs=%s response_size=%s latency_ms=%.2f",
            query,
            len(context_docs),
            len(response),
            elapsed_ms(start_ms),
        )
        return response

if __name__ == '__main__':
    rag = RagSummarizeService()
    print(rag.rag_summarize("small house fit which model"))
