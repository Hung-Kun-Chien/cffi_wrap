import json
import numpy as np
from collections import namedtuple


def dict2class(dictionary, name='dict_class', exclude_list=[]):
    temp = dictionary.copy()
    for key, value in temp.items():
        if isinstance(value, dict) and key not in exclude_list:
            temp[key] = dict2class(value, key, exclude_list)
    return namedtuple(name, temp.keys())(**temp)


class PAR:
    def __init__(self, par=None):
        self._par = {}
        self.non_class_convert_list = []
        self.key_list = []
        if not (par == None):
            self._par = par if isinstance(par, dict) else read_json(par)

    def set(self,
            key,
            value,
            force=False,
            type=None,
            not_convert_to_class=False):
        self.key_list.append(key)
        if not_convert_to_class == True:
            self.non_class_convert_list.append(key)

        if force:
            self._par[key] = value
        elif key.replace('.', '_') in self._par.keys():
            self._par[key] = self._par.pop(key.replace('.', '_'))
            if self._par[key] is None:
                self._par[key] = value
            else:
                self._par[key] = self._par[key]
        elif key in self._par.keys():
            if self._par[key] is None:
                self._par[key] = value
            else:
                self._par[key] = self._par[key]
        else:
            self._par[key] = value

        if type is not None:
            if not type == dict:
                assert not isinstance(
                    self._par[key],
                    dict), '{}={} is dict, should not set to type={}'.format(
                        key, self._par[key], type)
            if isinstance(type, list):
                assert self._par[key] in type, '{}={} not in {}'.format(
                    key, self._par[key], type)
            if type in [str, int, float]:
                if isinstance(self._par[key], list):
                    self._par[key] = [type(a) for a in self._par[key]]
                else:
                    self._par[key] = type(self._par[key])

        return self._par[key]

    def get(self, key=None):
        if not (key == None):
            if key in self.key_list:
                return self._par[key]
            else:
                return None
        else:
            return {k: v for k, v in self._par.items() if k in self.key_list}

    def get_dict(self, key=None):
        return dict_wrap(self.get(key))

    def get_class(self, key=None):
        return dict2class(self.get_dict(key),
                          exclude_list=self.non_class_convert_list)

    def save(self, fn):
        save_json(fn, self.get(), indent=4, sort_keys=True)


def dict_wrap(d_in):
    d_out = {}
    for k, v in d_in.items():
        d = d_out
        k_list = k.split('.')
        for i, ksub in enumerate(k_list):
            if ksub in d.keys():
                d = d[ksub]
                assert isinstance(
                    d, dict
                ), 'dict_extend error: key="{}" naming comflict'.format(ksub)
            else:
                if i == len(k_list) - 1: d.update({ksub: v})  ## assign value
                else: d.update({ksub: {}})  ## placeholder
                d = d[ksub]
    return d_out


def save_json(fn, x, indent=4, sort_keys=False):
    if not fn.endswith('.json'): fn = fn + '.json'
    with open(fn, 'w') as file:
        file.write(
            json.dumps(x,
                       indent=indent,
                       sort_keys=sort_keys,
                       ensure_ascii=True))
