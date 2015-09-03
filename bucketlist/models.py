from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse


def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    name_url = models.CharField(max_length=128)

    def create_category(self):
        self.name_url = encode_url(self.name)
        
    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    category_url = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    name_url = models.CharField(max_length=128)

    country = models.CharField(max_length=128)
    date_added = models.DateTimeField(default = timezone.now)
    was_done = models.BooleanField(default=False)
    years_visted = models.CommaSeparatedIntegerField(max_length=200, blank=True, null=True)
    picture_link = models.URLField(blank=True, null=True)
    likes = models.IntegerField(default=0)
    notes = models.TextField(blank=True) 

    def create_page(self):
        self.category_url = encode_url(self.category)
        self.name_url = encode_url(self.name)
        self.date_added = timezone.now()
        self.was_done = False
        self.likes = 0
        self.save()

    def finish_bucket_item(self):
        #self.datedone = timezone.now()
        self.was_done = True
        self.save()

    #def get_absolute_url(self):
    #    return reverse('bucketlist.views.detail', args=[str(self.name)])

    def __str__(self):
        return self.name

class Place(models.Model):
    categorys = (
        ('Eat', 'Eat'),
        ('See', 'See'),
        ('Sleep', 'Sleep'),
    )

    name = models.CharField(max_length=128)
    location = models.ForeignKey(Page)
    category = models.CharField(max_length=10, choices=categorys)
    address = models.CharField(max_length=128, blank=True, null=True)
    likes = models.IntegerField(default=0)
    notes = models.TextField(blank=True)

    #def get_absolute_url(self):
    #    return reverse('detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.name