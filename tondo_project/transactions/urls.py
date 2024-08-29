
from django.urls import path
from .views import (
    GetDetails,
    SaveDetails
)

urlpatterns = [
    path('get_details', GetDetails.as_view()),
    path('save_details', SaveDetails.as_view()),
]