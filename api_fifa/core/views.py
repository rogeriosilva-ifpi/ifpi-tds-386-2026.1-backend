from django.shortcuts import render
from .models import Selecao, Sede
from rest_framework import viewsets
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from .serializers import SelecaoSerializer, SedeSerializer


def index(request):
    contexto = {
        'total_selecoes': Selecao.objects.count(),
        'total_sedes':    Sede.objects.count(),
    }
    return render(request, 'index.html', contexto)


# put your views here
def listar_selecoes(request):
    # Busca as selecoes no BD
    selecoes = Selecao.objects.all()

    # Monta os dados(contexto) para o template
    contexto = {'selecoes': selecoes}

    # Indica qual o template e envia os dados para ele
    return render(request, 'selecoes.html', contexto)


def listar_sedes(request):
    return render(request, 'sedes.html', {'sedes': Sede.objects.all()})


# API Views

class SelecaoModelViewSet(viewsets.ModelViewSet):
    queryset = Selecao.objects.all()
    serializer_class = SelecaoSerializer


class SedeCreateListView(views.APIView):

    # GET /api/sedes
    def get(self, request):
        sedes = Sede.objects.all()
        serializer = SedeSerializer(sedes, many=True)
        return Response(serializer.data)
    
    # POST /api/sedes
    def post(self, request):
        serializer = SedeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class SedeDetailUpdateDeleteView(views.APIView):
    
    def get(self, request, id):
        sede = Sede.objects.get(pk=id)
        serializer = SedeSerializer(sede)
        return Response(serializer.data)

    def put(self, request, id):
        sede = Sede.objects.get(pk=id)
        serializer = SedeSerializer(sede, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        sede = Sede.objects.get(pk=id)
        sede.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)