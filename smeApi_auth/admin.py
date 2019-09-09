from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from smeApi_auth.models import User, Profile, ApiKey


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0
    fields = ('id', )
    readonly_fields = fields


@admin.register(User)
class _UserAdmin(UserAdmin):
    list_display = ('id', 'email', 'name', )
    search_fields = ('eamil', 'firstname', )
    readonly_fields = ('create_date', 'modify_date', )
    inlines = [
        ProfileInline,
    ]

    def name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'create_date', )
    raw_id_fields = ['user']
    readonly_fields = ('create_date', 'modify_date', )
    search_fields = ['user', ]

    def get_queryset(self, request):
        return super(ProfileAdmin, self).get_queryset(
            request).order_by('-create_date')


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'user', 'create_date', 'email', )
    raw_id_fields = ['user']
    readonly_fields = ('key', 'create_date', 'modify_date', )
    search_fields = ['user', ]

    def get_queryset(self, request):
        return super(ApiKeyAdmin, self).get_queryset(
            request).order_by('-create_date')

    def email(self, obj):
        return obj.user.email
