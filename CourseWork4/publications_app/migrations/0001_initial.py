# Generated by Django 3.0.5 on 2020-05-01 12:16

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cathedra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cathedra_number', models.IntegerField()),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('foundation_date', models.DateField()),
                ('issue', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('year', models.DateField()),
                ('pages_number', models.PositiveIntegerField()),
                ('pages_from', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PublicationAuthorship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pages_authored', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PublicationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('patronymic', models.CharField(max_length=64)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('cathedra', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='publications_app.Cathedra')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='publications_app.Position')),
                ('publications', models.ManyToManyField(blank=True, through='publications_app.PublicationAuthorship', to='publications_app.Publication')),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('address', models.CharField(max_length=256)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='publications_app.City')),
            ],
        ),
        migrations.AddField(
            model_name='publicationauthorship',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publications_app.Teacher'),
        ),
        migrations.AddField(
            model_name='publicationauthorship',
            name='publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publications_app.Publication'),
        ),
        migrations.AddField(
            model_name='publication',
            name='authors',
            field=models.ManyToManyField(blank=True, through='publications_app.PublicationAuthorship', to='publications_app.Teacher'),
        ),
        migrations.AddField(
            model_name='publication',
            name='collection',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='publications_app.Collection'),
        ),
        migrations.AddField(
            model_name='publication',
            name='publication_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='publications_app.PublicationType'),
        ),
        migrations.AddField(
            model_name='publication',
            name='publisher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='publications_app.Publisher'),
        ),
    ]
