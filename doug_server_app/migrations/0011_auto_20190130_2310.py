# Generated by Django 2.1.5 on 2019-01-31 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doug_server_app', '0010_change_ondelete_secretaria_fk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secretario',
            name='secretaria',
            field=models.ForeignKey(null=True, on_delete=None, related_name='secretario', to='doug_server_app.Secretaria'),
        ),
    ]
