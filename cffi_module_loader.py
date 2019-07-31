import numpy as np
from cffi import FFI
from utility_lib import PAR
from parsing_io_h import get_ctypes_table
from os.path import isfile, join
import os

proj = 'cffi_lib'
root_path = os.getcwd().replace('\\', '/').split(proj)[0] + proj

str = lambda x: self.new("char[]", x.encode('ascii'))


class module_loader:
    def set_par(self, par_in):
        par = PAR(par_in)
        par.set('name', 'X')
        par.set('io_ctype', 'io_t*')
        par.set('lib_fn', None)
        par.set('wrap_io_h', None)
        par.set('wrap_func_h', None)
        par.set('io_ctype_h',
                root_path + '/src/cpp/commlib/cffi_io_ctype.h',
                force=True)
        par.set('in_ctypes', {}, not_convert_to_class=True)
        par.set('fx_onoff', 'bypass')
        par.set('btr_onoff', 'bypass')
        par.set('im_name', 'a')
        par.set('debug', False)
        self.par = par.get_class()

    def __init__(self, **par):
        self.set_par(par)
        assert (self.par.wrap_io_h is not None)
        assert (self.par.wrap_func_h is not None)
        self.ffi = FFI()
        for fn in [
                self.par.io_ctype_h, self.par.wrap_io_h, self.par.wrap_func_h
        ]:
            with open(fn) as f:
                self.ffi.cdef(f.read(), override=True)

        self.par.in_ctypes.update(get_ctypes_table(self.par.wrap_io_h))
        self.io_ctype = {}
        self.io_dict = {}
        self.io_buf = {}
        self.io2buf_dict = {}
        self.set_io_functs()
        self.load_lib()
        self.set_access_func()
        self.set_ctype(**self.par.in_ctypes)
        self.vec_c = lambda x: self.vec_x(
            x.astype(np.complex128), ctype='double _Complex', xtype='vec_c_t')
        self.vec_f = lambda x: self.vec_x(
            x.astype(np.float64), ctype='double', xtype='vec_c_t')

    def load_lib(self, fn=None):
        if fn is None: fn = self.par.lib_fn
        assert (isfile(fn))
        self.lib = self.ffi.dlopen(fn)

    def set_io_functs(self):
        self.new = lambda ctype, init=None, **var: self.ffi.new(
            ctype, init, **var)
        self.to_str = lambda x: self.ffi.string(x)
        self.str = lambda x: self.new("char[]", x.encode('ascii'))

        rmd = lambda x: {k: v for k, v in x.items() if k != 'dat'}
        new_buf = lambda x, k: self.new('%s*' % k, rmd(x))

        self.newbuf_dict = {"var": lambda x: x}
        self.io2buf_dict = {"var": lambda x: x}
        self.newbuf_dict['str'] = self.str
        self.io2buf_dict['str'] = lambda x: str(x)
        self.io2buf_dict['vec_c_t'] = lambda x: self.x2buf(
            x, np.complex128, 'double _Complex')
        self.io2buf_dict['vec_f_t'] = lambda x: self.x2buf(
            x, np.float64, 'double')
        self.io2buf_dict['vec_i_t'] = lambda x: self.x2buf(x, np.int32, 'int')
        self.io2buf_dict['vec_b_t'] = lambda x: self.x2buf(x, np.int32, 'int')
        self.io2buf_dict['cbuf_t'] = lambda x: self.x2buf(
            x, np.complex128, 'double _Complex')
        self.io2buf_dict['fbuf_t'] = lambda x: self.x2buf(
            x, np.float64, 'double')
        self.io2buf_dict['bbuf_t'] = lambda x: self.x2buf(x, np.int32, 'int')
        self.io2buf_dict['ibuf_t'] = lambda x: self.x2buf(x, np.int32, 'int')

        self.newbuf_dict['vec_c_t'] = lambda x: new_buf(x, 'vec_c_t')
        self.newbuf_dict['vec_f_t'] = lambda x: new_buf(x, 'vec_f_t')
        self.newbuf_dict['vec_i_t'] = lambda x: new_buf(x, 'vec_i_t')
        self.newbuf_dict['vec_b_t'] = lambda x: new_buf(x, 'vec_b_t')
        self.newbuf_dict['cbuf_t'] = lambda x: new_buf(x, 'cbuf_t')
        self.newbuf_dict['fbuf_t'] = lambda x: new_buf(x, 'fbuf_t')
        self.newbuf_dict['ibuf_t'] = lambda x: new_buf(x, 'ibuf_t')
        self.newbuf_dict['bbuf_t'] = lambda x: new_buf(x, 'bbuf_t')

        self.cpx = lambda x, y=0.0: self.new("double _Complex *", x + y * 1j)
        self.newbuf_dict['cpx_t'] = self.cpx
        self.io2buf_dict['cpx_t'] = lambda x: complex(x)

        self.newbuf = lambda k: self.newbuf_dict[self.io_ctype[k]]
        self.io2buf = lambda k: self.io2buf_dict[self.io_ctype[k]]

    def x2buf(self, x, datatype, ctype):
        if isinstance(x, list): x = np.array(x)
        if len(x.shape) == 2:
            out = {
                'dat': np.reshape(x.astype(datatype), -1),
                'd': 2,
                'r': x.shape[0],
                'c': x.shape[1]
            }
        else:
            out = {
                'dat': np.reshape(x.astype(datatype), -1),
                'd': 1,
                'l': x.shape[0]
            }
        out['v'] = self.ffi.cast('%s*' % ctype, out['dat'].ctypes.data)
        return out

    def set_access_func(self):
        try:
            self.setup = self.lib.setup
        except:
            print('module %s not found setup function' % self.par.name)
        try:
            self.reset = self.lib.reset
        except:
            print('module %s not found reset function' % self.par.name)

    def run(self, **args):
        self.set_io(**args)
        self.io = self.new(self.par.io_ctype, self.io_dict)
        self.lib.run(self.io)
        return self.get_io()

    def set_ctype(self, **var):
        for k, v in var.items():
            assert (v in self.newbuf_dict.keys()
                    ), "%s = %s not in the valid ctype list=%s" % (
                        k, v, list(self.newbuf_dict.keys()))
        self.io_ctype.update(var)

    def input(self, **var):
        self.io_buf.update({k: self.io2buf(k)(v) for k, v in var.items()})
        self.io_dict.update(
            {k: self.newbuf(k)(self.io_buf[k])
             for k in var.keys()})

    def set_io(self, **var):
        self.input(**var)

    def get_io(self, *args):
        get_arr = lambda x: np.reshape(x['dat'], (x['r'], x['c'])) if x[
            'd'] == 2 else x['dat']
        get_iov = lambda k: get_arr(self.io_buf[k]) if isinstance(
            self.io_buf[k], dict) else self.io_buf[k]
        if len(args) == 1 and args[0] in self.io_buf.keys():
            return get_iov(args[0])
        elif len(args):
            return {k: get_iov(k) for k in args if k in self.io_buf.keys()}
        else:
            return {k: get_iov(k) for k in self.io_buf.keys()}

    def vec_x(self, x, ctype, xtype):
        p = self.ffi.cast('%s*' % ctype, x.ctypes.data)
        return self.new('%s*' % xtype, {'v': p, 'l': len(x)})
