from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User, ActivationToken, Profile


class ProfileInline(admin.StackedInline):
    model = Profile

@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('username', 'is_superuser', 'is_active', 'last_login')
    list_filter = ('email', 'username', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('id', 'username', 'email', 'password')}),
        ('Permissions', {
            'fields': ('is_superuser', 'is_active', 'user_permissions')}),
    )
    readonly_fields = ('id',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'is_superuser', 'is_active')}
         ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    inlines = (ProfileInline,)

admin.site.register(ActivationToken)
admin.site.register(Profile)
