from django.shortcuts import render
from .models import Selecao, Sede


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
