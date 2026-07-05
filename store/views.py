from django.shortcuts import render

def store_view(request):
    """
    Vista para renderizar la página independiente de la Tienda Especializada
    con enfoque de nicho gastronómico y dolores del CRM.
    """
    return render(request, 'store/store_view.html')
