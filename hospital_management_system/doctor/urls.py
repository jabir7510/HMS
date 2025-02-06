from django.urls import path
from .views import DoctorDashboardView, PatientListView, PatientDetailView, AddPrescriptionView, MedicalRecordsView

urlpatterns = [
    path("dashboard/", DoctorDashboardView.as_view(), name="doctor_dashboard"),
    path("patients/", PatientListView.as_view(), name="patient_list"),
    path("patients/<str:patient_id>/", PatientDetailView.as_view(), name="patient_detail"),
    path("patients/<str:patient_id>/add-prescription/", AddPrescriptionView.as_view(), name="add_prescription"),
    path("patients/<str:patient_id>/medical-records/", MedicalRecordsView.as_view(), name="medical_records"),
]
