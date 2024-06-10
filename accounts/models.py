from django.db import models
from django.contrib.auth.models import User
import random
import os
from django.core.files import File
from urllib.request import urlretrieve

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    locale = models.CharField(max_length=255)
    headline = models.CharField(max_length=255, null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    linkedin_photo_url = models.URLField(max_length=500, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def color_code(self):
        random.seed(self.user.username)
        return ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])

    def download_linkedin_photo(self):
        if self.linkedin_photo_url:
            result = urlretrieve(self.linkedin_photo_url)
            self.profile_photo.save(
                os.path.basename(self.linkedin_photo_url),
                File(open(result[0], 'rb'))
            )
            self.save()