from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver


carousel = './carousel/%Y/%m/%d/'
class Carousel(models.Model):
    title     = models.CharField(max_length=100)
    content   = models.TextField()
    image     = models.ImageField(upload_to=carousel ,default='default.jpg',blank=True, null=True)
    is_active = models.BooleanField(default=False)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.image.path)

            if img.height > 1024 or img.width > 1024:
                output_size = (1024, 1024)
                img.thumbnail(output_size)
                img.save(self.image.path)
        except Exception as e:
            pass    
    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={'pk': self.pk})


Featuretts = './Featuretts/%Y/%m/%d/'    
class Featuretts(models.Model):
    title     = models.CharField(max_length=100)
    content   = models.TextField()
    is_active = models.BooleanField(default=False) 
    image     = models.ImageField(upload_to=Featuretts ,default='default.jpg',blank=True, null=True)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.image.path)

            if img.height > 500 or img.width > 500:
                output_size = (500, 500)
                img.thumbnail(output_size)
                img.save(self.image.path)
        except Exception as e:
            pass        

Marketing = './Marketing/%Y/%m/%d/'    
class Marketing(models.Model):
    title     = models.CharField(max_length=100)
    content   = models.TextField()
    is_active = models.BooleanField(default=False) 
    image     = models.ImageField(upload_to=Marketing ,default='default.jpg',blank=True, null=True)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.image.path)

            if img.height > 140 or img.width > 140:
                output_size = (140, 140)
                img.thumbnail(output_size)
                img.save(self.image.path)
        except Exception as e:
            pass        

class Ticker(models.Model):
    title     = models.CharField(max_length=300)
    def __str__(self):
        return self.title
