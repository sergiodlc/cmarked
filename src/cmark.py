#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Example for using the shared library from python
# Will work with either python 2 or python 3
# Requires cmark library to be installed

#from ctypes import CDLL, c_char_p, c_long
from ctypes import *
import sys
import platform

sysname = platform.system()

if sysname == 'Darwin':
    libname = "libcmark.dylib"
elif sysname == 'Windows':
    libname = "cmark.dll"
else:
    libname = "libcmark.so"
cmark = CDLL(libname)

markdown = cmark.cmark_markdown_to_html
markdown.restype = c_char_p
markdown.argtypes = [c_char_p, c_long, c_long]

opts = 0 # defaults

def md2html(text):
    if sys.version_info >= (3,0):
        textbytes = text.encode('utf-8')
        textlen = len(textbytes)
        return markdown(textbytes, textlen, opts).decode('utf-8')
    else:
        textbytes = text
        textlen = len(text)
        return markdown(textbytes, textlen, opts)


class NotImplemented(Structure):
    pass



class Chunk(Structure):
    _fields_ = [
            ('data', POINTER(c_ubyte)),
            ('len', c_int32),
            ('alloc', c_int32),
            ]

class StrBuf(Structure):
    _fields_ = [
            ('mem', POINTER(NotImplemented)),
            ('ptr', POINTER(c_ubyte)),
            ('asize', c_int32),
            ('size', c_int32),
            ]

class List(Structure):
    _fields_ = [
            ('list_type', c_int),
            ('marker_offset', c_int),
            ('padding', c_int),
            ('start', c_int),
            ('delimiter', c_int),
            ('bullet_char', c_ubyte),
            ('tight', c_bool),
            ]

class Code(Structure):
    _fields_ = [
            ('info', Chunk),
            ('literal', Chunk),
            ('fence_length', c_uint8),
            ('fence_offset', c_uint8),
            ('fence_char', c_ubyte),
            ('fenced', c_int8),
            ]

class Heading(Structure):
    _fields_ = [
            ('level', c_int),
            ('setext', c_bool),
            ]

class Link(Structure):
    _fields_ = [
            ('url', Chunk),
            ('title', Chunk),
            ]

class Custom(Structure):
    _fields_ = [
            ('on_enter', Chunk),
            ('on_exit', Chunk),
            ]

class NodeAs(Union):
    _fields_ = [
            ('literal', Chunk),
            ('list', List),
            ('code', Code),
            ('heading', Heading),
            ('link', Link),
            ('custom', Custom),
            ('html_block_type', c_int),
            ]

class Node(Structure):
    pass

Node._fields_ = [
    ('content', StrBuf),
    ('next', POINTER(Node)),
    ('prev', POINTER(Node)),
    ('parent', POINTER(Node)),
    ('first_child', POINTER(Node)),
    ('last_child', POINTER(Node)),
    ('user_data', c_void_p),
    ('start_line', c_int),
    ('start_column', c_int),
    ('end_line', c_int),
    ('end_column', c_int),
    ('type', c_uint16),
    ('flags', c_uint16),
    ('as', NodeAs),
]

class IterState(Structure):
    _fields_ = [
            ('ev_type', c_int),
            ('node', POINTER(Node)),
            ]

class Iter(Structure):
    _fields_ = [
            ('mem', POINTER(NotImplemented)),
            ('root', POINTER(Node)),
            ('cur', IterState),
            ('next', IterState),
            ]

parse_document = cmark.cmark_parse_document
parse_document.restype = POINTER(Node)
#parse_document.restype = Node
parse_document.argtypes = [c_char_p, c_long, c_long]

render_html = cmark.cmark_render_html
render_html.restype = c_char_p
render_html.argtypes = [POINTER(Node), c_long]

node_free = cmark.cmark_node_free
node_free.restype = None
node_free.argtypes = [POINTER(Node)]

node_get_literal = cmark.cmark_node_get_literal
node_get_literal.restype = c_char_p
node_get_literal.argtypes = [POINTER(Node)]

node_get_type_string = cmark.cmark_node_get_type_string
node_get_type_string.restype = c_char_p
node_get_type_string.argtypes = [POINTER(Node)]

iter_new = cmark.cmark_iter_new
iter_new.restype = POINTER(Iter)
iter_new.argtypes = [POINTER(Node)]

iter_next = cmark.cmark_iter_next
iter_next.restype = c_int
iter_next.argtypes = [POINTER(Iter)]

iter_free = cmark.cmark_iter_free
iter_free.restype = None
iter_free.argtypes = [POINTER(Iter)]

iter_get_node = cmark.cmark_iter_get_node
iter_get_node.restype = POINTER(Node)
iter_get_node.argtypes = [POINTER(Iter)]

CMARK_EVENT_NONE, CMARK_EVENT_DONE, CMARK_EVENT_ENTER, CMARK_EVENT_EXIT = 0, 1, 2, 3
def event_type(ev):
    return {0: 'CMARK_EVENT_NONE', 1: 'CMARK_EVENT_DONE', 2: 'CMARK_EVENT_ENTER', 3: 'CMARK_EVENT_EXIT'}[ev]


def traverse(text):
    utext = text.encode('utf-8')
    doc = parse_document(utext, len(utext), 0)

    # Traverse the tree:
    it = iter_new(doc)
    ev_type = iter_next(it)
    while ev_type != CMARK_EVENT_DONE:
        node = iter_get_node(it)
        # Process the node:
        print("Literal:", node_get_literal(node))
        print("\tType string:\t", node_get_type_string(node))
        print("\tEvent type:\t", event_type(ev_type))
        print("\tFrom:\t(" + str(node.contents.start_line) + ", " + str(node.contents.start_column) + ")")
        print("\tTo:\t(" + str(node.contents.end_line) + ", " + str(node.contents.end_column) + ")")

        ev_type = iter_next(it)
    iter_free(it)
