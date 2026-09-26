"""Generate editable UI variants and measured vector stage plans; no app code."""
from pathlib import Path
import json,math,html,importlib.util
BASE=Path(__file__).resolve().parents[1];ROOT=BASE/'Stages'
spec=importlib.util.spec_from_file_location('ui',BASE/'Tools/ui_assets.py');u=importlib.util.module_from_spec(spec);spec.loader.exec_module(u)
UI=BASE/'UI/Stages';UI.mkdir(parents=True,exist_ok=True)
stages=[('01-workshop','Rooftop Repair Club'),('02-garden','Moonleaf Garden'),('03-terrace','Starlight Terrace')]
states={}
for i,(slug,title) in enumerate(stages,1):
 overlay=u.game_overlay();header=overlay[0];header['w']=300;header['h']=98
 header['children'][1]['text']=title
 header['children'].append(u.text('Stage progress',0,0,f'ROOFTOP {i} OF 3',12,'cyan',600))
 states[f'{slug}-gameplay']={'stage':slug,'overlay':overlay}
 # Modal uses one uninterrupted safe region; image coordinates only, not a device guarantee.
 children=[u.ico('check',0,0,36,'deepTeal'),u.text('Completion title',0,0,'All toys reached!' if i==3 else 'Toy reached!',28,'ink',700),u.text('Completion detail',0,0,'Three rooftops. One happy corgi.' if i==3 else f'{title} complete.',14,'muted',400),u.button('Replay demo' if i==3 else 'Next rooftop',0,0,332,'replay' if i==3 else 'swipe-right'),u.button('Replay rooftop',0,0,332,'replay',True)]
 panel=u.group('Stage completion panel',342,184,396,352,children,'cream',28,18,'VERTICAL',32)
 states[f'{slug}-complete']={'stage':slug,'overlay':[u.rect('Completion scrim',0,0,1080,720,'night',opacity=.46),panel]}
for name,state in states.items():
 state['overlay']=[u.layout(e) for e in state['overlay']]
 (UI/(name+'-overlay.svg')).write_text(u.svg(state['overlay'],title='Fold & Fetch '+name+' design overlay'))
