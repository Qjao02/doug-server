# Generated by Django 2.1.5 on 2019-03-06 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doug_server_app', '0014_auto_20190130_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departamento',
            name='curso',
            field=models.ForeignKey(null=True, on_delete=None, related_name='departamento', to='doug_server_app.Curso'),
        ),
    ]
