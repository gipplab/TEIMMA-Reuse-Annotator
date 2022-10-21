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