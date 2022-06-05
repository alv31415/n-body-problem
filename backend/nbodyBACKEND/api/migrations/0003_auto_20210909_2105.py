# Generated by Django 3.2.7 on 2021-09-09 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_integrator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='integrator',
            old_name='nbody',
            new_name='nbody_id',
        ),
        migrations.AlterField(
            model_name='integrator',
            name='nbody_id',
            field=models.ForeignKey(db_column='nbody_id', on_delete=django.db.models.deletion.CASCADE, to='api.nbody'),
        ),
    ]