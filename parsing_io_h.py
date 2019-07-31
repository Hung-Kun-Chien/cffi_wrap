def remove_mark_region(lines):
    a = [i for i, l in enumerate(lines) if l.startswith('/*')]
    b = [
        i for i, l in enumerate(lines) if l.startswith('*') and l.endswith('/')
    ]
    mask_ind = []
    for s, e in zip(a, b):
        mask_ind += lines[s:(e + 1)]
    for a in mask_ind:
        lines.remove(a)
    return lines


def get_ctype(sss):
    if sss.find('*') != -1:
        ctype = sss.split('*')[0].replace(' ', '')
        name = sss.split('*')[1].replace(' ', '')
        if (ctype.startswith('vec')
                and ctype.endswith('t')) or ctype.endswith('buf_t'):
            pass
        elif ctype == 'char':
            ctype = 'str'
        else:
            ctype = 'var'
    else:
        ctype = sss.split(' ')[0].replace(' ', '')
        name = sss.split(' ')[1].replace(' ', '')
        ctype = 'var'
    return {name: ctype}


def get_ctypes_table(fn):
    with open(fn, 'r') as f:
        lines = [l.lstrip().replace('\n', '') for l in f.readlines()]
        lines = remove_mark_region(lines)
        lines = [
            l for l in lines if len(l) and not (
                l.endswith('{') or l.startswith('}') or l.startswith('//'))
        ]
        lines = [l.split(';')[0].split('/*')[0] for l in lines]
        ctypetable = {}
        for l in lines:
            ctypetable.update(get_ctype(l))
    return ctypetable


if __name__ == '__main__':
    print(get_ctypes_table('aaa.h'))
