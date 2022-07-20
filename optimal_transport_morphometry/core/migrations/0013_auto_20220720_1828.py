# Generated by Django 3.2.13 on 2022-07-20 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_dataset_unique_owner_dataset_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='analysis_complete',
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='preprocessing_complete',
        ),
        migrations.AddField(
            model_name='dataset',
            name='analysis_status',
            field=models.CharField(
                choices=[
                    ('Pending', 'Pending'),
                    ('Running', 'Running'),
                    ('Finished', 'Finished'),
                    ('Failed', 'Failed'),
                ],
                default='Pending',
                max_length=32,
            ),
        ),
        migrations.AddField(
            model_name='dataset',
            name='preprocessing_status',
            field=models.CharField(
                choices=[
                    ('Pending', 'Pending'),
                    ('Running', 'Running'),
                    ('Finished', 'Finished'),
                    ('Failed', 'Failed'),
                ],
                default='Pending',
                max_length=32,
            ),
        ),
    ]