from utils.config_handler import prompts_config
from utils.path_tool import get_abs_path
from utils.logger_handler import logger


def load_system_prompts():
    try:
        system_prompt_path = get_abs_path(prompts_config["main_prompt_path"])
    except KeyError as e:
        logger.error(f"no main_prompt_path in config file: {e}")
        raise e
    try:
        return open(system_prompt_path, "r",encoding="utf-8").read()
    except Exception as e:
        logger.error(f"process prompt fail {e}")
        raise e


def load_report_prompts():
    try:
        report_prompt_path = get_abs_path(prompts_config["report_prompt_path"])
    except KeyError as e:
        logger.error(f"no report_prompt_path in config file: {e}")
        raise e
    try:
        return open(report_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"process report prompt fail {e}")
        raise e


def load_rag_prompts():
    try:
        rag_prompt_path = get_abs_path(prompts_config["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"no rag_summarize_prompt_path in config file: {e}")
        raise e
    try:
        return open(rag_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"process rag prompt fail {e}")
        raise e

if __name__ == '__main__':
    print(load_report_prompts())