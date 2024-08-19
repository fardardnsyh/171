from django.db import models
import uuid

class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    pdf_file = models.FileField(upload_to='pdfs/', max_length=255)
    word_file = models.FileField(upload_to='words/', blank=True, null=True)
    pptx_file  = models.FileField(upload_to='pptx/', blank=True, null=True)
    image_file = models.FileField(upload_to='images/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)