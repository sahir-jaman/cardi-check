from django.urls import path

from ..views.appointments import (
    PrivateAppointmentDetail,
    PrivateAppointmentList,
    PrivateAppointmentScheduleList,
    PrivateAppointmentTimeSlotList,
)

urlpatterns = [
    path(
        "/time-slots",
        PrivateAppointmentTimeSlotList.as_view(),
        name="we.appointment-time-slot-list",
    ),
    path(
        "/schedules",
        PrivateAppointmentScheduleList.as_view(),
        name="we.appointment-schedule-list",
    ),
    path(
        "/<uuid:appointment_uid>",
        PrivateAppointmentDetail.as_view(),
        name="we.appointment-detail",
    ),
    path(
        "",
        PrivateAppointmentList.as_view(),
        name="we.appointment-list",
    ),
]
