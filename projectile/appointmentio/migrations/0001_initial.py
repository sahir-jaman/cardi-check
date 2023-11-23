# Generated by Django 4.2.1 on 2023-08-21 08:39

import appointmentio.utils
import autoslug.fields
import dirtyfields.dirtyfields
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import simple_history.models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accountio", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Appointment",
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
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False,
                        populate_from=appointmentio.utils.get_appointment_slug,
                        unique=True,
                    ),
                ),
                (
                    "symptom_period",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("HOURS", "Hours"),
                            ("DAYS", "Days"),
                            ("WEEKS", "Weeks"),
                            ("MONTHS", "Months"),
                            ("SIX_MONTHS_OR_MORE", "Six months or more"),
                        ],
                        max_length=30,
                    ),
                ),
                (
                    "appointment_type",
                    models.CharField(
                        choices=[
                            ("CONSULTATION", "Consultation"),
                            ("FOLLOWUP", "Follow Up"),
                            ("OTHER", "Other"),
                        ],
                        default="CONSULTATION",
                        max_length=20,
                    ),
                ),
                (
                    "appointment_for",
                    models.CharField(
                        choices=[("ME", "Me"), ("SOMEONE_ELSE", "Someone Else")],
                        default="ME",
                        max_length=20,
                    ),
                ),
                ("complication", models.CharField(blank=True, max_length=500)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("COMPLETED", "Completed"),
                            ("REQUESTED", "Requested"),
                            ("SCHEDULED", "Scheduled"),
                            ("PENDING", "Pending"),
                            ("CANCELED", "Canceled"),
                            ("HIDDEN", "Hidden"),
                            ("REMOVED", "Removed"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "is_visible",
                    models.BooleanField(default=False, help_text="Use for visibility."),
                ),
                (
                    "is_previous",
                    models.BooleanField(
                        default=True, help_text="Show previous medical records."
                    ),
                ),
                ("cancellation_reason", models.TextField(blank=True, null=True)),
                ("conference_link", models.URLField(blank=True)),
                ("first_name", models.CharField(blank=True, max_length=255)),
                ("last_name", models.CharField(blank=True, max_length=255)),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        max_length=128,
                        region=None,
                        verbose_name="Phone Number",
                    ),
                ),
                ("email", models.EmailField(blank=True, max_length=254)),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("FEMALE", "Female"),
                            ("MALE", "Male"),
                            ("UNKNOWN", "Unknown"),
                            ("OTHER", "Other"),
                        ],
                        max_length=20,
                    ),
                ),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("age", models.PositiveIntegerField(blank=True, null=True)),
                ("height", models.FloatField(blank=True, null=True)),
                ("weight", models.IntegerField(blank=True, null=True)),
                (
                    "blood_group",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("NOT_SET", "Not Set"),
                            ("A+", "A Positive"),
                            ("A-", "A Negative"),
                            ("B+", "B Positive"),
                            ("B-", "B Negative"),
                            ("AB+", "Ab Positive"),
                            ("AB-", "Ab Negative"),
                            ("O+", "O Positive"),
                            ("O-", "O Negative"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "schedule_start",
                    models.DateTimeField(
                        blank=True,
                        help_text="Appointment schedule start time",
                        null=True,
                    ),
                ),
                (
                    "schedule_end",
                    models.DateTimeField(
                        blank=True, help_text="Appointment schedule end time", null=True
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
            name="AppointmentAllergicMedicationConnector",
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
                    "other_medicine",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="AppointmentDateTimeSlotConnector",
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
                ("date", models.DateField(blank=True, null=True)),
                ("is_booked", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="AppointmentMedicationConnector",
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
                ("usage", models.CharField(blank=True, max_length=500, null=True)),
                (
                    "other_medicine",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="AppointmentSeekHelpConnector",
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
                    "seek_help_for",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="AppointmentTimeSlot",
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
                ("schedule_time", models.TimeField(blank=True, null=True)),
                ("slot", models.TimeField(blank=True, null=True)),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="AppointmentTwilioConnector",
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
                ("room_name", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalAppointment",
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
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False,
                        populate_from=appointmentio.utils.get_appointment_slug,
                    ),
                ),
                (
                    "symptom_period",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("HOURS", "Hours"),
                            ("DAYS", "Days"),
                            ("WEEKS", "Weeks"),
                            ("MONTHS", "Months"),
                            ("SIX_MONTHS_OR_MORE", "Six months or more"),
                        ],
                        max_length=30,
                    ),
                ),
                (
                    "appointment_type",
                    models.CharField(
                        choices=[
                            ("CONSULTATION", "Consultation"),
                            ("FOLLOWUP", "Follow Up"),
                            ("OTHER", "Other"),
                        ],
                        default="CONSULTATION",
                        max_length=20,
                    ),
                ),
                (
                    "appointment_for",
                    models.CharField(
                        choices=[("ME", "Me"), ("SOMEONE_ELSE", "Someone Else")],
                        default="ME",
                        max_length=20,
                    ),
                ),
                ("complication", models.CharField(blank=True, max_length=500)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("COMPLETED", "Completed"),
                            ("REQUESTED", "Requested"),
                            ("SCHEDULED", "Scheduled"),
                            ("PENDING", "Pending"),
                            ("CANCELED", "Canceled"),
                            ("HIDDEN", "Hidden"),
                            ("REMOVED", "Removed"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "is_visible",
                    models.BooleanField(default=False, help_text="Use for visibility."),
                ),
                (
                    "is_previous",
                    models.BooleanField(
                        default=True, help_text="Show previous medical records."
                    ),
                ),
                ("cancellation_reason", models.TextField(blank=True, null=True)),
                ("conference_link", models.URLField(blank=True)),
                ("first_name", models.CharField(blank=True, max_length=255)),
                ("last_name", models.CharField(blank=True, max_length=255)),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        max_length=128,
                        region=None,
                        verbose_name="Phone Number",
                    ),
                ),
                ("email", models.EmailField(blank=True, max_length=254)),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("FEMALE", "Female"),
                            ("MALE", "Male"),
                            ("UNKNOWN", "Unknown"),
                            ("OTHER", "Other"),
                        ],
                        max_length=20,
                    ),
                ),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("age", models.PositiveIntegerField(blank=True, null=True)),
                ("height", models.FloatField(blank=True, null=True)),
                ("weight", models.IntegerField(blank=True, null=True)),
                (
                    "blood_group",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("NOT_SET", "Not Set"),
                            ("A+", "A Positive"),
                            ("A-", "A Negative"),
                            ("B+", "B Positive"),
                            ("B-", "B Negative"),
                            ("AB+", "Ab Positive"),
                            ("AB-", "Ab Negative"),
                            ("O+", "O Positive"),
                            ("O-", "O Negative"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "schedule_start",
                    models.DateTimeField(
                        blank=True,
                        help_text="Appointment schedule start time",
                        null=True,
                    ),
                ),
                (
                    "schedule_end",
                    models.DateTimeField(
                        blank=True, help_text="Appointment schedule end time", null=True
                    ),
                ),
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
                "verbose_name": "historical appointment",
                "verbose_name_plural": "historical appointments",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="Ingredient",
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
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False, populate_from="name", unique=True
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
            name="Medicine",
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
                ("description", models.CharField(blank=True, max_length=400)),
                ("manufacturer", models.CharField(blank=True, max_length=255)),
                ("strength", models.CharField(blank=True, max_length=255)),
                ("dosage_form", models.CharField(blank=True, max_length=255)),
                ("route", models.CharField(blank=True, max_length=255)),
                ("side_effects", models.TextField(blank=True)),
                ("package_size", models.CharField(blank=True, max_length=255)),
                ("package_type", models.CharField(blank=True, max_length=255)),
                ("storage_conditions", models.CharField(blank=True, max_length=255)),
                ("expiration_date", models.DateField(blank=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("ACTIVE", "Active"),
                            ("HIDDEN", "Hidden"),
                            ("REMOVED", "Removed"),
                            ("RESTRICTED", "Restricted"),
                            ("DISCONTINUED", "Discontinued"),
                        ],
                        default="ACTIVE",
                        max_length=30,
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
            name="Prescription",
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
                ("next_visit", models.DateTimeField(blank=True, null=True)),
                (
                    "is_visible",
                    models.BooleanField(
                        default=False, help_text="Is doctor can read medical records."
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
            name="PrescriptionInformation",
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
                    "status",
                    models.CharField(
                        choices=[
                            ("ACTIVE", "Active"),
                            ("PENDING", "Pending"),
                            ("CANCELED", "Canceled"),
                            ("HIDDEN", "Hidden"),
                            ("REMOVED", "Removed"),
                        ],
                        default="ACTIVE",
                        max_length=30,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("ADVICES", "Advices"),
                            ("DIAGNOSIS", "Diagnosis"),
                            ("COMPLAINTS", "Complaints"),
                            ("EXAMINATIONS", "Examinations"),
                        ],
                        default="ADVICES",
                        max_length=30,
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
            name="PrescriptionMedicineConnector",
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
                ("dosage", models.CharField(blank=True, max_length=255)),
                ("frequency", models.CharField(blank=True, max_length=255)),
                ("start_date", models.DateTimeField(auto_now_add=True)),
                ("end_date", models.DateTimeField(blank=True, null=True)),
                ("interval", models.CharField(blank=True, max_length=255)),
            ],
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="SeekHelp",
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
                ("name", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="WeekDay",
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
                    "day",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("SUNDAY", "Sunday"),
                            ("MONDAY", "Monday"),
                            ("TUESDAY", "Tuesday"),
                            ("WEDNESDAY", "Wednesday"),
                            ("THURSDAY", "Thursday"),
                            ("FRIDAY", "Friday"),
                            ("SATURDAY", "Saturday"),
                        ],
                        default="PENDING",
                        max_length=20,
                    ),
                ),
                ("off_day", models.BooleanField(default=False)),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accountio.organization",
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
            name="Shift",
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
                ("shift_label", models.CharField(max_length=50)),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                (
                    "weekday",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="appointmentio.weekday",
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
            name="Refill",
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
                ("message", models.TextField(blank=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("REQUESTED", "Requested"),
                            ("FULFILLED", "Fulfilled"),
                            ("CANCELED", "Canceled"),
                        ],
                        default="REQUESTED",
                        max_length=30,
                    ),
                ),
                (
                    "appointment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="appointmentio.appointment",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
    ]