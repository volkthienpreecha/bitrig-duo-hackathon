"""Rebuild editable local UI SVGs, palette documentation, and Figma input data.

This produces design assets only. No runtime/game code is generated.
"""
from pathlib import Path
import json, math, html

ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / 'UI'
PALETTE = ROOT / 'Palette'
COLORS = {
    'cream':'#F3E7CF', 'ink':'#243A40', 'night':'#17292F',
    'deepTeal':'#245E5A', 'teal':'#4D9B91', 'copper':'#B77950',
    'cyan':'#82D9CE', 'peach':'#F0B49A', 'gold':'#D7A35C',
    'leaf':'#738A64', 'muted':'#526368', 'line':'#CDBF9E',
}
PATHS = {
 'swipe-left':'M19 12H5 M10 7L5 12L10 17',
 'swipe-right':'M5 12H19 M14 7L19 12L14 17',
 'swipe-up':'M12 19V5 M7 10L12 5L17 10',
 'swipe-down':'M12 5V19 M7 14L12 19L17 14',
 'pause':'M8 5V19 M16 5V19',
 'resume':'M8 5L19 12L8 19Z',
 'restart':'M5 8A8 8 0 1 1 4 15 M5 3V8H10',
 'replay':'M5 8A8 8 0 1 1 4 15 M5 3V8H10',
 'audio-on':'M4 9H8L13 5V19L8 15H4Z M17 8C20 10 20 14 17 16',
 'audio-off':'M4 9H8L13 5V19L8 15H4Z M17 9L22 15 M22 9L17 15',
 'release':'M12 3V13 M8 9L12 13L16 9 M4 17H20V21H4Z',
 'fold':'M3 6L10 3L14 7L21 4V18L14 21L10 17L3 20Z M10 3V17 M14 7V21',
 'bell':'M5 16H19L17 13V9C17 2 7 2 7 9V13Z M10 20H14',
 'check':'M5 12L10 17L19 7',
}
def esc(s): return html.escape(str(s), quote=True)
def icon(name, color='ink', size=24):
    c=COLORS.get(color,color)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none"><title>{name.replace("-"," ")}</title><path d="{PATHS[name]}" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def elem(kind,name,**kw): return dict(type=kind,name=name,**kw)
def text(name,x,y,s,size=16,color='ink',weight=600): return elem('text',name,x=x,y=y,text=s,size=size,color=color,weight=weight)
def rect(name,x,y,w,h,color='cream',radius=0,opacity=1): return elem('rect',name,x=x,y=y,w=w,h=h,color=color,radius=radius,opacity=opacity)
def ico(name,x,y,size=24,color='ink'): return elem('icon',name,x=x,y=y,w=size,h=size,color=color,svg=icon(name,color,size))
def group(name,x,y,w,h,children,fill=None,radius=0,gap=0,axis=None,padding=0):
    return elem('group',name,x=x,y=y,w=w,h=h,children=children,fill=fill,radius=radius,gap=gap,axis=axis,padding=padding)
def button(label,x,y,w=144,icon_name=None,secondary=False):
    ch=[]
    if icon_name: ch.append(ico(icon_name,0,0,22,'ink' if secondary else 'cream'))
    ch.append(text('Label',0,0,label,16,'ink' if secondary else 'cream'))
    return group(label+' action',x,y,w,52,ch,'cream' if secondary else 'deepTeal',16,10,'HORIZONTAL',16)
def iconbutton(name,x,y):return group(name+' control',x,y,44,44,[ico(name,0,0)],'cream',16,0,'HORIZONTAL',10)

