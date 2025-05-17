from django.shortcuts import render, get_object_or_404, redirect
from .models import colaborador, RegistroVehiculo, MovimientoVehiculo, QR
from .forms import  ColaboradorForm, PlacaForm, RegistroForm
from django.contrib import messages

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
    qr = get_object_or_404(QR, uuid=uuid)

    if request.method == 'POST':
        # PASO 1: Revisar si solo se recibió la placa
        if 'placa' in request.POST and 'nombre_completo' not in request.POST:
            placa = request.POST['placa'].strip().upper()
            colaborador_obj = colaborador.objects.filter(placa=placa).first()

            if colaborador_obj:
                # Ya existe → registrar movimiento
                registro, _ = RegistroVehiculo.objects.get_or_create(qr=qr, placa=placa)
                ultimo = MovimientoVehiculo.objects.filter(registro=registro).order_by('-timestamp').first()
                tipo = 'entrada' if not ultimo or ultimo.tipo == 'salida' else 'salida'
                MovimientoVehiculo.objects.create(registro=registro, tipo=tipo)

                return render(request, 'movimiento_registrado.html', {
                    'registro': registro,
                    'colaborador': colaborador_obj,
                    'tipo': tipo
                })

            else:
                # No existe → mostrar formulario completo con placa ya ingresada
                form = ColaboradorForm(initial={'placa': placa})
                return render(request, 'registro_colaborador.html', {
                    'form': form,
                    'qr': qr
                })

        # PASO 2: Si llegó el formulario completo
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            nuevo_colab = form.save(commit=False)
            nuevo_colab.qr = qr
            nuevo_colab.save()

            registro = RegistroVehiculo.objects.create(qr=qr, placa=nuevo_colab.placa)
            MovimientoVehiculo.objects.create(registro=registro, tipo='entrada')

            return render(request, 'completado.html', {
                'registro': registro,
                'tipo': 'entrada',
                'mensaje': 'Registro completado con éxito'
            })
    else:
        # Mostrar solo el formulario de la placa
        form = PlacaForm()

    return render(request, 'registro_form.html', {'form': form, 'qr': qr})
