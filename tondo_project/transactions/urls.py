
from django.urls import path
from .views import (
    GetDetails,
    SaveDetaile
)

urlpatterns = [
    path('get_details/', GetDetails.as_view()),
    path('save_details/', SaveDetaile.as_view()),
]