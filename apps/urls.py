from django.urls import path, include

urlpatterns = [
    path('', include('apps.core.urls')),  # entry point to other project app urls
    path('', include('apps.workspace.urls')),
    path('', include('apps.access.urls')), 
]
