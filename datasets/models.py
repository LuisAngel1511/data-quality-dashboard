from django.db import models

class Dataset(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="datasets/")
    n_rows = models.BigIntegerField(null=True, blank=True)
    n_cols = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Column(models.Model):
    ROLE_CHOICES = [
        ("numeric","numeric"),
        ("categorical","categorical"),
        ("datetime","datetime"),
        ("text","text"),
    ]
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="columns")
    name = models.CharField(max_length=255)
    dtype_detected = models.CharField(max_length=64)
    role = models.CharField(max_length=16, choices=ROLE_CHOICES)

class Profile(models.Model):
    dataset = models.OneToOneField(Dataset, on_delete=models.CASCADE, related_name="profile")
    stats_json = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
