

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import IoTData  # Import IoT model


# ------------------- REGISTER -------------------
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        # Auto-add +91 prefix to phone number if missing
        if not phone.startswith('+'):
            phone = '+91' + phone.strip()

        if User.objects.filter(username=username).exists():
            messages.error(request, "⚠ Username already exists!")
        else:
            hashed_password = make_password(password)
            User.objects.create(username=username, first_name=phone, password=hashed_password)
            messages.success(request, "✅ Registration successful! Please login.")
            return redirect('login')

    return render(request, 'register.html')


# ------------------- LOGIN (With Email Alert) -------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                login(request, user)
                messages.success(request, f"Welcome, {username}! 🎉")

                # ✅ Send login notification via email
                subject = "SmartHome Login Alert"
                message = f"Hi {username}, you have successfully logged into your SmartHome account."
                recipient = user.email if user.email else settings.EMAIL_HOST_USER

                try:
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
                    print("✅ Email sent successfully.")
                except Exception as e:
                    print("⚠ Email send failed:", e)

                return redirect('home')

            else:
                messages.error(request, "❌ Invalid password.")
        except User.DoesNotExist:
            messages.error(request, "❌ User not found.")

    return render(request, 'login.html')



# ------------------- HOME (IoT Dashboard + Sensors) -------------------
from django.shortcuts import render, redirect
from .models import IoTData, ESP32Data

def home_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Existing recent IoT updates (UNCHANGED)
    recent_data = IoTData.objects.all().order_by('-created_at')[:5]

    # Original static sensors (UNCHANGED)
    sensors = {
        'Temperature': '27°C',
        'Humidity': '55%',
        'Motion': 'Detected',
        'Light': 'ON',
    }

    # ✅ ADD: Get latest ESP32 data (without changing old logic)
    latest = ESP32Data.objects.last()
    if latest:
        sensors.update({
            "Temperature": f"{latest.temperature} °C",
            "Humidity": f"{latest.humidity} %",
            "Smoke": latest.smoke
        })

    # ✅ ADD: append ESP32 data into recent list
    esp32_recent = ESP32Data.objects.order_by('-id')[:5]

    return render(request, 'home.html', {
        'sensors': sensors,
        'recent_data': recent_data,
        'esp32_recent': esp32_recent  # extra data without breaking old code
    })


def about(request):
    return render(request, "about.html")

def privacy(request):
    return render(request, "privacy.html")

def help_page(request):
    return render(request, "help.html")

def contact(request):
    return render(request, "contact.html")


# ------------------- DASHBOARD (Extended Home) -------------------
# home/views.py
from django.shortcuts import render

def weather_iot(request):
    # Temporary dummy IOT sensor data
    context = {
        "temperature": 25.3,
        "humidity": 55,
        "pressure": 1013
    }
    return render(request, "weather_iot.html", context)


# ------------------- IoT API Endpoint -------------------
@csrf_exempt
def iot_api_view(request):
    """
    IoT device POST example:
    {
        "sensor_type": "temperature",
        "value": 28.6,
        "unit": "°C"
    }
    """
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            sensor_type = body.get('sensor_type')
            value = float(body.get('value', 0))
            unit = body.get('unit', '')

            IoTData.objects.create(sensor_type=sensor_type, value=value, unit=unit)
            return JsonResponse({'status': 'success', 'message': 'Data saved!'}, status=201)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    elif request.method == "GET":
        data = list(IoTData.objects.all().order_by('-created_at').values()[:10])
        return JsonResponse({'status': 'success', 'data': data}, status=200)

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)


# ------------------- LOGOUT -------------------
def logout_view(request):
    logout(request)
    messages.success(request, "✅ You have been logged out.")
    return redirect('login')

# ------------------After LOGin-----------------

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")   # <-- Redirect to Dashboard
        else:
            messages.error(request, "Invalid Username or Password!")

    return render(request, "login.html")

def dashboard(request):
    return render(request, "dashboard.html")

#--------------------Sensors---------------------------------------
from django.shortcuts import render
from .models import ESP32Data

