from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'superadmin'
admin.site.site_title = 'Aiegent Superadmin'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/ttsgenerators/', include('ttsgenerators.urls')),
]
