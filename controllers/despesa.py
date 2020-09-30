# -*- coding: utf-8 -*-
import datetime
@auth.requires_login()
def acesso(): 
    data=request.now.year
    ano=request.now.month
    mes=request.args(0, cast=int)
    ano=request.args(1, cast=int)
    primeira_data=datetime.date(ano, mes, 1)
    ultima_data=datetime.date(ano, mes, 1)

    if (mes==12):
        ultima_data=datetime.date(ano+1, 1, 1)
    else:
        ultima_data=datetime.date(ano, mes+1, 1)
    rows = db((db.despesa.data_pagamento>=primeira_data)&(db.despesa.data_pagamento<ultima_data)).select(orderby=db.despesa.data_pagamento)
    return locals()

def alterar():
    data=request.now
    response.view = 'generic.html' # use a generic view
    despesa=db.despesa(request.args(0, cast=int))
    db.despesa.id.readable = False
    db.despesa.id.writable = False
    
    form = SQLFORM(db.despesa, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        
        redirect(URL('acesso', args=[data.month,data.year]))
        
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    #2 consultas no banco
    return  dict(form=form)