def schematic():
    # Flat, deliberately schematic placement reference. Final game uses smooth 3D art.
    c=[rect('Schematic night',0,0,1080,720,'night')]
    buildings=[(10,236,105,320),(122,306,64,270),(194,208,100,365),(828,272,95,316),(943,224,127,372)]
    for i,(x,y,w,h) in enumerate(buildings): c.append(rect('Distant rooftop '+str(i),x,y,w,h,'ink',14))
    c += [rect('Left roof',186,434,300,100,'deepTeal',22),rect('Roof cream rim',176,412,324,36,'cream',16),rect('Right roof',666,426,254,108,'deepTeal',22),rect('Right roof cream rim',656,404,274,36,'cream',16),rect('Workshop',210,260,192,155,'teal',25),rect('Workshop warm window',240,297,66,75,'peach',14),rect('Workshop door',321,298,49,117,'deepTeal',10),rect('Copper chute rail',432,215,202,18,'copper',9),rect('Beam ready',484,270,158,28,'cream',10),rect('Soft left planter',192,381,28,33,'copper',7),rect('Soft right planter',865,374,30,30,'copper',7),ico('bell',812,340,40,'gold')]
    c += [elem('ellipse','Kaprao body marker',x=352,y=371,w=65,h=39,color='gold'),elem('ellipse','Kaprao head marker',x=390,y=359,w=34,h=33,color='gold'),rect('Kaprao scarf marker',392,388,23,8,'teal',4)]
    c += [text('Reference label',408,566,'Schematic scene for UI placement',12,'cream',400)]
    return c

def game_overlay():
    header=group('Level header',36,32,232,74,[text('Game name',0,0,'FOLD & FETCH',12,'cream',600),text('Level name',0,0,'Rooftop repair',18,'cream',600)],'night',16,4,'VERTICAL',16)
    hint=group('Context hint',36,612,446,60,[ico('fold',0,0,24),group('Hint copy',0,0,368,40,[text('Hint title',0,0,'Fold to aim the chute.',16,'ink',600),text('Hint detail',0,0,'Tap Release when the beam lines up.',14,'muted',400)],None,0,2,'VERTICAL')],'cream',16,12,'HORIZONTAL',16)
    return [header,iconbutton('audio-on',948,32),iconbutton('pause',1000,32),hint,button('Retry',744,620,144,'restart',True),button('Release',900,620,144,'release')]

def paused_overlay():
    return [rect('Pause dim',0,0,1080,720,'night',opacity=.52),group('Pause panel',350,188,380,344,[text('Pause title',0,0,'Taking a breather',28,'ink',700),text('Pause detail',0,0,'Kaprao can wait.',14,'muted',400),button('Resume',0,0,316,'resume'),button('Replay rooftop',0,0,316,'replay',True),group('Audio row',0,0,316,44,[ico('audio-on',0,0),text('Audio label',0,0,'Sound on',14,'ink',600)],None,0,10,'HORIZONTAL',0)],'cream',28,18,'VERTICAL',32)]

def complete_overlay():
    return [rect('Complete dim',0,0,1080,720,'night',opacity=.42),group('Complete panel',350,188,380,344,[ico('bell',0,0,40,'deepTeal'),text('Complete title',0,0,'Toy reached!',28,'ink',700),text('Complete detail',0,0,'Nice work, Kaprao.',14,'muted',400),button('Replay rooftop',0,0,316,'replay'),group('Audio row',0,0,316,44,[ico('audio-on',0,0),text('Audio label',0,0,'Sound on',14,'ink',600)],None,0,10,'HORIZONTAL',0)],'cream',28,18,'VERTICAL',32)]

def layout(e):
    if e['type']=='group':
        for ch in e['children']: layout(ch)
        if e.get('axis'):
            pad=e.get('padding',0);gap=e.get('gap',0);axis=e['axis']
            sizes=[(ch.get('w',len(ch.get('text',''))*ch.get('size',16)*.52),ch.get('h',ch.get('size',16)*1.25)) for ch in e['children']]
            if axis=='HORIZONTAL':
                total=sum(x[0] for x in sizes)+gap*(len(sizes)-1)
                cursor=(e['w']-total)/2 if ('action' in e['name'] or 'control' in e['name']) else pad
                for ch,(w,h) in zip(e['children'],sizes):ch.update(x=cursor,y=(e['h']-h)/2);cursor+=w+gap
            else:
                cursor=pad
                for ch,(w,h) in zip(e['children'],sizes):ch.update(x=pad,y=cursor);cursor+=h+gap
    return e
