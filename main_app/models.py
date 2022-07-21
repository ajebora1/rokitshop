from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from datetime import datetime, date
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    date = models.DateField(('Upload Date'), auto_now_add=True)
    description = models.TextField(max_length=250)
    posted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    min_bid = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("detail", kwargs={"item_id": self.pk})
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(null=True, max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
        
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
class Bid(models.Model):
    date = models.DateField(('Upload Date'), auto_now_add=True)
    current_bid = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.item.name

    class Meta:
        ordering = ["-current_bid"]

class Photo(models.Model):
    url = models.CharField(max_length=200)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for item_id: {self.item_id} @{self.url}"

class UserPhoto(models.Model):
    url = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for user_id: {self.user_id} @{self.url}"
