from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import RegistrationForm, UserChangeForm
from .models import ActivationToken, BlockedUser, Profile, ResetToken, User


def block_users(modeladmin, request, queryset):
    for user in queryset:
        user.block()


block_users.short_description = 'Block selected users'


class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = RegistrationForm
    form = UserChangeForm
    model = User
    actions = (block_users,)
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
admin.site.register(ResetToken)
admin.site.register(Profile)
admin.site.register(BlockedUser)
