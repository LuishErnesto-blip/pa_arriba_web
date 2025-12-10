import requests
import json
from django.conf import settings

def enviar_mensaje_whatsapp(numero_destino, nombre_usuario, fase_final, puntaje):
    """
    Envía el mensaje de diagnóstico automático vía WhatsApp Cloud API.
    """
    # 1. Limpieza del número (Quitar el '+' si existe, asegurar el '593')
    # Asumimos que el usuario puede poner 099... o 59399...
    numero = str(numero_destino).strip().replace("+", "").replace(" ", "")
    
    if numero.startswith("0"):
        numero = "593" + numero[1:] # Reemplaza el 0 inicial por 593
    elif not numero.startswith("593"):
        numero = "593" + numero # Si no tiene código de país, lo agrega

    # 2. Configuración de la API de Meta (Usaremos variables de entorno después)
    # Por ahora dejamos los placeholders para que tú pongas tus credenciales
    url = "https://graph.facebook.com/v17.0/922198437639839/messages"
    token = "EAATz5PVndoYBQGuzfp0JUzrecCi6b3neZBnfC7FNJhLZCHZASr80eR0ejAmdhsdEzFa4GZB4sMCnOJ5gRZAwpWCIDZCZB7iXKOPt3EAXWT4dIAGdaQb34FFScgIsZBc6wvLuXzBj9zAe5H4LGQgn1wT7PO9n9uwryCPGfuunXGLs7SlPpQARzybSQZA9ALbl5Np3XtRMP10vmCLEgCyKh3kRm7Dtog88vwJJqzv1wBynYIwG38Q9gHO8ofpNQcQYbR7mZAVWAG78ZBb3gA5wD0YQQ2GEAh1BwCkclEuU6qLAmYZD"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 3. Cuerpo del Mensaje (Plantilla o Texto Libre)
    # Para iniciar conversación (si pasaron más de 24h), Meta exige PLANTILLA.
    # Pero si es respuesta inmediata a un clic de anuncio, a veces permite texto.
    # Vamos a probar con TEXTO simple primero (en modo desarrollo).
    
    mensaje_texto = f"Hola {nombre_usuario} 👋 Soy el Asistente de Pa'arriba.\n\nRecibí tu diagnóstico del Termómetro del Caos.\n\n📊 *Tu Resultado:* {fase_final} (Puntaje: {puntaje}/16).\n\nEsto significa que tu negocio tiene oportunidades críticas de mejora. Como premio por tu interés, quiero regalarte 3 DÍAS de acceso total a nuestra App Oxígeno.\n\n¿Te interesa activarlo ahora?"

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": numero,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": mensaje_texto
            }
        }
      
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print(f"✅ WhatsApp enviado a {numero}")
            return True
        else:
            print(f"❌ Error WhatsApp: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión WhatsApp: {e}")
        return False