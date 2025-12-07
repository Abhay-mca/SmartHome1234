# from django.db import models
# from django.utils import timezone

# class User(models.Model):
#     username = models.CharField(max_length=100, unique=True)
#     password = models.CharField(max_length=255)
#     phone = models.CharField(max_length=15, default='9999999999')

#     def __str__(self):
#         return self.username


# # 🆕 New IoT Data Model
# class IoTData(models.Model):
#     SENSOR_TYPES = [
#         ('temperature', 'Temperature'),
#         ('humidity', 'Humidity'),
#         ('motion', 'Motion'),
#         ('light', 'Light'),
#         ('gas', 'Gas'),
#     ]

#     sensor_type = models.CharField(max_length=50, choices=SENSOR_TYPES)
#     value = models.FloatField()
#     unit = models.CharField(max_length=10, default='')  # e.g. °C, %, etc.
#     created_at = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"{self.sensor_type}: {self.value}{self.unit} ({self.created_at.strftime('%Y-%m-%d %H:%M:%S')})"

from django.db import models

class IoTData(models.Model):
    sensor_type = models.CharField(max_length=100)
    value = models.FloatField()
    unit = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor_type}: {self.value}{self.unit}"

# from django.db import models

# class ContactMessage(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


from django.db import models

class SensorData(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.value}"


from django.db import models

class ESP32Data(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    smoke = models.CharField(max_length=50)

    # ✅ ADD THIS LINE
    light = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
