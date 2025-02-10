from django.shortcuts import render, redirect
from django.views import View
from pymongo import MongoClient
from django.contrib import messages
from .forms import UpdatePatientForm

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["hospital_management"]
users_collection = db["users"]
appointments_collection = db["appointments"]

class PatientProfileView(View):
    def get(self, request):
        if "username" not in request.session or request.session.get("role") != "patient":
            return redirect("login")

        patient = users_collection.find_one({"username": request.session["username"]})
        form = UpdatePatientForm(initial={
            "name": patient["name"],
            "age": patient["age"],
            "gender": patient["gender"],
            "address": patient["address"],
            "contact": patient["contact"],
            "medical_history": patient["medical_history"]
        })
        return render(request, "patient_profile_update.html", {"patient": patient, "form": form})

    def post(self, request):
        if "username" not in request.session or request.session.get("role") != "patient":
            return redirect("login")

        form = UpdatePatientForm(request.POST)
        if form.is_valid():
            updated_data = {
                "name": form.cleaned_data["name"],
                "age": form.cleaned_data["age"],
                "gender": form.cleaned_data["gender"],
                "address": form.cleaned_data["address"],
                "contact": form.cleaned_data["contact"],
                "medical_history": form.cleaned_data["medical_history"],
            }

            users_collection.update_one({"username": request.session["username"]}, {"$set": updated_data})
            messages.success(request, "Profile updated successfully!")
            return redirect("patient_profile")
        else:
            return render(request, "patient_profile_update.html", {"form": form})
    
class PatientDashboardView(View):
    def get(self, request):
        # Check if the user is logged in and is a patient
        if "username" not in request.session or request.session.get("role") != "patient":
            return redirect("login")

        # Fetch the patient's details
        patient = users_collection.find_one({"username": request.session["username"]})

        # Fetch the list of doctors
        doctors = list(users_collection.find({"role": "doctor"}))

        # Fetch the patient's appointment history
        appointments = list(appointments_collection.find({
            "patient_username": request.session["username"]
        }))

        # Render the patient dashboard with all the necessary data
        return render(request, "patient_dashboard.html", {
            "patient": patient,
            "doctors": doctors,
            "appointments": appointments
        })

    def post(self, request):
        # Check if the user is logged in and is a patient
        if "username" not in request.session or request.session.get("role") != "patient":
            return redirect("login")

        # Handle the appointment booking form submission
        doctor_username = request.POST.get("doctor_username")
        date = request.POST.get("date")
        time = request.POST.get("time")

        if not doctor_username or not date or not time:
            messages.error(request, "All fields are required.")
            return redirect("patient_dashboard")



        # Insert the new appointment into the appointments collection
        appointments_collection.insert_one({
            "patient_username": request.session["username"],
   
            "doctor_username": doctor_username,
            "date": date,
            "time": time,
            "status": "pending"
        })

        messages.success(request, "Appointment booked successfully!")
        return redirect("patient_dashboard")