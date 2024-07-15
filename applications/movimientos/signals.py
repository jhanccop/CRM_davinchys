from applications.cuentas.models import Account

def update(instance, categoria):
    """ UPDATE DE MOVIMIENTOS """
    from applications.movimientos.models import Transactions

    # id de movimiento en trasacciones
    idMovimiento = instance.id
    category = categoria

    # id de transaccion
    idTransaccion = Transactions.objects.filter(
        category = category,
        idTransaction = idMovimiento,
        ).last()

    # verificacion de variacion en monto original
    if idTransaccion.amount != instance.amount:
    
        # extranccion de tabla de cuenta involucrada en la actualizacion
        listaTransacciones = Transactions.objects.filter(
            idAccount = idTransaccion.idAccount,
            id__gte = idTransaccion.id
        ).order_by("id")

        # restaurar monto inicial quitando la ultima operacion (egreso o ingreso)
        M0 = 0
        if idTransaccion.transactionType == "0":
            M0 = idTransaccion.balance + idTransaccion.amount
        else:
            M0 = idTransaccion.balance - idTransaccion.amount

        idTransaccion.balance = M0
        idTransaccion.amount = instance.amount
        idTransaccion.save()

        for transaction in listaTransacciones:
            iTransaciton = Transactions.objects.get(id = transaction.id)

            print(iTransaciton.transactionType,iTransaciton.amount,M0)

            if iTransaciton.transactionType == "0":
                iTransaciton.balance = M0 - iTransaciton.amount
            else:
                iTransaciton.balance = M0 + iTransaciton.amount
            iTransaciton.save()

            M0 = iTransaciton.balance

        account = Account.objects.get(id = instance.idAccount.id)
        account.accountBalance = M0
        account.save()
        
    return instance

def update_cuentas_transferencias(sender, instance, **kwargs):
  from .models import Transactions

  if kwargs["created"]:
  
    # ============= EGRESO CUENTA ORIGEN ===========
    transaction = Transactions()
    transaction.dateTime = instance.created_at
    transaction.idAccount = instance.idSourceAcount
    transaction.category = "7"
    transaction.idTransaction = instance.id
    transaction.transactionName = instance
    transaction.clientName = instance.idDestinationAcount
    transaction.currency = instance.idSourceAcount.currency
    transaction.amount = instance.SourceAmount
    transaction.transactionType = "0"

    account = Account.objects.get(id = instance.idSourceAcount.id)
    mov = account.accountBalance - instance.SourceAmount
    transaction.balance = mov
    transaction.idAccount = instance.idSourceAcount
    transaction.save()

    account.accountBalance = mov
    account.save()

    # ============= INGRESO CUENTA DESTINO ===========
    transaction2 = Transactions()
    transaction2.dateTime = instance.created_at
    transaction2.idAccount = instance.idDestinationAcount
    transaction2.category = "7"
    transaction2.idTransaction = instance.id
    transaction2.transactionName = instance
    transaction.clientName = instance.idSourceAcount
    transaction2.currency = instance.idDestinationAcount.currency
    transaction2.amount = instance.DestinationAmount
    transaction2.transactionType = "1"

    account2 = Account.objects.get(id = instance.idDestinationAcount.id)
    mov = account.accountBalance - instance.DestinationAmount
    transaction2.balance = mov
    transaction2.idAccount = instance.idDestinationAcount
    transaction2.save()

    account2.accountBalance = mov
    account2.save()
  
  else:
    #update(instance, "6")
    #update(instance, "6")
    pass

  return instance
