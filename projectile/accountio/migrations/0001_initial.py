# Generated by Django 4.2.1 on 2023-08-21 08:39

import accountio.utils
import autoslug.fields
import dirtyfields.dirtyfields
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import simple_history.models
import uuid
import versatileimagefield.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Affiliation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uid",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(blank=True, max_length=250)),
                ("hospital_name", models.CharField(blank=True, max_length=250)),
                ("expire_at", models.DateField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("ACTIVE", "Active"),
                            ("REJECTED", "Rejected"),
                            ("HIDDEN", "Hidden"),
                            ("REMOVED", "Removed"),
                        ],
                        db_index=True,
                        default="PENDING",
                        max_length=20,
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Descendant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uid",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ("-created_at",),
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Diagnosis",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uid",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Examination",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uid",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalOrganization",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                (
                    "uid",
                    models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
                ),
                ("created_at", models.DateTimeField(blank=True, editable=False)),
                ("updated_at", models.DateTimeField(blank=True, editable=False)),
                (
                    "serial_number",
                    models.PositiveIntegerField(db_index=True, editable=False),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False,
                        populate_from=accountio.utils.get_organization_slug,
                    ),
                ),
                ("registration_no", models.CharField(blank=True, max_length=50)),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        db_index=True,
                        max_length=128,
                        region=None,
                        verbose_name="Phone Number",
                    ),
                ),
                ("email", models.EmailField(blank=True, max_length=254)),
                (
                    "appointment_duration",
                    models.TimeField(
                        blank=True, help_text="Duration per Appointment", null=True
                    ),
                ),
                (
                    "appointment_interval",
                    models.TimeField(
                        blank=True, help_text="Interval between Appointment", null=True
                    ),
                ),
                ("website_url", models.URLField(blank=True)),
                ("blog_url", models.URLField(blank=True)),
                ("linkedin_url", models.URLField(blank=True)),
                ("instagram_url", models.URLField(blank=True)),
                ("facebook_url", models.URLField(blank=True)),
                ("twitter_url", models.URLField(blank=True)),
                (
                    "size",
                    models.CharField(
                        choices=[
                            ("ZERO_TO_ONE", "0-1 employees"),
                            ("TWO_TO_TEN", "2-10 employees"),
                            ("ELEVEN_TO_FIFTY", "11-50 employees"),
                            ("FIFTY_ONE_PLUS", "51-200 employees"),
                            ("TWO_HUNDRED_PLUS", "201-500 employees"),
                            ("FIVE_HUNDRED_PLUS", "501-1,000 employees"),
                            ("ONE_THOUSAND_PLUS", "1,001-5,000 employees"),
                            ("FIVE_THOUSAND_PLUS", "5,001-10,000 employees"),
                            ("TEN_THOUSAND_PLUS", "10,001+ employees"),
                        ],
                        default="ZERO_TO_ONE",
                        max_length=20,
                    ),
                ),
                (
                    "summary",
                    models.CharField(
                        blank=True,
                        help_text="Short summary about company.",
                        max_length=500,
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        help_text="Longer description about company.",
                        max_length=500,
                    ),
                ),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("UNKNOWN", "Unknown"),
                            ("CLINIC", "Clinic"),
                            ("OTHER", "Other"),
                        ],
                        db_index=True,
                        default="UNKNOWN",
                        max_length=20,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("DRAFT", "Draft"),
                            ("PLACEHOLDER", "Placeholder"),
                            ("PENDING", "Pending"),
                            ("ACTIVE", "Active"),
                            ("HIDDEN", "Hidden"),
                            ("REMOVED", "Removed"),
                        ],
                        db_index=True,
                        default="DRAFT",
                        max_length=20,
                    ),
                ),
                ("avatar", models.TextField(blank=True, max_length=100, null=True)),
                ("hero", models.TextField(blank=True, max_length=100, null=True)),
                ("logo_wide", models.TextField(blank=True, max_length=100, null=True)),
                ("image", models.TextField(blank=True, max_length=100, null=True)),
                ("policies", models.CharField(blank=True, max_length=700)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical organization",
                "verbose_name_plural": "historical organizations",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="Investigation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uid",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Organization",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uid",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "serial_number",
                    models.PositiveIntegerField(editable=False, unique=True),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False,
                        populate_from=accountio.utils.get_organization_slug,
                        unique=True,
                    ),
                ),
                ("registration_no", models.CharField(blank=True, max_length=50)),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        db_index=True,
                        max_length=128,
                        region=None,
                        unique=True,
                        verbose_name="Phone Number",
                    ),
                ),
                ("email", models.EmailField(blank=True, max_length=254)),
                (
                    "appointment_duration",
                    models.TimeField(
                        blank=True, help_text="Duration per Appointment", null=True
                    ),
                ),
                (
                    "appointment_interval",
                    models.TimeField(
                        blank=True, help_text="Interval between Appointment", null=True
                    ),
                ),
                ("website_url", models.URLField(blank=True)),
                ("blog_url", models.URLField(blank=True)),
                ("linkedin_url", models.URLField(blank=True)),
                ("instagram_url", models.URLField(blank=True)),
                ("facebook_url", models.URLField(blank=True)),
                ("twitter_url", models.URLField(blank=True)),
                (
                    "size",
                    models.CharField(
                        choices=[
                            ("ZERO_TO_ONE", "0-1 employees"),
                            ("TWO_TO_TEN", "2-10 employees"),
                            ("ELEVEN_TO_FIFTY", "11-50 employees"),
                            ("FIFTY_ONE_PLUS", "51-200 employees"),
                            ("TWO_HUNDRED_PLUS", "201-500 employees"),
                            ("FIVE_HUNDRED_PLUS", "501-1,000 employees"),
                            ("ONE_THOUSAND_PLUS", "1,001-5,000 employees"),
                            ("FIVE_THOUSAND_PLUS", "5,001-10,000 employees"),
                            ("TEN_THOUSAND_PLUS", "10,001+ employees"),
                        ],
                        default="ZERO_TO_ONE",
                        max_length=20,
                    ),
                ),
                (
                    "summary",
                    models.CharField(
                        blank=True,
                        help_text="Short summary about company.",
                        max_length=500,
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        help_text="Longer description about company.",
                        max_length=500,
                    ),
                ),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("UNKNOWN", "Unknown"),
                            ("CLINIC", "Clinic"),
                            ("OTHER", "Other"),
                        ],
                        db_index=True,
                        default="UNKNOWN",
                        max_length=20,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("DRAFT", "Draft"),
                            ("PLACEHOLDER", "Placeholder"),
                            ("PENDING", "Pending"),
                            ("ACTIVE", "Active"),
                            ("HIDDEN", "Hidden"),
                            ("REMOVED", "Removed"),
                        ],
                        db_index=True,
                        default="DRAFT",
                        max_length=20,
                    ),
                ),
                (
                    "avatar",
                    versatileimagefield.fields.VersatileImageField(
                        blank=True,
                        null=True,
                        upload_to=accountio.utils.get_organization_media_path_prefix,
                    ),
                ),
                (
                    "hero",
                    versatileimagefield.fields.VersatileImageField(
                        blank=True,
                        null=True,
                        upload_to=accountio.utils.get_organization_media_path_prefix,
                    ),
                ),
                (
                    "logo_wide",
                    versatileimagefield.fields.VersatileImageField(
                        blank=True,
                        null=True,
                        upload_to=accountio.utils.get_organization_media_path_prefix,
                    ),
                ),
                (
                    "image",
                    versatileimagefield.fields.VersatileImageField(
                        blank=True,
                        null=True,
                        upload_to=accountio.utils.get_organization_media_path_prefix,
                    ),
                ),
                ("policies", models.CharField(blank=True, max_length=700)),
            ],
            options={
                "ordering": ("-created_at",),
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="OrganizationUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uid",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("INITIATOR", "Initiator"),
                            ("STAFF", "Staff"),
                            ("ADMIN", "Admin"),
                            ("OWNER", "Owner"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("INVITED", "Invited"),
                            ("PENDING", "Pending"),
                            ("ACTIVE", "Active"),
                            ("REJECTED", "Rejected"),
                            ("HIDDEN", "Hidden"),
                            ("REMOVED", "Removed"),
                        ],
                        default="PENDING",
                        max_length=20,
                    ),
                ),
                ("is_default", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name_plural": "Organization Users",
                "ordering": ("-created_at",),
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="PrescriptionAdditionalConnector",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uid",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "diagnosis",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="accountio.diagnosis",
                    ),
                ),
                (
                    "examination",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="accountio.examination",
                    ),
                ),
                (
                    "investigation",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="accountio.investigation",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
    ]