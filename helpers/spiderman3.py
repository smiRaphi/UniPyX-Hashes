import os,re,itertools
from lib.crypto import crc_hash
BN = os.path.splitext(os.path.abspath(__file__))[0]

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

P = r"<path>"
BL = {
    'yxqjdGdk',
    'VU7dJ',
    'j1hq','Irrr','frrr','jrrr','q.ur',
    'E.Wr','iqZ0','jT3R','LRRR','LRTR',
    'OPYR','g16r','_LQy','Q08r','errr',
    'krtr','Cqxr','HPWR','PPUR','PPVR',
    'Ppxr','UVWY','hqrr','hr3r','hrrr',
    'iPx0','l.tR','kpX0','mNW',
    # 'Q180',
    # 'NO',
}
fmt = lambda x:x.lower()
hsh = 'slf'

L = set([int(x,16) for x in open(BN + '.list').read().split('\n') if x])
nl = set(open(BN + '.hsh').read().split('\n'))
l = set([crc_hash(fmt(x).encode('ascii'),hsh) for x in nl])

def chk(n,prx=True,first=True):
    if n in BL: return

    h = crc_hash(fmt(n).encode('ascii'),hsh)
    if h in l:
        if prx: print(f'Already in DB | {h:08X}')
    elif h in L:
        print(f'{h:08X} | {n}')
        print('Yay! :D')
        nl.add(n)
        l.add(h)
    else:
        if prx: print('Nay D:')

if 0:
    while 1:
        i = input(': ')
        if not i: break
        if i.startswith('ds "') and i[-1] == '"': i = i[4:-1].replace('\\\\','\\')
        elif i[0] == i[-1] == '"': i = i[1:-1].replace('\\\\','\\')
        chk(i,True)
if 1:
    rg = re.compile(r'(?:(?<=[\0-,\:-@`\{-\xFF])|^)([a-zA-Z0-9_\-\./\\]{5,64})(?:(?=[\0-,\:-@`\{-\xFF])|$)'.encode())
    fs = rldir(P)
    for f in fs:
        if not os.path.exists(f): continue
        for rr in rg.findall(open(f,'rb').read()):
            for r in rr.replace(b'\\',b'/').split(b'/'):
                try: r = r.decode('ascii');assert r.isprintable()
                except: continue
                chk(r,False)
                if '.' in r:
                    r = os.path.splitext(r)[0]
                    if len(r) > 5: chk(r,False)
if 1:
    for n in nl.copy():
        n = os.path.splitext(n)[0]
        chk(n,False)
if 1:
    for f in rldir(P):
        chk(os.path.splitext(os.path.basename(f))[0],False)
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
        tl = 0
        for d in digit_blocks:
            length = len(d)
            tl += length
            gen = (f"{i:0{length}d}" for i in range(10**length))
            digit_generators.append(gen)
        if tl > 5: continue

        for digit_combo in itertools.product(*digit_generators):
            result = []
            for ix in range(len(digit_combo)):
                result.append(text_parts[ix])
                result.append(digit_combo[ix])
            result.append(text_parts[-1])

            chk("".join(result),False)

print(f'{len(l)} / {(len(L))} | {len(l)/(len(L))*100:.2f}%')
nl = '\n'.join(sorted(nl)).encode('ascii')
open(BN + '.hsh','wb').write(nl)

