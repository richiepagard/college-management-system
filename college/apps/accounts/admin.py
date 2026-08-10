from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.accounts.models import User, UserProfile
from apps.accounts.admin_forms import UserCreationForm, UserChangeForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["phone_number", "email", "is_admin"]
    list_filter = ["is_active", "is_admin", "is_staff", "is_superuser", "groups"]
    search_fields = ["phone_number", "email"]
    ordering = ["phone_number", "email"]
    filter_horizontal = ["groups", "user_permissions"]
    list_per_page = 30

    fieldsets = (
        [_("Personal Information"),
            {
                "fields": ("phone_number", "email", "password")
            }
        ],
        [_("Permissions"),
            {
                "classes": ("collapse",),
                "fields": (
                    "is_active", "is_admin", "is_staff",
                    "is_superuser", "groups", "user_permissions"
                )
            }
        ],
    )

    add_fieldsets = (
        [_("Personal Information"),
            {
                "fields": ("phone_number", "email", "password1", "password2")
            }
        ],
        [_("Permissions"),
            {
                "classes": ("collapse",),
                "fields": (
                    "is_active", "is_admin", "is_staff", "is_superuser",
                    "groups", "user_permissions"
                )
            }
        ],
    )

    def get_form(self, request, obj=None, **kwargs):
        """
        Customizes the user form based on the user's permissions.

        Checks whether the logged-in user is a superuser. If the user is not a superuser, 
        the 'is_superuser' field in the form will be disabled, preventing any changes 
        to this attribute.
        """
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True

        return form


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "username", "firstname", "lastname"]
    list_filter = ["created_at", "updated_at", "birth_date", "is_active"]
    search_fields = ["username", "firstname", "lastname"]
    readonly_fields = ["created_at", "updated_at"]
    raw_id_fields = ["user"]
    list_per_page = 30

    fieldsets = (
        [_("Personal Information"),
            {
                "fields": ("user", "username", "national_code", "birth_date")
            }
        ],
        [_("Extra Information"),
            {
                "classes": ("collapse",),
                "fields": ("firstname", "lastname", "is_active", "avatar_image")
            }
        ],
        [_("Dates Information"),
            {
                "classes": ("collapse",),
                "fields": ("created_at", "updated_at")
            }
        ]
    )
