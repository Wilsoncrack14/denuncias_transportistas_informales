from django.urls import path
from .views import DashboardStatsView, DashboardUserStatsView

urlpatterns = [
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('dashboard/my-stats/', DashboardUserStatsView.as_view(), name='dashboard-user-stats'),
]
