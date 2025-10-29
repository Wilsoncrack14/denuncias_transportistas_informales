from django.urls import path
from .views import (
    DenunciaCreateView,
    DenunciaListView,
    DenunciaDetailView,
    DenunciaUpdateView,
    DenunciaDeleteView,
    DenunciaStatusUpdateView,
    MyDenunciasStatsView,
    DenunciaHeatmapView,
    DenunciaEvidenciaUploadView,
    DenunciaEvidenciaDeleteView
)

urlpatterns = [
    path('incidents/', DenunciaListView.as_view(), name='denuncia-list'),
    path('incidents/create/', DenunciaCreateView.as_view(), name='denuncia-create'),
    path('incidents/<int:pk>/', DenunciaDetailView.as_view(), name='denuncia-detail'),
    path('incidents/<int:pk>/update/', DenunciaUpdateView.as_view(), name='denuncia-update'),
    path('incidents/<int:pk>/delete/', DenunciaDeleteView.as_view(), name='denuncia-delete'),
    path('incidents/<int:pk>/status/', DenunciaStatusUpdateView.as_view(), name='denuncia-status-update'),

    path('incidents/<int:pk>/evidences/upload/', DenunciaEvidenciaUploadView.as_view(), name='evidencia-upload'),
    path('incidents/evidence/<int:pk>/delete/', DenunciaEvidenciaDeleteView.as_view(), name='evidencia-delete'),

    path('incidents/stats/', MyDenunciasStatsView.as_view(), name='denuncia-stats'),
    path('incidents/heatmap/', DenunciaHeatmapView.as_view(), name='denuncia-heatmap'),
]
