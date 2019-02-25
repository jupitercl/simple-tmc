from django import forms

CUOTAS_CHOICES = (
    (1, "1 Cuota"),
    (2, "2 Cuotas"),
    (3, "3 Cuotas"),
    (4, "4 Cuotas"),
    (5, "5 Cuotas"),
    (6, "6 Cuotas"),
    (7, "7 Cuotas"),
    (8, "8 Cuotas"),
    (9, "9 Cuotas"),
    (10, "10 Cuotas"),
    (11, "11 Cuotas"),
    (12, "12 Cuotas"),
    (13, "Más de 12 Cuotas")
)


class TmcForm(forms.Form):
    monto = forms.IntegerField(required=True)
    cuotas = forms.ChoiceField(choices=CUOTAS_CHOICES,
                               initial='1',
                               widget=forms.Select(),
                               required=True)
    fecha = forms.DateField(input_formats=['%d/%m/%Y'], label='Fecha TMC',
                            required=True, widget=forms.DateTimeInput(
                                attrs={'class': 'datetimepicker-input',
                                       'data-target': '#datetimepicker1'})
                            )
