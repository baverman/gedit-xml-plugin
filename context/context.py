# -*- coding: utf-8 -*-

import re

class Node(object):
    def __init__(self, parent, start, name, end):
        self.parent = parent
        self.start = start
        self.name = name
        self.end = end
        self.open_node = None

class TagCloseContext(object):
    def __init__(self, open_tag_name):
        self.open_tag_name = open_tag_name

class TagOpenContext(object):
    def __init__(self, partial_name, context):
        self.partial_name = partial_name
        self.context = context

def get_position(line, column, xml):
    pos = 0
    for i, l in enumerate(xml.splitlines(True)):
        if i + 1 < line:
            pos += len(l)
        else:
            return pos + column
            
    return pos

def get_context(xml, end_position):
    comments = []
    
    def is_in_comment(tag_pos):
        for start, end in comments:
            if start <= tag_pos <= end:
                return True
                
        return False
    
    for match in re.finditer(u'(?is)<!--.*?-->', xml):
        comments.append((match.start(), match.end()))
    
    parent = None
    current = None
    for match in re.finditer(u'(?isu)(<\?|(</|<)(?P<tag>[a-z0-9_:]*))', xml):
        tag = match.group()
        tag_pos = match.start()
        
        if is_in_comment(tag_pos): continue         
        
        if tag[1] == '?': continue
        
        if tag_pos > end_position: break

        tag_name = match.group('tag').lower()
        
        if tag[1] == '/':
            is_open = False
            tag_end_pos = match.end() + 1
        else:
            full_close_pos = xml.find('/>', tag_pos)
            semi_close_pos = xml.find('>', tag_pos)
            
            if full_close_pos < semi_close_pos:
                is_open = None
                tag_end_pos = full_close_pos + 2
            else:
                is_open = True                
                tag_end_pos = semi_close_pos + 1

        if is_open:
            if tag_pos + len(tag_name) >= end_position:
                tag_name = tag_name[:end_position - tag_pos - 1]
            current = parent = Node(parent, tag_pos, tag_name, tag_end_pos)
        elif is_open == False:
            old_parent = parent
            parent = parent.parent
            current = Node(parent, tag_pos, tag_name, tag_end_pos)
            current.open_node = old_parent 
        elif is_open is None and tag_end_pos > end_position:
            current = Node(parent, tag_pos, tag_name, tag_end_pos)
        
    return current

def guess_context(line, column, xml):
    if not  isinstance(xml, unicode):
        raise Exception('I can handle only unicode data')

    end_position = get_position(line, column, xml)
    
    node = get_context(xml, end_position)
    
    if node.open_node:
        return TagCloseContext(node.open_node.name)
    
    context = []
    current = node
    
    node = node.parent
    while(node):
        context.insert(0, node.name)
        node = node.parent
        
    return TagOpenContext(current.name, context)  