def sensors(request):
    latest = ESP32Data.objects.last()  # Get latest ESP32 data

    sensors_list = [
        {"name": "Temperature", "value": f"{latest.temperature}°C", "unit": "°C", "icon": "🌡️"},
        {"name": "Humidity", "value": f"{latest.humidity}%", "unit": "%", "icon": "💧"},
        {"name": "Gas Sensor", "value": latest.smoke, "unit": "", "icon": "⚠️"},
    ]

    return render(request, "sensors.html", {"sensors": sensors_list})


#-----------------
from django.shortcuts import render
from .models import SensorData

def sensors(request):
    latest = SensorData.objects.last()

    # If no data exists, use default values
    if latest is None:
        temperature = "N/A"
        humidity = "N/A"
        gas = "N/A"
    else:
        temperature = f"{latest.temperature}"
        humidity = f"{latest.humidity}"
        gas = f"{latest.gas_status}"

    sensors_list = [
        {"name": "Temperature", "value": temperature, "unit": "°C", "icon": "🌡️"},
        {"name": "Humidity", "value": humidity, "unit": "%", "icon": "💧"},
        {"name": "Gas Sensor", "value": gas, "unit": "", "icon": "⚠️"},
    ]

    return render(request, "sensors.html", {"sensors": sensors_list})

#------------------Controls---------------------------

def controls(request):
    return render(request, 'controls.html')

#------------------Report--------------------------------

def report(request):
    sensors = {
        "Temperature": 28,
        "Humidity": 41,
        "Gas Sensor": "Normal",
        "Smoke Sensor": "Safe",
        "Motion Sensor": "No Motion",
    }

    return render(request, "report.html", {"sensors": sensors})


# -------------------- FORGOT PASSWORD ----------------------

def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get("username")

        # Check if user exists
        if User.objects.filter(username=username).exists():
            request.session["reset_user"] = username
            return redirect("reset_password")

        messages.error(request, "User not found!")
        return redirect("forgot_password")

    return render(request, "forgot_password.html")

#-------------------------- Create Reset Password --------------------

def reset_password(request):
    username = request.session.get("reset_user")

    if not username:
        return redirect("forgot_password")

    if request.method == "POST":
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("reset_password")

        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()

        messages.success(request, "Password updated successfully!")
        return redirect("login")

    return render(request, "reset_password.html")

#------------------Forgot Password-----------------------

import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        # Check if user exists
        if not User.objects.filter(email=email).exists():
            messages.error(request, "Email not found!")
            return redirect('forgot_password')

        # Generate 6-digit OTP
        otp = random.randint(100000, 999999)

        # Save OTP in session
        request.session['otp'] = otp
        request.session['email'] = email

        # Send OTP through email
        send_mail(
            subject="SmartHome Password Reset OTP",
            message=f"Your OTP is {otp}",
            from_email="yourgmail@gmail.com",
            recipient_list=[email],
        )

        messages.success(request, "OTP sent to your email!")
        return redirect("verify_otp")

    return render(request, "forgot_password.html")

#--------------------verify otp-------------------------

def verify_otp(request):
    if request.method == "POST":
        entered = request.POST.get("otp")
        saved = str(request.session.get("reset_otp"))

        if entered == saved:
            return redirect("reset_password")
        else:
            messages.error(request, "Invalid OTP")
            return redirect("verify_otp")

    return render(request, "verify_otp.html")

#------------------------Reset Password--------------------------------------------------

from django.contrib.auth.models import User

def reset_password(request):
    email = request.session.get("reset_email")  # email entered in forgot_password

    if request.method == "POST":
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        if password != confirm:
            messages.error(request, "Passwords do not match!")
            return redirect("reset_password")

        try:
            # If you registered users with username instead of email:
            user = User.objects.get(username=email)  # change email → username
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successful!")
            return redirect("login")
        except User.DoesNotExist:
            messages.error(request, "User not found!")
            return redirect("forgot_password")

    return render(request, "reset_password.html")


