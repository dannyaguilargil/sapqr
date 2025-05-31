# 🚗 Sistema de Registro de Vehículos con QR - IMSALUD

Este proyecto es un sistema de control de acceso para vehículos mediante escaneo de códigos QR. Permite registrar automáticamente la entrada o salida de un colaborador según la placa del vehículo o QR asignado.

## 🧩 Características principales

- Escaneo de código QR para registro de entrada/salida.
- Registro de colaboradores y sus placas.
- Validación automática de la placa antes de registrar un nuevo colaborador.
- Registro visual de movimientos (entrada/salida).
- Exportación de datos con `django-import-export`.
- Interfaz responsiva para dispositivos móviles.

## ⚙️ Tecnologías utilizadas

- Python 3.10+
- Django 4.x
- SQLite o PostgreSQL
- django-import-export
- Feedparser (opcional, si se desean mostrar noticias)
- Panel de administracion con JET

## 🚀 Instalación

1. **Clona el repositorio**:
    ```bash

    cd sapqr
    ```

2. **Crea y activa un entorno virtual**:
    ```bash
    python -m venv venv
    source venv/bin/activate        # Linux/Mac
    .\venv\Scripts\activate         # Windows
    ```

3. **Instala las dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Aplica migraciones**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Crea un superusuario**:
    ```bash
    python manage.py createsuperuser
    ```

6. **Inicia el servidor**:
    ```bash
    python manage.py runserver
    ```


Puedes acceder al dashboard administrativo del proyecto en:

🔹 [https://dashy.dannyhub.com](https://dashy.dannyhub.com)

## 📬 Contacto

Si tienes dudas, sugerencias o deseas colaborar:

📧 **dev@dannyhub.com**

---

Desarrollado para la E.S.E. IMSALUD - d4n7.dev
