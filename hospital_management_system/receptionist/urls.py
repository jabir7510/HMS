from django.urls import path
from .views import ReceptionistDashboardView, ApproveRejectAppointmentView

urlpatterns = [
    path("dashboard/", ReceptionistDashboardView.as_view(), name="receptionist_dashboard"),
    # path("appointments/", ApproveRejectAppointmentView.as_view(), name="approve_reject_appointment"),
    path("appointments/<str:appointment_id>/", ApproveRejectAppointmentView.as_view(), name="approve_reject_appointment"),
]
