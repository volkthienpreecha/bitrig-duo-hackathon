"""Assemble labeled technical sheets/GIFs from genuine Kaprao Blender renders."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'Previews/Kaprao'
font_path='/System/Library/Fonts/Supplemental/Arial.ttf'
def font(s):return ImageFont.truetype(font_path,s)
sheet=Image.new('RGB',(2640,820),'#eee7dd');d=ImageDraw.Draw(sheet)
d.text((56,28),'KAPRAO / MODEL TURNAROUND',font=font(34),fill='#403730')
d.text((56,72),'Actual geometry • meters • +X forward • Y-up exchange files',font=font(21),fill='#716458')
for i,(name,label) in enumerate([('front','FRONT / +X'),('left','LEFT SIDE'),('rear','REAR / −X'),('right','RIGHT SIDE')]):
    im=Image.open(P/('kaprao-'+name+'.png')).convert('RGB').resize((640,640),Image.Resampling.LANCZOS)
    x=30+i*655;sheet.paste(im,(x,116));d.text((x+18,770),label,font=font(24),fill='#403730')
sheet.save(P/'kaprao-turnaround.png')
frames=P/'MotionFrames'
for clip,short,duration in [('Idle_Look','idle-look',1000),('Walk_InPlace','walk-in-place',67),('Jump_Fall','jump-fall',200),('Celebrate','celebrate',330)]:
    files=sorted(frames.glob(clip+'-*.png'))
    if not files:continue
    imgs=[Image.open(p).convert('RGB') for p in files]
    palette=imgs[0].quantize(colors=200,method=Image.Quantize.MEDIANCUT)
    gif=[im.quantize(palette=palette,dither=Image.Dither.FLOYDSTEINBERG) for im in imgs]
    kwargs={'loop':0} if clip in ('Idle_Look','Walk_InPlace') else {}
    gif[0].save(P/('kaprao-'+short+'.gif'),save_all=True,append_images=gif[1:],duration=duration,optimize=False,**kwargs)
# These are exact known stale build by-products; no user-authored source is removed.
for p in [ROOT/'Source/Kaprao/kaprao.blend1',ROOT/'Exports/Kaprao/textures/color_D5CBBA.exr']:
    if p.exists():p.unlink()
print('Created actual-model turnaround and four motion GIFs.')
