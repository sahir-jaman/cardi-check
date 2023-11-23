from datetime import datetime, date, timedelta

from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accountio.models import Organization

from appointmentio.choices import AppointmentStatus, AppointmentType
from appointmentio.models import (
    Appointment,
    AppointmentSeekHelpConnector,
    AppointmentAllergicMedicationConnector,
    AppointmentMedicationConnector,
    WeekDay,
    Shift,
    AppointmentTimeSlot,
    AppointmentDateTimeSlotConnector,
    AppointmentTreatedConditionConnector,
    Prescription,
)

from common.slim_serializer import (
    PrivateSeekHelpSlimSerializer,
    PrivateAllergicMedicationSlimSerializer,
    PrivateCurrentMedicationSlimSerializer,
    PrivateMediaImageConnectorSlimSerializer,
    PrivateWeekDayWriteSlimSerializer,
    PrivateShiftSlimSerializer,
    PrivatePrescriptionSlimSerializer,
    PrivateAppointmentPatientSlimSerializer,
    PublicDoctorSlimSerializer,
)
from contentio.models import Feedback

from core.choices import UserType
from core.models import User

from doctorio.models import Doctor

from mediaroomio.models import MediaImageConnector

from notificationio.services import notification_for_appointment_status

from patientio.models import Patient

from threadio.models import Thread
from threadio.choices import ThreadKind


