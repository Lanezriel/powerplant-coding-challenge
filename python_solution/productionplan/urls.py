from django.urls import path
from .views import ProductionPlan

urlpatterns = [
    path('', ProductionPlan.as_view()),
]