from django.shortcuts import render, redirect
from django.views import View
from pymongo import MongoClient
from django.http import HttpResponseNotFound, JsonResponse
from bson import ObjectId
from django.contrib import messages 
# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["hospital_management"]
users_collection = db["users"]
medical_records_collection = db["medical_records"]
appointments_collection = db["appointments"]

class DoctorDashboardView(View):
    def get(self, request):
        username = request.session.get("username")
        if not username:
            return redirect("login")
        doctor = users_collection.find_one({"username": username})

        patients_cursor = users_collection.find({"role": "patient"})
        
        # Check if the query returns any patients
        patients = list(patients_cursor)  # Convert cursor to list
        # print("Patients:", patients)
        
        # Explicitly pass the _id as a normal attribute
        for patient in patients:
            patient['id'] = str(patient['_id'])  # Convert the ObjectId to a string for the template

        return render(request, "dashboard.html", {"doctor": doctor, "patients": patients})

class PatientListView(View):
    def get(self, request):
        patients = list(users_collection.find({"role": "patient"}))
        return render(request, "patient_list.html", {"patients": patients})


class PatientDetailView(View):
    def get(self, request, patient_id):
        try:
            # Convert string ID to ObjectId
            object_id = ObjectId(patient_id)
            patient = users_collection.find_one({"_id": object_id})
            
            if not patient:
                return HttpResponseNotFound(f"Patient with ID {patient_id} not found.")
            
            # Convert ObjectId to string for the template
            patient['id'] = str(patient['_id'])
            
            # Find medical records using string patient_id
            medical_records = list(medical_records_collection.find({"patient_id": patient_id}))
            
            return render(request, "patient_detail.html", {
                "patient": patient,
                "medical_records": medical_records,
                "patient_id": patient_id  # Pass the string ID for the form action
            })
            
        except Exception as e:
            return HttpResponseNotFound(f"Error retrieving patient: {str(e)}")

class DoctorAppointmentsView(View):
    def get(self, request):
        if "username" not in request.session or request.session.get("role") != "doctor":
            return redirect("login")

        doctor_username = request.session["username"]
        appointments = list(appointments_collection.find({
            "doctor_username": doctor_username,
            "status": "approved"
        }))

        for appointment in appointments:
            appointment["id"] = str(appointment["_id"])

        return render(request, "doctor_appointments.html", {"appointments": appointments})
class AppointmentHistoryView(View):
    def get(self, request):
        if "username" not in request.session or request.session.get("role") != "doctor":
            return redirect("login")

        doctor_username = request.session["username"]
        appointments = list(appointments_collection.find({
            "doctor_username": doctor_username
        }).sort("updated_at", -1))  # Sort by recent updates

        for appointment in appointments:
            appointment["id"] = str(appointment["_id"])

        return render(request, "appointment_history.html", {"appointments": appointments})


class AddPrescriptionView(View):
    def post(self, request, patient_id):
        try:
            data = {
                "patient_id": patient_id,  # Store as string ID
                "doctor": request.session.get("username"),
                "prescription": request.POST.get("prescription"),
                "notes": request.POST.get("notes"),
            }
            medical_records_collection.insert_one(data)
            messages.success(request, 'Prescription added successfully!')
            return redirect('patient_detail', patient_id=patient_id)
        except Exception as e:
            messages.error(request, f'Error adding prescription: {str(e)}')
            return JsonResponse({"error": str(e)}, status=400)

class MedicalRecordsView(View):
    def get(self, request, patient_id):
        records = list(medical_records_collection.find({"patient_id": patient_id}))
        return render(request, "medical_records.html", {"records": records})
