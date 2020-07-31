# -*- coding: utf-8 -*-
@auth.requires_login()
def pre_cadastro(): 
    response.view = 'generic.html' # use a generic view
    
    form = SQLFORM(db.pre_cadastro).process()
    if form.accepted:
        redirect(URL('default', 'index'))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    #else:
        #response.flash = 'Preencha o formulario'
    return  dict(form=form)
@auth.requires_login()
def cadastro_pessoa(): 
    response.view = 'generic.html' # use a generic view
    
    form = SQLFORM(db.pessoa).process()
    if form.accepted:
        redirect(URL('acesso'))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    #else:
        #response.flash = 'Preencha o formulario'
    return  dict(form=form)


@auth.requires_login()
def alterar_pessoa(): 
    response.view = 'generic.html' # use a generic view
    rows = db((db.contrato_aluguel.locador==(request.args(0)))).select()
    rows += db((db.contrato_aluguel.locatario==(request.args(0)))).select()
    rows += db((db.contrato_aluguel.avalista==(request.args(0)))).select()
    deletar= True
    if len(rows)>0:
        deletar= False
        db.pessoa.id.readable = False
        db.pessoa.id.writable = False
        db.pessoa.nome.writable = False
        db.pessoa.cpf.writable = False
        db.pessoa.rg.writable = False
        db.pessoa.tipo_pessoa.writable = False
    
    db.pessoa.id.readable = False
    db.pessoa.id.writable = False
    
    form = SQLFORM(db.pessoa, request.args(0, cast=int), deletable=deletar)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('acesso'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)
@auth.requires_login()
def acesso():
    
    consul=(request.args(0))
    if consul and consul!='nome':
        rows = db((((db.pessoa.nome.contains(request.args(0)))|(db.pessoa.cpf.contains(request.args(0)))|(db.pessoa.telefone.contains(request.args(0))))&(db.pessoa.nome!="SEM AVALISTA"))&((db.pessoa.id!= 1)& (db.pessoa.id!= 51))).select(orderby=~db.pessoa.id,limitby=(0,25))
    elif consul=='nome':
        rows = db(((db.pessoa.nome.contains(request.args(0)))|(db.pessoa.cpf.contains(request.args(0)))|(db.pessoa.telefone.contains(request.args(0))))&((db.pessoa.id!= 1)& (db.pessoa.id!= 1))).select(orderby=~db.pessoa.nome,limitby=(0,25))
    else:
        rows = db((db.pessoa.nome!="SEM AVALISTA")&((db.pessoa.id!= 1) & (db.pessoa.id!= 51))).select(orderby=~db.pessoa.id,limitby=(0,50))
    return locals()
