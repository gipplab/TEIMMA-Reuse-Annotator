from django.db import models

# Create your models here.

class Annotations(models.Model):
	annotation = models.JSONField()

class PlainText(models.Model):
	filename = models.CharField(max_length=200)
	plaintext = models.TextField()

class Math(models.Model):
	filename = models.CharField(max_length=200)
	math = models.JSONField()

class HTMLFiles(models.Model):
	filename = models.CharField(max_length=200)
	htmlfile = models.TextField()

class Pair(models.Model):
    filename1 = models.CharField(max_length=255)
    filename2 = models.CharField(max_length=255)
    case_type = models.CharField(max_length=255)
    case_function = models.CharField(max_length=255)
    comments = models.TextField()
    feedback = models.CharField(max_length=255)
    
    # Add any additional fields or methods as needed
    
    def __str__(self):
        return f"Pair: {self.filename1} - {self.filename2}"