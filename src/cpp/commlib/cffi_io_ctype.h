#pragma once

typedef double _Complex cpx_t;

typedef struct{
    size_t l,r,c,d;
    int *v;
} bbuf_t;

typedef struct{
    size_t l,r,c,d;
    double *v;
} fbuf_t;

typedef struct{
    size_t l,r,c,d;
    int *v;
} ibuf_t;

typedef struct{
    size_t l,r,c,d;
    cpx_t* v;
} cbuf_t;

typedef fbuf_t vec_f_t;
typedef bbuf_t vec_b_t;
typedef cbuf_t vec_c_t;
typedef ibuf_t vec_i_t;
