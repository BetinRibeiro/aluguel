# -*- coding: utf-8 -*-
import datetime
@auth.requires_login()
def acesso():
    #fara a busca das datas menores que os proximos 3 meses e que não estão quitadas
    data=request.now
    primeira_data=request.now
    if data.month==1:
        primeira_data=datetime.date(data.year-1, 11, data.day)
    elif data.month==2:
        primeira_data=datetime.date(data.year-1, 12, data.day)
    else:
        primeira_data=datetime.date(data.year, data.month-2, data.day)
    if data.month<=9:
        databusca=datetime.date(data.year, data.month+3, data.day)
    else:
        databusca=datetime.date(data.year+1, 1, data.day)
        #(db.recebimento.quitado==False) &
    
        
    rows = db((db.recebimento.data_vencimento<databusca)).select(orderby=db.recebimento.data_vencimento)
    return locals()


@auth.requires_login()
def alterar_quitar():
    data=request.now
    response.view = 'generic.html' # use a generic view
    recebimento=db.recebimento(request.args(0, cast=int))
    db.recebimento.id.readable = False
    db.recebimento.id.writable = False
    if not recebimento.quitado:
        recebimento.data_pagamento = request.now
        recebimento.update_record()
    
    form = SQLFORM(db.recebimento, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        recebimento=db.recebimento(request.args(0, cast=int))
        if recebimento.quitado:
            redirect(URL('recebimento_periodo', args=[data.month,data.year]))
        else:
            redirect(URL('acesso',args=recebimento.contrato_aluguel))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    #2 consultas no banco
    return  dict(form=form)

@auth.requires_login()
def ver_recibo():
    recebimento=db.recebimento(request.args(0, cast=int))
    contrato=db.contrato_aluguel(recebimento.contrato_aluguel)
    locador=db.pessoa(contrato.locador)
    locatario=db.pessoa(contrato.locatario)
    imovel=db.imovel(contrato.imovel)
    return locals()

@auth.requires_login()
def recebimento_periodo():
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
    rows = db((db.recebimento.data_vencimento>=primeira_data)&(db.recebimento.data_vencimento<ultima_data)).select(orderby=db.recebimento.data_vencimento)
    return locals()
