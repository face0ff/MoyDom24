# Generated by Django 4.1.6 on 2023-02-11 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services_app', '0002_alter_unit_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('date_edit', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PriceTariffServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('services', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services_app.services')),
                ('tariff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services_app.tariff')),
            ],
            options={
                'unique_together': {('tariff', 'services')},
            },
        ),
    ]
