from django.core.management.base import BaseCommand
from denuncias_service.models import Denuncia
from users_service.models import User
from faker import Faker
import random
from decimal import Decimal

fake = Faker('es_ES')

class Command(BaseCommand):
    help = 'Genera 500 denuncias de prueba con coordenadas reales de Perú'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=500,
            help='Número de denuncias a crear (por defecto: 500)'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR('No hay usuarios en la base de datos. Ejecuta primero: python manage.py create_test_users'))
            return
        
        coordenadas_reales = [
            # Lima - Zona Centro
            (-12.046374, -77.042793, 'Lima', 'Lima Cercado'),
            (-12.058219, -77.036133, 'Lima', 'Lima Cercado'),
            (-12.063487, -77.034929, 'Lima', 'Lima Cercado'),
            
            # Lima - Miraflores
            (-12.119180, -77.030114, 'Lima', 'Miraflores'),
            (-12.121951, -77.029822, 'Lima', 'Miraflores'),
            (-12.123456, -77.031234, 'Lima', 'Miraflores'),
            (-12.117890, -77.028765, 'Lima', 'Miraflores'),
            (-12.125678, -77.032456, 'Lima', 'Miraflores'),
            
            # Lima - San Isidro
            (-12.095644, -77.035751, 'Lima', 'San Isidro'),
            (-12.098765, -77.037890, 'Lima', 'San Isidro'),
            (-12.093456, -77.034567, 'Lima', 'San Isidro'),
            
            # Lima - Surco
            (-12.134567, -76.994321, 'Lima', 'Surco'),
            (-12.138901, -76.996789, 'Lima', 'Surco'),
            (-12.132345, -76.992345, 'Lima', 'Surco'),
            
            # Lima - La Molina
            (-12.082345, -76.940567, 'Lima', 'La Molina'),
            (-12.079876, -76.943210, 'Lima', 'La Molina'),
            
            # Lima - San Juan de Lurigancho (zona con más población)
            (-11.993456, -77.012345, 'Lima', 'San Juan de Lurigancho'),
            (-11.989876, -77.015678, 'Lima', 'San Juan de Lurigancho'),
            (-11.996543, -77.009876, 'Lima', 'San Juan de Lurigancho'),
            (-11.991234, -77.013456, 'Lima', 'San Juan de Lurigancho'),
            
            # Lima - Villa El Salvador
            (-12.213456, -76.934567, 'Lima', 'Villa El Salvador'),
            (-12.219876, -76.938901, 'Lima', 'Villa El Salvador'),
            
            # Lima - Callao (zona portuaria - alta incidencia)
            (-12.056321, -77.118765, 'Callao', 'Callao'),
            (-12.051234, -77.121234, 'Callao', 'Callao'),
            (-12.059876, -77.115678, 'Callao', 'Callao'),
            (-12.054321, -77.119876, 'Callao', 'Callao'),
            
            # Lima - Los Olivos
            (-11.971234, -77.068901, 'Lima', 'Los Olivos'),
            (-11.975678, -77.065432, 'Lima', 'Los Olivos'),
            
            # Lima - Comas
            (-11.938765, -77.041234, 'Lima', 'Comas'),
            (-11.942345, -77.044567, 'Lima', 'Comas'),
            
            # Arequipa - Centro
            (-16.398901, -71.537234, 'Arequipa', 'Cercado'),
            (-16.402345, -71.534567, 'Arequipa', 'Cercado'),
            (-16.396543, -71.539876, 'Arequipa', 'Cayma'),
            
            # Cusco - Centro Histórico
            (-13.516543, -71.978765, 'Cusco', 'Cusco'),
            (-13.518901, -71.976432, 'Cusco', 'Cusco'),
            (-13.514321, -71.980123, 'Cusco', 'Wanchaq'),
            
            # Trujillo - Centro
            (-8.109876, -79.030567, 'La Libertad', 'Trujillo'),
            (-8.113456, -79.027890, 'La Libertad', 'Trujillo'),
            (-8.107654, -79.032345, 'La Libertad', 'Victor Larco'),
            
            # Piura - Centro
            (-5.194567, -80.632109, 'Piura', 'Piura'),
            (-5.197890, -80.629876, 'Piura', 'Piura'),
            
            # Chiclayo
            (-6.771234, -79.838901, 'Lambayeque', 'Chiclayo'),
            (-6.774567, -79.836543, 'Lambayeque', 'Chiclayo'),
            
            # Iquitos
            (-3.749876, -73.250123, 'Loreto', 'Iquitos'),
            (-3.746543, -73.253456, 'Loreto', 'Iquitos'),
        ]
        
        tipos_denuncias = [
            'accident', 'theft', 'assault', 'domestic_violence', 'fraud',
            'missing_person', 'vandalism', 'drug_trafficking', 'homicide',
            'harassment', 'cybercrime', 'sexual_abuse', 'weapon_possession',
            'public_disturbance', 'child_abuse', 'animal_abuse',
            'property_dispute', 'corruption', 'kidnapping', 'other'
        ]
        
        tipos_comunes = ['theft', 'assault', 'vandalism', 'harassment', 'fraud', 'accident']
        
        estados = ['Pending', 'In Progress', 'Resolved']
        
        descripciones_por_tipo = {
            'theft': [
                'Se observó un robo en la vía pública',
                'Hurto de pertenencias en transporte público',
                'Robo a mano armada en establecimiento comercial',
                'Sustracción de vehículo estacionado',
                'Robo de celular en la calle'
            ],
            'assault': [
                'Agresión física entre personas',
                'Pelea callejera con lesiones',
                'Ataque con arma blanca',
                'Agresión en local público'
            ],
            'vandalism': [
                'Daños a propiedad privada',
                'Grafitis en pared de vivienda',
                'Rotura de luna de vehículo',
                'Destrucción de mobiliario urbano'
            ],
            'harassment': [
                'Acoso verbal en la calle',
                'Amenazas telefónicas',
                'Hostigamiento por redes sociales',
                'Seguimiento intimidatorio'
            ],
            'fraud': [
                'Estafa mediante llamada telefónica',
                'Fraude en compra online',
                'Engaño con falsa oferta laboral',
                'Clonación de tarjeta bancaria'
            ],
            'accident': [
                'Choque vehicular en intersección',
                'Atropello de peatón',
                'Accidente de tránsito con daños materiales',
                'Colisión entre vehículos'
            ],
            'domestic_violence': [
                'Violencia física en el hogar',
                'Agresión psicológica familiar',
                'Violencia contra la pareja'
            ],
            'drug_trafficking': [
                'Venta de sustancias ilegales',
                'Microcomerialización de drogas',
                'Consumo en vía pública'
            ],
        }
        
        self.stdout.write(self.style.WARNING(f'Creando {count} denuncias...'))
        
        created_denuncias = 0
        for i in range(count):
            try:
                user = random.choice(users)
                
                if random.random() < 0.7:
                    tipo = random.choice(tipos_comunes)
                else:
                    tipo = random.choice(tipos_denuncias)

                coord_base = random.choice(coordenadas_reales)
                
                if random.random() < 0.6:
                    lat = Decimal(str(coord_base[0]))
                    lon = Decimal(str(coord_base[1]))
                else:
                    variacion = random.uniform(0.001, 0.005)
                    lat = Decimal(str(coord_base[0] + random.uniform(-variacion, variacion)))
                    lon = Decimal(str(coord_base[1] + random.uniform(-variacion, variacion)))
                
                region = coord_base[2]
                distrito = coord_base[3]
                
                if tipo in descripciones_por_tipo:
                    desc_base = random.choice(descripciones_por_tipo[tipo])
                else:
                    desc_base = f'Incidente de tipo {tipo}'
                
                descripcion = f"{desc_base}. Ocurrido en {distrito}, {region}. {fake.sentence()}"
                
                if random.random() < 0.5:
                    estado = 'Pending'
                elif random.random() < 0.8:
                    estado = 'In Progress'
                else:
                    estado = 'Resolved'
                
                denuncia = Denuncia.objects.create(
                    user=user,
                    description=descripcion,
                    district=distrito,
                    region=region,
                    lat=lat,
                    lon=lon,
                    _type=tipo,
                    status=estado
                )
                
                created_denuncias += 1
                
                if (i + 1) % 50 == 0:
                    self.stdout.write(self.style.SUCCESS(f'  Creadas {i + 1}/{count} denuncias...'))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  Error creando denuncia {i + 1}: {str(e)}'))
                continue
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Se crearon exitosamente {created_denuncias} denuncias'))
        
        total = Denuncia.objects.count()
        por_estado = {}
        for estado in estados:
            count = Denuncia.objects.filter(status=estado).count()
            por_estado[estado] = count
        
        self.stdout.write(self.style.SUCCESS(f'\nEstadísticas:'))
        self.stdout.write(f'  Total denuncias en BD: {total}')
        for estado, count in por_estado.items():
            self.stdout.write(f'  {estado}: {count}')
