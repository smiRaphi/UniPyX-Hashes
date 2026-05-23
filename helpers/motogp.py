P = r"<path with executable & extracted files>"
fmt = lambda x:x.lower()
BL = {
    'oBTQR.cheat',
    'BpWF.bin',
    '5UUmBj.revpoints',
    '3DOM.speedopoints',
    'VAC3.params', # ?
    'PCG72.font', # ?
    'B5KBB.pivots',
}

def java_hash(i:bytes):
    h = 0
    for b in i: h = (h * 31 + b) & 0xFFFFFFFF
    return h

import os,re,itertools
def rldir(i:str,files=True) -> list[str]:
    i = str(i)
    o = []
    for x in os.listdir(i):
        x = i + '\\' + x
        if os.path.isfile(x): o.append(x)
        else:
            if not files: o.append(x)
            o += rldir(x,files=files)
    return o

L = set([int(x,16) for x in open('check.list','r').read().split('\n')]) # one hex hash per line
nl = open('motogp.hsh','rb').read().replace(b'\r',b'').split(b'\n')
l = set([java_hash(x.lower()) for x in nl])
nl = set([x.decode('ascii') for x in nl])

def chk(n,prx=True,first=True):
    if n in BL: return

    h = java_hash(fmt(n.encode('ascii')))
    if h in l:
        if prx: print(f'Already in DB | {h:08X}')
    elif h in L:
        print(f'{h:08X} | {n}')
        print('Yay! :D')
        nl.add(n)
        l.add(h)
    else:
        if prx: print('Nay D:')

EXS = {'tex','mesh','xwb','centers','cheat','title','bin','tpage','params','xbx','pivots','font','skeleton','animcoll','animmesh','speedopoints','revpoints','animclipz','bumpmap','particle','stencil','planar'}

if 0:
    for n in nl.copy(): chk(n,False)
if 0:
    while 1:
        i = input(': ')
        if not i: break
        if i.startswith('ds "') and i[-1] == '"': i = i[4:-1].replace('\\\\','\\')
        elif i[0] == i[-1] == '"': i = i[1:-1].replace('\\\\','\\')
        chk(i,True)
if 1:
    rg = re.compile(r'(?:(?<=[\0-,\:-@`\{-\xFF])|^)([a-zA-Z0-9_\-\./\\]{4,64})(?:(?=[\0-,\:-@`\{-\xFF])|$)'.encode())
    fs = rldir(P)
    for f in fs:
        if not os.path.exists(f): continue
        for rr in rg.findall(open(f,'rb').read()):
            for r in rr.replace(b'\\',b'/').split(b'/'):
                try: r = r.decode('ascii');assert r.isprintable()
                except: continue
                chk(r,False)
                for x in EXS:
                    chk(r + '.' + x,False)
                if '.' in r:
                    r = os.path.splitext(r)[0]
                    for x in EXS:
                        chk(r + '.' + x,False)
if 1:
    for n in nl.copy():
        n = os.path.splitext(n)[0]
        chk(n,False)
        for x in EXS: chk(n + '.' + x,False)
if 1:
    for f in rldir(P):
        f = os.path.splitext(f)[0]
        for x in EXS:
            chk(f + '.' + x,False)
if 1:
    rp = re.compile(r'\d{1,4}')
    fns = [x for x in nl if rp.search(x)]

    DN = set()
    for f in fns:
        text_parts = rp.split(f)
        digit_blocks = rp.findall(f)
        dna = (*(len(x) for x in digit_blocks),*text_parts)
        if dna in DN: continue
        DN.add(dna)

        digit_generators = []
        for d in digit_blocks:
            length = len(d)
            gen = (f"{i:0{length}d}" for i in range(10**length))
            digit_generators.append(gen)

        for digit_combo in itertools.product(*digit_generators):
            result = []
            for ix in range(len(digit_combo)):
                result.append(text_parts[ix])
                result.append(digit_combo[ix])
            result.append(text_parts[-1])

            chk("".join(result),False)
if 1:
    for n in nl.copy():
        if '_' in n:
            for r in os.path.splitext(n)[0].split('_'):
                for x in EXS: chk(r + '.' + x,False)

print(f'{len(l)} / {(len(L))} | {len(l)/(len(L))*100:.2f}%')
nl = '\n'.join(sorted(nl)).encode('ascii')
open('motogp.hsh','wb').write(nl)