class PrivateAppointmentListSerializer(serializers.ModelSerializer):
    doctor = PublicDoctorSlimSerializer(read_only=True)
    doctor_uid = serializers.SlugRelatedField(
        queryset=Doctor.objects.get_status_editable(),
        slug_field="uid",
        write_only=True,
        allow_null=True,
        allow_empty=True,
        required=False,
    )
    patient = PrivateAppointmentPatientSlimSerializer(read_only=True)
    seek_help_list = serializers.SerializerMethodField(read_only=True)
    allergic_medication_list = serializers.SerializerMethodField(read_only=True)
    current_medication_list = serializers.SerializerMethodField(read_only=True)
    file_item_list = serializers.SerializerMethodField(read_only=True)
    appointment_date = serializers.CharField(write_only=True)
    appointment_time = serializers.CharField(write_only=True)
    parent_appointment = serializers.SlugRelatedField(
        queryset=Appointment.objects.all(),
        slug_field="uid",
        write_only=True,
        required=False,
        allow_empty=True,
        allow_null=True,
    )
    social_security_number = serializers.CharField(write_only=True, required=False)
    feedback = serializers.SerializerMethodField(read_only=True)

    def validate(self, data):
        user = self.context["request"].user
        doctor_uid: Doctor = data.get("doctor_uid", None)
        organization: Organization = user.get_organization()
        if doctor_uid and not organization.doctor_set.filter(pk=doctor_uid.pk).exists():
            raise ValidationError({"doctor_uid": "Invalid organization doctor."})

        return data

    class Meta:
        model = Appointment
        fields = [
            "uid",
            "serial_number",
            "appointment_for",
            "appointment_type",
            "complication",
            "symptom_period",
            "status",
            "is_visible",
            "patient",
            "doctor",
            "schedule_start",
            "schedule_end",
            "doctor_uid",
            "first_name",
            "last_name",
            "date_of_birth",
            "phone",
            "social_security_number",
            "email",
            "weight",
            "height",
            "blood_group",
            "gender",
            "seek_help_list",
            "allergic_medication_list",
            "current_medication_list",
            "file_item_list",
            "is_previous",
            "appointment_date",
            "appointment_time",
            "appointment_type",
            "parent_appointment",
            "feedback",
        ]

        read_only_fields = ["serial_number"]

    def get_seek_help_list(self, obj):
        seek_helps = AppointmentSeekHelpConnector.objects.filter(appointment=obj)
        return PrivateSeekHelpSlimSerializer(seek_helps, many=True).data

    def get_allergic_medication_list(self, obj):
        allergic_medications = AppointmentAllergicMedicationConnector.objects.filter(
            appointment=obj
        )
        return PrivateAllergicMedicationSlimSerializer(
            allergic_medications, many=True
        ).data

    def get_current_medication_list(self, obj):
        current_medications = AppointmentMedicationConnector.objects.filter(
            appointment=obj
        )
        return PrivateCurrentMedicationSlimSerializer(
            current_medications, many=True
        ).data

    def get_file_item_list(self, obj):
        file_items = MediaImageConnector.objects.filter(
            appointment=obj, patient=obj.patient
        )
        request = self.context.get("request")

        return PrivateMediaImageConnectorSlimSerializer(
            file_items, many=True, context={"request": request}
        ).data

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise ValidationError("This email already exists.")
        return value

    def validate_social_security_number(self, value):
        if value and User.objects.filter(social_security_number=value).exists():
            raise ValidationError("Social security number already exists.")
        return value

    def get_feedback(self, obj):
        feedback_data = {
            "doctor": {
                "rating": None,
                "comment": None,
                "created_at": None,
            },
            "patient": {
                "rating": None,
                "comment": None,
                "created_at": None,
            },
        }

        feedbacks = (
            obj.feedback_set.select_related("doctor", "patient")
            .filter()
            .order_by("rated_by_doctor")
        )

        if feedbacks:
            for feedback in feedbacks:
                if feedback.rated_by_doctor:
                    feedback_data["doctor"]["rating"] = feedback.rating
                    feedback_data["doctor"]["comment"] = feedback.comment
                    feedback_data["doctor"]["created_at"] = feedback.created_at
                else:
                    feedback_data["patient"]["rating"] = feedback.rating
                    feedback_data["patient"]["comment"] = feedback.comment
                    feedback_data["patient"]["created_at"] = feedback.created_at

        return feedback_data

    def create(self, validated_data):
        with transaction.atomic():
            request = self.context["request"]
            phone_number = validated_data.get("phone", None)
            first_name = validated_data.get("first_name", "")
            last_name = validated_data.get("last_name", "")
            date_of_birth = validated_data.get("date_of_birth", None)
            email = validated_data.get("email", "")
            gender = validated_data.get("gender", "")
            blood_group = validated_data.get("blood_group", "")
            height = validated_data.get("height", None)
            weight = validated_data.get("weight", None)
            social_security_number = validated_data.pop("social_security_number", None)
            appointment_date = validated_data.pop("appointment_date", None)
            appointment_time = validated_data.pop("appointment_time", None)
            organization: Organization = request.user.get_organization()
            appointment_type = validated_data.get("appointment_type", "")
            parent_appointment = validated_data.pop("parent_appointment", None)

            date = datetime.strptime(appointment_date, "%Y-%m-%d")
            time = datetime.strptime(appointment_time, "%H:%M").time()

            # creating user if not found
            if phone_number:
                if User.objects.filter(phone=phone_number).exists():
                    try:
                        patient = Patient.objects.select_related("user").get(
                            user__phone=phone_number
                        )
                    except:
                        raise ValidationError("Patient not found!")

                    user = patient.user

                    validated_data["first_name"] = user.first_name
                    validated_data["last_name"] = user.last_name
                    validated_data["date_of_birth"] = user.date_of_birth
                    validated_data["email"] = user.email
                    validated_data["gender"] = user.gender
                    validated_data["blood_group"] = user.blood_group
                    validated_data["height"] = user.height
                    validated_data["weight"] = user.weight
                else:
                    if not social_security_number:
                        raise ValidationError("Social security number must be set.")

                    user = User.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        date_of_birth=date_of_birth,
                        phone=phone_number,
                        social_security_number=social_security_number,
                        email=email,
                        gender=gender,
                        blood_group=blood_group,
                        height=height,
                        weight=weight,
                        username=phone_number,
                        type=UserType.PATIENT,
                    )
            else:
                user = request.user

            patient, _ = Patient.objects.get_or_create(
                user=user, organization=organization
            )
            validated_data["patient"] = patient
            validated_data["doctor"] = validated_data.pop("doctor_uid", None)
            validated_data["organization"] = organization
            validated_data["creator_user"] = request.user

            day = date.strftime("%A").upper()

            try:
                weekday = WeekDay.objects.select_related("organization").get(
                    organization=organization, day=day, off_day=False
                )
            except WeekDay.DoesNotExist:
                raise ValidationError("Off Day!")

            try:
                appointment_time_slot = AppointmentTimeSlot.objects.select_related(
                    "organization", "weekday"
                ).get(organization=organization, weekday=weekday, slot=time)
            except AppointmentTimeSlot.DoesNotExist:
                raise ValidationError("Appointment schedule time doesn't exist!")

            try:
                booked_slot = AppointmentDateTimeSlotConnector.objects.get(
                    organization=organization,
                    date=date,
                    appointment_time_slot__slot=time,
                    is_booked=True,
                )
                raise ValidationError("This appointment time slot is already booked.")
            except AppointmentDateTimeSlotConnector.DoesNotExist:
                pass

            appointment = Appointment.objects.create(**validated_data)

            if appointment_type == AppointmentType.CONSULTATION:
                appointment.status = (
                    AppointmentStatus.REQUESTED
                    if appointment.doctor is None
                    else AppointmentStatus.SCHEDULED
                )
                appointment.save()

            if appointment_type == AppointmentType.FOLLOWUP:
                if parent_appointment is None:
                    raise ValidationError(
                        "Parent appointment is required for follow-up appointments."
                    )
                appointment.parent = parent_appointment
                appointment.doctor = parent_appointment.doctor
                appointment.status = AppointmentStatus.SCHEDULED
                appointment.save()

            AppointmentDateTimeSlotConnector.objects.create(
                organization=organization,
                appointment=appointment,
                date=date,
                appointment_time_slot=appointment_time_slot,
            )

            appointment.schedule_start = datetime.combine(date, time)

            appointment.save()

            # create notification instance
            notification_for_appointment_status(appointment)

            return appointment


