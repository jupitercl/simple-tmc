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
        reajustable = request.POST.get("reajustable", None)
        cuotas = int(request.POST['cuotas'])
        month = request.POST['fecha'][3:5]
        year = request.POST['fecha'][6:]

        rangos_lte3 = {('11', '21'): [0, 5000],
                       ('10', '26'): [5001, float('inf')]}

        rangos_gt3 = {('45',): [0, 50],
                      ('4', '28'): [0, 100],
                      ('7', '30', '33'): [0, 200],
                      ('44',): [51, 200],
                      ('5', '31'): [101, 200],
                      ('8', '27', '35'): [201, 5000],
                      ('6', '32'): [201, float('inf')],
                      ('9', '29', '34'): [5001, float('inf')]}

        if reajustable:
            if cuotas > 12:
                tipo = '20', '23'
                if monto > 2000:
                    tipo += '14', '22'
                else:
                    tipo += '13', '24'
            else:
                tipo = '12', '21'
        elif cuotas <= 3:
            tipo = [tipos for tipos, (low, high) in rangos_lte3.items()
                    if low <= monto <= high]
            tipo = [i for sub in tipo for i in sub]
        else:
            tipo = [tipos for tipos, (low, high) in rangos_gt3.items()
                    if low <= monto <= high]
            tipo = [i for sub in tipo for i in sub]

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
