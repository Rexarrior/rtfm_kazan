from django.db import models as models
from core.proto_models import db_models_pb2 as proto


class CustomUser(models.Model):
    user_id = models.BigAutoField(primary_key=True)


class Measure(models.Model):
    user_id = models.ForeignKey('CustomUser',
                              on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    operator_id = models.ForeignKey('Operator', related_name='operator_id', on_delete=models.CASCADE)
    signal = models.FloatField()
    time = models.DateField()


class Operator(models.Model):
    name = models.CharField()
    operator_id = models.AutoField(primary_key=True)


class Setting(models.Model):
    name = models.CharField(unique=True, primary_key=True)
    value = models.FloatField()


class Coverage(models.Model):
    coverage_id = models.AutoField(primary_key=True)
    operator_id = models.ForeignKey('Operator', related_name='operator_id', on_delete=models.CASCADE)
    reliability = models.FloatField()


class Name(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    coverage_id = models.ForeignKey("Coverage", related_name='coverage_id', on_delete=models.CASCADE)


class Scores(models.Model):
    user_id = models.ForeignKey('CustomUser', related_name='user_id', on_delete=models.CASCADE)
    score = models.FloatField()