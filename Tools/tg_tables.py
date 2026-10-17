"""Decode BTC's key/length-framed protobuf tables from the local extraction."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def varint(data,pos):
    value=shift=0
    while True:
        byte=data[pos];pos+=1;value|=(byte&127)<<shift
        if byte<128:return value,pos
        shift+=7
        if shift>70:raise ValueError('Invalid varint')

def message(data):
    pos=0;fields={}
    while pos<len(data):
        tag,pos=varint(data,pos);number,wire=tag>>3,tag&7
        if wire==0:value,pos=varint(data,pos)
        elif wire in (1,5):
            size=8 if wire==1 else 4;value=data[pos:pos+size].hex();pos+=size
        elif wire==2:
            size,pos=varint(data,pos);value=data[pos:pos+size];pos+=size
            try:value=value.decode('utf8')
            except UnicodeDecodeError:value={'hex':value.hex()}
        else:raise ValueError((number,wire,pos))
        fields.setdefault(str(number),[]).append(value)
    return fields

def read(name):
    data=(ROOT/'Research/TokyoGhoul/Tables'/f'{name}.bin').read_bytes();pos=0;rows={}
    while pos<len(data):
        size=data[pos];pos+=1;key=data[pos:pos+size].decode('utf8');pos+=size
        size=int.from_bytes(data[pos:pos+2],'big');pos+=2
        rows[key]=message(data[pos:pos+size]);pos+=size
    assert pos==len(data)
    return rows

if __name__=='__main__':
    import json,sys
    print(json.dumps(read(sys.argv[1]),ensure_ascii=False,indent=2))
