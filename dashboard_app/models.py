# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date, timedelta

from django.conf import settings

import uuid
from django.db import models
from django.db.models.fields import DateField
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from django.core import validators


from django.urls import reverse

import random   
import string  
import secrets 

from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from mimetypes import guess_type
from django_countries.fields import CountryField









# GENERATE RANDOM STRING WITH LENGTH 
def random_string(num):   
    res = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(num))  
    return str(res)







# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True
    def save_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The given email must be set'))
        email = self.normalize_email(email)
        user  = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = False
        return self.save_user(email, password, **extra_fields)

    def create_staffuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = False
        
        return self.save_user(email, password, **extra_fields) 

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('is_superuser should be True'))
        extra_fields['is_staff'] = True
        return self.save_user(email, password, **extra_fields) 
    





ROLE = (
    ("User", _("User")),
    # ("Agent", _("Agent")),
)

class User(AbstractBaseUser, PermissionsMixin):
    id        = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_("Nome"), max_length=255,)
    last_name  = models.CharField(_("Prenom"), max_length=255,)
    email      = models.EmailField(_("Email"), max_length=200, unique=True, validators = [validators.EmailValidator()])
    is_staff   = models.BooleanField(default=False)
    is_active  = models.BooleanField(default=True)
    i_agree    = models.BooleanField(_("Terms and conditions"), blank=True, null=True, default=False)
    role       = models.CharField(_("Role"), max_length=100, choices=ROLE, null=True, blank=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email










# PROFILE MODEL

class Profile(models.Model):
    STATUS_CHOICES = (
        ('Masculin', 'Masculin'),
        ('Feminin', 'Feminin'),
    )
    user 	      = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)
    photo         = models.ImageField(_("Photo"), upload_to='Images/%Y/%m/', null=True, blank=True)
    phone         = models.CharField(_("Numéro de téléphone"), max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(_("Date de Naissance"), blank=True, null=True)
    country       = CountryField(_("Pays"), max_length=255, null=True, blank=True)
    city          = models.CharField(_("Ville"), max_length=255, null=True, blank=True)
    address       = models.CharField(_("Adresse"), max_length=255, null=True, blank=True)
    gender        = models.CharField(_("Options"), max_length=100, choices=STATUS_CHOICES, null=True, blank=True)
    position      = models.CharField(_("Pays"), max_length=255, null=True, blank=True)
    facebook      = models.URLField(_("Facebook Link"), max_length=255, null=True, blank=True)
    instagram     = models.URLField(_("Instagram Link"), max_length=255, null=True, blank=True)
    twitter       = models.URLField(_("Twitter Link"), max_length=255, null=True, blank=True)
    linked_in     = models.URLField(_("Linked In Link"), max_length=255, null=True, blank=True)
    active        = models.BooleanField(_("Est actif"), default=True)
    timestamp     = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated       = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.user.email

    class Meta:
        ordering = ('-timestamp',)










# SUPPLIER MODEL

class Supplier(models.Model):
    name            = models.CharField(_("Nom"), max_length=255, null=False, blank=False, unique=True)
    email           = models.EmailField(_("Email"), max_length=255, null=False, blank=False)
    phone           = models.CharField(_("Numéro de téléphone"), max_length=255, null=True, blank=True)
    country        = CountryField(_("Pays"), max_length=255, null=True, blank=True)
    city            = models.CharField(_("Ville"), max_length=255, null=True, blank=True)
    address         = models.CharField(_("Adresse"), max_length=255, null=True, blank=True)
    website         = models.URLField(_("Site Web"), max_length=255, null=True, blank=True)
    facebook_link   = models.URLField(_("Lien Facebook"), max_length=255, null=True, blank=True)
    twitter_link    = models.URLField(_("Lien Twitter"), max_length=255, null=True, blank=True)
    instagram_link  = models.URLField(_("Lien  Instagram"), max_length=255, null=True, blank=True)
    active          = models.BooleanField(_("Est actif"), default=True)
    timestamp       = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated         = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False, related_name="provider_created_by")
    
    def __str__(self):
        return self.name






# STOCK MODEL
class Stock(models.Model):
    supplier    = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True, related_name="supplier")
    quantity    = models.PositiveIntegerField(_("Quantité"), null=True, blank=True, default=1)
    total       = models.DecimalField(_("Total(cfa)"), decimal_places=2, max_digits=7, null=False, blank=False)
    description = models.TextField(_("Description"), null=False, blank=False)
    active      = models.BooleanField(_("Est actif"), default=True)
    timestamp   = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated     = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    
    def __str__(self):
        return self.supplier.name

    class Meta:
        ordering = ('-timestamp',)








# PRODUCT IMAGE MODEL
class ProductImage(models.Model):
    file       = models.FileField(_("Fichier(pdf,image)"), upload_to="Product/%Y/%m/%d/", null=False, blank=False)
    name       = models.CharField(_("Nom"), max_length=255, null=False, blank=False, unique=True)
    active     = models.BooleanField(_("Est actif"), default=True)
    timestamp  = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated    = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-timestamp',)







# PRODUCT CATEGORY MODEL

class ProductCategory(models.Model):
    name       = models.CharField(_("Nom"), max_length=255, null=False, blank=False, unique=True)
    active     = models.BooleanField(_("Est actif"), default=True)
    timestamp  = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated    = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    slug       = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-timestamp',)










# PRODUCT MODEL

