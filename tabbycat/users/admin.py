from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _


# ==============================================================================
# Authentication and Authorization
# ==============================================================================

admin.site.unregister(Group) # No need to show groups


class CustomUserLabelsMixin():
    def __init__(self, *args, **kwargs):
        super(CustomUserLabelsMixin, self).__init__(*args, **kwargs)
        self.fields['is_staff'].help_text = _("Users with Staff status can"
            " view and edit the Edit Database area. This is potentially "
            "dangerous and should be reserved for the actual Tab Director(s).")
        self.fields['is_superuser'].help_text = _("Superusers have full "
            "access all areas of Tabbycat necessary to run a tournament. Users "
            "who are not Superusers are still able to perform data-entry tasks "
            "such as adding results and feedback but can't access confidential "
            "areas such as the Breaks and Feedback sections. Members of "
            "the adjudication core are generally given Superuser status if "
            "they know what they are doing.")


class UserChangeFormFormExtended(CustomUserLabelsMixin, UserChangeForm):
    pass


class UserCreationFormExtended(CustomUserLabelsMixin, UserCreationForm):
    pass


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')

    fieldsets = ( # Hide groups and user permission fields
        ('Personal info', {'fields': ('username', 'email', 'password')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = ( # Set permissions when creating
        (None, {
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_superuser')
        }),
    )

    add_form = UserCreationFormExtended
    form = UserChangeFormFormExtended


User = get_user_model()
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
