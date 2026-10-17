"""Convert BTC kakugan UVs and layered kagune materials to native GC assets.

Uses the publisher's original eye atlases, effect textures, masks and colors.
No generated/repainted artwork. Geometry, skin weights and animations stay intact.
"""
from pathlib import Path
import json,struct,sys
import numpy as np
from PIL import Image
from UnityPy.helpers.MeshHelper import MeshHandler
sys.path.insert(0,str(Path(__file__).parent))
helper=Path(__file__).with_name('build_kaneki_assets.py')
exec(compile(helper.read_text().split("donor='253")[0],str(helper),'exec'))
manifest=read((OUT/'br-m.bin').read_bytes());bundles,aliases,dirs=manifest
report=json.loads((OUT/'assets.json').read_text())
units=json.loads((ROOT/'Research/TokyoGhoul/roster-port-inventory.json').read_text())
audit_path=ROOT/'Research/TokyoGhoul/visual-refinement-report.json'
audit=json.loads(audit_path.read_text()) if audit_path.exists() else []

def sample(image,size,entry,speed=None,time=0):
    a=np.asarray(image.convert('RGBA'),dtype=np.float32)/255
    h,w=a.shape[:2];v,u=np.mgrid[0:size,0:size].astype(np.float32)
    u=(u+.5)/size;v=1-(v+.5)/size
    u=u*entry['m_Scale']['x']+entry['m_Offset']['x']
    v=v*entry['m_Scale']['y']+entry['m_Offset']['y']
    if speed:
        u+=speed.get('r',0)*time;v+=speed.get('g',0)*time
    return a[((1-v)%1*h).astype(int).clip(0,h-1),(u%1*w).astype(int).clip(0,w-1)]