def render(e):
    typ=e['type'];x=e.get('x',0);y=e.get('y',0);c=COLORS.get(e.get('color'),e.get('color'))
    if typ=='rect':return f'<rect id="{esc(e["name"])}" x="{x}" y="{y}" width="{e["w"]}" height="{e["h"]}" rx="{e["radius"]}" fill="{c}" opacity="{e["opacity"]}"/>'
    if typ=='ellipse':return f'<ellipse cx="{x+e["w"]/2}" cy="{y+e["h"]/2}" rx="{e["w"]/2}" ry="{e["h"]/2}" fill="{c}"/>'
    if typ=='text':return f'<text id="{esc(e["name"])}" x="{x}" y="{y+e["size"]}" font-family="Nunito, ui-rounded, -apple-system, Arial, sans-serif" font-size="{e["size"]}" font-weight="{e["weight"]}" fill="{c}">{esc(e["text"])}</text>'
    if typ=='icon':return f'<g id="{esc(e["name"])}" transform="translate({x} {y}) scale({e["w"]/24})"><path d="{PATHS[e["name"]]}" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></g>'
    if typ=='group':
        fill=f'<rect width="{e["w"]}" height="{e["h"]}" rx="{e["radius"]}" fill="{COLORS[e["fill"]]}"/>' if e.get('fill') else ''
        return f'<g id="{esc(e["name"])}" transform="translate({x} {y})">{fill}'+''.join(render(ch) for ch in e['children'])+'</g>'
def svg(elements,w=1080,h=720,title='Fold & Fetch UI concept'):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><title>{esc(title)}</title>'+''.join(render(layout(e)) for e in elements)+'</svg>'
def linear(v):return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4
def srgb(hex):return [int(hex[i:i+2],16)/255 for i in (1,3,5)]
def oklch(hex):
    r,g,b=map(linear,srgb(hex));l=(.4122214708*r+.5363325363*g+.0514459929*b)**(1/3);m=(.2119034982*r+.6806995451*g+.1073969566*b)**(1/3);s=(.0883024619*r+.2817188376*g+.6299787005*b)**(1/3)
    L=.2104542553*l+.793617785*m-.0040720468*s;a=1.9779984951*l-2.428592205*m+.4505937099*s;b=.0259040371*l+.7827717662*m-.808675766*s
    return f'oklch({L*100:.2f}% {math.hypot(a,b):.4f} {(math.degrees(math.atan2(b,a))+360)%360:.2f})'
def luminance(hex):return sum(v*w for v,w in zip(map(linear,srgb(hex)),(.2126,.7152,.0722)))
def contrast(a,b):
    hi,lo=sorted([luminance(COLORS[a]),luminance(COLORS[b])],reverse=True);return round((hi+.05)/(lo+.05),2)

