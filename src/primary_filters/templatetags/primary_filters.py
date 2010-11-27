# -*- coding: utf-8 -*-
#
#  This file is part of django-primary-filters.
#
#  django-primary-filters provides some extra filters that are often needed by Django projects.
#
#  Development Web Site:
#    - http://www.codetrax.org/projects/django-primary-filters
#  Public Source Code Repository:
#    - https://source.codetrax.org/hgroot/django-primary-filters
#
#  Copyright 2010 George Notaras <gnot [at] g-loaded.eu>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import re
from BeautifulSoup import BeautifulSoup, Comment

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()



@register.filter
@stringfilter
def dash2space(value):
    return value.replace('-', ' ')
    
@register.filter
@stringfilter
def space2dash(value):
    return value.replace(' ', '-')


@register.filter
@stringfilter
def strfdt(value, arg):
    """Example Filter
    
    Use with:
    
        {% load primary_blog_tags %}
        ...
        {{ entry.date_published|strfdt:"%A, %d %B" }}
        ...
        
    """
    return value + '--' + arg




re_hyperlink = re.compile('<a ', re.UNICODE | re.IGNORECASE)

@register.filter
@stringfilter
def nofollowlinks(value):
    """Adds the nofollow attribute to hyperlinks
    
    Use with:
    
        {% load primary_blog_tags %}
        ...
        {{ comment.comment|nofollowlinks }}
        ...
        
    """
    return re_hyperlink.sub('<a rel="nofollow" ', value)



@register.filter
def sanitize(value, allowed_tags):
    """Strips all HTML tags except those in the 'allowed_tags' list.
    
    Argument should be in form 'tag2:attr1:attr2 tag2:attr1 tag3', where tags
    are allowed HTML tags, and attrs are the allowed attributes for that tag.
    
    Requires: BeautifulSoup
    
    Taken from:
    
        http://www.djangosnippets.org/snippets/1655/
    
    Also see:
    
        http://www.djangosnippets.org/snippets/205/#c2355
    
    """
    js_regex = re.compile(r'[\s]*(&#x.{1,7})?'.join(list('javascript')))
    allowed_tags = [tag.split(':') for tag in allowed_tags.split()]
    allowed_tags = dict((tag[0], tag[1:]) for tag in allowed_tags)
    #return repr(allowed_tags)
    soup = BeautifulSoup(value)
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()
    
    for tag in soup.findAll(True):
        if tag.name.lower() not in allowed_tags:
            tag.hidden = True
        else:
            tag.attrs = [(attr, js_regex.sub('', val)) for attr, val in tag.attrs
                         if attr.lower() in allowed_tags[tag.name.lower()]]
    
#    for tag in soup.findAll(True):
#        if tag.name not in allowed_tags:
#            tag.hidden = True
#        else:
#            tag.attrs = [(attr, js_regex.sub('', val)) for attr, val in tag.attrs
#                         if attr in allowed_tags[tag.name]]
    
    return soup.renderContents().decode('utf8')