class PrivateAppointmentDetailSerializer(serializers.ModelSerializer):
    doctor = PublicDoctorSlimSerializer(read_only=True)
    doctor_uid = serializers.SlugRelatedField(
        queryset=Doctor.objects.get_status_editable(),
        slug_field="uid",
        write_only=True,
        allow_null=True,
        allow_empty=True,
        required=False,
    )
    patient = PrivateAppointmentPatientSlimSerializer(read_only=True)
    seek_help_list = serializers.SerializerMethodField(read_only=True)
    allergic_medication_list = serializers.SerializerMethodField(read_only=True)
    current_medication_list = serializers.SerializerMethodField(read_only=True)
    treated_conditions = serializers.SerializerMethodField()
    file_item_list = serializers.SerializerMethodField(read_only=True)
    recent_prescription = serializers.SerializerMethodField(
        read_only=True, allow_null=True, required=False
    )
    parent_appointment = serializers.SlugRelatedField(
        queryset=Appointment.objects.all(),
        slug_field="uid",
        write_only=True,
        required=False,
        allow_empty=True,
        allow_null=True,
    )
    appointment_date = serializers.CharField(write_only=True)
    appointment_time = serializers.CharField(write_only=True)
    feedback = serializers.SerializerMethodField()

    def validate(self, data):
        user = self.context["request"].user
        doctor_uid: Doctor = data.get("doctor_uid", None)
        organization: Organization = user.get_organization()
        if doctor_uid and not organization.doctor_set.filter(pk=doctor_uid.pk).exists():
            raise ValidationError({"doctor_uid": "Invalid organization doctor."})

        return data

    class Meta:
        model = Appointment
        fields = [
            "uid",
            "serial_number",
            "appointment_for",
            "appointment_type",
            "complication",
            "symptom_period",
            "status",
            "is_visible",
            "patient",
            "doctor",
            "schedule_start",
            "schedule_end",
            "doctor_uid",
            "first_name",
            "last_name",
            "date_of_birth",
            "phone",
            "email",
            "weight",
            "height",
            "blood_group",
            "gender",
            "seek_help_list",
            "allergic_medication_list",
            "current_medication_list",
            "treated_conditions",
            "file_item_list",
            "is_previous",
            "parent_appointment",
            "appointment_date",
            "appointment_time",
            "recent_prescription",
            "feedback",
        ]

        read_only_fields = ["serial_number"]

    def get_seek_help_list(self, obj):
        seek_helps = AppointmentSeekHelpConnector.objects.filter(appointment=obj)
        seek_help_names = [
            seek_help.seek_help.name for seek_help in seek_helps if seek_help.seek_help
        ]
        seek_help_for = seek_helps.filter(seek_help_for__isnull=False).first()
        data = {
            "seek_help": seek_help_names,
            "seek_help_for": seek_help_for.seek_help_for if seek_help_for else None,
        }
        return data

    def get_allergic_medication_list(self, obj):
        allergic_medications = AppointmentAllergicMedicationConnector.objects.filter(
            appointment=obj
        )
        return PrivateAllergicMedicationSlimSerializer(
            allergic_medications, many=True
        ).data

    def get_current_medication_list(self, obj):
        current_medications = AppointmentMedicationConnector.objects.filter(
            appointment=obj
        )
        return PrivateCurrentMedicationSlimSerializer(
            current_medications, many=True
        ).data

    def get_treated_conditions(self, obj):
        treated_conditions = AppointmentTreatedConditionConnector.objects.filter(
            appointment=obj
        )
        treated_condition_names = [
            treated_condition.treated_condition.name
            for treated_condition in treated_conditions
            if treated_condition.treated_condition
        ]
        treated_condition_for = treated_conditions.filter(
            treated_condition_for__isnull=False
        ).first()
        data = {
            "treated_condition": treated_condition_names,
            "treated_condition_for": treated_condition_for.treated_condition_for
            if treated_condition_for
            else None,
        }
        return data

    def get_file_item_list(self, obj):
        file_items = MediaImageConnector.objects.filter(
            appointment=obj, patient=obj.patient
        )
        request = self.context.get("request")

        return PrivateMediaImageConnectorSlimSerializer(
            file_items, many=True, context={"request": request}
        ).data

    def get_recent_prescription(self, obj):
        patient = obj.patient
        recent_prescription = (
            Prescription.objects.filter(patient=patient, appointment=obj)
            .order_by("-created_at")
            .first()
        )
        serializer = PrivatePrescriptionSlimSerializer(
            recent_prescription, context=self.context
        )
        data = serializer.data

        if data.get("doctor"):
            doctor_data = data.get("doctor")
            if doctor_data and "image" in doctor_data:
                request = self.context.get("request")
            image_url = doctor_data.get("image")

            if image_url:
                doctor_data["image"] = request.build_absolute_uri(image_url)
        return data

    def get_feedback(self, obj):
        feedback_data = {
            "doctor": {
                "rating": None,
                "comment": None,
                "created_at": None,
            },
            "patient": {
                "rating": None,
                "comment": None,
                "created_at": None,
            },
        }

        feedbacks = (
            obj.feedback_set.select_related("doctor", "patient")
            .filter()
            .order_by("rated_by_doctor")
        )

        if feedbacks:
            for feedback in feedbacks:
                if feedback.rated_by_doctor:
                    feedback_data["doctor"]["rating"] = feedback.rating
                    feedback_data["doctor"]["comment"] = feedback.comment
                    feedback_data["doctor"]["created_at"] = feedback.created_at
                else:
                    feedback_data["patient"]["rating"] = feedback.rating
                    feedback_data["patient"]["comment"] = feedback.comment
                    feedback_data["patient"]["created_at"] = feedback.created_at

        return feedback_data

    def update(self, instance, validated_data):
        with transaction.atomic():
            request = self.context["request"]
            phone_number = validated_data.get("phone", None)
            first_name = validated_data.get("first_name", "")
            last_name = validated_data.get("last_name", "")
            date_of_birth = validated_data.get("date_of_birth", "")
            email = validated_data.get("email", "")
            gender = validated_data.get("gender", "")
            blood_group = validated_data.get("blood_group", "")
            height = validated_data.get("height", "")
            weight = validated_data.get("weight", "")
            status = validated_data.get("status", None)
            doctor_uid = validated_data.get("doctor_uid", None)
            organization: Organization = request.user.get_organization()
            parent_appointment = validated_data.pop("parent_appointment", None)
            appointment_type = validated_data.get("appointment_type", None)
            appointment_date = validated_data.pop("appointment_date", None)
            appointment_time = validated_data.pop("appointment_time", None)

            instance.appointment_type = validated_data.get(
                "appointment_type", instance.appointment_type
            )

            if phone_number:
                user, _ = User.objects.get_or_create(
                    phone=phone_number,
                    defaults={
                        "first_name": first_name,
                        "last_name": last_name,
                        "date_of_birth": date_of_birth,
                        "email": email,
                        "gender": gender,
                        "blood_group": blood_group,
                        "height": height,
                        "weight": weight,
                        "username": phone_number,
                        "type": UserType.PATIENT,
                    },
                )
            else:
                user = request.user

            validated_data["doctor"] = validated_data.get("doctor_uid", instance.doctor)
            validated_data["user"] = user
            validated_data["organization"] = organization

            if parent_appointment is not None:
                instance.parent = parent_appointment
                instance.status = AppointmentStatus.SCHEDULED
                validated_data["doctor"] = parent_appointment.doctor

                # create notification instance
                notification_for_appointment_status(instance)

            if appointment_type == "CONSULTATION":
                instance.parent = None
                instance.status = AppointmentStatus.REQUESTED
                validated_data["doctor"] = None

                # create notification instance
                notification_for_appointment_status(instance)

            if appointment_date or appointment_time:
                if appointment_date:
                    get_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
                else:
                    get_date = instance.schedule_start.date()

                if appointment_time:
                    get_time = datetime.strptime(appointment_time, "%H:%M").time()
                else:
                    get_time = instance.schedule_start.time()

                get_day = get_date.strftime("%A").upper()

                AppointmentDateTimeSlotConnector.objects.filter(
                    organization=organization, appointment=instance
                ).delete()

                if AppointmentDateTimeSlotConnector.objects.filter(
                    organization=organization,
                    date=get_date,
                    appointment_time_slot__slot=get_time,
                    is_booked=True,
                ).exists():
                    raise ValidationError(
                        "This appointment time slot is already booked."
                    )

                try:
                    weekday = WeekDay.objects.select_related("organization").get(
                        organization=organization, day=get_day, off_day=False
                    )
                except WeekDay.DoesNotExist:
                    raise ValidationError("Off Day!")

                try:
                    appointment_time_slot = AppointmentTimeSlot.objects.select_related(
                        "organization", "weekday"
                    ).get(organization=organization, weekday=weekday, slot=get_time)

                except AppointmentTimeSlot.DoesNotExist:
                    raise ValidationError("Appointment schedule time doesn't exist!")

                AppointmentDateTimeSlotConnector.objects.create(
                    organization=organization,
                    appointment=instance,
                    date=get_date,
                    appointment_time_slot=appointment_time_slot,
                )

                instance.schedule_start = datetime.combine(get_date, get_time)

            if status == AppointmentStatus.COMPLETED:
                now = datetime.now()
                instance.schedule_end = now

                try:
                    appointment_uid = self.context["view"].kwargs.get("appointment_uid")

                    appointment = Appointment.objects.get(uid=appointment_uid)
                    schedule_date = appointment.schedule_start.date()
                    schedule_time = appointment.schedule_start.time()
                except Appointment.DoesNotExist:
                    raise ValidationError("Appointment not found!")

                day = schedule_date.strftime("%A").upper()

                try:
                    weekday = WeekDay.objects.select_related("organization").get(
                        organization=appointment.organization, day=day, off_day=False
                    )
                    appointment_time_slot = AppointmentTimeSlot.objects.select_related(
                        "organization", "weekday"
                    ).get(
                        organization=appointment.organization,
                        weekday=weekday,
                        slot=schedule_time,
                    )
                    date_time_slot_connector = (
                        AppointmentDateTimeSlotConnector.objects.select_related(
                            "organization", "appointment", "appointment_time_slot"
                        ).filter(
                            organization=appointment.organization,
                            appointment=appointment,
                            date=schedule_date,
                            appointment_time_slot=appointment_time_slot,
                        )
                    )
                except AppointmentTimeSlot.DoesNotExist:
                    raise ValidationError("Appointment schedule time doesn't exist!")

                date_time_slot_connector.update(is_booked=False)

                # create notification instance
                notification_for_appointment_status(instance)

            appointment = super().update(
                instance=instance, validated_data=validated_data
            )

            if status == AppointmentStatus.SCHEDULED and doctor_uid:
                # create notification instance
                notification_for_appointment_status(appointment)

            return appointment


