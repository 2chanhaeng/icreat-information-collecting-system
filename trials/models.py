from django.db import models


class Trial(models.Model):
    """
    '과제명': str,
    '과제번호': str,
    '연구기간': str,
    '연구범위': str,
    '연구종류': str,
    '연구책임기관': str,
    '임상시험단계(연구모형)': str,
    '전체목표연구대상자수': int,
    '진료과': str
    """

    name = models.CharField(max_length=100, verbose_name="과제명")
    number = models.CharField(
        unique=True,
        max_length=100,
        verbose_name="과제번호",
    )
    period = models.CharField(max_length=100, verbose_name="연구기간")
    scope = models.CharField(max_length=100, verbose_name="연구범위")
    kind = models.CharField(max_length=100, verbose_name="연구종류")
    institution = models.CharField(
        max_length=100,
        verbose_name="연구책임기관",
    )
    stage = models.CharField(
        max_length=100,
        verbose_name="임상시험단계(연구모형)",
    )
    target = models.IntegerField(
        verbose_name="전체목표연구대상자수",
        null=True,  # Some data does not have this field.
    )
    department = models.CharField(max_length=100, verbose_name="진료과")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.number})"