def main():
    for d in [UI/'Icons',UI/'States',PALETTE,ROOT/'Validation']:d.mkdir(parents=True,exist_ok=True)
    for name in PATHS:(UI/'Icons'/f'{name}.svg').write_text(icon(name))
    states={}
    for name,fn in [('gameplay',game_overlay),('pause',paused_overlay),('completion',complete_overlay)]:
        overlays=[layout(e) for e in fn()];states[name]={'w':1080,'h':720,'scene':schematic(),'overlay':overlays}
        (UI/'States'/f'{name}-overlay.svg').write_text(svg(overlays,title=f'Fold & Fetch {name} overlay'))
        (UI/'States'/f'{name}-concept.svg').write_text(svg(schematic()+overlays,title=f'Fold & Fetch {name} concept, schematic scene'))
    hints=[('swipe-left','Swipe left','Move left'),('swipe-right','Swipe right','Move right'),('swipe-up','Swipe up','Jump'),('swipe-down','Swipe down in the air','Dash'),('fold','Fold to aim the chute.','Depth and height change together.'),('release','Beam lined up?','Tap Release.')]
    hint_els=[rect('Hint sheet canvas',0,0,1000,672,'cream'),text('Hint sheet title',40,32,'One hint, at the right moment.',28,'ink',700),text('Hint sheet detail',40,76,'Show contextually. Dismiss after the first successful action.',16,'muted',400)]
    for i,(name,a,b) in enumerate(hints):
        hint_els += [ico(name,44,136+i*82,32),text('Hint '+str(i),96,134+i*82,a,18),text('Explanation '+str(i),96,162+i*82,b,14,'muted',400)]
    (UI/'hint-library.svg').write_text(svg(hint_els,1000,672,'Contextual gesture hints'))
    usage={'cream':'Opaque controls, painted roof edges, corgi muzzle','ink':'UI text, tool details, silhouette separation','night':'Sky, deep recesses, pause dim','deepTeal':'Primary UI action, doors and deep painted surfaces','teal':'Kaprao scarf, shop enamel, secondary world accents','copper':'Warm metal rails, lamps, repair details','cyan':'Small emissive signs, RGB glasses accent','peach':'Warm lamp glow and tiny sign accents','gold':'Kaprao coat and bell','leaf':'Desaturated rooftop plants','muted':'Secondary text on cream','line':'Quiet control borders and warm neutral trim'}
    material={'cream':(.72,0),'ink':(.7,0),'night':(.95,0),'deepTeal':(.55,0),'teal':(.48,0),'copper':(.32,.65),'cyan':(.3,0),'peach':(.35,0),'gold':(.78,0),'leaf':(.82,0),'muted':(.75,0),'line':(.78,0)}
    palette={name:{'hex':hex,'oklch':oklch(hex),'usage':usage[name],'roughness':material[name][0],'metallic':material[name][1],'emission':'small localized accents only' if name in ('cyan','peach') else 'none'} for name,hex in COLORS.items()}
    (PALETTE/'palette.json').write_text(json.dumps(palette,indent=2)+'\n')
    (PALETTE/'palette.css').write_text(':root {\n'+''.join(f'  --ff-{name}: {oklch(hex)}; /* {hex} */\n' for name,hex in COLORS.items())+'}\n')
    sheet=[rect('Palette sheet background',0,0,1440,950,'cream'),text('Palette title',48,36,'Night shift, warm lights.',38,'ink',700),text('Palette subtitle',48,96,'Fold & Fetch  /  Color and material reference',18,'muted',400)]
    for i,(name,hex) in enumerate(COLORS.items()):
        x=48+(i%4)*344;y=158+(i//4)*244
        sheet += [rect(name+' swatch',x,y,312,116,name,20),text(name+' name',x,y+132,name,18),text(name+' hex',x,y+160,hex,14,'muted',400),text(name+' material',x,y+186,f'Roughness {material[name][0]:.2f}  ·  Metal {material[name][1]:.2f}',13,'muted',400)]
    sheet += [text('Palette footnote',48,902,'Use smooth curved geometry. Cyan and peach emission stay localized; UI never glows.',16,'ink',400)]
    (PALETTE/'material-sheet.svg').write_text(svg(sheet,1440,950,'Fold & Fetch color and material sheet'))
    (UI/'ui-spec.json').write_text(json.dumps({'colors':COLORS,'iconPaths':PATHS,'states':states,'hints':hints,'referenceOnly':True,'gameplayPreviewState':'aiming; first launch uses movement hint','behavior':{'retry':'Checkpoint recovery, always accessible during active play.','replayRooftop':'Restart current stage from beginning.','release':'Lower-right safe region beside Retry; enabled when settled even if misaligned.','goal':'Player reaches toy after genuine bridge readiness.','hintAuthority':'Master-Prompt.md state table; jump/dash practice is optional.'}},indent=2)+'\n')
    ratios={a+'/'+b:contrast(a,b) for a,b in [('ink','cream'),('deepTeal','cream'),('muted','cream'),('cream','night')]}
    (ROOT/'Validation'/'ui-contrast.json').write_text(json.dumps({'method':'WCAG sRGB relative luminance','ratios':ratios,'normalTextThreshold':4.5,'allPairsPass':all(x>=4.5 for x in ratios.values())},indent=2)+'\n')
    print(json.dumps({'icons':len(PATHS),'states':len(states),'paletteColors':len(COLORS),'contrast':ratios},indent=2))
if __name__=='__main__':main()
