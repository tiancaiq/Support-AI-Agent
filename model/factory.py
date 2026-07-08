from abc import ABC, abstractmethod
import os
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import BaseChatModel
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from utils.config_handler import  rag_config


def get_required_api_key() -> str:
    env_name = rag_config.get("api_key_env", "DASHSCOPE_API_KEY")
    api_key = os.getenv(env_name)
    if not api_key:
        raise RuntimeError(
            f"Missing API key. Set {env_name} in your environment or local .env file."
        )
    return api_key


class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass

class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | ChatTongyi]:
        return ChatTongyi(model = rag_config["chat_model_name"], api_key= get_required_api_key())


class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | DashScopeEmbeddings]:
        return DashScopeEmbeddings(model = rag_config["embedding_model_name"], dashscope_api_key= get_required_api_key())



chat_model = ChatModelFactory().generator()
embedding_model = EmbeddingsFactory().generator()
