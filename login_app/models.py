from django.db import models
from django.contrib.auth.models import User
from secrets import token_urlsafe


# Because we will store the info in the db we need the following new model class
class PasswordResetRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # The token is a cryptographically strong random sequence of characters that can safely be url encoded
    token = models.CharField(max_length=43, default=token_urlsafe)
    # created_timestamp will only be set that one time
    created_timestamp = models.DateTimeField(auto_now_add=True)
    # updated_timestamp will be set every time the object is saved
    updated_timestamp = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.user} - {self.created_timestamp} - {self.token}'

# the user enters his username or email address to request a password reset
# the system generates a PasswordResetRequest and send the information to the user 
# the user enters then his username, new password, new password confirmation, and the secret token
# if everything is ok, the system will set the new password, and allow the user to login again