from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ClimateDataset

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'is_staff', 'is_active')}
        ),
    )

    # Add Custom CSS
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

# Register CustomUser model with the custom admin view
admin.site.register(CustomUser, CustomUserAdmin)

# Register ClimateDataset model (example)
class ClimateDatasetAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded_by', 'upload_date', 'file')
    list_filter = ('upload_date', 'uploaded_by')
    search_fields = ('name', 'uploaded_by__username')
    ordering = ('-upload_date',)

admin.site.register(ClimateDataset, ClimateDatasetAdmin)
