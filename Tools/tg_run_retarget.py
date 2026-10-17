"""Bake the native GC running cycle onto BTC's generic skeletons.

Only local rotations are transferred, relative to each rig's rest pose.
Imported bone lengths/scales and the character root stay source-owned.
Unity's runtime dense curve stream is rebuilt, not just its editor curves.
"""
from copy import deepcopy
import bisect, math, struct, zlib
import numpy as np


def hierarchy(env):
    names = {o.path_id: o.read().m_Name for o in env.objects if o.type.name == 'GameObject'}
    nodes = {o.path_id: o.read_typetree() for o in env.objects if o.type.name == 'Transform'}
    roots = [i for i,t in nodes.items() if not t['m_Father']['m_PathID']]
    root = next((i for i in roots if names[nodes[i]['m_GameObject']['m_PathID']].endswith('_body_0001')), roots[0])
    keep = set()
    def descend(i):
        keep.add(i)
        for p in nodes[i]['m_Children']: descend(p['m_PathID'])
    descend(root)
    def path(i):
        if i == root: return ''
        t = nodes[i]; p = path(t['m_Father']['m_PathID'])
        return (p + '/' if p else '') + names[t['m_GameObject']['m_PathID']]
    return {path(i): t for i, t in nodes.items() if i in keep}


def curve_samples(tree, times):
    """Decode Unity streamed cubics, dense samples and constant channels."""
    c = tree['m_MuscleClip']['m_Clip']['data']; s = c['m_StreamedClip']
    raw = struct.pack('<' + 'I' * len(s['data']), *s['data']); offset = 0
    tracks = [[] for _ in range(s['curveCount'])]
    while offset < len(raw):
        time, count = struct.unpack_from('<fi', raw, offset); offset += 8
        for _ in range(count):
            index, a, b, slope, value = struct.unpack_from('<i4f', raw, offset); offset += 20
            tracks[index].append((time, a, b, slope, value))
    d = c['m_DenseClip']; constants = c['m_ConstantClip']['data']
    out = []
    for time in times:
        values = []
        for track in tracks:
            index = max(0, bisect.bisect_right([k[0] for k in track], time) - 1)
            key = track[index]; delta = max(0., time - key[0]) if math.isfinite(key[0]) else 0.
            values.append(((key[1] * delta + key[2]) * delta + key[3]) * delta + key[4])
        if d['m_CurveCount']:
            frame = max(0., min(d['m_FrameCount'] - 1., (time - d['m_BeginTime']) * d['m_SampleRate']))
            lo = int(frame); hi = min(lo + 1, d['m_FrameCount'] - 1); alpha = frame - lo
            n = d['m_CurveCount']; data = d['m_SampleArray']
            values.extend(data[lo*n+j]*(1-alpha)+data[hi*n+j]*alpha for j in range(n))
        values.extend(constants); out.append(values)
    widths = {1: 3, 2: 4, 3: 3, 4: 3}; result = {}; offset = 0
    for b in tree['m_ClipBindingConstant']['genericBindings']:
        width = widths.get(b['attribute'], 1) if b['typeID'] == 4 else 1
        result[(b['path'], b['attribute'], b['typeID'])] = np.array([v[offset:offset+width] for v in out])
        offset += width
    assert all(len(v) == offset for v in out), (len(out[0]), offset)
    return result


def quaternion(value): return np.array([value[n] for n in ('x', 'y', 'z', 'w')], dtype=float)
def qmul(a, b):
    v = a[3]*b[:3] + b[3]*a[:3] + np.cross(a[:3], b[:3])
    return np.r_[v, a[3]*b[3] - np.dot(a[:3], b[:3])]
def inverse(q): return q * np.array([-1., -1., -1., 1.]) / np.dot(q, q)


def retarget_run(native_run, native_model, target_model, target_idle):
    native = hierarchy(native_model); target = hierarchy(target_model)
    stop = native_run['m_MuscleClip']['m_StopTime']; frames = 33
    times = np.linspace(0., stop, frames); rate = (frames-1)/stop
    motion = curve_samples(native_run, times)
    base = curve_samples(target_idle, [0.])
    native_by_name = {p.rsplit('/', 1)[-1]: (p, t) for p, t in native.items()}
    bindings = []; samples = []; moved = []
    for path, t in target.items():
        if not path: continue
        h = zlib.crc32(path.encode()); name = path.rsplit('/', 1)[-1]
        for attr, field, keys in [(1, 'm_LocalPosition', ('x','y','z')), (2, 'm_LocalRotation', ('x','y','z','w')), (3, 'm_LocalScale', ('x','y','z'))]:
            value = base.get((h, attr, 4), np.array([[t[field][n] for n in keys]]))[0]
            values = np.tile(value, (frames, 1))
            # The model root and Bip001 retain source orientation. Transfer
            # pelvis/limb rotations only; never donor translations or scale.
            if attr == 2 and name.startswith('Bip001 ') and name in native_by_name:
                npth, nt = native_by_name[name]
                src = motion.get((zlib.crc32(npth.encode()), 2, 4))
                if src is not None:
                    correction = qmul(quaternion(t[field]), inverse(quaternion(nt[field])))
                    values = np.array([qmul(correction, q) for q in src])
                    values /= np.linalg.norm(values, axis=1)[:,None]
                    for i in range(1, frames):
                        if np.dot(values[i-1], values[i]) < 0: values[i] *= -1
                    values[-1] = values[0]
                    if np.max(np.linalg.norm(values - values[0], axis=1)) > .05: moved.append(name)
            bindings.append(dict(path=h, attribute=attr, script=dict(m_FileID=0,m_PathID=0),typeID=4,customType=0,isPPtrCurve=0,isIntCurve=0,isSerializeReferenceCurve=0))
            samples.append(values)
    dense = np.concatenate(samples, axis=1)
    tree = deepcopy(native_run); tree['m_Name'] = 'run'
    for key in ['m_RotationCurves','m_CompressedRotationCurves','m_EulerCurves','m_PositionCurves','m_ScaleCurves','m_FloatCurves','m_PPtrCurves']: tree[key] = []
    tree['m_Compressed'] = False; tree['m_SampleRate'] = float(rate); tree['m_WrapMode'] = 2
    tree['m_ClipBindingConstant'] = dict(genericBindings=bindings, pptrCurveMapping=[])
    muscle = tree['m_MuscleClip']; muscle['m_LoopTime'] = True
    muscle['m_LoopBlend'] = False; muscle['m_StartTime'] = 0.; muscle['m_StopTime'] = float(stop)
    muscle['m_Clip']['data'] = dict(m_StreamedClip=dict(data=[],curveCount=0,discreteCurveCount=0),m_DenseClip=dict(m_FrameCount=frames,m_CurveCount=dense.shape[1],m_SampleRate=float(rate),m_BeginTime=0.,m_SampleArray=dense.flatten().tolist()),m_ConstantClip=dict(data=[]))
    muscle['m_ValueArrayDelta'] = [dict(m_Start=float(a),m_Stop=float(b)) for a,b in zip(dense[0],dense[-1])]
    muscle['m_ValueArrayReferencePose'] = []
    # Native footsteps and runtime event names are preserved.
    assert all(n in moved for n in ['Bip001 L Thigh','Bip001 R Thigh','Bip001 L Calf','Bip001 R Calf']), moved
    return tree, dict(frames=frames,duration=stop,animated_bones=moved,bindings=len(bindings))
