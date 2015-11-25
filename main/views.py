
# Create your views here.
# -*- coding: UTF-8 -*-

from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.template import Context
from django.http import HttpResponse
from django.core.paginator import Paginator
from main.models import Database_entries
from django.db import connection
from django.db import models
import collections

PAGE_PER_CONTENT = 10 * 2
Param = collections.namedtuple('Param',
                               'page_no filter_type lctgr_nm mctgr_nm sctgr_nm tag')
OptionValues = {'filter_type': ['all', '0', '1', '-1'],
                'lctgr_nm': ['all'],
                'mctgr_nm': ['all'],
                'sctgr_nm': ['all'],
                'tag': ['all']
                }


def parse_parameter(request):
  """
  parse GET paratmers:
  page_no filter_type lctgr_nm mctgr_nm sctgr_nm tag
  
  """
  page_no = int(request.GET.get('page_no', 1))
  filter_type = request.GET.get('filter_type', 'all')
  lctgr_nm = request.GET.get('lctgr_nm', 'all')
  mctgr_nm = request.GET.get('mctgr_nm', 'all')
  sctgr_nm = request.GET.get('sctgr_nm', 'all')
  tag = request.GET.get('tag', 'all')
  
  return Param(page_no=page_no,
         filter_type=filter_type,
         lctgr_nm=lctgr_nm,
         mctgr_nm=mctgr_nm,
         sctgr_nm=sctgr_nm,
         tag=tag
         )


def update_option_values():
  global OptionValues
  cursor = connection.cursor()
  cursor.execute("SET NAMES \'utf8\'")
  cursor.execute('SELECT DISTINCT __lctgr_nm__ FROM 11st_julia')
  lctgr_nm_list = cursor.fetchall()
  lctgr_nm_list = ['all'] + [unicode(lctgr_nm[0]) for lctgr_nm in lctgr_nm_list]
  OptionValues['lctgr_nm'] = lctgr_nm_list
  cursor.execute('SELECT DISTINCT __mctgr_nm__ FROM 11st_julia')
  mctgr_nm_list = cursor.fetchall()
  mctgr_nm_list = ['all'] + [unicode(mctgr_nm[0]) for mctgr_nm in mctgr_nm_list]
  OptionValues['mctgr_nm'] = mctgr_nm_list
  cursor.execute('SELECT DISTINCT __sctgr_nm__ FROM 11st_julia')
  sctgr_nm_list = cursor.fetchall()
  sctgr_nm_list = ['all'] + [unicode(sctgr_nm[0]) for sctgr_nm in sctgr_nm_list]
  OptionValues['sctgr_nm'] = sctgr_nm_list
  cursor.execute('SELECT DISTINCT __tag__ FROM 11st_julia')
  tag_list = cursor.fetchall()
  tag_list = ['all'] + [unicode(tag[0]) for tag in tag_list]
  OptionValues['tag'] = tag_list
  
  
def get_records(param):
  print param
  records = Database_entries.objects.all()
  #records = Database_entries.objects.order_by('-RalphRaurenScore')
  # add
  #records = records.filter(isUnique='1')
  if param.filter_type != 'all':
    records = records.filter(label=int(param.filter_type))
  if param.lctgr_nm != 'all':
    records = records.filter(lctgr_nm=unicode(param.lctgr_nm))
  if param.mctgr_nm != 'all':
    records = records.filter(mctgr_nm=unicode(param.mctgr_nm))
  if param.sctgr_nm != 'all':
    records = records.filter(sctgr_nm=unicode(param.sctgr_nm))
  if param.tag != 'all':
    records = records.filter(tag=unicode(param.tag))
  return records
  

def listing(request):
  """  get current page's results  """
  param = parse_parameter(request)

  #if param.page_no is -1:
  #  update_option_values()
  update_option_values()

  records = get_records(param)
  # adjust page number note: Paginator use 1-based index
  paginator = Paginator(records, PAGE_PER_CONTENT)
  if param.page_no is -1:
    param = param._replace(page_no=paginator.num_pages)
  return paginator.page(param.page_no), paginator.num_pages, param


def main(request):
  page_records, page_no_max, param = listing(request)
  
  t = get_template('style.html')
  style_html = t.render(Context({}))

  t = get_template('pagination.html')
  print param.page_no, page_no_max
  pagination_html = t.render(Context({'page_no': param.page_no,
                    'page_no_next': param.page_no+1,
                    'page_no_prev': param.page_no-1,
                    'page_no_max': page_no_max,
                    'page_list':
                      [p for p in range(param.page_no-4, param.page_no+5) \
                        if p > 0 and p <= page_no_max]}))

  t = get_template('option.html')
  option_html = t.render(Context({
                                  'filter_type': OptionValues['filter_type'],
                                  'lctgr_nm': OptionValues['lctgr_nm'],
                                  'mctgr_nm': OptionValues['mctgr_nm'],
                                  'sctgr_nm': OptionValues['sctgr_nm'],
                                  'tag': OptionValues['tag'],
                                  'selected_filter_type': param.filter_type,
                                  'selected_lctgr_nm': param.lctgr_nm,
                                  'selected_mctgr_nm': param.mctgr_nm,
                                  'selected_sctgr_nm': param.sctgr_nm,
                                  'selected_tag': param.tag
                                 }))
  #print option_html
  
  t = get_template('main.html')
  id_list = [int(record.id) for record in page_records]
  main_html = t.render(Context({'records': page_records,
                                'id_list': id_list,
                                'style_html': style_html,
                                'page_html': pagination_html,
                                'option_html': option_html}))

  return HttpResponse(main_html)


def update(request):
  target_id = request.GET.get('id', None)
  command = request.GET.get('command', None)
  if target_id is None or command is None:
    return HttpResponse('{"success":"0", "msg":"FAIL"}')
  record = Database_entries.objects.get(id=target_id)
  if record is None:
    return HttpResponse('{"success":"0", "msg":"FAIL"}')
  if command == 'good':
    record.label = 0
    record.save()
  elif command == 'bad':
    record.label = 1
    record.save()
  elif command == 'unknown':
    record.label = -1 
    record.save()
  return HttpResponse('{"success":"1", "msg":"OK"}')
