
#-*- encoding: utf-8 -*-
from django.db import models

class Database_entries(models.Model):
  prd_nm = models.CharField(db_column='__prd_nm__', max_length=96)
  url = models.CharField(max_length=768, db_column='__org_img_url__', blank=True)
  label = models.IntegerField(null=True, db_column='label', blank=True)
  lctgr_nm = models.CharField(max_length=64, db_column='__lctgr_nm__', blank=True)
  mctgr_nm = models.CharField(max_length=64, db_column='__mctgr_nm__', blank=True)
  sctgr_nm = models.CharField(max_length=64, db_column='__sctgr_nm__', blank=True)
  tag = models.CharField(max_length=64, db_column='__tag__', blank=True)
  gender = models.CharField(max_length=4, db_column='__gender_ctgr__', blank=True)

  class Meta:
    db_table = u'11st_julia'