#-------------==============-------------
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
import random

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        print("Entered:", email)  # debug

        # generate OTP
        otp = random.randint(100000, 999999)

        # save OTP in session
        request.session["reset_email"] = email
        request.session["reset_otp"] = otp

        # send email
        send_mail(
            subject="Your SmartHome Password Reset OTP",
            message=f"Your OTP for password reset is: {otp}\nDo not share it with anyone.",
            from_email="abhayrajawat20501@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(request, "OTP sent to your email!")
        return redirect("verify_otp")

    return render(request, "forgot_password.html")

#-------------------------------register----------------------------------------------------

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        messages.success(request, "Registration successful! Please login.")
        return redirect("login")

    return render(request, "register.html")

#=======================resend_otp============================

from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib import messages
import random

def resend_otp(request):
    # Generate a new 6-digit OTP
    otp = str(random.randint(100000, 999999))
    
    # Save OTP in session
    request.session['reset_otp'] = otp

    # Assuming the user's email is stored in session
    email = request.session.get('reset_email')
    
    if email:
        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP is: {otp}",
            from_email="your_email@gmail.com",  # Replace with your email
            recipient_list=[email],
            fail_silently=False,
        )
        messages.success(request, "A new OTP has been sent to your email.")
    else:
        messages.error(request, "No email found in session.")

    return redirect("verify_otp")

#-------------------------------------Receive ESP32 Data-----------------------------
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

sensor_data = {
    "temperature": "0",
    "humidity": "0",
    "gas_status": "Safe",
    "smoke_status": "No Smoke",
    "motion_status": "No Motion",
    "light": "0",
    "flame_status": "Not Detected",
    "door_status": "Closed"
}

@csrf_exempt
def update_sensors(request):

    if request.method == "POST":
        data = json.loads(request.body)
        sensor_data.update(data)
        return JsonResponse({"status": "success", "message": "Data updated"})

    return JsonResponse(sensor_data)

#-----------------------Save Data in Cloud DB----------------------

from django.shortcuts import render
from django.core.mail import send_mail
from .models import ContactMessage

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Save to DB
        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )

        # Send email to your Gmail
        send_mail(
            subject=f"New Contact Message from {name}",
            message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
            from_email="abhayrajawat20501@gmail.com",
            recipient_list=["abhayrajawat20501@gmail.com"],  # where message will come
            fail_silently=False,
        )

        return render(request, "contact.html", {"success": True})

    return render(request, "contact.html")


#-----------------------SENSOR DATA-------------------

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# Temporary in-memory sensor storage
SENSOR_DATA = {
    "Temperature": {"value": "0°C", "icon": "🌡️"},
    "Humidity": {"value": "0%", "icon": "💧"},
    "Smoke": {"value": "Unknown", "icon": "⚠️"}
}

@csrf_exempt
def sensors_api(request):
    """
    Handle POST requests from ESP32 and return current sensor data.
    """
    global SENSOR_DATA
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            SENSOR_DATA["Temperature"]["value"] = str(data.get("Temperature", 0)) + "°C"
            SENSOR_DATA["Humidity"]["value"] = str(data.get("Humidity", 0)) + "%"
            SENSOR_DATA["Smoke"]["value"] = data.get("Smoke", "Unknown")
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse(SENSOR_DATA)

#----------------------------sensors_page----------------------------------

from django.shortcuts import render

def sensors_page(request):
    # You can fetch real sensor data here if you want
    context = {
        "temperature": 25,
        "humidity": 70,
        "smoke": "No"
    }
    return render(request, "sensors.html", context)

#---------------------------IOT -----------------------------------

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import ESP32Data  # your model to save sensor data
import json

@csrf_exempt
def esp32_api(request):
    if request.method == "POST":
        try:
            # decode JSON sent from ESP32
            data = json.loads(request.body.decode("utf-8"))

            temperature = data.get("Temperature")
            humidity = data.get("Humidity")
            smoke = data.get("Smoke")

            light = data.get("Light")   # ✅ NEW: LDR value

            # save to database
            ESP32Data.objects.create(
                temperature=temperature,
                humidity=humidity,
                smoke=smoke,
                light=light   # ✅ NEW: Save LDR data
            )

            print(f"Received data: {data}")  # for debug
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    elif request.method == "GET":
        # return latest sensor data
        latest = ESP32Data.objects.last()
        if latest:
            data = {
                "Temperature": latest.temperature,
                "Humidity": latest.humidity,
                "Smoke": latest.smoke,
                "Light": latest.light   # ✅ NEW: send LDR data to webpage
            }
        else:
            data = {
                "Temperature": 0,
                "Humidity": 0,
                "Smoke": "Unknown",
                "Light": "Unknown"   # ✅ NEW default
            }
        return JsonResponse(data)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=405)

