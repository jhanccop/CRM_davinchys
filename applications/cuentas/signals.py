
def update_accounts(sender, instance, **kwargs):
    from applications.cuentas.models import Account
    if kwargs['created']:
        account = Account.objects.get(id = instance.idAcount.id)
               
        account.realBalance = instance.realBalance
        account.lastUpdateReal = instance.created_at
        account.save()
    else:
        pass
        #update(instance, "0")
    return instance

