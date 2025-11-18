from django.shortcuts import render, redirect # Agregamos 'redirect' para redireccionar después del POST
from .models import TermometroRespuesta
from django.urls import reverse # Importamos reverse, aunque usaremos el nombre de URL directamente

# --------------------------------------------------------------------------------
# LÓGICA DE CLASIFICACIÓN DEL TEST DE CAOS (se mantiene igual)
# --------------------------------------------------------------------------------

def obtener_puntaje_respuesta(respuesta_str):
    """
    Convierte la respuesta del formulario a un valor numérico (1 a 4).
    """
    try:
        return int(respuesta_str)
    except (TypeError, ValueError):
        return 0

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
    
    # 1. Obtener puntajes de las 4 áreas (asegurando que sean números)
    p_crece = obtener_puntaje_respuesta(request.POST.get("respuesta_crece"))
    p_avanza = obtener_puntaje_respuesta(request.POST.get("respuesta_avanza"))
    p_mejora = obtener_puntaje_respuesta(request.POST.get("respuesta_mejora"))
    p_reemprende = obtener_puntaje_respuesta(request.POST.get("respuesta_reemprende"))

    # 2. Calcular el puntaje total de caos
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

    # 5. Redireccionar con mensaje de éxito (usaremos la sesión para pasar los datos)
    # Guardamos los resultados en la sesión antes de redirigir
    request.session["exito"] = True
    request.session["fase_final"] = fase_final
    request.session["puntaje_caos"] = puntaje_total

    # Redirigimos de vuelta a la vista de la landing para mostrar el mensaje de éxito
    return redirect('termometro:diagnostico')