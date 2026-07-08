
"""YAML configuration loaders."""

import os
import yaml
from pip._internal.cli import main

from utils.path_tool import get_abs_path


def load_env_file(env_path: str = get_abs_path(".env")):
    if not os.path.exists(env_path):
        return

    with open(env_path, mode="r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def load_rag_config(config_path: str= get_abs_path("config/rag.yml"), encoding: str="utf-8"):
    with open(config_path, mode="r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def load_chroma_config(config_path: str= get_abs_path("config/chroma.yml"), encoding: str="utf-8"):
    with open(config_path, mode="r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def load_prompts_config(config_path: str= get_abs_path("config/prompts.yml"), encoding: str="utf-8"):
    with open(config_path, mode="r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def load_agent_config(config_path: str= get_abs_path("config/agent.yml"), encoding: str="utf-8"):
    with open(config_path, mode="r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


load_env_file()

rag_config = load_rag_config()
chroma_config = load_chroma_config()
prompts_config = load_prompts_config()
agent_config = load_agent_config()

if __name__ == '__main__':
    print(rag_config["api_key_env"])
