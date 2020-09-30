# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig()

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = []
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
db.define_table('empresa',
                Field('auth_user','reference auth_user', label='Usuario'),
                Field('nome', 'string', label='Nome',requires = IS_UPPER()),
                Field('descricao', 'text', label='Descrição',requires = IS_UPPER()),
                format='%(nome)s')
db.define_table('pre_cadastro',
                Field('nome', 'string', label='Nome',requires = IS_UPPER()),
                Field('cpf', 'string', label='CPF',requires = IS_UPPER()),
                Field('telefone', 'string', label='Telefone',requires = IS_UPPER()),
                Field('obs', 'text', label='Observações',requires = IS_UPPER()),
                format='%(nome)s')
db.define_table('pessoa',
                Field('tipo_pessoa', 'string', default='FÍSICA',requires=IS_IN_SET(['JURIDICA', 'FÍSICA'])),
                Field('nome', 'string', label='N.C/R.S',requires = IS_UPPER()),
                Field('cpf', 'string', label='CPF/CNPJ',requires = IS_UPPER()),
                Field('rg', 'string', label='RG',requires = IS_UPPER()),
                Field('telefone', 'string',requires = IS_UPPER()),
                Field('uf', 'string', label='UF', default='CE', requires=IS_IN_SET(['RO','AC','AM','RR','PA','AP','TO','MA','PI','CE','RN','PB','PE','AL','SE','BA','MG','ES','RJ','SP','PR','SC','RS','MS','MT','GO','DF'])),
                Field('cidade', 'string',default='JUAZEIRO DO NORTE', requires = IS_UPPER()),
                Field('bairro', 'string', requires = IS_UPPER()),
                Field('cep', 'string', default='63050-000',requires = IS_UPPER()),
                Field('lougradouro', 'string',default='RUA/AV', requires = IS_UPPER()),
                Field('numero', 'string', requires = IS_UPPER()),
                Field('complemento', 'string', requires = IS_UPPER()),
                format='%(nome)s')
db.define_table('imovel',
                Field('tipo', 'string', default='RESIDENCIAL',requires=IS_IN_SET(['COMERCIAL', 'RESIDENCIAL'])),
                Field('subtipo', 'string', default='CASA',requires=IS_IN_SET(['APART. HOTEL', 'APARTAMENTO', 'DUPLEX', 'CASA', 'CHÁCARA', 'FLAT','GALPÃO', 'KITNET', 'PRÉDIO', 'TERRENO'])),
                Field('uf', 'string', label='UF', default='CE', requires=IS_IN_SET(['RO','AC','AM','RR','PA','AP','TO','MA','PI','CE','RN','PB','PE','AL','SE','BA','MG','ES','RJ','SP','PR','SC','RS','MS','MT','GO','DF'])),
                Field('cidade', 'string',default='JUAZEIRO DO NORTE', requires = IS_UPPER()),
                Field('bairro', 'string', requires = IS_UPPER()),
                Field('cep', 'string', default='63050-000',requires = IS_UPPER()),
                Field('lougradouro', 'string',default='RUA/AV', requires = IS_UPPER()),
                Field('numero', 'string', requires = IS_UPPER()),
                Field('complemento', 'string', requires = IS_UPPER()),
                Field('preco', 'double',label="Preço", notnull=True, default=0),
                Field('disponivel', 'boolean', writable=False, readable=False, default=True),
                format='%(subtipo)s %(lougradouro)s  %(numero)s')

db.define_table('contrato_aluguel',
                Field('imovel','reference imovel', label='Imovel', notnull=True),
                Field('locador','reference pessoa', label='Locador', notnull=True),
                Field('locatario','reference pessoa', label='Locatário', notnull=True),
                Field('avalista','reference pessoa', label='Fiador'),
                Field('tipo', 'string', default='RESIDENCIAL',requires=IS_IN_SET(['COMERCIAL', 'RESIDENCIAL']), notnull=True),

                Field('virgencia_meses', 'integer', label='Vigência em Meses', notnull=True, default=12, requires=IS_IN_SET([6,12,24,36,48,60,120])),
                Field('data_inicial', 'date', label="Data Inicial", default=request.now, requires = IS_DATE(format=('%d-%m-%Y')), notnull=True),
                Field('data_final', 'date', label="Data Final", writable=False, readable=False, default=request.now, requires = IS_DATE(format=('%d-%m-%Y')), notnull=True),
                Field('dia_vencimento', 'integer', label='Dia do Vencimento', writable=False, readable=False, notnull=True, default=5, requires=IS_IN_SET([5,10,15,20,25,30])),
                Field('valor', 'double', label='Valor do Aluguel', notnull=True, default=0),
                Field('valor_ext', 'string', label='Valor Escrito', notnull=True, default="",requires = IS_UPPER()),
                Field('local_contrato', 'string', default='Juazeiro do Norte - CE',requires = IS_UPPER(), notnull=True),
                Field('data_contrato', 'date', label="Data do Contrato", default=request.now, requires = IS_DATE(format=('%d-%m-%Y')), notnull=True),
                Field('finalizado', 'boolean', writable=False, readable=False, default=True),
                )

db.contrato_aluguel.locador.requires = IS_IN_DB(db(db.pessoa.id== 1), 'pessoa.id', '%(nome)s')

db.contrato_aluguel.locatario.requires = IS_IN_DB(db((db.pessoa.id!= 51) & (db.pessoa.id!= 1)), 'pessoa.id', '%(nome)s')

db.contrato_aluguel.avalista.requires = IS_IN_DB(db(db.pessoa.id!=1), 'pessoa.id', '%(nome)s')

db.define_table('recebimento',
                Field('imovel','reference imovel', label='Imovel', writable=False, readable=True),
                Field('contrato_aluguel','reference contrato_aluguel', label='Contrato de Aluguel', writable=False, readable=False),
                Field('data_vencimento', 'date', writable=False, readable=True, label="Data Vencimento", default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('tipo_pagamento', 'string', default='DINHEIRO',requires=IS_IN_SET(['DINHEIRO', 'CARTÃO', 'DEPÓSITO'])),
                Field('data_pagamento', 'date', label="Data Pagamento", default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),

                Field('valor', 'double', writable=False, readable=True, label='Valor do Aluguel', notnull=True, default=0),

                Field('juros', 'double', label='Valor dos Juros', notnull=True, default=0),
                Field('obs', 'string', label='Observação',default='#'),
                Field('quitado', 'boolean', writable=True, readable=False, default=False),
                format='%(nome)s')

db.define_table('despesa',
                Field('imovel','reference imovel', label='Imovel', writable=False, readable=True),
                Field('data_pagamento', 'date', label="Data", default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('descricao', 'string', label='Descrição',default='Descrição'),
                Field('valor', 'double', label='Valor', notnull=True, default=0),
                format='%(descricao)s')
