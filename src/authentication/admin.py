from django.contrib import admin
from .forms import UserForm
from .models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if obj:
            kwargs['form'] = UserForm
        return super(UserAdmin, self).get_form(request, obj, **kwargs)
