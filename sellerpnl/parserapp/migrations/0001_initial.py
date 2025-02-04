# Generated by Django 5.0.7 on 2024-07-29 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CSVFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_type', models.CharField(choices=[('type1', 'Type 1'), ('type2', 'Type 2'), ('type3', 'Type 3'), ('type4', 'Type 4')], max_length=10)),
                ('file', models.FileField(upload_to='csv_files/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