class Product(models.Model):
    category      = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name="product_Image")
    stock         = models.ForeignKey(Stock, on_delete=models.SET_NULL, blank=True, null=True, related_name="stock")
    name          = models.CharField(_("Nom"), max_length=255, null=False, blank=False, unique=True)
    unity_price   = models.DecimalField(_("Prix Unitaire"), decimal_places=2, max_digits=7, null=True, blank=True)
    quantity    = models.PositiveIntegerField(_("Quantité"), null=True, blank=True, default=1)
    discount      = models.DecimalField(_("Reduction"), decimal_places=2, max_digits=15, null=False, blank=False)
    product_image = models.ForeignKey(ProductImage, on_delete=models.SET_NULL, blank=True, null=True, related_name="product_category")
    brand_name    = models.CharField(_("Nom Commercial"), max_length=255, null=False, blank=False, unique=True)
    genetic_name  = models.CharField(_("Nom Générique"), max_length=255, null=False, blank=False, unique=True)
    description   = models.TextField(_("Description"), null=False, blank=False)
    active        = models.BooleanField(_("Est actif"), default=True)
    timestamp     = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated       = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    slug          = models.SlugField(_("Slug"), max_length=255, null=True, blank=True, editable=False, unique=False)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-timestamp',)
        









# SALE MODEL

class Sale(models.Model):
    reference  = models.CharField(_("Reference"), max_length=255, null=False, blank=False, unique=True)
    product    = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, related_name="product")
    quantity   = models.DecimalField(_("Quantité"), decimal_places=2, max_digits=15, null=False, blank=False)
    total      = models.DecimalField(_("Total"), decimal_places=2, max_digits=15, null=False, blank=False)
    recu       = models.FileField(_("Fichier(pdf,image)"), upload_to="Recu/%Y/%m/%d/", null=False, blank=False)
    active     = models.BooleanField(_("Est actif"), default=True)
    timestamp  = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated    = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-timestamp',)









# APPOINTMENT SYMPTOM MODEL
class AppointmentSymptom(models.Model):
    name       = models.CharField(_("Nom"), max_length=255, null=False, blank=False, unique=True)
    active     = models.BooleanField(_("Est actif"), default=True)
    timestamp  = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated    = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-timestamp',)











# APPOINTMENT MODEL

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('Masculin', 'Masculin'),
        ('Feminin', 'Feminin'),
    )
    first_name   = models.CharField(_("First Name"), max_length=255, null=False, blank=False)
    last_name    = models.CharField(_("Last Name"), max_length=255, null=False, blank=False)
    email        = models.EmailField(_("Email"), max_length=255, null=False, blank=False)
    phone        = models.CharField(_("Numéro de téléphone"), max_length=255, null=True, blank=True)
    subject      = models.CharField(_("Sujet"), max_length=255, null=False, blank=False, unique=True)
    gender       = models.CharField(_("Options"), max_length=100, choices=STATUS_CHOICES, null=False, blank=False)
    # 👉 try to see the field age 🔥
    age          = models.IntegerField(_("Age"),  null=False, blank=False)
    hour         = models.DateTimeField(_("Horaire Rv"), auto_now_add=True, auto_now=False)
    date         = models.DateField(_("Date de RV"), blank=False, null=False)
    description  = models.TextField(_("Description"), null=False, blank=False)
    active     = models.BooleanField(_("Est actif"), default=True)
    timestamp  = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated    = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-timestamp',)








# APPOINTMENT PRESCRIPTION MODEL

class AppointmentPrescription(models.Model):
    product_name        = models.CharField(_("Nom du Produit"), max_length=255, null=False, blank=False, unique=True)
    quantity            = models.DecimalField(_("Quantité"), decimal_places=2, max_digits=15, null=False, blank=False)
    heart_rate          = models.DecimalField(_("Pression Cardiac"), decimal_places=2, max_digits=15, null=False, blank=False)
    weight              = models.DecimalField(_("Poids"), decimal_places=2, max_digits=15, null=False, blank=False)
    blood_rate          = models.DecimalField(_("Taux Sanguin"), decimal_places=2, max_digits=15, null=False, blank=False)
    body_temperature    = models.DecimalField(_("Temperature Corporelle"), decimal_places=2, max_digits=15, null=False, blank=False)
    glucose_level       = models.DecimalField(_("Taux de Glucose"), decimal_places=2, max_digits=15, null=False, blank=False)
    blood_pressure      = models.DecimalField(_("Pression Sanguine"), decimal_places=2, max_digits=15, null=False, blank=False)
    day                 = models.DateField(_("Jour de RV"), blank=False, null=False)
    appointment_symptom = models.TextField(_("Symptome Patient"), null=False, blank=False)
    morning_times       = models.BooleanField(_("Matin"), default=False)
    afternoon_times     = models.BooleanField(_("Apres Midi"), default=False)
    evening_times       = models.BooleanField(_("Soir"), default=True)
    night_times         = models.BooleanField(_("Nuit"), default=True)
    appointment         = models.ForeignKey(Appointment, on_delete=models.SET_NULL, blank=True, null=True, related_name="product")
    price               = models.DecimalField(_("Prix"), decimal_places=2, max_digits=15, null=False, blank=False)
    by                  = models.CharField(_("Nom du Pharmacien(e)"), max_length=255, null=False, blank=False, unique=True)
    active              = models.BooleanField(_("Est actif"), default=True)
    timestamp           = models.DateTimeField(_("Créé le"), auto_now_add=True, auto_now=False)
    updated             = models.DateTimeField(_("Modifié le"), auto_now_add=False, auto_now=True)
    
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-timestamp',)





