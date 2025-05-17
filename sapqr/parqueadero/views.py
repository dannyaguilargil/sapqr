from django.shortcuts import render, get_object_or_404, redirect
from .models import colaborador, RegistroVehiculo, MovimientoVehiculo, QR
from .forms import  ColaboradorForm, PlacaForm, RegistroForm

def registro_general(request):
    if request.method == 'POST':
        # Paso 1: ver si es solo la placa o todos los datos
        if 'placa' in request.POST and 'nombre_completo' not in request.POST:
            placa = request.POST['placa'].strip().upper()
            colaborador_obj = colaborador.objects.filter(placa=placa).first()

            if colaborador_obj:
                # Ya existe, registrar entrada o salida
                registro, _ = RegistroVehiculo.objects.get_or_create(qr=colaborador_obj.qr, placa=placa)
                ultimo = MovimientoVehiculo.objects.filter(registro=registro).order_by('-timestamp').first()
                tipo = 'entrada' if not ultimo or ultimo.tipo == 'salida' else 'salida'
                MovimientoVehiculo.objects.create(registro=registro, tipo=tipo)
                return render(request, 'movimiento_registrado.html', {'registro': registro, 'tipo': tipo})
            else:
                # No existe, mostrar formulario completo
                form = ColaboradorForm(initial={'placa': placa})
                return render(request, 'registro_colaborador.html', {'form': form})

        # Paso 2: si llega el formulario completo
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            nuevo_colab = form.save(commit=False)
            
            # Usamos un QR general, lo puedes crear manualmente o buscar uno existente
            qr_general, _ = QR.objects.get_or_create(uuid="11111111-1111-1111-1111-111111111111")  # ejemplo UUID fijo
            nuevo_colab.qr = qr_general
            nuevo_colab.save()

            # Crear registro de vehículo
            registro = RegistroVehiculo.objects.create(qr=qr_general, placa=nuevo_colab.placa)
            MovimientoVehiculo.objects.create(registro=registro, tipo='entrada')

            return render(request, 'completado.html', {
                'registro': registro,
                'tipo': 'entrada',
                'mensaje': 'Registro completado con éxito'
            })
    else:
        form = PlacaForm()

    return render(request, 'registro_form.html', {'form': form})


def registro_qr(request, uuid):
    # Buscar el QR por UUID
    qr = get_object_or_404(QR, uuid=uuid)
    
    # Comprobar si la placa ya está registrada
    placa = request.GET.get('placa')  # Suponemos que la placa viene como parámetro en el escaneo del QR

    # Buscar el registro de vehículo asociado con la placa
    registro = RegistroVehiculo.objects.filter(qr=qr, placa=placa).first()

    if not registro:
        # Si el vehículo no está registrado, mostramos un formulario de registro
        if request.method == 'POST':
            form = RegistroForm(request.POST)
            if form.is_valid():
                # Guardamos el nuevo registro
                nuevo = form.save(commit=False)
                nuevo.qr = qr
                nuevo.save()

                # Crear el movimiento de entrada
                MovimientoVehiculo.objects.create(registro=nuevo, tipo='entrada')

                return render(request, 'registro/completado.html', {
                    'registro': nuevo,
                    'tipo': 'entrada'
                })
        else:
            form = RegistroForm()

        return render(request, 'registro/formulario.html', {'form': form, 'qr': qr})
    
    # Si ya está registrado, buscamos el último movimiento
    ultimo_movimiento = MovimientoVehiculo.objects.filter(registro=registro).order_by('-timestamp').first()
    
    # Determinamos si es entrada o salida
    tipo = 'entrada' if not ultimo_movimiento or ultimo_movimiento.tipo == 'salida' else 'salida'

    # Registrar el movimiento
    MovimientoVehiculo.objects.create(registro=registro, tipo=tipo)

    return render(request, 'registro/movimiento_registrado.html', {
        'registro': registro,
        'tipo': tipo
    })