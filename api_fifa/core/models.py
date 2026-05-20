from django.db import models


GRUPO_CHOICES = (
    ('A', 'Grupo A'),
    ('B', 'Grupo B'),
    ('C', 'Grupo C'),
    ('D', 'Grupo D'),
    ('E', 'Grupo E'),
    ('F', 'Grupo F'),
    ('G', 'Grupo G'),
)

class Selecao(models.Model):
    pais = models.CharField(max_length=200, null=False, blank=False)
    tecnico = models.CharField(max_length=200, null=False, blank=False)
    grupo_fase1 = models.CharField(choices=GRUPO_CHOICES)


class Sede(models.Model):
    cidade = models.CharField(max_length=200, null=False, blank=False)
    estadio = models.CharField(max_length=200, null=False, blank=False)
