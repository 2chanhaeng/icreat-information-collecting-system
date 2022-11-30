from .utils.requests import get_data, save_data_to_csv
from .models import Trial

verbose_to_field = {
    "과제명": "name",
    "과제번호": "number",
    "연구기간": "period",
    "연구범위": "scope",
    "연구종류": "kind",
    "연구책임기관": "institution",
    "임상시험단계(연구모형)": "stage",
    "전체목표연구대상자수": "target",
    "진료과": "department",
}


def update_data():
    data = get_data()
    save_data_to_csv(data)
    counter = {"success": 0, "fail": 0}
    for row in data:
        trial_info = {verbose_to_field[k]: v for k, v in row.items()}
        if not trial_info.get("target"):
            trial_info.pop("target")
        try:
            trial = Trial.objects.update_or_create(**trial_info)
            print(f"Successfully create {trial}.")
            counter["success"] += 1
        except Exception as e:
            name = row.get("name")
            error = str(e)
            if name:  # If name exists, print the name and error.
                print(f"{name} is not created by {error}.")
            else:  # If name does not exist, print error.
                print(f"Some data is not created by {error}.")
                for key, value in row.items():
                    print(f"  {key}: {value}")
            counter["fail"] += 1
    match counter["success"], counter["fail"]:
        case (0, 0):
            summary = "No data is created."
        case (0, fails):
            summary = f"All {fails} data is not created."
        case (successes, 0):
            summary = f"All {successes} data is created."
        case (successes, fails):
            total = successes + fails
            percentage = successes / total * 100
            summary = (
                f"{successes} data is created."
                + f" {fails} data is not created."
                + f" {percentage:.2f}% of {total} data is created."
            )
    print(summary)
