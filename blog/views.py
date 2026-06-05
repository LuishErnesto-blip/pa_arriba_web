from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q
import csv
import datetime
from .models import Post, Prospecto


def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by("-published_date")
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, "blog/detalle_post.html", {"post": post})


@staff_member_required
def dashboard_crm(request):
    hoy = timezone.now().date()
    manana = hoy + datetime.timedelta(days=1)
    inicio_semana = hoy - datetime.timedelta(days=hoy.weekday())
    inicio_mes = hoy.replace(day=1)
    proximos_30 = hoy + datetime.timedelta(days=30)
    fecha_desde = request.GET.get("fecha_desde", "")
    fecha_hasta = request.GET.get("fecha_hasta", "")
    etapa_filtro = request.GET.get("etapa", "")
    qs = Prospecto.objects.all()
    if fecha_desde:
        qs = qs.filter(fecha_registro__date__gte=fecha_desde)
    if fecha_hasta:
        qs = qs.filter(fecha_registro__date__lte=fecha_hasta)
    if etapa_filtro:
        qs = qs.filter(etapa=etapa_filtro)
    total = qs.count()
    if request.GET.get("export") == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=dashboard_crm.csv"
        writer = csv.writer(response)
        writer.writerow(["Negocio", "Dueno", "Telefono", "Etapa", "Dolor", "Canal", "Fecha Registro"])
        for p in qs:
            writer.writerow([
                p.nombre_negocio, p.nombre_dueño, p.telefono,
                p.get_etapa_display(),
                p.get_dolor_principal_display() if p.dolor_principal else "",
                p.get_canal_entrada_display() if p.canal_entrada else "",
                p.fecha_registro.strftime("%Y-%m-%d")
            ])
        return response
    pipeline = qs.filter(etapa__in=["e0","e1","e2","e3","e4"]).count()
    pipeline_pct = round(pipeline / total * 100, 1) if total else 0
    perdidos = qs.filter(etapa="perdido").count()
    perdidos_pct = round(perdidos / total * 100, 1) if total else 0
    congelador = qs.filter(etapa="congelador").count()
    alianza = qs.filter(etapa="alianza").count()
    cerrados = qs.filter(etapa="cerrado").count()
    tasa_perdida = perdidos_pct
    e0 = qs.filter(etapa="e0").count()
    e1 = qs.filter(etapa="e1").count()
    e2 = qs.filter(etapa="e2").count()
    e3 = qs.filter(etapa="e3").count()
    e4 = qs.filter(etapa="e4").count()
    cerrados_mes = qs.filter(etapa="cerrado", fecha_registro__date__gte=inicio_mes).count()
    def ratio(a, b):
        return round(a / b * 100, 1) if b else 0
    r_e0_e1 = ratio(e1, e0 + e1)
    r_e1_e2 = ratio(e2, e1 + e2)
    r_e2_e3 = ratio(e3, e2 + e3)
    r_e3_e4 = ratio(e4, e3 + e4)
    r_e4_cerrado = ratio(cerrados, e4 + cerrados)
    costos_ojo = qs.filter(dolor_principal="costos_ojo").count()
    costos_ojo_pct = ratio(costos_ojo, total)
    meta_ad1 = qs.filter(canal_entrada="meta_ad1").count()
    sin_dolor = qs.filter(Q(dolor_principal__isnull=True) | Q(dolor_principal="")).count()
    sin_canal = qs.filter(Q(canal_entrada__isnull=True) | Q(canal_entrada="")).count()
    con_email = qs.exclude(correo__isnull=True).exclude(correo="").count()
    con_email_pct = ratio(con_email, total)
    con_ubicacion = qs.exclude(ubicacion__isnull=True).exclude(ubicacion="").count()
    con_ubicacion_pct = ratio(con_ubicacion, total)
    con_acuerdo = qs.exclude(acuerdo_1__isnull=True).exclude(acuerdo_1="").count()
    con_acuerdo_pct = ratio(con_acuerdo, total)
    con_notas = qs.exclude(notas_generales__isnull=True).exclude(notas_generales="").count()
    con_notas_pct = ratio(con_notas, total)
    sin_proxima = qs.filter(Q(proxima_accion__isnull=True) | Q(proxima_accion=""), Q(fecha_proxima_accion__isnull=True)).count()
    vencidas_hoy = qs.filter(fecha_proxima_accion__lt=hoy).count()
    manana_count = qs.filter(fecha_proxima_accion=manana).count()
    esta_semana = qs.filter(fecha_registro__date__gte=inicio_semana).count()
    hoy_count = qs.filter(fecha_registro__date=hoy).count()
    reactivar = qs.filter(etapa="congelador", fecha_proxima_accion__gte=hoy, fecha_proxima_accion__lte=proximos_30).count()
    calientes = Prospecto.objects.filter(etapa__in=["e2","e3","e4"]).order_by("fecha_proxima_accion")[:20]
    context = {
        "hoy": hoy,
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta,
        "etapa_filtro": etapa_filtro,
        "etapas": Prospecto.ETAPAS,
        "total": total,
        "pipeline": pipeline, "pipeline_pct": pipeline_pct,
        "perdidos": perdidos, "perdidos_pct": perdidos_pct,
        "congelador": congelador,
        "alianza": alianza,
        "cerrados": cerrados,
        "tasa_perdida": tasa_perdida,
        "e0": e0, "e1": e1, "e2": e2, "e3": e3, "e4": e4,
        "cerrados_mes": cerrados_mes,
        "r_e0_e1": r_e0_e1, "r_e1_e2": r_e1_e2,
        "r_e2_e3": r_e2_e3, "r_e3_e4": r_e3_e4,
        "r_e4_cerrado": r_e4_cerrado,
        "costos_ojo": costos_ojo, "costos_ojo_pct": costos_ojo_pct,
        "meta_ad1": meta_ad1,
        "sin_dolor": sin_dolor, "sin_canal": sin_canal,
        "con_email_pct": con_email_pct,
        "con_ubicacion_pct": con_ubicacion_pct,
        "con_acuerdo_pct": con_acuerdo_pct,
        "con_notas_pct": con_notas_pct,
        "sin_proxima": sin_proxima,
        "vencidas_hoy": vencidas_hoy,
        "manana_count": manana_count,
        "esta_semana": esta_semana,
        "hoy_count": hoy_count,
        "reactivar": reactivar,
        "calientes": calientes,
    }
    return render(request, "blog/dashboard_crm.html", context)
