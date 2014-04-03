# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Item'
        db.create_table(u'web_api_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('post_email', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_api.NewPostEmail'])),
            ('claimed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_api.EmailThread'], null=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'web_api', ['Item'])

        # Adding model 'ClaimedItemEmail'
        db.create_table(u'web_api_claimeditememail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('received', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_api.EmailThread'])),
        ))
        db.send_create_signal(u'web_api', ['ClaimedItemEmail'])

        # Adding M2M table for field items on 'ClaimedItemEmail'
        m2m_table_name = db.shorten_name(u'web_api_claimeditememail_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('claimeditememail', models.ForeignKey(orm[u'web_api.claimeditememail'], null=False)),
            ('item', models.ForeignKey(orm[u'web_api.item'], null=False))
        ))
        db.create_unique(m2m_table_name, ['claimeditememail_id', 'item_id'])

        # Adding model 'EmailThread'
        db.create_table(u'web_api_emailthread', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'web_api', ['EmailThread'])

        # Adding model 'NewPostEmail'
        db.create_table(u'web_api_newpostemail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('received', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_api.EmailThread'])),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'web_api', ['NewPostEmail'])


    def backwards(self, orm):
        # Deleting model 'Item'
        db.delete_table(u'web_api_item')

        # Deleting model 'ClaimedItemEmail'
        db.delete_table(u'web_api_claimeditememail')

        # Removing M2M table for field items on 'ClaimedItemEmail'
        db.delete_table(db.shorten_name(u'web_api_claimeditememail_items'))

        # Deleting model 'EmailThread'
        db.delete_table(u'web_api_emailthread')

        # Deleting model 'NewPostEmail'
        db.delete_table(u'web_api_newpostemail')


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
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'web_api.item': {
            'Meta': {'object_name': 'Item'},
            'claimed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'post_email': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web_api.NewPostEmail']"}),
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