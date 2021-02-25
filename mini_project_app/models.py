from django.contrib.auth.models import User
# A model class is a database table
from django.db import models


# Subclass which inherits from models.Model superclass
class Todo(models.Model):
    # The user is created as a property on the todo model with the type ForeignKey
    # ForeignKey tells Django how to link the Todo model with the User model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    # field to mark the todos completed / not
    status = models.BooleanField(default=False)


    # __str__ is a way to convert Python objects into strings
    # __str__ is called when the object returns a string
    def __str__(self):
        # f is python's way of dealing with string interpolation
        return f"{self.text} - {self.status}"
