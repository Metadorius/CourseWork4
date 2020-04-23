from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Cathedra(models.Model):
    cathedra_number = models.IntegerField()
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=512)

    def __str__(self):
        return f'{self.title} ({self.cathedra_number})'


class Position(models.Model):
    position_name = models.CharField(max_length=64)

    def __str__(self):
        return self.position_name


class Teacher(models.Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    patronymic = models.CharField(max_length=64)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    phone_number = PhoneNumberField(unique=True)
    cathedra = models.ForeignKey(Cathedra, on_delete=models.PROTECT)
    email = models.EmailField()

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'
