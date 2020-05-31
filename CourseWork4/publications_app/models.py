from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime
from polymorphic.models import PolymorphicModel
from math import inf
# Author-related stuff


# class Cathedra(models.Model):
#     number = models.IntegerField()
#     name = models.CharField(max_length=128)

#     class Meta:
#         verbose_name = "Кафедра"
#         verbose_name_plural = "Кафдеры"

#     def __str__(self):
#         return f'{self.name} ({self.number})'


# class Position(models.Model):
#     name = models.CharField(max_length=64)

#     class Meta:
#         verbose_name = "Должность"
#         verbose_name_plural = "Должности"

#     def __str__(self):
#         return self.name


class Author(models.Model):
    surname = models.CharField('Фамилия', max_length=64)
    name = models.CharField('Имя', max_length=64)
    patronymic = models.CharField('Отчество', max_length=64)
    # position = models.ForeignKey(Position, on_delete=models.PROTECT)
    # phone_number = PhoneNumberField(unique=True)
    # cathedra = models.ForeignKey(Cathedra, on_delete=models.PROTECT)
    works = models.ManyToManyField(
        'GenericWork', blank=True, through='WorkAuthorship', verbose_name='Работы')
    # email = models.EmailField()

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'

    def short_name(self):
        return f'{self.surname} {self.name[0]}. {self.patronymic[0]}.'

# Publication-related stuff

class WorkAuthorship(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    work = models.ForeignKey('GenericWork', on_delete=models.CASCADE, verbose_name='Работа')
    pages_authored = models.PositiveIntegerField('Страницы авторства', blank=True, null=True)

    class Meta:
        verbose_name = "Авторство"
        verbose_name_plural = "Авторства"
        unique_together = (('author', 'work'),)

    def get_max_pages_authored(self):
        if not hasattr(self.work, 'pages_number'):
            return inf
        other_authored = sum(
            [wa.pages_authored for wa in WorkAuthorship.objects.exclude(author=self.author).filter(work=self.work).all()])
        return self.work.pages_number - other_authored


    def get_other_authors(self):
        return self.work.authors.exclude(pk=self.author.pk)

    def __str__(self):
        return f'{self.author}: {self.work}'

    def clean(self):
        if not hasattr(self.work, 'pages_number'):
            self.pages_authored = None
        if self.pages_authored and self.pages_authored > self.get_max_pages_authored():
            raise ValidationError(
                'Новое значение страниц авторства больше, чем возможно, исходя из общего кол-ва страниц авторства всех авторов!')


class WorkType(models.Model):
    name = models.CharField('Тип работы', max_length=128, unique=True)

    class Meta:
        verbose_name = "Тип работы"
        verbose_name_plural = "Типы работ"

    def __str__(self):
        return self.name


class GenericWork(PolymorphicModel):
    title = models.CharField('Название', max_length=128)
    work_type = models.ForeignKey('WorkType', on_delete=models.PROTECT, verbose_name='Тип работы')
    authors = models.ManyToManyField(
        Author, through='WorkAuthorship', blank=True, verbose_name='Авторы')

    class Meta:
        verbose_name = "Работа"
        verbose_name_plural = "Работы"

    # def get_pages_number(self):
    #     return sum([wa.pages_authored for wa in WorkAuthorship.objects.filter(work=self).all()])

    def __str__(self):
        return self.title

    def get_work_data(self):
        return ''

    def get_year(self):
        return None



class CollectionWork(GenericWork):
    collection_issue = models.ForeignKey(
        'CollectionIssue', on_delete=models.PROTECT, verbose_name='Выпуск собрания')
    pages_number = models.PositiveIntegerField('Число страниц')
    pages_from = models.PositiveIntegerField('Страница начала')

    class Meta:
        verbose_name = "Работа в собрании"
        verbose_name_plural = "Работы в собраниях"

    def get_ending_page(self):
        return self.pages_from + self.pages_number - 1

    def get_year(self):
        return self.collection_issue.year

    def get_work_data(self):
        return f'{self.collection_issue}. – C.{self.pages_from}-{self.get_ending_page()}'

    def clean(self):
        for authorship in WorkAuthorship.objects.filter(work=self).all():
            if authorship.pages_authored and authorship.pages_authored > authorship.get_max_pages_authored():
                raise ValidationError(
                    'Указано больше страниц авторства, чем возможно!')


class IndependentWork(GenericWork):
    year = models.PositiveIntegerField('Год', validators=[MinValueValidator(
        1900), MaxValueValidator(datetime.now().year)], default=datetime.now().year)
    publisher = models.ForeignKey(
        'Publisher', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Издатель')
    pages_number = models.PositiveIntegerField('Число страниц')

    class Meta:
        verbose_name = "Самостоятельная работа"
        verbose_name_plural = "Самостоятельные работы"

    def get_year(self):
        return self.year

    def get_work_data(self):
        return f'{self.publisher}, {self.year}'

    def clean(self):
        for authorship in WorkAuthorship.objects.filter(work=self).all():
            if authorship.pages_authored and authorship.pages_authored > authorship.get_max_pages_authored():
                raise ValidationError(
                    'Указано больше страниц авторства, чем возможно!')


class Country(models.Model):
    name = models.CharField('Страна', max_length=128, unique=True)

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class Owner(models.Model):
    name = models.CharField('Владелец патента', max_length=128, unique=True)

    class Meta:
        verbose_name = "Владелец патента"
        verbose_name_plural = "Владельцы патентов"

    def __str__(self):
        return self.name


class Patent(GenericWork):
    patent_code = models.PositiveIntegerField('Код патента')
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='Страна')
    ipc = models.CharField('Код МПК', max_length=12, validators=[RegexValidator(
        regex=r'[A-H][0-9][1-9][A-Z] [1-9][0-9]{0,2}/[0-9]{2}',
        message="Введите код МПК в соответсвии со схемой (напр. A01B 12/34)!")])
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, verbose_name='Владелец патента')
    patent_number = models.CharField('Номер патента', max_length=24)
    issue_date = models.DateField('Дата заявки', validators=[
        MaxValueValidator(datetime.now().date())])
    publication_date = models.DateField('Дата публикации', validators=[
        MaxValueValidator(datetime.now().date())])
    bulletin_number = models.PositiveIntegerField('Номер бюллетня')

    def get_year(self):
        return self.publication_date.year

    def get_work_data(self):
        return f'Пат. {self.patent_code} {self.country}, МПК {self.ipc}; власник {self.owner}. – № {self.patent_number}; заявл. {self.issue_date:%d.%m.%Y}; опубл. {self.publication_date:%d.%m.%Y}, Бюл. №{self.bulletin_number}.'

    class Meta:
        verbose_name = "Патент"
        verbose_name_plural = "Патенты"

    def clean(self):
        if (self.issue_date > self.publication_date):
            raise ValidationError('Дата заявки не может быть больше даты публикации!')


