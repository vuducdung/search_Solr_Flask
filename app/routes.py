# -*- coding: utf8 -*-
from __future__ import print_function
from app import app
from app.forms import LoginForm
from flask import render_template, flash, redirect, url_for
from flask_paginate import Pagination, get_page_args
from flask import request
import json

import pysolr


solr = pysolr.Solr('http://localhost:8983/solr/project', timeout=10)


@app.route('/', methods=['GET', 'POST'])
def index(result=""):
    if request.args.get('mail', None):
        result = request.args['mail']    
    results = solr.search(result,rows=100)
    if len(results)==0:
        results= ""
    page = request.args.get('page', 1, type=int)
    pagination = Pagination(
            page=page,
            total=len(results),
            error_out=False,
            record_name='results',
            per_page=10,
            css_framework='bootstrap4'
            ) 
    if len(results)==0:
        return render_template(
            'search.html',
            inputsearch= result,
            )
    else:
        results=list(results)
        return render_template(
            'search.html',
            results=results[(page-1)*10:page*10],
            pagination=pagination,
            page=page,
            len=len(results),
            format_total=True,
            format_number=True,
            per_page=10,
            inputsearch= result,
            )


# @app.route('/',methods=['GET', 'POST'])
# def index():
#     # page = request.args.get(get_page_parameter(), type=int, default=1)
#     form = LoginForm()
#     # search = False
#     # q = request.args.get('q')
#     # if q:
#     #     search = True
        
#     # page = request.args.get('page', 1, type=int)

#     if form.validate_on_submit()  :
       
#         if request.args.get('page'):
#             global text
#             sql = text
#         else:
#             sql = form.search.data
#             text = sql

#         results = solr.search(sql,rows=30) 
#         results=list(results)

#         search = False
#         q = request.args.get('q')
#         if q:
#             search = True
        
#         page = 1
#         # page=int(request.args.getlist('page',1))
#         # page, per_page, offset = get_page_args(page_parameter='page',
#         #     per_page_parameter='per_page')

#         pagination = Pagination(
#             page=page,
#             total=len(results),
#             error_out=False,
#             record_name='results',
#             per_page=10)
#         return render_template('index.html',
#             form=form,
#             results=results[(page-1)*10:page*10],
#             pagination=pagination,
#             page=page,
#             format_total=True,
#             format_number=True,
#             x=request.args.get('page')
#             )   
#     return render_template('search.html', form=form)







  