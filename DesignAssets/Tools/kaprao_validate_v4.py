"""Validate delivered GLB buffers, skins, clip endpoints, root motion and triangle budget."""
import json,struct,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1] / 'Revisions/Kaprao-v4'
p=ROOT/'Exports/Kaprao/kaprao.glb';b=p.read_bytes()
magic,version,total=struct.unpack_from('<4sII',b,0)
assert magic==b'glTF' and version==2 and total==len(b)
n,t=struct.unpack_from('<II',b,12);doc=json.loads(b[20:20+n]);bn,bt=struct.unpack_from('<II',b,20+n);blob=b[28+n:28+n+bn]
types={5120:('b',1),5121:('B',1),5122:('h',2),5123:('H',2),5125:('I',4),5126:('f',4)}
sizes={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}
def acc(i):
    a=doc['accessors'][i];v=doc['bufferViews'][a['bufferView']];ty,sz=types[a['componentType']];num=sizes[a['type']];step=v.get('byteStride',sz*num);start=v.get('byteOffset',0)+a.get('byteOffset',0)
    return [struct.unpack_from('<'+ty*num,blob,start+k*step) for k in range(a['count'])]
checks=[]
def check(name,passed,detail):
    checks.append({'check':name,'passed':bool(passed),'detail':detail})
meshes=[];all_pos=[];tri=0;max_norm_error=0;weight_error=0;degenerate=0
for m in doc['meshes']:
    mt=0;pv=0
    for prim in m['primitives']:
        assert prim.get('mode',4)==4
        a=prim['attributes'];positions=acc(a['POSITION']);normals=acc(a['NORMAL']);weights=acc(a['WEIGHTS_0']);joints=acc(a['JOINTS_0']);idx=[x[0] for x in acc(prim['indices'])]
        check(m['name']+' finite attributes',all(math.isfinite(v) for row in positions+normals+weights for v in row),'position, normal and skin-weight buffers')
        check(m['name']+' indices in range',all(0<=i<len(positions) for i in idx),len(idx))
        check(m['name']+' valid skin joints',all(0<=i<len(doc['skins'][0]['joints']) for row in joints for i in row),'shared quadruped skin')
        max_norm_error=max(max_norm_error,max(abs(math.sqrt(sum(x*x for x in row))-1) for row in normals))
        weight_error=max(weight_error,max(abs(sum(row)-1) for row in weights))
        mt+=len(idx)//3;pv+=len(positions);all_pos.extend(positions)
        for z in range(0,len(idx),3):
            x,y,w=[positions[idx[z+j]] for j in range(3)];u=[y[i]-x[i] for i in range(3)];v=[w[i]-x[i] for i in range(3)];c=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
            if sum(q*q for q in c)<1e-20:degenerate+=1
    tri+=mt;meshes.append({'name':m['name'],'triangles':mt,'exported_vertices_including_material_splits':pv,'primitives':len(m['primitives'])})
check('all normals approximately unit length',max_norm_error<.002,max_norm_error)
check('all skin weights normalized',weight_error<.0001,weight_error)
check('no zero-area rendered triangles',degenerate==0,degenerate)
check('revision geometry ceiling (not a device benchmark)',tri<=60000,tri)
check('no exported collision or studio geometry',not any(n.get('name','').startswith(('COL_','STUDIO')) for n in doc['nodes']),[n.get('name') for n in doc['nodes']])
check('removable sunglasses node exists',any(n.get('name')=='Kaprao_RGB_Sunglasses_REMOVABLE' for n in doc['nodes']),'hide that one skinned node')
root=next(i for i,n in enumerate(doc['nodes']) if n.get('name')=='root')
clips=[]
for animation in doc.get('animations',[]):
    name=animation['name'];loop=name in ('Idle_Look','Walk_InPlace');dur=0;error=0;root_motion=0
    for channel in animation['channels']:
        s=animation['samplers'][channel['sampler']];times=acc(s['input']);values=acc(s['output']);dur=max(dur,times[-1][0]-times[0][0]);error=max(error,max(abs(a-b) for a,b in zip(values[0],values[-1])))
        if channel['target']['node']==root and channel['target']['path']=='translation':root_motion=max(root_motion,max(abs(a-b) for val in values for a,b in zip(val,values[0])))
    check(name+' no root translation',root_motion<1e-7,root_motion)
    if loop:check(name+' seamless endpoint values',error<1e-5,error)
    clips.append({'name':name,'duration_seconds':round(dur,5),'loop':loop,'channel_count':len(animation['channels']),'endpoint_max_error':error,'root_translation_max_error':root_motion})
check('all required clips exported',set(a['name'] for a in clips)=={'Idle_Look','Walk_InPlace','Jump_Fall','Celebrate'},[a['name'] for a in clips])
bounds=[[min(p[i] for p in all_pos) for i in range(3)],[max(p[i] for p in all_pos) for i in range(3)]]
check('floor at Y zero',abs(bounds[0][1])<.005,bounds)
report={'file':str(p.relative_to(ROOT)),'bytes':len(b),'result':'PASS' if all(c['passed'] for c in checks) else 'FAIL','scope':'File-level GLB validation only. Native SceneKit/Duo testing is performed separately by the coordinator.','mesh_count':len(meshes),'skin_count':len(doc['skins']),'joint_count':len(doc['skins'][0]['joints']),'material_count':len(doc['materials']),'triangles':tri,'world_coordinate_contract':'Y-up; +X route/character forward; meters; origin on floor.','bounds_in_exported_geometry_m':bounds,'meshes':meshes,'clips':clips,'checks':checks}
(ROOT/'Validation/kaprao-validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:report[k] for k in ('result','triangles','material_count','skin_count','joint_count','clips')},indent=2))
if report['result']!='PASS':raise SystemExit(1)
