#coding=utf-8
#Version: V 1.0
author: 'WangSheng'
date: '2019/5/16 14:52'

def convert(data):

    if isinstance(data, bytes):  return data.decode('ascii')
    if isinstance(data, dict):   return dict(map(convert, data.items()))
    if isinstance(data, tuple):  return map(convert, data)
    return data
