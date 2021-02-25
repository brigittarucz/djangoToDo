# Provides from the package the built in admin site
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Path is whatever you decide
    path('admin/', admin.site.urls),
    # include() includes other URLconf modules rooting a set of URLs below other ones
    path('todo/', include('mini_project_app.urls')),
    # Django expect this route for redirecting unauthorized requests so we will use it for the login app as well
    path('accounts/', include('login_app.urls')),
]