from django.contrib import admin
from .models import Ad, Profile, TargetAd


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_phone', 'is_priority')

    fields = ('name', 'is_priority')

    def user_phone(self, obj):
        return obj.user.username

    user_phone.short_description = 'Телефон'

    def has_add_permission(self, request):
        return False


admin.site.register(Ad)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(TargetAd)

# Register your models here.