for unit in units:
    if unit['race']!='Ghoul':continue
    logical='phoenix_kaneki_model' if unit['source']=='1065' else 'phoenix_tg_'+unit['source']+'_model'
    row=next(r for r in report if r['logical']==logical)
    env=UnityPy.load(str(OUT/row['file']));asset=env.assets[0]
    markers={o.read().m_Name for o in env.objects if o.type.name=='Material'}
    if 'PhoenixTGVisualsV3' in markers:continue
    eyes_already_fixed='PhoenixTGVisualsV2' in markers
    sources={f:load(ROOT/'Research/TokyoGhoul/PortAssets'/f,True) for f in unit['files'] if not f.endswith(('_head','_full'))}
    cab={a.name:a for e in sources.values() for a in e.assets}
    def resolve(owner,p):
        if not p['m_PathID']:return None
        a=owner.assets_file
        if p['m_FileID']:a=cab[a.externals[p['m_FileID']-1].path.rsplit('/',1)[-1]]
        return a.objects[p['m_PathID']]
    original={o.read().m_Name:o for e in sources.values() for o in e.objects if o.type.name=='Material'}
    mats={o.path_id:o for o in env.objects if o.type.name=='Material'}
    native=gc('848ECA5317DD03D78753BB38EEA703D5')
    shader=next(o for o in native.objects if o.type.name=='Shader' and o.read_typetree().get('m_ParsedForm',{}).get('m_Name')=='Mobile/Particles/Alpha Blended')
    nextid=max(8500000000000000000,max(asset.objects))
    def add(obj):
        global nextid
        nextid+=1;return clone(obj,asset,nextid)
    sid=add(shader).path_id
    sheet=next(o for o in native.objects if o.type.name=='Shader' and o.read_typetree().get('m_ParsedForm',{}).get('m_Name')=='SevenDeadlySins/SpriteSheet')
    sheet_id=add(sheet).path_id
    body_material=next((o for o in mats.values() if o.read().m_Name.lower().endswith('_body')),None)
    body_material=body_material.read_typetree() if body_material else None
    texdonor=next(o for o in env.objects if o.type.name=='Texture2D')
    eye_count=0;kagune_count=0
    # Eye material identifies exact submesh vertex ranges, so hair, teeth and
    # the skin texture are never recolored. UV0 is native float16 or float32.
    for renderer in list(env.objects):
        if eyes_already_fixed:break
        if renderer.type.name!='SkinnedMeshRenderer':continue
        rt=renderer.read_typetree()
        for mi,mp in enumerate(rt['m_Materials']):
            mat=mats[mp['m_PathID']];name=mat.read().m_Name
            if not any(part in name.lower() for part in ['_eyes','_eye']):continue
            mesh=asset.objects[rt['m_Mesh']['m_PathID']];mt=mesh.read_typetree()
            h=MeshHandler(mesh.read());h.process();vd=mesh.read().m_VertexData
            channel=vd.m_Channels[4];streams=h.get_streams(vd.m_Channels,vd.m_VertexCount);stream=streams[channel.stream]
            raw=bytearray(mt['m_VertexData']['m_DataSize']);fmt=h.endianess+('ee' if channel.format==1 else 'ff');assert channel.format in [0,1]
            sub=mt['m_SubMeshes'][mi]
            for vi in range(sub['firstVertex'],sub['firstVertex']+sub['vertexCount']):
                u,v=h.m_UV0[vi]
                if u<.5 and v<.75:
                    center=.6 if v>.4 else .2
                    u=.73+(u-.25)*1.2;v=.28+(v-center)*1.2
                elif v>=.75:
                    u,v=.95,.85
                struct.pack_into(fmt,raw,stream.offset+vi*stream.stride+channel.offset,u,v)
            mt['m_VertexData']['m_DataSize']=bytes(raw);mesh.save_typetree(mt);eye_count+=1
    # Bake the source layered surface shader into an RGBA texture. Masks,
    # UV tiling and HDR tints survive the URP -> GC material conversion.
    for mid,mat in mats.items():
        tree=mat.read_typetree();name=tree['m_Name'];src=next((o for n,o in original.items() if name.endswith('_'+n)),None)
        if src is None:continue
        old=src.read_typetree();props=old['m_SavedProperties'];tex=dict(props['m_TexEnvs']);floats=dict(props['m_Floats']);colors=dict(props['m_Colors'])
        if not any(k in name.lower() for k in ['weapon','hezi','kagune']):continue
        if '_MainTex1' not in tex and not any(k in name.lower() for k in ['hezi','kagune']):continue
        size=256;rgb=np.zeros((size,size,3),np.float32);alpha=np.zeros((size,size),np.float32)
        active_time=0
        def fetch(key):
            entry=tex.get(key)
            if not entry or not entry['m_Texture']['m_PathID']:return None
            obj=resolve(src,entry['m_Texture'])
            speed_key='_MainSpeed' if key=='_MainTex' else '_MaskSpeed' if key=='_MaskTex' else key.replace('Tex','Speed')
            speed=colors.get(speed_key) if floats.get('_UV_Speed',0) else None
            return sample(obj.read().image,size,entry,speed,active_time)
        base=fetch('_BaseTex') if '_BaseTex' in tex else fetch('_MainTex')
        if base is not None:rgb=base[:,:,:3].copy();alpha=base[:,:,3].copy()
        color=colors.get('_MainColor',dict(r=1,g=1,b=1,a=1))
        if '_MainTex1' not in tex:
            if base is None:
                # Source emissive geometry: retain its color with subdued
                # opacity, instead of an opaque clipped-white solid sheet.
                rgb[:]=[color[k] for k in ['r','g','b']];alpha[:]=.15
            else:
                rgb*=np.array([color[k] for k in ['r','g','b']]);mask=fetch('_MaskTex')
                if mask is not None:alpha*=mask[:,:,0]
        for n in range(1,5):
            layer=fetch('_MainTex'+str(n))
            if layer is None or not floats.get(['','_FirstLayer','_SecondLayer','_ThirdLayer','_FourthLayer'][n],1):continue
            tint=colors.get('_MainColor'+str(n),dict(r=1,g=1,b=1,a=1))
            mask=fetch('_MaskTex'+str(n));amount=layer[:,:,3]*floats.get('_Alpha'+str(n),1)*floats.get('_AlphaV'+str(n),1)
            if mask is not None:amount*=mask[:,:,0]
            amount=np.clip(amount,0,1)
            rgb+=layer[:,:,:3]*np.array([tint[k] for k in ['r','g','b']])*amount[:,:,None]
            alpha=np.maximum(alpha,amount)
        # Compress intensity together, preserving original hue/saturation.
        # Per-channel tone mapping washed red kagune into orange/gray.
        rgb=rgb/np.maximum(1,np.max(rgb,axis=2,keepdims=True))
        rgba=np.dstack([np.clip(rgb,0,1),np.clip(alpha,0,1)])
        speed=colors.get('_MainSpeed',{})
        animated=bool(base is not None and floats.get('_UV_Speed',0) and any(speed.get(k,0) for k in ('r','g')) and '_MainTex1' not in tex)
        if animated:
            # Native GC SpriteSheet animates the original scrolling surface;
            # no foreign MonoBehaviour or runtime shader compiler is needed.
            frames=[]
            component=max(abs(speed.get('r',0)),abs(speed.get('g',0)))
            duration=1/component
            for frame in range(16):
                active_time=duration*frame/16
                layer=fetch('_MainTex');frame_rgb=layer[:,:,:3]*np.array([color[k] for k in ('r','g','b')])
                frame_rgb/=np.maximum(1,np.max(frame_rgb,axis=2,keepdims=True))
                frame_alpha=layer[:,:,3].copy();mask=fetch('_MaskTex')
                if mask is not None:frame_alpha*=mask[:,:,0]
                frames.append(np.uint8(np.dstack([frame_rgb,np.clip(frame_alpha,0,1)])*255))
            image=np.zeros((size*4,size*4,4),np.uint8)
            for frame,pixels in enumerate(frames):
                y,x=divmod(frame,4);image[y*size:(y+1)*size,x*size:(x+1)*size]=pixels
        else:image=np.uint8(rgba*255)
        texture=add(texdonor);td=texture.read();td.m_Name=unit['model']+'_layered_'+name;td.set_image(Image.fromarray(image));td.save()
        tree.update(m_Shader=ptr(sid),m_CustomRenderQueue=3000,m_ValidKeywords=[],m_InvalidKeywords=[],stringTagMap=[('RenderType','Transparent')])
        tree['m_SavedProperties']=dict(m_TexEnvs=[('_MainTex',dict(m_Texture=ptr(texture.path_id),m_Scale=dict(x=1,y=1),m_Offset=dict(x=0,y=0)))],m_Ints=[],m_Floats=[('_InvFade',1.0)],m_Colors=[('_TintColor',dict(r=.5,g=.5,b=.5,a=.5))])
        if animated:
            tree['m_Shader']=ptr(sheet_id)
            tree['m_SavedProperties']['m_Floats']=[('_Cols',4),('_Rows',4),('_Speed',16/duration),('_AnimOffset',0),('_FlipX',0),('_Fadeout',1),('_Culling',floats.get('_Cull',0)),('_SrcBlend',floats.get('_SrcBlend',5)),('_DstBlend',floats.get('_DstBlend',10)),('_YBillboard',0),('_AlphaTest',0),('UseFog',0),('_BounceAmplitude',0)]
            tree['m_SavedProperties']['m_Colors']=[('_MainColor',dict(r=1,g=1,b=1,a=1))]
        elif body_material and base is not None and '_BaseTex' in tex and floats.get('_ZWrite',1)!=0:
            # Flesh/armor surfaces retain the native character shading and
            # depth writes; they are not translucent effect planes.
            props=deepcopy(body_material['m_SavedProperties'])
            for key,entry in props['m_TexEnvs']:
                if key=='_MainTex':entry['m_Texture']=ptr(texture.path_id)
            tree['m_Shader']=deepcopy(body_material['m_Shader'])
            tree.update(m_CustomRenderQueue=2000,stringTagMap=[('RenderType','Opaque')])
            tree['m_SavedProperties']=props
        mat.save_typetree(tree);kagune_count+=1
    marker=add(next(iter(mats.values())));mark=marker.read_typetree();mark['m_Name']='PhoenixTGVisualsV3';marker.save_typetree(mark)
    paths=[(p,v.asset.m_PathID) for o in env.objects if o.type.name=='AssetBundle' for p,v in o.read().m_Container]
    deps=bundles[bundle_key(row['file'])]['deps'];report.remove(row);emit(env,logical,paths,deps)
    audit[:]=[r for r in audit if r['source']!=unit['source']]
    audit.append(dict(source=unit['source'],name=unit['name'],eyes=eye_count,kagune_materials=kagune_count))
    print(unit['source'],eye_count,'eye submeshes;',kagune_count,'layered kagune materials',flush=True)
(OUT/'br-m.bin').write_bytes(write(*manifest));(OUT/'assets.json').write_text(json.dumps(report,indent=2))
audit_path.write_text(json.dumps(audit,indent=2))
