TIDL = (
    "611",
    "840",
    "841",
    "842",
    "834",
    "GDS",
    "GDT",
    "GDX",
    "GDL",
    "CDV",
    "CDP",
)
TID1 = (
    "834",
    "CDV",
    "CDP",
)
TIDF = (
    "842",
)
TIDB = (
    "834",
)

import httpx,re
from lib.pyob import PyOBinX

def makedb():
    TL = {
        "Naomi":           "N",
        "Naomi Multiboard":"N",
        "Naomi GD-ROM":    "N",
        "Naomi Satellite Terminal":"N",
        "Naomi 2":         "2",
        "Naomi 2 Satellite Terminal":"2",
        "Chihiro":         "C",
        "Chihiro GD-ROM":  "C",
        "Chihiro Satellite Terminal":"C",
        "Triforce":        "T",
        "Triforce GD-ROM": "T",
    }

    d = PyOBinX.new('sgkeys.pyob')

    r = httpx.get('https://www.citylan.it/index.php/Naomi_-_Chihiro_-_Triforce',timeout=60)
    lid = []
    for t,tid,key in re.findall(r'<tr>\n<td>[^<]+</td>\n<td>[^<]*</td>\n<td>([^<]+)</td>\n(?:<td>.*</td>\n){8}<td>([A-Z\d]+\-[A-Z\d]+)</td>\n(?:<td>.*</td>\n){14}<td>(?:0x)?([A-Fa-f\d]{16}|[A-Fa-f\d]{8})</td>\n',r.text):
        if len(key) not in {8,16}: continue
        if not t in TL:
            print(t,tid,'TL')
            continue
        if not '-' in tid: continue
        tbn,tidn = tid.split('-')
        if not tbn in TIDL:
            print(tid,'TIDL')
            continue
        lid.append(tid)
        t = TL[t]
        if t == 'N' and len(key) == 16: t = 'L'
        elif t == '2' and len(key) == 16: t = '3'

        if not t in d: d[t] = {}
        d[t][tid] = bytes.fromhex(key)

        # old code kept for id verification
        tidb = TIDL.index(tbn)
        if tbn in TIDF:
            bytes([tidb])
            tidn.encode('ascii')
        else:
            if tbn in TID1: tidn = tidn[1:]
            if not len(tidn) in {4,5}: raise ValueError(tid)
            bytes([tidb | (0x80 if len(tidn) == 5 else 0)])
            if tbn in TIDB: int(tidn[:4]).to_bytes(2,'big')
            else:
                if int(tidn[:4]) > 0xFF: raise ValueError(tid)
                bytes([int(tidn[:4])])

    return lid

if __name__ == '__main__':
    lid = makedb()
    print("{'" + "','".join(sorted(lid)) + "'}")
