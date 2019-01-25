# Generated by Django 2.1.5 on 2019-01-25 15:43

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
                ('contato', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
                ('email', models.EmailField(default=None, max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Secretario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
                ('email', models.EmailField(default=None, max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Secretaria',
            fields=[
                ('secretario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='doug_server_app.Secretario')),
                ('email', models.EmailField(max_length=254)),
                ('telefone', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='departamento',
            name='chefe_departamento',
            field=models.OneToOneField(on_delete=None, to='doug_server_app.Professor'),
        ),
        migrations.AddField(
            model_name='departamento',
            name='corpo_docente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='professores', to='doug_server_app.Professor'),
        ),
        migrations.AddField(
            model_name='curso',
            name='departamento_fk',
            field=models.OneToOneField(on_delete=None, to='doug_server_app.Departamento'),
        ),
        migrations.AddField(
            model_name='curso',
            name='secretaria_fk',
            field=models.OneToOneField(on_delete=None, to='doug_server_app.Secretaria'),
        ),
    ]
