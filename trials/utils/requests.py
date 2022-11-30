import csv
from datetime import datetime
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


def get_data() -> list[dict[str, str | int]]:
    page = 1
    per_page = DEFAULT_PER_PAGE
    response = get_response(page, per_page)
    initdata = response.json()
    total_count = initdata.get("totalCount")
    if not total_count:
        print(__name__, "No data")
        print(f"status code: {response.status_code}")
        print(f"{response.text}")
        return []
    total_page = total_count // per_page + 2
    data = initdata.get("data") + sum(
        (
            get_response(page, per_page).json().get("data")
            for page in range(2, total_page)
        ),
        [],
    )
    return data


def save_data_to_csv(data: list[dict[str, str | int]]) -> None:
    """
    Save `list[dict]` type data to csv file.
    The file is saved in the `data` directory.
    The name is in `%Y%m%d-%H%M%S`(yyyymmdd-HHMMSS) format when this function is executed.
    The fieldname is defined by the key of the first dictionary of the list.
    """
    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    with open(DATA_PATH / f"{now}.csv", "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, data[0].keys())
        writer.writeheader()
        writer.writerows(data)
