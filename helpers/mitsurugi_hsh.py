from lib.crypto import crc_hash

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

BL = {
    b'7bAK6.cln',
    b'DDDUUUUUUMMMKKKHHH.w9a',
    b'Tc3K_1IW.w9o',
    b'786444.ogg',
}

def crc(i:str): return crc_hash(i.lower(),'crc32_bzip2')
crcs = [int(x,16) for x in open('mitsurugi.list').read().split('\n')]
PH = 'mitsurugi.hsh'
P = r"<path>"
l = {crc(x.strip()):x for x in open(PH,'rb').read().replace(b'\r',b'').split(b'\n') if x}
EXS = set(x.split(b'.')[-1].lower().decode('ascii') for x in l.values())

def chk(i,prx=True):
    i = i.strip()
    if isinstance(i,str): i = i.encode('ascii')
    if not i.startswith(b'data\\') or i in BL: return
    h = crc(i)
    if h in l:
        if prx: print('Already in DB')
    elif h in crcs:
        print(f'{h:08X} | {i.decode("ascii")}')
        print('Yay! :D')
        l[h] = i
    else:
        if prx: print('Nay D:')

if 0:
    while 1:
        i = input(': ')
        if not i: break
        i = i.replace('\\','/')
        chk(i)
        chk(i.replace('/','\\'))
if 0:
    rg = re.compile(r'[\0-,\:-@`\{-\xFF]([a-zA-Z0-9_\-\./\\]{5,256})[\0-,\:-@`\{-\xFF]'.encode())
    for f in rldir(P):
        for r in rg.findall(open(f,'rb').read()):
            if not r.startswith(b'data\\'): continue
            try: r = r.decode('ascii');assert r.isprintable()
            except: continue
            chk(r,False)
            for x in EXS:
                chk(r + '.' + x,False)
            if '.' in r:
                r = os.path.splitext(r)[0]
                for x in EXS:
                    chk(r + '.' + x,False)

print(f'{len(l)} / {len(crcs)} | {len(l)/len(crcs)*100:.2f}%')
d = b'\n'.join(sorted(l.values()))
open(PH,'wb').write(d)