(UI/'stage-ui-spec.json').write_text(json.dumps({'referenceOnly':True,'runtimeDefault':'Workshop only; hide stage progress and Next until master progression gate passes.','canvas':[1080,720],'stages':[{'id':i+1,'slug':s,'name':n} for i,(s,n) in enumerate(stages)],'states':states,'minimumTouchTargetPt':44,'behavior':{'retry':'Always accessible during active play; restore current-stage pre-gap checkpoint at live hinge pose.','release':'Native lower-right safe region, beside Retry; relocate outside projected objects and reserved regions.','next':'Only for enabled and verified progression. Available after the player reaches the goal on a genuinely seated beam; reset all stage state before entry.','replayRooftop':'Replay current stage from start.','replayDemo':'After stage 3, restart stage 1.','progress':'Read-only identity, not a level-selection control.','safeRegions':'Reposition within actual uninterrupted usable regions; never center a modal across the physical hinge.'}},indent=2)+'\n')
# Native editable text remains in SVG. Plans show actual measured anchors and proposed boxes.
def rect(x,y,w,h,fill,stroke='#78938e',r=5):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'
def text(x,y,s,size=18,color='#F3E7CF',weight=500):return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{html.escape(s)}</text>'
def line(x,y,x2,y2,color='#82D9CE',dash=''):return f'<path d="M{x} {y} L{x2} {y2}" stroke="{color}" stroke-width="2" fill="none"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def wrap(body,title):return '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1100" viewBox="0 0 1600 1100"><title>'+html.escape(title)+'</title>'+rect(0,0,1600,1100,'#17292F','#17292F',0)+body+'</svg>'
for slug,title in stages:
 d=ROOT/slug;file=d/'Validation/geometry.json'
 if not file.exists():continue
 g=json.loads(file.read_text());a=g['anchors_game'];depth=g['stage']['depth']
 top=text(56,65,title+' / top plan',32,weight=700)+text(56,104,'METERS · X = ROUTE · Z = DEPTH · DESIGN GEOMETRY, NOT PHYSICS PROOF',16,'#82D9CE')
 # X horizontal, game Z down. Draw world region with physically scaled route/pockets.
 tx=lambda x:790+x*110;tz=lambda z:580+z*110
 def box_top(x,z,w,h,c):return rect(tx(x-w/2),tz(z-h/2),w*110,h*110,c)
 top+=box_top(0,-.8,8.9,5.6,'#203d43')
 for x in [-2.55,2.55]:top+=box_top(x,depth,2.9,1.9,'#F3E7CF')
 for x in [a['ANCHOR_left_beam_contact'][0],a['ANCHOR_right_beam_contact'][0]]:top+=box_top(x,depth,.58,1.04,'#6F9D83')
 # Actual 2.96m route pocket opening. Beam here is a dashed seated reference.
 for sign in [-1,1]:top+=box_top(sign*1.29,depth,.38,.64,'#243449')
 top+=box_top(0,depth,2.9,.54,'#B77950')
 top+=line(tx(-4),tz(depth),tx(4),tz(depth),'#82D9CE','8 6')
 top+=line(tx(-1.8),tz(-1.2),tx(1.8),tz(-1.2),'#F0B49A')
 labels=[('START',a['ANCHOR_corgi_start'],(-65,160)),('GOAL',a['ANCHOR_exit_goal'],(-40,160)),('LEFT SUPPORT',a['ANCHOR_left_beam_contact'],(-100,124)),('RIGHT SUPPORT',a['ANCHOR_right_beam_contact'],(5,124)),('HINGE X',a['ANCHOR_hinge_axis'],(-65,-28))]
 for label,p,(dx,dy) in labels:
  x,y=tx(p[0]),tz(p[2]);top+=f'<circle cx="{x}" cy="{y}" r="6" fill="#82D9CE"/>'+line(x,y,x+dx+30,y+dy-20)+text(x+dx,y+dy,label,17)
 top+=box_top(-3,depth-.63,.56,.36,'#4D9B91')+text(tx(-3)-20,tz(depth-.63)+4,'CURB',12)
 top+=text(400,825,'UPPER CHUTE / RELEASE GATE: above route; see side plan.',17)
 top+=text(80,870,f'Route Z = {depth:+.2f} m. Both decks, supports, beam and goal use the same route offset.',21)
 top+=text(80,914,'2.90 m beam · 0.54 m deck depth · 2.96 m pocket opening · 30 mm end clearance',20)
 top+=text(80,956,'Tray below the gap. Optional curb sits off the main walking lane. Backdrop is non-walkable scenery.',18)
 top+=text(80,1025,'Native exports contain named anchors and separate collision proposals. Calibrate the hinge in the event app.',17,'#82D9CE')
 (d/'Previews/layout-top.svg').write_text(wrap(top,title+' top plan'))
 side=text(56,65,title+' / side plan',32,weight=700)+text(56,104,'LOOKING ALONG +X · Z = DEPTH · Y = HEIGHT · HINGE AXIS POINTS INTO VIEW',16,'#82D9CE')
 sx=lambda z:690+z*230;sy=lambda y:760-y*175
 side+=rect(sx(depth-.95),sy(0),1.9*230,.25*175,'#F3E7CF')
 side+=rect(sx(depth-.27),sy(0),.54*230,.22*175,'#B77950')
 side+=rect(sx(depth-1.125),sy(-.9),2.25*230,.22*175,'#4D9B91')
 hx,hy=sx(-1.2),sy(3)
 side+=f'<circle cx="{hx}" cy="{hy}" r="8" fill="#F0B49A"/>'+text(hx-155,hy-28,'HINGE (Y 3.00, Z -1.20)',18)
 for j,p in enumerate(g['fold_poses']):
  q=p['held_center_game'];px,py=sx(q[2]),sy(q[1]);color=['#AABCB6','#82D9CE','#E7BC76'][j]
  side+=line(hx,hy,px,py,color,'8 5' if j!=1 else '')+rect(px-.27*230,py-.11*175,.54*230,.22*175,color)
  side+=text(1110,265+j*64,f'{j+1}: {p["offset_degrees"]:+.1f}° offset',19,color)
  side+=text(1110,290+j*64,f'Z error {p["depth_error_m"]:+.2f} m',16,color)
  if j==1:side+=line(px,py,px,sy(0),'#82D9CE','4 5')
 side+=text(1080,570,'Fold changes depth + height.',19)+text(1080,606,'Settle, then tap Release.',19)+text(1080,642,'Gate follows the chute.',19)
 side+=text(1080,780,'DECK Y = 0 / SEATED BEAM',17)+text(1080,936,'RECOVERY TRAY',17)
 side+=text(80,985,'Both named supports overlap in this side view. The lower beam reference is seated, not a landing animation.',18)
 side+=text(80,1027,'Offsets are Blender design rotations. They are not absolute Duo hinge angles or guaranteed physical outcomes.',17,'#82D9CE')
 (d/'Previews/layout-side.svg').write_text(wrap(side,title+' side plan'))
print('DESIGN_SVGS_COMPLETE',len(states))
