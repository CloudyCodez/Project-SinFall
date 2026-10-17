"""Keep a source generic clip continuation, interpolating its exact cut pose."""
import struct, math

def trim_clip_start(tree,cut):
 m=tree['m_MuscleClip'];assert 0<cut<m['m_StopTime']
 data=m['m_Clip']['data'];stream=data['m_StreamedClip'];assert data['m_DenseClip']['m_CurveCount']==0
 raw=struct.pack('<'+'I'*len(stream['data']),*stream['data']);frames=[];off=0
 while off<len(raw):
  time,count=struct.unpack_from('<fi',raw,off);off+=8;keys=[]
  for _ in range(count):keys.append(struct.unpack_from('<i4f',raw,off));off+=20
  frames.append((time,keys))
 latest={}
 for time,keys in frames:
  if time<=cut:
   for key in keys:latest[key[0]]=(time,key)
 keys=[]
 for index,(time,key) in sorted(latest.items()):
  _,a,b,c,d=key;dt=cut-time if abs(time)<1e30 else 0
  keys.append((index,a,b+3*a*dt,c+2*b*dt+3*a*dt*dt,d+c*dt+b*dt*dt+a*dt*dt*dt))
 assert len(keys)==stream['curveCount'],(len(keys),stream['curveCount'])
 out=bytearray()
 kept=[(0.0,keys)]+[(time-cut if abs(time)<1e30 else time,keys) for time,keys in frames if time>cut]
 for time,keys in kept:
  out.extend(struct.pack('<fi',time,len(keys)))
  for key in keys:out.extend(struct.pack('<i4f',*key))
 stream['data']=list(struct.unpack('<'+'I'*(len(out)//4),out));m['m_StartTime']=0.0;m['m_StopTime']-=cut
 tree['m_Events']=[dict(e,time=e['time']-cut) for e in tree['m_Events'] if e['time']>=cut]
 for name in ['m_RotationCurves','m_EulerCurves','m_PositionCurves','m_ScaleCurves','m_FloatCurves','m_PPtrCurves']:tree[name]=[]
 assert not tree.get('m_CompressedRotationCurves')
 return tree
