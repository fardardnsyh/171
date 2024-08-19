from django.db import migrations, models
import uuid

def copy_data(apps, schema_editor):
    Document = apps.get_model('app', 'Document')
    for document in Document.objects.all():
        document.uuid = uuid.uuid4()
        document.save()

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
            preserve_default=False,
        ),
        migrations.RunPython(copy_data),
        migrations.RemoveField(
            model_name='document',
            name='id',
        ),
        migrations.RenameField(
            model_name='document',
            old_name='uuid',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='document',
            name='id',
            field=models.UUIDField(primary_key=True, serialize=False),
        ),
    ]
