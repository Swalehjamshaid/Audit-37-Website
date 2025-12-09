from django.contrib import admin
from .models import Website, Audit, AuditMetric

admin.site.register(Website)
admin.site.register(Audit)
admin.site.register(AuditMetric)
