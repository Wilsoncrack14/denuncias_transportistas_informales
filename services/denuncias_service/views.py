from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from core.pagination import CustomPageNumberPagination
from .models import Denuncia, DenunciaEvidencia
from .serializers import (
    DenunciaSerializer,
    DenunciaCreateUpdateSerializer,
    DenunciaListSerializer,
    DenunciaStatusUpdateSerializer,
    DenunciaEvidenciaSerializer
)
from .permissions import IsOwnerOrSuperUser, IsSuperUserOrReadOnly
from users_service.permissions import IsSuperUser

class DenunciaCreateView(generics.CreateAPIView):
    serializer_class = DenunciaCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        denuncia = Denuncia.objects.get(id=serializer.instance.id)
        response_serializer = DenunciaSerializer(denuncia, context={'request': request})
        
        return Response({
            'message': 'Denuncia creada exitosamente',
            'denuncia': response_serializer.data
        }, status=status.HTTP_201_CREATED)

class DenunciaListView(generics.ListAPIView):
    serializer_class = DenunciaListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_superuser:
            queryset = Denuncia.objects.all()
        else:
            queryset = Denuncia.objects.filter(user=user)
        
        queryset = queryset.select_related('user').order_by('-created_at')
        
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(description__icontains=search) |
                Q(district__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search)
            )
        
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        type_filter = self.request.query_params.get('type', None)
        if type_filter:
            queryset = queryset.filter(_type=type_filter)
        
        region_filter = self.request.query_params.get('region', None)
        if region_filter:
            queryset = queryset.filter(region__icontains=region_filter)
        
        return queryset

class DenunciaDetailView(generics.RetrieveAPIView):
    queryset = Denuncia.objects.all()
    serializer_class = DenunciaSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperUser]
    lookup_field = 'pk'

class DenunciaUpdateView(generics.UpdateAPIView):
    queryset = Denuncia.objects.all()
    serializer_class = DenunciaCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperUser]
    lookup_field = 'pk'
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        response_serializer = DenunciaSerializer(instance, context={'request': request})
        
        return Response({
            'message': 'Denuncia actualizada exitosamente',
            'denuncia': response_serializer.data
        })
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

class DenunciaDeleteView(generics.DestroyAPIView):
    queryset = Denuncia.objects.all()
    serializer_class = DenunciaSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperUser]
    lookup_field = 'pk'
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        denuncia_id = instance.id
        denuncia_type = instance.get__type_display()
        
        self.perform_destroy(instance)
        
        return Response({
            'message': f'Denuncia #{denuncia_id} de tipo "{denuncia_type}" eliminada exitosamente.'
        }, status=status.HTTP_200_OK)

class DenunciaStatusUpdateView(generics.UpdateAPIView):
    queryset = Denuncia.objects.all()
    serializer_class = DenunciaStatusUpdateSerializer
    permission_classes = [IsAuthenticated, IsSuperUser]
    lookup_field = 'pk'
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        response_serializer = DenunciaSerializer(instance, context={'request': request})
        
        return Response({
            'message': f'Estado de la denuncia actualizado a "{instance.get_status_display()}"',
            'denuncia': response_serializer.data
        })

class MyDenunciasStatsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        if user.is_superuser:
            queryset = Denuncia.objects.all()
        else:
            queryset = Denuncia.objects.filter(user=user)
        
        total = queryset.count()
        pending = queryset.filter(status='Pending').count()
        in_progress = queryset.filter(status='In Progress').count()
        resolved = queryset.filter(status='Resolved').count()
        
        types_count = {}
        for choice in queryset.values_list('_type', flat=True).distinct():
            types_count[choice] = queryset.filter(_type=choice).count()
        
        return Response({
            'total_denuncias': total,
            'por_estado': {
                'pending': pending,
                'in_progress': in_progress,
                'resolved': resolved
            },
            'por_tipo': types_count
        })

class DenunciaHeatmapView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        if user.is_superuser:
            queryset = Denuncia.objects.all()
        else:
            queryset = Denuncia.objects.filter(user=user)
        
        queryset = queryset.filter(
            lat__isnull=False,
            lon__isnull=False
        ).exclude(
            lat=0,
            lon=0
        )
        
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        type_filter = self.request.query_params.get('type', None)
        if type_filter:
            queryset = queryset.filter(_type=type_filter)
        
        region_filter = self.request.query_params.get('region', None)
        if region_filter:
            queryset = queryset.filter(region__icontains=region_filter)
        
        all_denuncias = list(queryset)
        denuncias = []
        
        proximity_radius = 0.01
        
        for denuncia in all_denuncias:
            lon = float(denuncia.lon)
            lat = float(denuncia.lat)
            
            peso = 1.0
            for other in all_denuncias:
                if other.id != denuncia.id:
                    other_lon = float(other.lon)
                    other_lat = float(other.lat)
                
                    dist_lon = abs(lon - other_lon)
                    dist_lat = abs(lat - other_lat)
                    
                    if dist_lon <= proximity_radius and dist_lat <= proximity_radius:
                        distance = (dist_lon ** 2 + dist_lat ** 2) ** 0.5
                        if distance < proximity_radius:
                            peso += (1 - (distance / proximity_radius)) * 0.5
            
            denuncias.append({
                'lon': lon,
                'lat': lat,
                'peso': round(peso, 2),
                'id': denuncia.id,
                'type': denuncia._type,
                'type_display': denuncia.get__type_display(),
                'status': denuncia.status,
                'region': denuncia.region,
                'district': denuncia.district,
                'created_at': denuncia.created_at.isoformat()
            })
        
        if denuncias:
            avg_lon = sum(d['lon'] for d in denuncias) / len(denuncias)
            avg_lat = sum(d['lat'] for d in denuncias) / len(denuncias)
            center = {'lon': avg_lon, 'lat': avg_lat}
        else:
            center = {'lon': -75.0152, 'lat': -9.1899}
        
        return Response({
            'denuncias': denuncias,
            'total': len(denuncias),
            'center': center
        })


class DenunciaEvidenciaUploadView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrSuperUser]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, pk):
        try:
            denuncia = Denuncia.objects.get(pk=pk)
            self.check_object_permissions(request, denuncia)
            
            file = request.FILES.get('file')
            if not file:
                return Response({'error': 'No se proporcionó ningún archivo'}, status=status.HTTP_400_BAD_REQUEST)
            
            file_extension = file.name.split('.')[-1].lower()
            image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            video_extensions = ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm']
            
            if file_extension in image_extensions:
                file_type = 'image'
            elif file_extension in video_extensions:
                file_type = 'video'
            else:
                return Response({'error': 'Formato de archivo no soportado'}, status=status.HTTP_400_BAD_REQUEST)
            
            evidence = DenunciaEvidencia.objects.create(
                incident=denuncia,
                file=file,
                file_type=file_type
            )
            
            serializer = DenunciaEvidenciaSerializer(evidence, context={'request': request})
            return Response({
                'message': 'Evidencia subida exitosamente',
                'evidence': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Denuncia.DoesNotExist:
            return Response({'error': 'Denuncia no encontrada'}, status=status.HTTP_404_NOT_FOUND)


class DenunciaEvidenciaDeleteView(generics.DestroyAPIView):
    queryset = DenunciaEvidencia.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return DenunciaEvidencia.objects.all()
        return DenunciaEvidencia.objects.filter(incident__user=user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.file.delete() 
        self.perform_destroy(instance)
        
        return Response({
            'message': 'Evidencia eliminada exitosamente'
        }, status=status.HTTP_200_OK)
