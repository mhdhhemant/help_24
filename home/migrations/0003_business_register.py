# Generated by Django 3.0.3 on 2020-04-12 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_business_detail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business_Register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=50)),
                ('pincode', models.IntegerField()),
                ('email', models.EmailField(max_length=200)),
                ('category', models.CharField(max_length=30)),
                ('phone', models.BigIntegerField()),
                ('address', models.CharField(max_length=200)),
                ('landmark', models.CharField(max_length=100)),
                ('website', models.URLField()),
                ('Description', models.TextField()),
                ('image', models.ImageField(upload_to='pics')),
            ],
        ),
    ]
