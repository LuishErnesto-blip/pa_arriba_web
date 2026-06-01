from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from blog.models import Prospecto
from datetime import date

class Command(BaseCommand):
    help = 'Envia alertas de leads con accion pendiente hoy'

    def handle(self, *args, **kwargs):
        hoy = date.today()
        leads_hoy = Prospecto.objects.filter(
            fecha_proxima_accion=hoy
        ).exclude(etapa__in=['perdido', 'congelador'])

        if not leads_hoy.exists():
            self.stdout.write('Sin leads pendientes hoy.')
            return

        cuerpo = f"OXIGENO CRM — Alertas {hoy.strftime('%d/%m/%Y')}\n"
        cuerpo += "=" * 45 + "\n\n"

        prioridad = {'e4': 1, 'e3': 2, 'e2': 3, 'e1': 4, 'e0': 5}
        leads_ordenados = sorted(
            leads_hoy,
            key=lambda x: prioridad.get(x.etapa, 9)
        )

        for lead in leads_ordenados:
            cuerpo += f"[{lead.get_etapa_display()}]\n"
            cuerpo += f"Negocio : {lead.nombre_negocio}\n"
            cuerpo += f"Contacto: {lead.nombre_dueño}\n"
            cuerpo += f"Tel     : {lead.telefono}\n"
            if lead.proxima_accion:
                cuerpo += f"Accion  : {lead.proxima_accion}\n"
            cuerpo += "-" * 35 + "\n\n"

        cuerpo += f"Total pendientes hoy: {leads_hoy.count()}\n"
        cuerpo += "pa-arriba.com/admin/blog/prospecto/\n"

        send_mail(
            subject=f"[OXIGENO CRM] {leads_hoy.count()} leads pendientes hoy {hoy.strftime('%d/%m')}",
            message=cuerpo,
            from_email='luis.bracerog06@gmail.com',
            recipient_list=['luis.bracerog06@gmail.com'],
            fail_silently=False,
        )
        self.stdout.write(f'Alerta enviada: {leads_hoy.count()} leads.')