# Collections


class Collection(models.Model):
    title = models.CharField('Название собрания', max_length=128)
    serie = models.CharField('Серия', max_length=128, blank=True, null=True)
    description = models.CharField('Характер собрания', max_length=128, blank=True, null=True)
    editorship = models.CharField('Под редакцией', max_length=128, blank=True, null=True)

    publisher = models.ForeignKey(
        'Publisher', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Издатель')

    class Meta:
        verbose_name = "Собрание работ"
        verbose_name_plural = "Собрания работ"

    def __str__(self):
        res = self.title
        if self.serie:
            res += f'. Серія «{self.serie}»'
        if self.description:
            res += f': {self.description}'
        if self.editorship:
            res += f' / {self.editorship}'
        if self.publisher:
            res += f'. – {self.publisher}'
        return res


class CollectionIssue(models.Model):
    collection = models.ForeignKey('Collection', on_delete=models.PROTECT, verbose_name='Собрание работ')
    year = models.PositiveIntegerField('Год выхода', 
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.now().year)])
    issue = models.CharField('Выпуск собрания', max_length=512, blank=True, null=True)  # bandaid

    class Meta:
        verbose_name = "Выпуск собрания"
        verbose_name_plural = "Выпуски собраний"

    def __str__(self):
        res = f'{self.collection}, {self.year}'
        if self.issue:
            res += f'. – {self.issue}'
        return res


class Publisher(models.Model):
    name = models.CharField('Издатель', max_length=64, unique=True)
    city = models.ForeignKey('City', on_delete=models.PROTECT, verbose_name='Город')

    class Meta:
        verbose_name = "Издатель"
        verbose_name_plural = "Издатели"

    def __str__(self):
        return f'{str(self.city)[0]}.: {self.name}'


class City(models.Model):
    name = models.CharField('Город', max_length=64, unique=True)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return self.name
