from django.contrib import admin
from .models import Ad, Profile, TargetAd


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_phone', 'working', 'is_priority')

    def user_phone(self, obj):
        return obj.user.username

    user_phone.short_description = 'Телефон'


admin.site.register(Ad)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(TargetAd)

# Register your models here.
