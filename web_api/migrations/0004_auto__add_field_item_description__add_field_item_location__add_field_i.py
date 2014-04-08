# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Item.description'
        db.add_column(u'web_api_item', 'description',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Item.location'
        db.add_column(u'web_api_item', 'location',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True),
                      keep_default=False)

        # Adding field 'Item.tags'
        db.add_column(u'web_api_item', 'tags',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Item.lat'
        db.add_column(u'web_api_item', 'lat',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=256, blank=True),
                      keep_default=False)

        # Adding field 'Item.lon'
        db.add_column(u'web_api_item', 'lon',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=256, blank=True),
                      keep_default=False)

        # Adding field 'Item.is_email'
        db.add_column(u'web_api_item', 'is_email',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Item.description'
        db.delete_column(u'web_api_item', 'description')

        # Deleting field 'Item.location'
        db.delete_column(u'web_api_item', 'location')

        # Deleting field 'Item.tags'
        db.delete_column(u'web_api_item', 'tags')

        # Deleting field 'Item.lat'
        db.delete_column(u'web_api_item', 'lat')

        # Deleting field 'Item.lon'
        db.delete_column(u'web_api_item', 'lon')

        # Deleting field 'Item.is_email'
        db.delete_column(u'web_api_item', 'is_email')


    models = {
        u'web_api.claimeditememail': {
            'Meta': {'object_name': 'ClaimedItemEmail'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['web_api.Item']", 'symmetrical': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'received': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web_api.EmailThread']"})
        },
        u'web_api.emailthread': {
            'Meta': {'object_name': 'EmailThread'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'web_api.item': {
            'Meta': {'object_name': 'Item'},
            'claimed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'lon': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'post_email': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web_api.NewPostEmail']"}),
            'tags': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web_api.EmailThread']", 'null': 'True'})
        },
        u'web_api.newpostemail': {
            'Meta': {'object_name': 'NewPostEmail'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'received': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web_api.EmailThread']"})
        }
    }

    complete_apps = ['web_api']