from django.contrib import admin
from .models import PasswordResetRequest


# To enable us to see this model in the Django admin panel
admin.site.register(PasswordResetRequest)
