from django.db import models


class BukuTelepon(models.Model):
    nama = models.CharField(max_length=255)
    no_telepon = models.CharField(max_length=13)
    alamat = models.TextField()
    perusahaan = models.CharField(max_length=255)
