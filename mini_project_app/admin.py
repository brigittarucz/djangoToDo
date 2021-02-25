from django.contrib import admin
from .models import Todo

# Without this, you will not see the models in the admin interface
admin.site.register(Todo)
