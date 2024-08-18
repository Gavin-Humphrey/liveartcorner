from django.db import models


class Statement(models.Model):
    text = models.CharField(max_length=1024)
    search_text = models.CharField(max_length=1024)
    conversation = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    in_response_to = models.CharField(max_length=1024, null=True, blank=True)
    search_in_response_to = models.CharField(max_length=1024)
    persona = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        db_table = "statement"
