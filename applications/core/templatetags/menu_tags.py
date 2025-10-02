from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.simple_tag
def is_menu_active(request, url_name):
    """
    Verifica si un item del menú está activo basado en la URL actual
    """
    if not url_name:
        return ''
    
    try:
        url = reverse(url_name)
        current_path = request.path
        
        # Para URLs que son raíces, coincidencia exacta
        if url == '/':
            return 'active bg-gradient-primary' if current_path == url else ''
        
        # Para otras URLs, verificar si la ruta actual comienza con la URL del menú
        return 'active bg-gradient-primary' if current_path.startswith(url) else ''
    
    except NoReverseMatch:
        return ''


@register.simple_tag
def is_submenu_active(request, menu_items):
    """
    Verifica si algún item del submenú está activo para mantener el menú expandido
    """
    for item in menu_items:
        try:
            if item['url_name']:
                url = reverse(item['url_name'])
                current_path = request.path
                
                if url == '/':
                    if current_path == url:
                        return 'show'
                elif current_path.startswith(url):
                    return 'show'
        
        except NoReverseMatch:
            continue
    
    return ''


@register.filter
def get_menu_icon(menu_key):
    """
    Devuelve el icono correspondiente para cada menú
    """
    icons = {
        'mi_espacio': 'fas fa-user-tie',
        'comercial': 'fas fa-people-carry',
        'finanzas': 'fas fa-hand-holding-usd',
        'rrhh': 'fas fa-user-friends',
        'produccion': 'far fa-building',
        'logistica': 'fas fa-truck',
        'consolidado': 'fas fa-desktop',
    }
    return icons.get(menu_key, 'fas fa-folder')