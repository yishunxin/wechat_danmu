# -*- coding:utf-8 -*-
__author__ = 'weijingqi'

import json

from sqlalchemy.orm.attributes import InstrumentedAttribute

'''
@brief:从表单变成model, item_class 是类，如Student
'''


def formtomodel(form, item_class):
    item = item_class()
    attrs = dir(item)
    for attr in attrs:
        if attr.startswith('_'):
            continue
        if attr in form:
            if form[attr] and (not isinstance(form[attr], basestring) or len(form[attr].strip()) > 0):
                setattr(item, attr, form[attr])
    return item


'''
@brief:json转换成item
'''


def jsontomodel(json_str, item_class):
    if not json_str:
        return item_class()
    data = json.loads(json_str)
    return dicttomodel(data, item_class)


def jsontomodellist(json_str, item_class):
    if not json_str:
        return []
    items = list()
    datas = json.loads(json_str)
    for data in datas:
        item = dicttomodel(data, item_class)
        items.append(item)
    return items


def dicttomodel(t_dict, item_class):
    item = item_class()
    attrs = dir(item)
    for attr in attrs:
        if attr.startswith('_'):
            continue
        if attr in t_dict:
            setattr(item, attr, t_dict[attr])
    return item


def jsonstr2model(jsonstr, item_class):
    t_data = json.loads(jsonstr)
    return dicttomodel(t_data, item_class)


'''
@brief:从表单变成model列表, item_class 是类，如Student
students[0].age 是表单的input name
students[1].age 是表单的input name
form_arrname 是students
'''


def formtomodellist(form, form_arrname, item_class, max_cnt):
    item = item_class()
    attrs = dir(item)
    has_item = False
    items = list()
    for i in range(0, max_cnt):
        for attr in attrs:
            if attr.startswith('_'):
                continue
            form_attr = "%s[%d].%s" % (form_arrname, i, attr)
            if form_attr in form:
                if form[form_attr] > 0:
                    setattr(item, attr, form[form_attr])
                    has_item = True
        if has_item:
            items.append(item)
            item = item_class()
            has_item = False
    return items


'''
@brief:将item的所有属性转换为key,value，可以在将model序列化为json的时候用
'''


def model_todict(item):
    item_dict = dict()
    for k, v in vars(item).iteritems():
        if k.startswith('_'):
            continue
        item_dict[k] = v
    return item_dict


'''
@brief:将item的所有属性转换为key,value，可以在将model序列化为json的时候用
'''


def models_todict(items):
    item_dicts = list()
    for item in items:
        item_dicts.append(model_todict(item))
    return item_dicts


'''
@brief:将item中的db.Column变成普通的dict, 可以在update中用
'''


def model_todbdict(item):
    item_dict = dict()
    for attr in type(item).__dict__.iteritems():
        field_name = attr[0]
        if isinstance(attr[1], InstrumentedAttribute):
            item_dict[field_name] = getattr(item, field_name)
    return item_dict


def pop_key(t_dict, key):
    if key in t_dict:
        t_dict.pop(key)
