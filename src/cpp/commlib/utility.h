/*
 * utility.h
 *
 *  Created on: 2017�~8��20��
 *      Author: kchung
 */

#pragma once
#include "std_lib_inc.h"
#define show(x) cout << (#x) << " = " << (x) << endl;
#define disp(x) cout << (x) << endl;

template <class OUT_t, class IN_t>
OUT_t &access_buf_t(IN_t *b, size_t i) {
    assert(b->d == 1 && b->l > i);
    return b->v[i];
}
template <class OUT_t, class IN_t>
OUT_t &access_buf_t(IN_t *b, size_t r, size_t c) {
    assert(b->d == 2 && b->r > r && b->c > c);
    return b->v[r * b->c + c];
}

inline double &fbuf(fbuf_t *b, size_t i) { return access_buf_t<double, fbuf_t>(b, i); }
inline cpx_t &cbuf(cbuf_t *b, size_t i) { return access_buf_t<cpx_t, cbuf_t>(b, i); }
inline int &ibuf(ibuf_t *b, size_t i) { return access_buf_t<int, ibuf_t>(b, i); }
inline int &bbuf(bbuf_t *b, size_t i) { return access_buf_t<int, bbuf_t>(b, i); }
inline double &fbuf(fbuf_t *b, size_t r, size_t c) { return access_buf_t<double, fbuf_t>(b, r, c); }
inline int &ibuf(ibuf_t *b, size_t r, size_t c) { return access_buf_t<int, ibuf_t>(b, r, c); }
inline int &bbuf(bbuf_t *b, size_t r, size_t c) { return access_buf_t<int, bbuf_t>(b, r, c); }
