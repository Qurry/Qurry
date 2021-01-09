from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User, ActivationToken, Profile


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('username', 'is_superuser', 'is_active',)
    list_filter = ('email', 'username', 'is_superuser', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {
            'fields': ('is_superuser', 'is_active', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'is_superuser', 'is_active')}
         ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    inlines = (ProfileInline,)


admin.site.register(User, UserAdmin)
admin.site.register(ActivationToken)
admin.site.register(Profile)
