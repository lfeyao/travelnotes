from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    name_url = models.CharField(max_length=128, blank=True, null=True)

    def create_category(self):
        self.name_url = encode_url(self.name)

    # def __str__(self):
    #     return self.name

    class Meta:
        permissions = ( 
            ( "read_category", "Can read Category" ),
        )

class Page(models.Model):
    category = models.ForeignKey(Category)
    category_url = models.CharField(max_length=128, blank=True, null=True)
    
    name = models.CharField(max_length=128)
    name_url = models.CharField(max_length=128, blank=True, null=True)

    country = models.CharField(max_length=128, blank=True, null=True)
    date_added = models.DateTimeField(default = timezone.now)
    was_done = models.BooleanField(default=False)
    years_visted = models.CommaSeparatedIntegerField(max_length=200, blank=True, null=True)
    
    picture_link = models.URLField(blank=True, null=True)
    user_id = models.CharField(default='114388032679125757664', max_length=128, blank=True, null=True)
    album_id = models.CharField(max_length=128, blank=True, null=True)
    auth_key = models.CharField(max_length=128, blank=True, null=True)

    likes = models.IntegerField(default=0)
    notes = models.TextField(blank=True) 

    def create_page(self):
        self.category_url = self.category.name_url
        self.name_url = encode_url(self.name)
        self.save()

    def finish_bucket_item(self):
        #self.datedone = timezone.now()
        self.was_done = True
        self.save()

    # def __str__(self):
    #     return self.name

class Place(models.Model):
    categorys = (
        ('Eat', 'Eat'),
        ('See', 'See'),
        ('Sleep', 'Sleep'),
    )

    name = models.CharField(max_length=128)
    name_url = models.CharField(max_length=128, blank=True, null=True)

    location = models.ForeignKey(Page)

    category = models.CharField(max_length=10, choices=categorys)
    address = models.CharField(max_length=128, blank=True, null=True)
    likes = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
  
    def create_place(self):
        self.name_url = encode_url(self.name)
        self.save()

    # def __str__(self):
    #     return self.name