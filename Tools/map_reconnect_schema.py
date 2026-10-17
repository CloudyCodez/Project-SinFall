"""Recover daily-reset field boundaries used by the reconnect response."""
import contextlib
import io
from bisect import bisect_right
with contextlib.redirect_stdout(io.StringIO()):
    import map_login_read_schema as m
root = 0x36b7c44
end = m.addresses[bisect_right(m.addresses, root)]
position = 0
field = ''
for ins in m.n.decoder.disasm(m.n.data[m.n.offset(root):m.n.offset(root)+end-root], root):
    if ins.mnemonic == 'add' and ins.op_str.startswith('x1,'):
        field = ins.op_str
    if ins.mnemonic in ('bl','b') and ins.op_str.startswith('#'):
        address = int(ins.op_str[1:], 0)
        if address in m.meta and '$$Read' in m.meta[address]['Name']:
            part = m.schema(address)
            print(position, field, part)
            position += len(part)
print('FULL',m.schema(root))
