"""Native Grand Cross bundle resource manifest (verified against ARM64 readers)."""
import struct, xxhash

class Reader:
    def __init__(self,data): self.data=data; self.pos=0
    def number(self,fmt):
        value=struct.unpack_from('<'+fmt,self.data,self.pos)[0]
        self.pos+=struct.calcsize('<'+fmt); return value
    def string(self):
        size=shift=0
        while True:
            c=self.number('B');size|=(c&127)<<shift
            if not c&128:break
            shift+=7
        b=self.data[self.pos:self.pos+size];self.pos+=size;return b.decode('utf8')

def string(s):
    b=s.encode('utf8');n=len(b);out=bytearray()
    while n>=128:out.append((n&127)|128);n>>=7
    return bytes(out)+bytes([n])+b

def read(data):
    r=Reader(data);bundles={}
    for _ in range(r.number('i')):
        key=r.number('q');crc=r.number('I');flags=r.number('H');size=r.number('i');section=r.number('i');name=r.string()
        deps=[r.number('q') for _ in range(r.number('i'))]
        extra=[r.number('q') for _ in range(r.number('i'))]
        bundles[key]=dict(crc=crc,flags=flags,size=size,section=section,name=name,deps=deps,extra=extra)
    aliases={r.number('q'):r.number('q') for _ in range(r.number('i'))}
    dirs={}
    for _ in range(r.number('i')):
        name=r.string();groups={}
        for _ in range(r.number('i')):
            key=r.number('q');groups[key]={r.number('q'):r.number('q') for _ in range(r.number('i'))}
        dirs[name]=groups
    assert r.pos==len(data),(r.pos,len(data))
    return bundles,aliases,dirs

def write(bundles,aliases,dirs):
    p=lambda f,*x:struct.pack('<'+f,*x)
    out=bytearray(p('i',len(bundles)))
    for key,r in bundles.items():
        out+=p('qIHii',key,r['crc'],r['flags'],r['size'],r['section'])+string(r['name'])
        for field in ('deps','extra'):
            out+=p('i',len(r[field]))
            for v in r[field]:out+=p('q',v)
    out+=p('i',len(aliases))
    for k,v in aliases.items():out+=p('qq',k,v)
    out+=p('i',len(dirs))
    for name,groups in dirs.items():
        out+=string(name)+p('i',len(groups))
        for k,entries in groups.items():
            out+=p('qi',k,len(entries))
            for a,b in entries.items():out+=p('qq',a,b)
    return bytes(out)

def hash_name(s):
    return struct.unpack('<q',xxhash.xxh64(s.lower().encode('utf-16le')).digest())[0]

def bundle_key(filename):
    # Directory lookups lowercase paths; loaded bundle dictionaries hash the
    # exact uppercase on-disk filename without that normalization.
    return struct.unpack('<q',xxhash.xxh64(filename.encode('utf-16le')).digest())[0]
