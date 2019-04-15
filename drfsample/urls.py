from django.contrib import admin
from django.urls import path, include


handler500 = 'rest_framework.exceptions.server_error'
handler400 = 'rest_framework.exceptions.bad_request'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('movies.urls')),

]
