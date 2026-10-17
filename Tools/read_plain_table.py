"""Decode unencrypted field-order binary tables from the preserved client DB."""
import json, re, struct
from functools import lru_cache
from pathlib import Path
root = Path('E:/7DS-Offline')
dump = (root / 'Research/Il2CppDumper/dump.cs').read_text(encoding='utf8')

@lru_cache(maxsize=None)
def table_fields(row_class):
    definition = re.search(r'public class ' + row_class + r'\b.*?// Properties', dump, re.S)[0]
    fields = re.findall(r'private (int|float|string|byte|bool|ItemType|List<int>|List<float>|List<byte>|List<string>) (\w+);', definition)
    # These are lazily computed from the four amount columns, not stored rows.
    if row_class == 'DBGambleDisplayRow':
        fields = [(kind, key) for kind, key in fields if not key.startswith('list_gamble_')]
    fields = [(kind, key) for kind, key in fields if not key.startswith('list_') or '_array_' in key]
    return fields


def write_table(rows, row_class):
    output = bytearray(struct.pack('<i', len(rows)))
    def string(value):
        data = value.encode('utf8'); size = len(data)
        while size >= 128:
            output.append((size & 127) | 128); size >>= 7
        output.append(size); output.extend(data)
    for row in rows:
        for kind, key in table_fields(row_class):
            value = row[key]
            if kind.startswith('List<'):
                output.extend(struct.pack('<i', len(value)))
                for item in value:
                    if kind == 'List<int>': output.extend(struct.pack('<i', item))
                    elif kind == 'List<float>': output.extend(struct.pack('<f', item))
                    elif kind == 'List<byte>': output.extend(struct.pack('<B',item))
                    else: string(item)
            elif kind == 'string': string(value)
            else: output.extend(struct.pack({'int':'<i','float':'<f','byte':'<B','bool':'<?','ItemType':'<B'}[kind], value))
    return bytes(output)


def read_table(name, row_class):
    fields = table_fields(row_class)
    data = (root / ('Research/DecodedCache/' + name + '.bin')).read_bytes()
    count, = struct.unpack_from('<i', data)
    offset = 4
    rows = []
    for _ in range(count):
        row = {}
        for kind, key in fields:
            if kind in ('List<int>', 'List<float>', 'List<byte>', 'List<string>'):
                length, = struct.unpack_from('<i', data, offset)
                offset += 4
                assert 0 <= length <= 100000
                if kind in ('List<int>','List<float>','List<byte>'):
                    row[key] = list(struct.unpack_from('<' + ('i' if kind=='List<int>' else 'f' if kind=='List<float>' else 'B') * length, data, offset))
                    offset += length * (4 if kind in ('List<int>','List<float>') else 1)
                else:
                    row[key] = []
                    for _ in range(length):
                        size = shift = 0
                        while True:
                            b = data[offset]; offset += 1
                            size |= (b & 127) << shift
                            if b < 128: break
                            shift += 7
                        row[key].append(data[offset:offset+size].decode('utf8'))
                        offset += size
            elif kind == 'string':
                length = shift = 0
                while True:
                    b = data[offset]; offset += 1
                    length |= (b & 127) << shift
                    if b < 128: break
                    shift += 7
                row[key] = data[offset:offset + length].decode('utf8')
                offset += length
            else:
                fmt = {'int':'<i', 'float':'<f', 'byte':'<B', 'bool':'<?', 'ItemType':'<B'}[kind]
                row[key], = struct.unpack_from(fmt, data, offset)
                offset += struct.calcsize(fmt)
        rows.append(row)
    assert offset == len(data), (name, offset, len(data))
    return rows

if __name__ == '__main__':
    rows = read_table('DB_skin_base', 'DBSkinBaseRow')
    (root / 'Research/DecodedCache/skins.json').write_text(json.dumps(rows, indent=2))
    print('Decoded', len(rows), 'skins')
    for row in rows[:5]:
        print({k:row[k] for k in ['id','skin_portrait_base','matching_hero_id','rating']})
    banners = read_table('DB_gamble_display', 'DBGambleDisplayRow')
    (root / 'Research/DecodedCache/banners.json').write_text(json.dumps(banners, indent=2))
    print('Decoded', len(banners), 'banners')
    for row in banners[:4]:
        print({k:row[k] for k in ['id','gamble_group','gamble_money_id_1','gamble_BG_name','event_gacha_start','event_gacha_end']})
