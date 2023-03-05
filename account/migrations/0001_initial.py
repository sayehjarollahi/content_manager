# Generated by Django 3.1.5 on 2023-03-05 06:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storage', models.BigIntegerField(default=1000000)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AttachCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('image', models.ImageField(null=True, upload_to='category_images/')),
                ('allowed_attach_categories', models.ManyToManyField(related_name='allowed_categories', to='account.AttachCategory')),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('is_private', models.BooleanField()),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contents', to='account.category')),
                ('creator_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_contents', to='account.account')),
            ],
        ),
        migrations.CreateModel(
            name='Suffix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='libraries', to='account.account')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.category')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('modification_date', models.DateField(null=True)),
                ('bytes', models.BinaryField(max_length=10000000)),
                ('suffix', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='files', to='account.suffix')),
            ],
        ),
        migrations.CreateModel(
            name='ContentAttributeKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=30)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.category')),
            ],
        ),
        migrations.CreateModel(
            name='ContentAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=50)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.content')),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_attributes', to='account.contentattributekey')),
            ],
        ),
        migrations.AddField(
            model_name='content',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.file'),
        ),
        migrations.AddField(
            model_name='content',
            name='library',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contents', to='account.library'),
        ),
        migrations.AddField(
            model_name='content',
            name='shared_with_accounts',
            field=models.ManyToManyField(related_name='shared_with_contents', to='account.Account'),
        ),
        migrations.AddField(
            model_name='category',
            name='allowed_suffixes',
            field=models.ManyToManyField(related_name='allowed_categories', to='account.Suffix'),
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('attach_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attachments', to='account.attachcategory')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='account.content')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.file')),
            ],
        ),
        migrations.AddField(
            model_name='attachcategory',
            name='allowed_suffixes',
            field=models.ManyToManyField(related_name='allowed_attach_categories', to='account.Suffix'),
        ),
    ]