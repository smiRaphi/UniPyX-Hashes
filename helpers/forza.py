P = r"out\CryptoTool_v4.5\CryptoTool\contexts"

import os,re
from lib.pyob import PyOBinX,PyOInlineF

RGTM = re.compile(r'> (\w+_tables_memory) = \{([^\}]+)\}')
RGT = re.compile(r'> (\w+)_tables = \{([^\}]+)\}')
RGK = re.compile(r'> (\w+)_keys = \{([^\}]+)\}')
RGOS = re.compile(r'uint32_t (\w+)_obfuscation_seed = 0x([0-9a-fA-F]{4,8});')
RGOM = re.compile(r'> (\w+)_crc32_mapping = \{([^\}]+)\}')

b = PyOBinX.new('forza_keys.pyob')
b['t'] = {}
b['k'] = {'null_encryption':b'\0'*(4*4*17)}
b['os'] = {}
b['om'] = {}
Pt = P + '/tables/'
Pk = P + '/keys/'

for x in os.listdir(Pt):
    if not x.endswith('.cpp'): continue
    s = open(Pt + x).read()
    d = {}
    for k,v in RGTM.findall(s): d[k] = bytes(eval(f'[{v}]'))
    for k,v in RGT.findall(s): b['t'][k] = bytes(eval(f'[{v}]',globals=d))
    for k,v in RGOM.findall(s): b['om'][k] = bytes(eval(f'[{v}]'))

for x in os.listdir(Pk):
    if not x.endswith(('.cpp','.h')): continue
    s = open(Pk + x).read()
    if x.endswith('.cpp'):
        for k,v in RGK.findall(s): b['k'][k] = bytes(eval(f'[{v}]'))
    else:
        for k,v in RGOS.findall(s): b['os'][k] = int(v,16)

b['c'] = [
    {'n':'fh5_v1.619.349.0','t':'file','b':0x200,'ek':'null','et':'fh4','dt':'fh4','mt':'fh4'},
    {'n':'fh5_v1.619.349.0','t':'profile','b':0x200,'et':'fh4','dt':'fh4','mt':'fh4'},
    {'n':'fh5_v1.619.349.0','t':'gamedb','b':0x20000,'ek':'null','et':'fh4','dt':'fh4','mt':'fh4','om':'fh5'},
    {'n':'fh5_v1.619.349.0','t':'sfs','b':0x20000,'ek':'null','et':'fh4','dt':'fh4','mt':'fh4'},
    {'n':'fh5_v1.614.70.0','t':'file','b':0x200,'ek':'null','et':'fh4','dt':'fh4','mt':'fh4'},
    {'n':'fh5_v1.614.70.0','t':'gamedb','b':0x20000,'ek':'null','et':'fh4','dt':'fh4','mt':'fh4','om':'fh5'},
    {'n':'fh5_v1.614.70.0','t':'sfs','b':0x20000,'ek':'null','et':'fh4','dt':'fh4','mt':'fh4'},
    {'n':'fh5','t':'file','b':0x200,'ek':'null','et':'fh4','dt':'fh4','mt':'fh4'},
    {'n':'fh5','t':'profile','b':0x200,'et':'fh4','dt':'fh4','mt':'fh4'},
    {'n':'fh5','t':'photo','b':0x200,'et':'fh4','dt':'fh4','mt':'fh4'},
    {'n':'fh5','t':'dynamic','b':0x200,'et':'fh4','dt':'fh4','mt':'fh4'},
    {'n':'fh5','t':'gamedb','b':0x20000,'ek':'null','et':'fh4','dt':'fh4','mt':'fh4','o':True},
    {'n':'fh5','t':'sfs','b':0x20000,'ek':'null','et':'fh4','dt':'fh4','mt':'fh4'},
    {'n':'fh4','t':'file','b':0x200,'ek':'null'},
    {'n':'fh4','t':'profile','b':0x200},
    {'n':'fh4','t':'photo','b':0x200},
    {'n':'fh4','t':'dynamic','b':0x200},
    {'n':'fh4','t':'gamedb','b':0x20000,'ek':'null','om':'fm6apex'},
    {'n':'fh4','t':'sfs','b':0x20000,'ek':'null'},
    {'n':'fh3dev','t':'profile','b':0x200,'ek':'fh3dev','dk':'fh3dev','mk':'fh3dev','et':'fh3','dt':'fh3','mt':'fh3'},
    {'n':'fh3','t':'file','b':0x200,'ek':'null'},
    {'n':'fh3','t':'profile','b':0x200},
    {'n':'fh3','t':'photo','b':0x200},
    {'n':'fh3','t':'gamedb','b':0x20000,'ek':'null','om':'fm6apex'},
    {'n':'fh3','t':'sfs','b':0x20000,'ek':'null'},
    {'n':'fm7','t':'configfile','b':0x200,'ek':'null'},
    {'n':'fm7','t':'profile','b':0x200},
    {'n':'fm7','t':'reward','b':0x200},
    {'n':'fm7','t':'photo','b':0x200},
    {'n':'fm7','t':'gamedb','b':0x20000,'ek':'null','os':'fm7_db','om':'fm6apex'},
    {'n':'fm7','t':'sfs','b':0x20000,'ek':'null'},
    {'n':'fm6apex','t':'configfile','b':0x200,'ek':'null'},
    {'n':'fm6apex','t':'profile','b':0x200},
    {'n':'fm6apex','t':'photo','b':0x200},
    {'n':'fm6apex','t':'gamedb','b':0x20000,'ek':'null','os':'fm6apex_db'},
]
for x in b['c']:
    for tn,tx in (
        ('ek','_encryption'),
        ('dk','_decryption'),
        ('mk','_mac'),
        ('et','_encryption'),
        ('dt','_decryption'),
        ('mt','_mac'),
    ):
        if not tn in x: x[tn] = x['n'].replace('.','_') + (('_' + x['t']) if tn[1] == 'k' else '')
        if not x[tn].endswith(tx): x[tn] += tx
        assert x[tn] in b[tn[1]],x
    if x.get('o') or 'os' in x or 'om' in x:
        if not 'os' in x: x['os'] = x['n'].replace('.','_') + '_' + x['t']
        if not 'om' in x: x['om'] = x['n']
        assert x['os'] in b['os'],x
        assert x['om'] in b['om'],x
        x.pop('o',0)

def post(db):
    for x in db['c']:
        x['_'] = x.copy()
        for tn in ('et','dt','mt','ek','dk','mk'):
            if tn in x: x[tn] = b[tn[1]][x[tn]]
        if 'os' in x: x['os'] = b['os'][x['os']]
        if 'om' in x: x['om'] = b['om'][x['om']]
        
b['_'] = PyOInlineF(post)

b.save()
