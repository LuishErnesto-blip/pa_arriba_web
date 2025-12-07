from django.shortcuts import render, redirect 
from .models import TermometroRespuesta
from django.urls import reverse 
from django.core.mail import send_mail 

# --------------------------------------------------------------------------------
# LÓGICA DE CLASIFICACIÓN DEL TEST DE CAOS (VERSION CORREGIDA)
# --------------------------------------------------------------------------------

# Diccionario de conversión de respuestas a puntajes
PUNTUACIONES_POR_RESPUESTA = {
    # CRECE, MEJORA, AVANZA, RE-EMPRENDE
    "Muy seguro": 5, "Funcionaría sin problema": 5, "Datos y análisis": 5, "Aliada": 5,
    "Tengo dudas": 3, "Se complicaría un poco": 3, "Experiencia e intuición": 3, "Confusa": 3,
    "No tengo idea": 1, "Se paralizaría": 1, "Imitación": 1, "Amenazante": 1,
}

def obtener_puntaje_respuesta(respuesta_str):
    """
    Busca la respuesta de texto en el diccionario y devuelve el puntaje numérico.
    """
    respuesta_limpia = respuesta_str.strip() if respuesta_str else ""
    return PUNTUACIONES_POR_RESPUESTA.get(respuesta_limpia, 0) # Si no encuentra, devuelve 0

def clasificar_fase(puntaje_total):
    """
    Clasifica el puntaje total en una de las cuatro fases de la marca Pa'arriba.
    Slogan: CRECE, AVANZA, MEJORA, RE-EMPRENDE
    """
    if puntaje_total >= 13:
        return "CRECE" # Mínimo Caos.
    elif puntaje_total >= 10:
        return "AVANZA" # Caos Bajo.
    elif puntaje_total >= 7:
        return "MEJORA" # Caos Moderado.
    else:
        return "RE-EMPRENDE" # Caos Alto.

# --------------------------------------------------------------------------------
# VISTA 1: MUESTRA EL FORMULARIO (SOLO GET)
# --------------------------------------------------------------------------------

def termometro_landing(request):
    # Esta vista ahora solo maneja la solicitud GET (mostrar el formulario).
    # Toda la lógica de POST se ha movido a diagnostico_submit.

    # 🧭 Renderizar formulario en GET
    # El contexto (exito, fase_final) lo puedes recibir aquí si la vista diagnostico_submit te redirecciona 
    # con parámetros GET, pero por ahora solo renderizamos.

    # 1. Recuperar datos de la sesión/GET si vienen de un envío exitoso (OPCIONAL: para mostrar el resultado)
    contexto = {
        "exito": request.session.pop("exito", False),
        "fase_final": request.session.pop("fase_final", None),
        "puntaje_caos": request.session.pop("puntaje_caos", None),
    }

    return render(request, "termometro/landing.html", contexto)

# --------------------------------------------------------------------------------
# VISTA 2: PROCESA EL FORMULARIO (SOLO POST)
# --------------------------------------------------------------------------------

def diagnostico_submit(request):
    # Si alguien llega a esta URL por GET, redirigimos a la landing
    if request.method != "POST":
        return redirect('termometro:diagnostico')
    
    # 1. Obtener puntajes de las 4 áreas (AHORA SÍ FUNCIONA LA CONVERSIÓN DE TEXTO A NÚMERO)
    p_crece = obtener_puntaje_respuesta(request.POST.get("respuesta_crece"))
    p_avanza = obtener_puntaje_respuesta(request.POST.get("respuesta_avanza"))
    p_mejora = obtener_puntaje_respuesta(request.POST.get("respuesta_mejora"))
    p_reemprende = obtener_puntaje_respuesta(request.POST.get("respuesta_reemprende"))

    # 2. Calcular el puntaje total de caos
    puntaje_total = p_crece + p_avanza + p_mejora + p_reemprende # Error tipográfico aquí, corregido en la prueba.

    # 2. Calcular el puntaje total de caos (CORREGIDO)
    puntaje_total = p_crece + p_avanza + p_mejora + p_reemprende
    
    # 3. Clasificar la fase final de la marca
    fase_final = clasificar_fase(puntaje_total)
    
    # 4. Crear el registro en la base de datos (con todos los datos)
    TermometroRespuesta.objects.create(
        nombre = request.POST.get("nombre"),
        email = request.POST.get("email"),
        whatsapp = request.POST.get("whatsapp"),
        tipo_negocio = request.POST.get("tipo_negocio"),
        
        # Guardamos las respuestas originales como texto (CharField)
        crece = request.POST.get("respuesta_crece"),
        avanza = request.POST.get("respuesta_avanza"),
        mejora = request.POST.get("respuesta_mejora"),
        reemprende = request.POST.get("respuesta_reemprende"),
        
        # Guardamos los resultados numéricos y la fase de la marca
        puntaje_caos = puntaje_total,
        fase_final = fase_final,
    )

    # --- 5. NOTIFICACIÓN POR CORREO ELECTRÓNICO (CÓDIGO QUE YA FUNCIONA) ---
    subject = f"🚨 NUEVO DIAGNÓSTICO PA'ARRIBA: {fase_final} (Puntaje {puntaje_total}/16)"
    message = (
        f"¡Hola Luis Ernesto!\n\n"
        f"Un nuevo emprendedor ha completado el Termómetro del Caos.\n"
        f"---------------------------------------------------\n"
        f"NOMBRE: {request.POST.get('nombre')}\n"
        f"EMAIL: {request.POST.get('email')}\n"
        f"WHATSAPP: {request.POST.get('whatsapp')}\n"
        f"TIPO DE NEGOCIO: {request.POST.get('tipo_negocio')}\n"
        f"---------------------------------------------------\n"
        f"DIAGNÓSTICO INICIAL: {fase_final} (Urge contacto)\n"
        f"PUNTAJE TOTAL: {puntaje_total}/16\n"
        f"RESPUESTAS:\n"
        f"  1. CRECE: {request.POST.get('respuesta_crece')}\n"
        f"  2. AVANZA: {request.POST.get('respuesta_avanza')}\n"
        f"  3. MEJORA: {request.POST.get('respuesta_mejora')}\n"
        f"  4. RE-EMPRENDE: {request.POST.get('respuesta_reemprende')}\n"
    )

    try:
        send_mail(
            subject,
            message,
            None, # Usará el DEFAULT_FROM_EMAIL de settings.py
            ['luis.bracerog06@gmail.com'], # Tu correo de recepción
            fail_silently=False,
        )
    except Exception as e:
        # En caso de que el correo falle (ej: contraseña incorrecta), no detiene el proceso de guardado.
        print(f"Error al enviar la notificación: {e}")
        pass
    
    # 6. Redireccionar con mensaje de éxito (usaremos la sesión para pasar los datos)
    # Guardamos los resultados en la sesión antes de redirigir
    request.session["exito"] = True
    request.session["fase_final"] = fase_final
    request.session["puntaje_caos"] = puntaje_total

    # Redirigimos de vuelta a la vista de la landing para mostrar el mensaje de éxito
    return redirect('termometro:diagnostico')