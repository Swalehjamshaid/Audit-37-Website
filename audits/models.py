from django.db import models
from django.contrib.auth.models import User

class Website(models.Model):
    url = models.URLField(unique=True)
    name = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.url.replace('https://', '').replace('http://', '').split('/')[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Audit(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_cumulative = models.BooleanField(default=False)

    def __str__(self):
        return f"Audit {self.id} - {self.website} - {self.timestamp.date()}"

class AuditMetric(models.Model):
    audit = models.ForeignKey(Audit, on_delete=models.CASCADE, related_name='metrics')
    name = models.CharField(max_length=255)
    value = models.FloatField()  # 0-100 score
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}: {self.value}"
