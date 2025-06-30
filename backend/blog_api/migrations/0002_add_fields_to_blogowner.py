from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('blog_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogowner',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='电话'),
        ),
        migrations.AddField(
            model_name='blogowner',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='地址'),
        ),
        migrations.AddField(
            model_name='blogowner',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='生日'),
        ),
    ] 