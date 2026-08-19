from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["user", "user__profile", "student_code", "is_active"]
    list_filter = ["is_active", "created_at", "updated_at"]
    search_fields = [
        "user__phone_number",
        "user__email",
        "user__profile_fullname",
        "student_code"
    ]
    raw_id_fields = ["user"]
    readonly_fields = ["student_code", "created_at", "updated_at"]

    fieldsets = (
            [_("Personal Information"),
                {
                    "fields": ("user", "student_code")
                }
            ],
            [_("Extra Information"),
                {
                    "classes": ("collapse",),
                    "fields": ("is_active",)
                }
            ],
            [_("Dates Information"),
                {
                    "classes": ("collapse",),
                    "fields": ("created_at", "updated_at")
                }
            ]
        )
