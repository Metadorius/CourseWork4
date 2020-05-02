from django.db import models
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

# Teacher-related stuff


class Cathedra(models.Model):
    cathedra_number = models.IntegerField()
    name = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.title} ({self.cathedra_number})'


class Position(models.Model):
    position_name = models.CharField(max_length=64)

    def __str__(self):
        return self.position_name


class Teacher(models.Model):
    surname = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    patronymic = models.CharField(max_length=64)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    phone_number = PhoneNumberField(unique=True)
    cathedra = models.ForeignKey(Cathedra, on_delete=models.PROTECT)
    publications = models.ManyToManyField(
        'Publication', blank=True, through='PublicationAuthorship')
    email = models.EmailField()

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'

# Publication-related stuff


class PublicationType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Publication(models.Model):
    title = models.CharField(max_length=128)
    authors = models.ManyToManyField(
        Teacher, through='PublicationAuthorship', blank=True)
    publication_type = models.ForeignKey(
        PublicationType, on_delete=models.PROTECT)
    year = models.DateField()
    pages_number = models.PositiveIntegerField()
    pages_from = models.PositiveIntegerField()
    publisher = models.ForeignKey(
        'Publisher', null=True, on_delete=models.SET_NULL)
    collection = models.ForeignKey(
        'Collection', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class PublicationAuthorship(models.Model):
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    pages_authored = models.PositiveIntegerField()

    def clean(self):
        if self.publcation.pages_number < self.pages_authored:
            raise ValidationError(
                'Страниц авторства не может быть больше, чем страниц публикации!')


class Collection(models.Model):
    title = models.CharField(max_length=128)
    foundation_date = models.DateField()
    issue = models.CharField(max_length=512)

    def __str__(self):
        return self.series


class Publisher(models.Model):
    name = models.CharField(max_length=64)
    city = models.ForeignKey('City', on_delete=models.PROTECT)
    address = models.CharField(max_length=256)


class City(models.Model):
    name = models.CharField(max_length=64)
