from django.contrib import admin

from zvonilka_test_phones.models import PhoneTest, TestCall


class TestCallInline(admin.TabularInline):
    model = TestCall
    extra = 0
    can_delete = False

    readonly_fields = ('person_name', 'phone', 'duration')
    fields = readonly_fields

    verbose_name_plural = 'Звонки'

    def person_name(self, obj: TestCall):
        return obj.person.name

    person_name.short_description = 'Имя'

    def phone(self, obj: TestCall):
        return obj.person.user.username

    phone.short_description = 'Номер'

    def duration(self, obj: TestCall):
        if not obj.date_done:
            return "✖"
        time = obj.date_done - obj.created_at
        return f"✔ {round(time.total_seconds(), 2)}s"

    duration.short_description = 'Время'

    # def get_fields(self, request, obj=None):
    #     return self.readonly_fields


class PhoneTestAdmin(admin.ModelAdmin):
    fields = ('test_phone',)
    inlines = (TestCallInline,)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ('test_phone', )
        return ()

    def get_inlines(self, request, obj):
        if obj is not None:
            return (TestCallInline, )
        return ()

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False

        return super().changeform_view(request, object_id, extra_context=extra_context)


# Register your models here.
admin.site.register(PhoneTest, PhoneTestAdmin)
admin.site.register(TestCall)
