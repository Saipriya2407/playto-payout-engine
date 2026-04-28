# from django.contrib import admin
# from django.urls import path,include

# urlpatterns = [
#            path('admin/',admin.site.urls),
#            path('api/v1/',include('payouts.urls')),
# ]
from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('payouts.urls')),
]