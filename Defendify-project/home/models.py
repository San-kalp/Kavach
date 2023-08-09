from django.db import models


class fraudlent_data_tag(models.Model):
    address = models.CharField(max_length=30)
    exposure = models.CharField(max_length=30)
    cluster_label = models.IntegerField()
    predicted_cluster_label =models.IntegerField()
    sanction_label = models.CharField(max_length=30)



