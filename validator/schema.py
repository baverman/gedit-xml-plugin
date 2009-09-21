# -*- coding: utf-8 -*-

from lxml import etree


class SchemaNotFoundException(Exception): pass


class SchemaValidator(object):
    def __init__(self, root, catalog):
        self.catalog = catalog
        self.root = root
        self.schema = self.get_schema(root)


    def get_xsd_filename_for_ns(self, ns):
        try:
            return self.catalog[ns]
        except KeyError:
            raise SchemaNotFoundException("Can't find xsd for [%s] namespace" % ns)
        
    
    def get_schema(self, root):
        merged_schema = \
            '<?xml version="1.0"?>' \
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" ' \
            'targetNamespace="http://global.namespace" ' \
            'xmlns="http://global.namespace" ' \
            'elementFormDefault="qualified">' \
        
        for ns in root.nsmap.values():
            filename = self.get_xsd_filename_for_ns(ns)
            merged_schema += '<xs:import schemaLocation="file://%s" />' % filename
            
        merged_schema += '</xs:schema>'
        
        return etree.XMLSchema(etree.XML(merged_schema))
        
    def validate(self):
        return self.schema.validate(self.root)
        
    def get_error_log(self):
        return self.schema.error_log
        
    error_log = property(get_error_log)
