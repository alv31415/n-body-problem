# Generated by Django 3.2.7 on 2021-09-09 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Integrator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('delta', models.FloatField()),
                ('tolerance', models.FloatField()),
                ('adaptive', models.BooleanField()),
                ('adaptive_constant', models.FloatField()),
                ('delta_lim', models.FloatField()),
                ('position_orbits', models.JSONField()),
                ('nbody', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.nbody')),
            ],
        ),
    ]