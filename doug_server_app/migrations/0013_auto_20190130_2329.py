# Generated by Django 2.1.5 on 2019-01-31 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doug_server_app', '0012_auto_20190130_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departamento',
            name='curso',
            field=models.OneToOneField(blank=True, null=True, on_delete=None, related_name='departamento', to='doug_server_app.Curso'),
        ),
        migrations.AlterField(
            model_name='secretaria',
            name='curso',
            field=models.OneToOneField(blank=True, null=True, on_delete=None, related_name='secretaria', to='doug_server_app.Curso'),
        ),
    ]
