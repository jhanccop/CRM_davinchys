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
                },
                {
                    'name': 'Ordenes Trabajo',
                    'url_name': '',
                    'mini_icon': 'WO',
                    'permission': 'ventas.view_purchaseorder'
                }
            ]
        },
        'finanzas': {
            'name': 'FINANZAS',
            'icon': 'fas fa-hand-holding-usd',
            'items': [
                # ── General ───────────────────────────────────────────────────
                {'name': 'Dashboard',         'url_name': 'finantial:dashboard',         'mini_icon': '📊', 'permission': None},
                {'name': 'Seg. por Ítem',     'url_name': 'finantial:item-tracking',     'mini_icon': '🔍', 'permission': None},
                # ── Operativa ─────────────────────────────────────────────────
                {'name': 'Operativa',         'url_name': '', 'mini_icon': '', 'is_separator': True, 'permission': None},
                {'name': 'Comprobantes',      'url_name': 'finantial:document-list',     'mini_icon': 'CP', 'permission': None},
                {'name': 'Transacciones',     'url_name': 'finantial:transaction-list',  'mini_icon': 'TX', 'permission': None},
                {'name': 'Mov. Bancarios',    'url_name': 'finantial:movement-list',     'mini_icon': 'MB', 'permission': None},
                {'name': 'Importar Extracto', 'url_name': 'finantial:import-statement',  'mini_icon': 'IM', 'permission': None},
                # ── Tesorería ─────────────────────────────────────────────────
                {'name': 'Tesorería',         'url_name': '', 'mini_icon': '', 'is_separator': True, 'permission': None},
                {'name': 'Antigüedad Cartera','url_name': 'finantial:ar-aging',          'mini_icon': 'AC', 'permission': None},
                {'name': 'Flujo de Caja',     'url_name': 'finantial:cashflow',          'mini_icon': 'FC', 'permission': None},
                {'name': 'Cierres Mensuales', 'url_name': 'finantial:closure-list',      'mini_icon': 'CM', 'permission': None},
                # ── Contabilidad ──────────────────────────────────────────────
                {'name': 'Contabilidad',      'url_name': '', 'mini_icon': '', 'is_separator': True, 'permission': None},
                {'name': 'Asientos',          'url_name': 'finantial:journal-list',      'mini_icon': 'AS', 'permission': None},
                {'name': 'Estado Resultados', 'url_name': 'finantial:profit-loss',       'mini_icon': 'ER', 'permission': None},
                # ── Tributario ────────────────────────────────────────────────
                {'name': 'Tributario',        'url_name': '', 'mini_icon': '', 'is_separator': True, 'permission': None},
                {'name': 'PLE SUNAT',         'url_name': 'finantial:ple-export',        'mini_icon': 'PL', 'permission': None},
                # ── Configuración ─────────────────────────────────────────────
                {'name': 'Configuración',     'url_name': '', 'mini_icon': '', 'is_separator': True, 'permission': None},
                {'name': 'Plan de Cuentas',   'url_name': 'finantial:chart-of-accounts', 'mini_icon': 'PC', 'permission': None},
                {'name': 'Centros de Costo',  'url_name': 'finantial:costcenter-list',   'mini_icon': 'CC', 'permission': None},
                {'name': 'Tipos de Cambio',   'url_name': 'finantial:exchangerate-list', 'mini_icon': 'TC', 'permission': None},
                {'name': 'Cód. Impuesto',     'url_name': 'finantial:taxcode-list',      'mini_icon': 'CI', 'permission': None},
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
            # Los separadores siempre pasan (se limpian al final si quedan vacíos)
            if item.get('is_separator'):
                filtered_items.append(item)
                continue
            # Si no hay restricción de permiso o el usuario tiene el permiso
            if not item['permission'] or (user.is_authenticated and user.has_perm(item['permission'])):
                filtered_items.append(item)

        # Eliminar separadores al inicio, al final, o consecutivos
        cleaned = []
        for item in filtered_items:
            if item.get('is_separator'):
                # No agregar si la lista está vacía o el último ya es separador
                if cleaned and not cleaned[-1].get('is_separator'):
                    cleaned.append(item)
            else:
                cleaned.append(item)
        # Quitar separador final si quedó
        if cleaned and cleaned[-1].get('is_separator'):
            cleaned.pop()
        filtered_items = cleaned
        
        # Solo incluir el menú si tiene items visibles
        if filtered_items:
            filtered_menu[menu_key] = {
                'name': menu_data['name'],
                'icon': menu_data['icon'],
                'items': filtered_items
            }
    
    return filtered_menu