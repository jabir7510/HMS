from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views import View
from pymongo import MongoClient
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.http import JsonResponse

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["hospital_management"]
users_collection = db["users"]

class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")
    
    def post(self, request):
        role = request.POST.get("role")
        username = request.POST.get("username")
        password = make_password(request.POST.get("password"))
        name = request.POST.get("name")
        
        if role not in ["doctor", "patient", "receptionist"]:
            messages.error(request, "Invalid role selected!")
            return redirect("register")
        
        user_data = {"username": username, "password": password, "role": role, "name": name}
        
        if role == "doctor":
            user_data.update({
                "qualification": request.POST.get("qualification"),
                "experience": request.POST.get("experience"),
                "specialization": request.POST.get("specialization")
            })
            
        elif role == "receptionist":
            user_data.update({
                "contact": request.POST.get("contact"),
            })
                
        elif role == "patient":
            user_data.update({
                "age": request.POST.get("age"),
                "gender": request.POST.get("gender"),
                "address": request.POST.get("address"),
                "contact": request.POST.get("contact"),
                "medical_history": request.POST.get("medical_history")
            })

        # Insert user data into MongoDB
        users_collection.insert_one(user_data)
        messages.success(request, "Registration successful! You can now login.")
        
        # Redirect to login page after successful registration
        return redirect("login")


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")
    
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = users_collection.find_one({"username": username})
        
        if user and check_password(password, user["password"]):
            request.session["username"] = username
            request.session["role"] = user["role"]
            
            if user["role"] == "doctor":
                return redirect("doctor_dashboard")
            elif user["role"] == "patient":
                return redirect("patient_dashboard")
            elif user["role"] == "receptionist":
                return redirect("receptionist_dashboard")
            else:
                return redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid credentials!")
            return redirect("login")

class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect("login")
