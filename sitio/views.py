from sitio.forms import TmcForm
from django.shortcuts import render
from apisbif.sbif_tmc import TMC
import logging

logger = logging.getLogger(__name__)


def tmc_view(request):
    if request.method == 'POST':
        form = TmcForm(request.POST)
        tmc = TMC()
        tipo = ()
        valor = None
        monto = int(request.POST['monto'])
        cuotas = int(request.POST['cuotas'])
        month = request.POST['fecha'][3:5]
        year = request.POST['fecha'][6:]
        if cuotas == 13:
            tipo = '20', '23'
            if monto > 2000:
                tipo += '14', '22'
            else:
                tipo += '13', '24'
        elif cuotas <= 3:
            tipo = '12', '21'
            if monto > 5000:
                tipo += '11', '25'
            else:
                tipo += '10', '26'
        elif cuotas > 3:
            tipo = '12', '21'
            if monto <= 200:
                tipo += '7', '30', '33'
                if monto <= 100:
                    tipo += '4', '28'
                elif monto in range(101, 201):
                    tipo += '5', '31'
            else:
                tipo += '6', '32'
            if monto in range(0, 51):
                tipo += '45',
            elif monto in range(51, 201):
                tipo += '44',
            elif monto in range(201, 5001):
                tipo += '8', '27', '35'
            elif monto > 5000:
                tipo += '9', '29', '34'

        if tipo:
            try:
                response_tmc = tmc.get_tmc(year, month)
                for operacion in response_tmc.TMCs:
                    if operacion.Tipo in tipo:
                        valor = '{}%'.format(operacion.Valor)
            except Exception as e:
                logger.error('Error al obtener TMC. {}'.format(e))
                valor = 'Sin Información'
    else:
        valor = None
        form = TmcForm()
    return render(request, 'tmc.html', {'form': form, 'valor': valor})
