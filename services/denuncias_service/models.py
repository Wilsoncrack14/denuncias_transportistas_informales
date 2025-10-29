from django.db import models
from core.regions import REGION_CHOICES

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('In Progress', 'In Progress'),
    ('Resolved', 'Resolved'),
]

TYPE_CHOICES = [
    ('accident', 'Accidente de tránsito'),
    ('theft', 'Robo o hurto'),
    ('assault', 'Agresión o violencia física'),
    ('domestic_violence', 'Violencia familiar o de pareja'),
    ('fraud', 'Estafa o fraude'),
    ('missing_person', 'Persona desaparecida'),
    ('vandalism', 'Vandalismo o daños a la propiedad'),
    ('drug_trafficking', 'Tráfico o consumo de drogas'),
    ('homicide', 'Homicidio o intento de homicidio'),
    ('harassment', 'Acoso o amenazas'),
    ('cybercrime', 'Delito informático'),
    ('sexual_abuse', 'Abuso o acoso sexual'),
    ('weapon_possession', 'Tenencia ilegal de armas'),
    ('public_disturbance', 'Alteración del orden público'),
    ('child_abuse', 'Maltrato infantil'),
    ('animal_abuse', 'Maltrato animal'),
    ('property_dispute', 'Conflicto por propiedad'),
    ('corruption', 'Corrupción o soborno'),
    ('kidnapping', 'Secuestro o tentativa'),
    ('other', 'Otro tipo de denuncia'),
]

class Denuncia(models.Model):
    user = models.ForeignKey('users_service.User', on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    district = models.CharField(max_length=100)
    region = models.CharField(max_length=100, choices=REGION_CHOICES)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    _type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    status = models.CharField(max_length=50, default='Pending', choices=STATUS_CHOICES)

    def __str__(self):
        return self.description[:50]


class DenunciaEvidencia(models.Model):
    incident = models.ForeignKey(Denuncia, on_delete=models.CASCADE, related_name='evidence')
    file = models.FileField(upload_to='denuncias/evidencias/%Y/%m/%d/')
    file_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_type} - {self.incident.id}"

    class Meta:
        verbose_name = 'Evidence'
        verbose_name_plural = 'Evidence'