from django.urls import reverse, NoReverseMatch

def menu_navigation(request):
    """
    Context processor que centraliza la lógica del menú para todo el CRM
    """
    
    # Estructura centralizada del menú
    menu_structure = {
        'mi_espacio': {
            'name': 'MI ESPACIO',
            'icon': 'fas fa-user-tie',
            'items': [
                {
                    'name': 'Dashboard',
                    'url_name': 'home_app:bienvenida',
                    'mini_icon': 'DA',
                    'permission': None  # Todos pueden ver
                },
                {
                    'name': 'Mis Asistencias', 
                    'url_name': 'rrhh_app:asistencia-user-list',
                    'mini_icon': 'MA',
                    'permission': None
                },
                {
                    'name': 'Mis Requerimientos',
                    'url_name': '', 
                    'mini_icon': 'RE',
                    'permission': 'compras.view_requerimiento'
                },
                {
                    'name': 'Mis Documentos',
                    'url_name': 'rrhh_app:mis-documentos', 
                    'mini_icon': 'MD',
                    'permission': None
                }
            ]
        },
        'comercial': {
            'name': 'COMERCIAL',
            'icon': 'fas fa-people-carry', 
            'items': [
                {
                    'name': 'Dashboard',
                    'url_name': 'comercial_reports_app:dashboard',
                    'mini_icon': 'DA',
                    'permission': 'comercial.view_dashboard'
                },
                {
                    'name': 'Clientes',
                    'url_name': 'stakeholders_app:cliente-lista',
                    'mini_icon': 'CL',
                    'permission': 'stakeholders.view_cliente'
                },
                {
                    'name': 'Proveedores',
                    'url_name': 'stakeholders_app:proveedor-lista',
                    'mini_icon': 'PR',
                    'permission': 'stakeholders.view_proveedor'
                },
                {
                    'name': 'Requerimientos',
                    'url_name': 'compras_app:list_requirement',
                    'mini_icon': 'RE',
                    'permission': 'compras.view_requerimiento'
                },
                {
                    'name': 'Ordenes de compra',
                    'url_name': 'compras_app:lista_ordenescompra',
                    'mini_icon': 'OC',
                    'permission': 'compras.view_ordencompra'
                },
                {
                    'name': 'Cotizaciones Clientes',
                    'url_name': 'ventas_app:cotizaciones-lista',
                    'mini_icon': 'CO',
                    'permission': 'ventas.view_cotizacion'
                },
                {
                    'name': 'PO Clientes',
                    'url_name': 'ventas_app:po-lista',
                    'mini_icon': 'PO',
                    'permission': 'ventas.view_purchaseorder'
                }
            ]
        },
        'finanzas': {
            'name': 'FINANZAS',
            'icon': 'fas fa-hand-holding-usd',
            'items': [
                {
                    'name': 'Dashboard',
                    'url_name': 'finanzas_reports_app:reporte-de-cuentas',
                    'mini_icon': 'DA',
                    'permission': 'finanzas.view_dashboard'
                },
                {
                    'name': 'Mov. Bancarios',
                    'url_name': 'movimientosBancarios_app:lista-movimientos',
                    'mini_icon': 'MB',
                    'permission': 'finanzas.view_conciliacion'
                },
                {
                    'name': 'Doc. Financieros',
                    'url_name': 'documentos_app:documento-financiero-lista',
                    'mini_icon': 'DF',
                    'permission': 'finanzas.view_conciliacion'
                },
                {
                    'name': 'Doc. Genericos',
                    'url_name': 'documentos_app:documento-generico-lista',
                    'mini_icon': 'DG',
                    'permission': 'finanzas.view_conciliacion'
                },
                {
                    'name': 'Cuentas bancarias',
                    'url_name': 'cuentas_app:cuentas-lista',
                    'mini_icon': 'CB',
                    'permission': 'finanzas.view_cuentabancaria'
                }
            ]
        },
        'rrhh': {
            'name': 'RRHH',
            'icon': 'fas fa-user-friends',
            'items': [
                {
                    'name': 'Dashboard',
                    'url_name': 'rrhh_app:dashboard',
                    'mini_icon': 'DA',
                    'permission': 'rrhh.view_dashboard'
                },
                {
                    'name': 'Empleados',
                    'url_name': 'rrhh_app:empleados-list',
                    'mini_icon': 'EM',
                    'permission': 'rrhh.view_empleado'
                },
                {
                    'name': 'Rep. Asistencia',
                    'url_name': 'rrhh_app:reporte_asistencia_persona',
                    'mini_icon': 'RA',
                    'permission': None#'rrhh.view_asistencia'
                },
                {
                    'name': 'Lista Asistencia',
                    'url_name': 'rrhh_app:asistencia-list',
                    'mini_icon': 'LA',
                    'permission': None#'rrhh.view_asistencia'
                },
                {
                    'name': 'Lista Documentos',
                    'url_name': 'rrhh_app:documentos-list',
                    'mini_icon': 'LD',
                    'permission': 'rrhh.view_asistencia'
                }
            ]
        },
        'produccion': {
            'name': 'PRODUCCION',
            'icon': 'far fa-building',
            'items': [
                {
                    'name': 'Dashboard',
                    'url_name': '',
                    'mini_icon': 'DA',
                    'permission': 'produccion.view_dashboard'
                },
                {
                    'name': 'Catálogo Transformadores',
                    'url_name': 'produccion_app:trafos-lista',
                    'mini_icon': 'CT',
                    'permission': 'produccion.view_fabricacion'
                }
            ]
        },
        'logistica': {
            'name': 'LOGISTICA',
            'icon': 'fas fa-truck',
            'items': [
                {
                    'name': 'Dashboard',
                    'url_name': '',
                    'mini_icon': 'DA',
                    'permission': 'logistica.view_dashboard'
                },
                {
                    'name': 'CONTENEDORES',
                    'url_name': 'logistica_app:lista-contenedores',
                    'mini_icon': 'CO',
                    'permission': 'logistica.view_requerimiento'
                }
            ]
        }
    }
    
    # Filtrar menús según permisos del usuario
    filtered_menu = filter_menu_by_permissions(request.user, menu_structure)
    
    # Agregar menú de consolidado para CEO
    if hasattr(request.user, 'position') and str(request.user.position) == "8":
        filtered_menu['consolidado'] = {
            'name': 'CONSOLIDADO',
            'icon': 'fas fa-desktop',
            'items': [
                {
                    'name': 'Dashboard',
                    'url_name': 'users_app:user-lista',
                    'mini_icon': 'DA',
                    'permission': None
                },
                {
                    'name': 'Proyecciones',
                    'url_name': 'users_app:user-lista',
                    'mini_icon': 'PR',
                    'permission': None
                },
                {
                    'name': 'Recursos', 
                    'url_name': 'users_app:user-lista',
                    'mini_icon': 'RH',
                    'permission': None
                }
            ]
        }
    
    return {
        'menu_structure': filtered_menu,
        'current_app': request.resolver_match.app_name if request.resolver_match else None
    }

def filter_menu_by_permissions(user, menu_structure):
    """
    Filtra los items del menú según los permisos del usuario
    """
    filtered_menu = {}
    
    for menu_key, menu_data in menu_structure.items():
        filtered_items = []
        
        for item in menu_data['items']:
            # Si no hay restricción de permiso o el usuario tiene el permiso
            if not item['permission'] or (user.is_authenticated and user.has_perm(item['permission'])):
                filtered_items.append(item)
        
        # Solo incluir el menú si tiene items visibles
        if filtered_items:
            filtered_menu[menu_key] = {
                'name': menu_data['name'],
                'icon': menu_data['icon'],
                'items': filtered_items
            }
    
    return filtered_menu