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
    token = "EAATz5PVndoYBQDBtEapITHRaI3GqZBfYBQvzmPCpVbKMMClLQ3C9OYwZBseOW3T9I0YNHNuy4OJs8iMEZAVGcZB4BAZAy1cMavxNFUEZCvfxqeThO19Ym1LwgtAwSI8w2MU79pVPTuAdhVP6x3WEv1RvtCCs91KAFsAXz56cvQF7PsZApECPhZCLSVpUe9Ejvsxbem6tQdsUVb8hSoQMBCUsTLXFGahuV1tUHwIsQUnSZCLm7AnaZBfiVCZBk8WMqBFqG2bW2EBytg4s7NB6mBM02VbrZCzCr5AEXIVTlhE9HwZDZD"
    
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
        "to": numero,
        "type": "text",
        "text": {
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