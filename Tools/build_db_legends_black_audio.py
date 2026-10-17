"""Package the downloaded Legends Rosé voice cues as native Unity PCM banks."""
import json,struct,wave,shutil
from pathlib import Path
import build_db_legends_models as c
from UnityPy.streams import EndianBinaryReader
from gc_bundle_manifest import read,write

native=c.ROOT/'Research/PhoneAssets/bm'
out=c.OUT/'s';out.mkdir(exist_ok=True)
manifest_path=out/'br-s.bin'
sound_manifest=read((manifest_path if manifest_path.exists() else native/'br-s.bin').read_bytes())
registrations=[]
for index in range(1,4):
    name=f'black_transform_voice_{index}'
    with wave.open(str(c.ROOT/f'Research/DBLegends/black-transform-voice-{index}.wav'),'rb') as f:
        assert f.getsampwidth()==2 and f.getframerate()==32000 and f.getnchannels()==1
        samples=f.getnframes();pcm=f.readframes(samples)
    # FSB5 PCM16, one mono 32-kHz sample, no optional metadata chunks.
    payload=struct.pack('<4s6I8s16s8s',b'FSB5',1,1,8,0,len(pcm),2,b'\0'*8,b'\0'*16,b'\0'*8)
    payload+=struct.pack('<Q',(7<<1)|(samples<<34))+pcm
    (c.ROOT/f'Research/DBLegends/{name}.fsb').write_bytes(payload)
    e=c.load(native/'s/E0C086ACE17A0BC49DB8956DFCB6587E')
    ab=next(o for o in e.objects if o.type.name=='AssetBundle')
    audio=next(o for o in e.objects if o.type.name=='AudioClip')
    e.assets[0].objects={ab.path_id:ab,audio.path_id:audio}
    t=audio.read_typetree();resource=t['m_Resource']['m_Source'].rsplit('/',1)[-1]
    resource_flags=e.file.files[resource].flags
    e.file.files[resource]=EndianBinaryReader(payload)
    e.file.files[resource].flags=resource_flags
    t.update(m_Name=name,m_LoadType=0,m_Channels=1,m_Frequency=32000,m_BitsPerSample=16,m_Length=samples/32000,m_SubsoundIndex=0,m_PreloadAudioData=True,m_LoadInBackground=False,m_CompressionFormat=0)
    t['m_Resource'].update(m_Offset=0,m_Size=len(payload));audio.save_typetree(t)
    path=f'assets/sevensins/patchresources/sound/dragonball/goku_black/{name}.wav'
    logical='phoenix_dbl_black_audio_'+str(index)
    c.report[:]=[r for r in c.report if r['logical']!=logical]
    c.emit(e,logical,[(path,audio.path_id)],[])
    row=next(r for r in c.report if r['logical']==logical);key=c.bundle_key(row['file'])
    shutil.copy2(c.OUT/row['file'],out/row['file'])
    sound_manifest[0][key]=dict(c.bundles[key],section=100,size=5)
    directory,filename=path[len('assets/sevensins/patchresources/'):].rsplit('/',1)
    sound_manifest[2].setdefault('assets/sevensins/patchresources/',{}).setdefault(c.hash_name(directory+'/'),{})[c.hash_name(filename)]=key
    registrations.append(dict(id=198510001+index-1,path='dragonball',sub_path='goku_black',filename=name))
manifest_path.write_bytes(write(*sound_manifest))
(c.OUT/'br-m.bin').write_bytes(c.write(*c.manifest));(c.OUT/'assets.json').write_text(json.dumps(c.report,indent=2))
(c.ROOT/'Research/DBLegends/black-audio-registration.json').write_text(json.dumps(registrations,indent=2))
print('Packaged three original Rosé transformation voice cues')
