from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserAgreement


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, CustomUserAdmin)




@admin.register(UserAgreement)
class UserAgreementAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'agreed', 'agreed_at')
    list_display = ('user', 'agreed', 'agreed_at')
    # def has_add_permission(self, request):
    #     return False  # Prevent manual addition
    # def has_delete_permission(self, request, obj=None):
    #     return False  # Prevent deletion