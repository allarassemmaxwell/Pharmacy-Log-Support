# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import *


admin.site.site_header = "Open data"


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'role', 'first_name', 'last_name', 'i_agree', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'i_agree', 'role', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'is_active', 'role', 'is_staff')
    ordering = ('email',)
    readonly_fields = ('last_login', 'i_agree',)








# # PROFILE ADMIN
class ProfileAdmin(admin.ModelAdmin):
    date_hierarchy      = 'timestamp'
    list_display        = ['user', 'phone', 'timestamp', 'updated']
    list_display_links  = ['user',]
    list_filter         = ['user']
    search_fields       = ['user']
    list_per_page       = 50
    class Meta:
        model = Profile
admin.site.register(Profile, ProfileAdmin)





# # PRODUCT CATEGORY ADMIN
class ProductCategoryAdmin(admin.ModelAdmin):
    date_hierarchy      = 'timestamp'
    list_display        = ['name', 'timestamp', 'updated']
    list_display_links  = ['name',]
    list_filter         = ['name']
    search_fields       = ['name']
    list_per_page       = 50
    class Meta:
        model = ProductCategory
admin.site.register(ProductCategory, ProductCategoryAdmin)




#  PRODUCT IMAGE ADMIN
class ProductImageAdmin(admin.ModelAdmin):
    date_hierarchy      = 'timestamp'
    list_display        = ['name', 'timestamp', 'updated']
    list_display_links  = ['name',]
    list_filter         = ['name']
    search_fields       = ['name']
    list_per_page       = 50
    class Meta:
        model = ProductImage
admin.site.register(ProductImage, ProductImageAdmin)











# # LANGUAGE ADMIN
class ProductAdmin(admin.ModelAdmin):
    date_hierarchy      = 'timestamp'
    list_display        = ['name', 'category', 'timestamp', 'updated']
    list_display_links  = ['name',]
    list_filter         = ['name']
    search_fields       = ['name']
    list_per_page       = 50
    class Meta:
        model = Product
admin.site.register(Product, ProductAdmin)





