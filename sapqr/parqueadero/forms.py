from django import forms
from .models import colaborador

class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = colaborador
        fields = ['nombre_completo', 'dependencia', 'marca', 'modelo', 'placa', 'telefono']
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Placa'}),
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'dependencia': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True  # hace todos los campos obligatorios


class PlacaForm(forms.Form):
    placa = forms.CharField(
        max_length=10,
        label='Placa del vehículo',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu placa',
            'autocomplete': 'off',
            'required': 'required'
        })
    )


class RegistroForm(forms.ModelForm):
    class Meta:
        model = colaborador  # Usamos el modelo colaborador para registrar los datos
        fields = ['placa', 'nombre_completo', 'dependencia', 'marca', 'modelo', 'telefono']
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'dependencia': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_placa(self):
        placa = self.cleaned_data.get('placa')
        # Validación extra para la placa, si es necesario
        if len(placa) < 6:  # Validar que la placa tenga el tamaño adecuado
            raise forms.ValidationError("La placa debe tener al menos 6 caracteres")
        return placa