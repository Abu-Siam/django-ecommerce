from django.contrib import admin
from account.models import MyUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
class UserModelAdmin(BaseUserAdmin):
    # The forms to add and change user instances


    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('phone', 'name','address','is_admin')
    list_filter = ('is_admin','name','address')
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('name','address')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'name','address','password1', 'password2'),
        }),
    )
    search_fields = ('phone',)
    ordering = ('phone',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(MyUser, UserModelAdmin)
