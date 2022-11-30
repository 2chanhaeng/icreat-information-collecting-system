from django.core.management.base import BaseCommand
from trials.models import Trial
from trials.utils.requests import get_data, save_data_to_csv


class Command(BaseCommand):
    help = "Initialize trials."

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

    def handle(self, *args, **options):
        Trial.objects.all().delete()
        data = get_data()
        save_data_to_csv(data)
        counter = {"success": 0, "fail": 0}
        for row in data:
            trial_info = {self.verbose_to_field[k]: v for k, v in row.items()}
            if not trial_info.get("target"):
                trial_info.pop("target")
            try:
                trial = Trial.objects.create(**trial_info)
                self.stdout.write(self.style.SUCCESS(f"Successfully create {trial}."))
                counter["success"] += 1
            except Exception as e:
                name = row.get("name")
                error = self.style.ERROR(str(e))
                if name:  # If name exists, print the name and error.
                    self.stdout.write(f"{name} is not created by {error}.")
                else:  # If name does not exist, print error.
                    self.stdout.write(f"Some data is not created by {error}.")
                    for key, value in row.items():
                        self.stdout.write(f"  {key}: {value}")
                counter["fail"] += 1
        match counter["success"], counter["fail"]:
            case (0, 0):
                summary = self.style.WARNING("No data is created.")
            case (0, fails):
                summary = self.style.ERROR(f"All {fails} data is not created.")
            case (successes, 0):
                summary = self.style.SUCCESS(f"All {successes} data is created.")
            case (successes, fails):
                total = successes + fails
                percentage = successes / total * 100
                summary = (
                    self.style.SUCCESS(f"{successes} data is created.")
                    + self.style.ERROR(f" {fails} data is not created.")
                    + f" {percentage:.2f}% of {total} data is created."
                )
        self.stdout.write(summary)
