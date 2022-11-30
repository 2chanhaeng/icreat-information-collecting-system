import requests
import environ
from pathlib import Path

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env(env_file=".env")
DEFAULT_PER_PAGE = 100
DATA_DIR_LITERAL = "data"
DATA_PATH = Path(DATA_DIR_LITERAL)
DATA_PATH.mkdir(exist_ok=True)


def get_response(page: int, per_page: int) -> requests.models.Response:
    """
    Get response from API
    {
        'currentCount': int,
        'data': [
            {
                '과제명': str,
                '과제번호': str,
                '연구기간': str,
                '연구범위': str,
                '연구종류': str,
                '연구책임기관': str,
                '임상시험단계(연구모형)': str,
                '전체목표연구대상자수': int,
                '진료과': str
            }
        ],
        'matchCount': int,
        'page': page,
        'perPage': per_page,
        'totalCount': int
    }
    """
    URL = (
        "https://api.odcloud.kr/api/3074271/v1/"
        "uddi:cfc19dda-6f75-4c57-86a8-bb9c8b103887"
    )
    response = requests.get(
        URL,
        params={"page": page, "perPage": per_page, "serviceKey": env("API_KEY")},
    )
    return response
