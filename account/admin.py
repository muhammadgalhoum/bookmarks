from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Contact
from .forms import ContactCreationForm, ContactChangeForm, CustomUserCreationForm, CustomUserChangeForm

# Register your models here.


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    form = ContactChangeForm
    add_form = ContactCreationForm
    raw_id_fields = ("user_from", "user_to")
    list_display = ("user_from", "user_to", "created")
    list_filter = ('created',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_from', 'user_to'),
        }),
    )
    
    fieldsets = (
        (None, {'fields': ('user_from', 'user_to')}),
    )
    


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser
    # inlines = [ContactInline, FollowingInline, FollowersInline]

    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    prepopulated_fields = {'slug': ('username',)}
    ordering = ('username',)
    
    # Don't put the slug field here it will cause an error
    readonly_fields = ("uuid","last_login", "date_joined")

    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'slug', 'email', 'password1', 'password2'),
        }),
    )
    
    fieldsets = (
        (None, {'fields': ('username', 'slug', 'uuid', 'password')}),
        
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'photo')}),
        
        ('Permissions', {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        
        ('Important Dates', {
            'classes': ('collapse',),
            'fields': ('last_login', 'date_joined'),
        }),
    )
 
    
# Incase I want to add the Contact modle inside the CustomUser mode 

# class ContactInline(admin.TabularInline):
#     model = Contact
#     fk_name = "user_from"
#     extra = 1
#     fields = ("user_to", "created")
#     readonly_fields = ("created",)


# class FollowingInline(admin.TabularInline):
#     model = Contact
#     fk_name = "user_from"
#     verbose_name = "User I Follow"
#     verbose_name_plural = "Users I Follow"
#     extra = 1
#     fields = ("user_to", "created")
#     readonly_fields = ("created",)


# class FollowersInline(admin.TabularInline):
#     model = Contact
#     fk_name = "user_to"
#     verbose_name = "My Follower"
#     verbose_name_plural = "My Followers"
#     extra = 1
#     fields = ("user_from", "created")
#     readonly_fields = ("created",)
