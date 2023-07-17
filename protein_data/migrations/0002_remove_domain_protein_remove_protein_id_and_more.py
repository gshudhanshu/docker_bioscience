# Generated by Django 4.2.3 on 2023-07-16 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('protein_data', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='domain',
            name='protein',
        ),
        migrations.RemoveField(
            model_name='protein',
            name='id',
        ),
        migrations.RemoveField(
            model_name='protein',
            name='domains',
        ),
        migrations.AlterField(
            model_name='protein',
            name='protein_id',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='protein',
            name='domains',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='protein_data.domain'),
        ),
    ]