class PrivateAppointmentScheduleCreateSerializer(serializers.Serializer):
    appointment_duration = serializers.TimeField(
        write_only=True, allow_null=True, required=False
    )
    appointment_interval = serializers.TimeField(
        write_only=True, allow_null=True, required=False
    )
    week_days = PrivateWeekDayWriteSlimSerializer(
        write_only=True, many=True, allow_null=True, allow_empty=True, required=False
    )

    def create(self, validated_data):
        with transaction.atomic():
            appointment_duration = validated_data.pop("appointment_duration", None)
            appointment_interval = validated_data.pop("appointment_interval", None)
            week_days = validated_data.pop("week_days", [])
            organization = self.context["request"].user.get_organization()

            organization.appointment_duration = appointment_duration
            organization.appointment_interval = appointment_interval
            organization.save()

            time_slot_list = []

            # Before creating or updating Weekday, we first delete all Weekdays to avoid multiple creation of Weekday.
            # if we delete all weekday it will delete all related AppointmentTimeSlot models data.
            # That will help us to avoid multiple creation of AppointmentTimeSlot also.
            WeekDay.objects.filter(organization=organization).delete()

            for week_day in week_days:
                shift_list = []

                week_day_object = WeekDay.objects.create(
                    organization=organization,
                    day=week_day["day"],
                    off_day=week_day["off_day"],
                )

                if "shifts" in week_day:
                    for shift in week_day["shifts"]:
                        shift_list.append(
                            Shift(
                                weekday=week_day_object,
                                shift_label=shift["shift_label"],
                                start_time=shift["start_time"],
                                end_time=shift["end_time"],
                            )
                        )

                if shift_list:
                    shifts = Shift.objects.bulk_create(shift_list)

                    for per_shift in shifts:
                        start_time = per_shift.start_time
                        end_time = per_shift.end_time

                        while start_time < end_time:
                            schedule_time = datetime.combine(
                                date.today(), start_time.replace(minute=0)
                            )
                            time_slot_list.append(
                                AppointmentTimeSlot(
                                    organization=organization,
                                    weekday=week_day_object,
                                    schedule_time=schedule_time.strftime("%H:%M"),
                                    slot=start_time,
                                )
                            )
                            start_time = (
                                datetime.combine(date.today(), start_time)
                                + timedelta(
                                    minutes=appointment_duration.minute
                                    + appointment_interval.minute
                                )
                            ).time()

            AppointmentTimeSlot.objects.bulk_create(time_slot_list)

            return validated_data


class PrivateAppointmentScheduleListSerializer(serializers.ModelSerializer):
    shifts = serializers.SerializerMethodField()

    class Meta:
        model = WeekDay
        fields = ["day", "off_day", "shifts"]
        read_only_fields = ["__all__"]

    def get_shifts(self, obj):
        shift = Shift.objects.filter(weekday=obj)

        return PrivateShiftSlimSerializer(shift, many=True).data
