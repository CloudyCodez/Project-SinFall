"""Stretch Unity generic animation time without changing its sampled poses."""
import math
import struct


def stretch_clip(tree, factor):
    assert math.isfinite(factor) and factor > 0
    muscle = tree['m_MuscleClip']
    stream = muscle['m_Clip']['data']['m_StreamedClip']
    raw = bytearray(struct.pack('<' + 'I' * len(stream['data']), *stream['data']))
    offset = 0
    while offset < len(raw):
        time, count = struct.unpack_from('<fi', raw, offset)
        assert 0 <= count <= stream['curveCount']
        # Unity uses +/-FLT_MAX sentinel frames. Keep those exactly intact.
        if math.isfinite(time) and abs(time) < 1e30:
            struct.pack_into('<f', raw, offset, time * factor)
        offset += 8
        for _ in range(count):
            index, cubic, quadratic, slope, value = struct.unpack_from('<i4f', raw, offset)
            assert 0 <= index < stream['curveCount']
            struct.pack_into('<i4f', raw, offset, index, cubic / factor**3,
                             quadratic / factor**2, slope / factor, value)
            offset += 20
    assert offset == len(raw)
    stream['data'] = list(struct.unpack('<' + 'I' * (len(raw)//4), raw))
    dense = muscle['m_Clip']['data']['m_DenseClip']
    dense['m_SampleRate'] /= factor
    dense['m_BeginTime'] *= factor
    for key in ['m_StartTime', 'm_StopTime']:
        muscle[key] *= factor
    muscle['m_AverageSpeed'] = {k: v / factor for k, v in muscle['m_AverageSpeed'].items()}
    muscle['m_AverageAngularSpeed'] /= factor
    tree['m_SampleRate'] /= factor
    for event in tree['m_Events']:
        event['time'] *= factor
    # Generic clips normally use runtime streams; keep editor curves consistent.
    for name in ['m_RotationCurves', 'm_EulerCurves', 'm_PositionCurves',
                 'm_ScaleCurves', 'm_FloatCurves', 'm_PPtrCurves']:
        for curve in tree.get(name, []):
            for key in curve.get('curve', {}).get('m_Curve', []):
                key['time'] *= factor
                for slope in ['inSlope', 'outSlope']:
                    if isinstance(key.get(slope), dict):
                        key[slope] = {k: v / factor for k, v in key[slope].items()}
                    elif slope in key:
                        key[slope] /= factor
    assert not tree.get('m_CompressedRotationCurves'), 'Packed editor rotation curves need explicit retiming'
    return tree
