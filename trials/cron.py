import sys
from pathlib import Path
from datetime import datetime
from .utils.requests import get_data, save_data_to_csv
from .models import Trial

LOG_PATH = Path(__file__).parent.parent / "log"
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


def log_updated_data():
    """
    Log the updated data.
    """
    now = datetime.now()
    log_fn = LOG_PATH / f"{now.strftime('%Y%m%d-%H%M%S')}.log"
    with open(log_fn, "w") as sys.stdout:
        update_data()
    sys.stdout = sys.__stdout__
    print(f"Log is saved to {log_fn}.")


def update_data():
    """
    Update data using get_data.
    If there is a new data, create a new Trial instance.
    Else if some data is updated, update the instance.
    """
    data = get_data()
    save_data_to_csv(data)
    counter = {"created": 0, "fail": 0, "updated": 0}
    for row in data:
        trial_info = {verbose_to_field[k]: v for k, v in row.items()}
        # Convert verbose name to field name
        if not trial_info.get("target"):
            # If the target is empty, skip the data
            # It will make the data null
            trial_info.pop("target")
        try:
            trial, is_created = Trial.objects.get_or_create(
                number=trial_info.pop("number"),
                defaults=trial_info,
            )
            # Get trial instance with number
        except Exception as e:
            name = row.get("name")
            error = str(e)
            if name:  # If name exists, print the name and error.
                print(f"{name} got {error}.")
            else:  # If name does not exist, print data and error.
                print(f"This data got {error}.")
                print("\n".join(f"  {key}: {value}" for key, value in row.items()))
            counter["fail"] += 1
            continue
        if is_created:
            # If the trial is created, print the created trial.
            print(f"Successfully create {trial}.")
            counter["created"] += 1
        else:
            # If the trial already exists,
            # check that the data is updated.
            trial, is_updated = update_if_changed(trial, trial_info)
            if is_updated:
                # If the data is updated, print the updated trial.
                trial.save()
                print(f"Successfully update {trial}.")
                counter["updated"] += 1
    summary = summarize_counter(counter)
    print(summary)


def update_if_changed(trial, trial_info):
    """
    Check that the data is updated.
    If the data is updated, update the instance.
    """
    for key, value in trial_info.items():
        is_updated = False
        if getattr(trial, key) != value:
            # If the data is changed,
            # update the data
            setattr(trial, key, value)
            # and set is_updated to True.
            is_updated = True
    return trial, is_updated


def summarize_counter(counter):
    """
    Summarize the counter.
    """
    updated = counter["updated"]
    created = counter["created"]
    fails = counter["fail"]
    successes = updated + created
    total = successes + fails
    if total == 0:
        return "Nothing is updated."
    percentage = successes / total * 100
    summary = (
        f"{created} data is created."
        + f" {updated} data is updated."
        + f" {fails} data is failed."
        + f" {percentage:.2f}% of {total} data is updated or created."
    )
    return summary
