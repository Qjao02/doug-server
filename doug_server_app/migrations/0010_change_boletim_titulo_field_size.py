# Generated by Django 2.1.5 on 2019-03-21 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doug_server_app', '0009_change_field_daeld_data_boletim_to_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edital',
            name='titulo',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='titulo',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
