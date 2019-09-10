# Generated by Django 2.1.5 on 2019-09-10 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doug_server_app', '0019_eventos_changed_datefield_to_datetimefield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evento',
            name='nome',
        ),
        migrations.AddField(
            model_name='evento',
            name='periodo',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
    ]