from django.urls import path
from .views import PatientDashboardView, PatientProfileView
urlpatterns = [
    path("dashboard/", PatientDashboardView.as_view(), name="patient_dashboard"),
    path("profile/", PatientProfileView.as_view(), name="patient_profile"),
    # path("appointments/book/", BookAppointmentView.as_view(), name="book_appointment"),
    # path("appointments/history/", AppointmentHistoryView.as_view(), name="appointment_history"),
]
