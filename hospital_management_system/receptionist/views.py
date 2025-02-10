from django.shortcuts import render, redirect
from django.views import View
from pymongo import MongoClient
from django.contrib import messages
from bson import ObjectId
# Create your views here.


client = MongoClient("mongodb://localhost:27017/")
db = client["hospital_management"]
appointments_collection = db["appointments"]

class ReceptionistDashboardView(View):
    def get(self, request):
        if "username" not in request.session or request.session.get("role") != "receptionist":
            return redirect("login")

        appointments = list(appointments_collection.find({"status": "pending"}))
        for appointment in appointments:
            appointment["id"] = str(appointment["_id"])  # Convert ObjectId to string

        return render(request, "receptionist_dashboard.html", {"appointments": appointments})

# class ApproveRejectAppointmentView(View):
#     def post(self, request, appointment_id):
#         if "username" not in request.session or request.session.get("role") != "receptionist":
#             return redirect("login")

#         status = request.POST.get("status")  # "approved" or "rejected"

#         appointments_collection.update_one(
#             {"_id": ObjectId(appointment_id)},
#             {"$set": {"status": status}}
#         )

#         messages.success(request, f"Appointment {status} successfully!")
#         return redirect("receptionist_dashboard")
from datetime import datetime

class ApproveRejectAppointmentView(View):
    def post(self, request, appointment_id):
        if "username" not in request.session or request.session.get("role") != "receptionist":
            return redirect("login")

        status = request.POST.get("status")  # "approved" or "rejected"
        
        appointment = appointments_collection.find_one({"_id": ObjectId(appointment_id)})
        if not appointment:
            messages.error(request, "Appointment not found!")
            return redirect("receptionist_dashboard")

        update_data = {
            "status": status,
            "updated_at": datetime.utcnow()  # Store the timestamp for history tracking
        }
        
        if status == "approved":
            update_data["doctor_username"] = appointment.get("doctor_username")  # Ensure doctor is assigned
        
        appointments_collection.update_one(
            {"_id": ObjectId(appointment_id)},
            {"$set": update_data}
        )

        messages.success(request, f"Appointment {status} successfully!")
        return redirect("receptionist_dashboard")
