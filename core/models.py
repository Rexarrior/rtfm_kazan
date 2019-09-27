from django.db import models as models


class CustomUser(models.Model):
    user_id = models.BigAutoField(primary_key=True)


class Measure(models.Model):
    user_id = models.ForeignKey('CustomUser',
                              on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    operator_id = models.ForeignKey('Operator', on_delete=models.CASCADE)
    signal = models.FloatField()
    time = models.DateField()


class Operator(models.Model):
    name = models.CharField(max_length=50)
    operator_id = models.AutoField(primary_key=True)


class Setting(models.Model):
    name = models.CharField(unique=True, primary_key=True, max_length=100)
    value = models.FloatField()


class Coverage(models.Model):
    coverage_id = models.AutoField(primary_key=True)
    operator_id = models.ForeignKey('Operator', on_delete=models.CASCADE)
    reliability = models.FloatField()


class CoveragePoints(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    coverage_id = models.ForeignKey("Coverage", on_delete=models.CASCADE)


class Scores(models.Model):
    user_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    score = models.FloatField()