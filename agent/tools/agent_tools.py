import os
import random

from langchain_core.tools import  tool
from rag.rag_service import RagSummarizeService
from utils.config_handler import agent_config
from utils.logger_handler import logger
from utils.path_tool import get_abs_path

rag = RagSummarizeService()
user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007"]
month_arr =["2025-01","2025-02","2025-03","2025-04","2025-05","2025-06","2025-07","2025-08","2025-09","2025-10",]
external_data ={}

@tool(description="retrieve robot vacuum knowledge from the vector database")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)

@tool(description="get weather of city")
def get_weather(city: str) -> str:
    return f"city:{city} sunny, rain soon"

@tool(description="get user city name")
def get_user_location() -> str:
    return random.choice(["London", "LA","SF"])

@tool(description="get user ID")
def get_user_id() -> str:
    return random.choice(user_ids)

@tool(description="get current month")
def get_current_month() -> str:
    return random.choice(month_arr)

def generate_external_data():
    """
    {
        "user_id" :{
           "month" :
           }
    }

    :return:
    """
    if not external_data:
        external_data_path = get_abs_path(agent_config["external_data_path"])

        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"external_data_path:{external_data_path} not exist")

        with open(external_data_path, "r", encoding = "utf-8") as f:
            for line in f.readlines()[1:]:
                arr: list[str] = line.strip().split(",")

                user_id: str = arr[0].replace('"', "")
                feature: str = arr[1].replace('"', "")
                efficiency: str = arr[2].replace('"', "")
                consumable: str = arr[3].replace('"', "")
                comparison: str = arr[4].replace('"', "")
                time: str = arr[5].replace('"', "")

                if user_id not in external_data:
                    external_data[user_id] = {}
                external_data[user_id][time] = {
                    "feature": feature,
                    "efficiency": efficiency,
                    "consumable": consumable,
                    "comparison": comparison,

                }

@tool(description="get external usage data; return an empty string if not found")
def fetch_external_data(user_id: str, month: str) -> str:
    generate_external_data()
    try:
        return external_data[user_id][month]
    except KeyError:
        logger.warning(f"user_id:{user_id} month:{month} not exist")
        return ""


@tool(description="prepare context for report generation")
def fill_context_for_report():
    return "fill_context_for_report success"


# if __name__ == '__main__':
#     print(fetch_external_data("1001", "2025-01"))
