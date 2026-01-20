from django.db import models


class AnomalyRecord(models.Model):
    title = models.CharField("記録名", max_length=100)
    description = models.TextField("記録内容")
    observed_at = models.DateTimeField("発生日時")
    
    LEVEL_CHOICES = [
        (1, "違和感"),
        (2, "軽度異常"),
        (3, "注意"),
        (4, "重大"),
        (5, "未分類"),
    ]
    anomaly_level = models.IntegerField(
        "異常レベル",
        choices=LEVEL_CHOICES,
        default=1
    )

    note = models.TextField(
        "備考（記録員メモ）",
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class PlayerJudgement(models.Model):
    record = models.ForeignKey(
        AnomalyRecord,
        on_delete=models.CASCADE,
        related_name="judgements"
    )

    JUDGEMENT_CHOICES = [
        (1, "問題なし"),
        (2, "軽微"),
        (3, "注意"),
        (4,"要注意"),
        (5,"重大"),
    ]
    judgement = models.IntegerField(choices=JUDGEMENT_CHOICES, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.record.title} / {self.get_judgement_display()}"
    

# Create your models here.
