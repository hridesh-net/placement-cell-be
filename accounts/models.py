from django.db import models
from django.contrib.auth.models import User

class ProfileLinkedin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='', blank=True, null=True)
    email = models.EmailField(default='')
    # linkedin_profile_url = models.URLField(blank=True)

    def __str__(self):
         return f"LinkedIn Profile of {self.user.username}"


