def CreateOrderTracking(sender, instance,**kwargs):
  from applications.pedidos.models import OrderTracking

  ids = OrderTracking.objects.filter(idOrder = instance.id).order_by('id')
  if len(ids) >= 1:
    pass
  else:
    tracking = OrderTracking()
    tracking.idOrder = instance.id
    tracking.dateChange = instance.created_at
    tracking.orderState = "0"
    tracking.save()
  return  instance

def CreatePurchaseTracking(sender, instance,**kwargs):
  from applications.pedidos.models import PurchaseTracking

  ids = PurchaseTracking.objects.filter(idOrder = instance.id).order_by('id')
  if len(ids) >= 1:
    pass
  else:
    tracking = PurchaseTracking()
    tracking.idOrder = instance.id
    tracking.dateChange = instance.created_at
    tracking.orderState = "0"
    tracking.save()
  return  instance

def CreateServiceTracking(sender, instance,**kwargs):
  from applications.pedidos.models import ServiceTracking

  ids = ServiceTracking.objects.filter(idOrder = instance.id).order_by('id')
  if len(ids) >= 1:
    pass
  else:
    tracking = ServiceTracking()
    tracking.idOrder = instance.id
    tracking.dateChange = instance.created_at
    tracking.orderState = "0"
    tracking.save()
  return  instance

def UpdateOrders(sender, instance,**kwargs):
  from applications.pedidos.models import Orders
  order = Orders.objects.get(id = instance.idOrder)
  order.IdOrderState = instance.orderState
  order.save()
  return instance

def UpdatePurchases(sender, instance,**kwargs):
  from applications.pedidos.models import PurchaseOrders
  order = PurchaseOrders.objects.get(id = instance.idOrder)
  order.IdOrderState = instance.orderState
  order.save()
  return instance

def UpdateServices(sender, instance,**kwargs):
  from applications.pedidos.models import ServiceOrders
  order = ServiceOrders.objects.get(id = instance.idOrder)
  order.IdOrderState = instance.orderState
  order.save()
  return instance


