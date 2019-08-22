# Generated by Django 2.1.5 on 2019-07-29 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doug_server_app', '0014_add_name_field_as_optional'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='nome',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='disciplinas',
            name='nome',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='professor',
            name='nome',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='secretario',
            name='nome',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='tutores',
            name='nome',
            field=models.CharField(max_length=30),
        ),
    ]
