// Compose editable vector UI and annotated design boards from actual-model renders.
const fs=require('fs'),path=require('path');
const sharp=require('/Users/volkthienpreecha/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const B=path.resolve(__dirname,'..'),R=path.join(B,'Stages'),U=path.join(B,'UI/Stages');
const names=['01-workshop','02-garden','03-terrace'];
const text=(x,y,s,size=24)=>`<text x="${x}" y="${y}" fill="#F3E7CF" font-family="Arial,sans-serif" font-size="${size}">${s}</text>`;
const svg=(w,h,b)=>Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}">${b}</svg>`);
async function main(){
 const spec=JSON.parse(fs.readFileSync(path.join(U,'stage-ui-spec.json')));const thumbs=[];
 for(const [name,state] of Object.entries(spec.states)){
  const bg=await sharp(path.join(R,state.stage,'Previews/hero.png')).resize(1080,720).png().toBuffer();
  const overlay=fs.readFileSync(path.join(U,name+'-overlay.svg'),'utf8');
  const body=overlay.slice(overlay.indexOf('</title>')+8,overlay.lastIndexOf('</svg>'));
  fs.writeFileSync(path.join(U,name+'-concept.svg'),`<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="720"><title>${name} design concept</title><image width="1080" height="720" href="data:image/png;base64,${bg.toString('base64')}"/>${body}</svg>`);
  await sharp(bg).composite([{input:Buffer.from(overlay)}]).png().toFile(path.join(U,name+'-concept.png'));
  await sharp(Buffer.from(overlay)).png().toFile(path.join(U,name+'-overlay.png'));
  thumbs.push(await sharp(path.join(U,name+'-concept.png')).resize(540,360).toBuffer());
 }
 await sharp({create:{width:1668,height:776,channels:4,background:'#17292F'}}).composite(thumbs.map((input,i)=>({input,left:12+Math.floor(i/2)*552,top:12+(i%2)*388}))).png().toFile(path.join(U,'contact-sheet.png'));
 const overview=[];
 for(let i=0;i<names.length;i++){
  const folder=path.join(R,names[i]),p=path.join(folder,'Previews'),g=JSON.parse(fs.readFileSync(path.join(folder,'Validation/geometry.json')));
  for(const name of ['layout-top','layout-side'])await sharp(path.join(p,name+'.svg')).png().toFile(path.join(p,name+'.png'));
  const shots=[];
  for(let j=1;j<=3;j++)shots.push({input:await sharp(path.join(p,`fold-0${j}.png`)).resize(960,640).toBuffer(),left:(j-1)*960,top:90});
  let labels=text(32,51,g.stage.title+' / fold storyboard',32);
  g.fold_poses.forEach((f,j)=>{labels+=text(j*960+32,775,`${j+1} / ${j===1?'ALIGNED DESIGN REFERENCE':'DEPTH MISS REFERENCE'} / ${f.offset_degrees.toFixed(1)} deg`,22)+text(j*960+32,815,`Release depth error: ${f.depth_error_m.toFixed(2)} m`,20)});
  labels+=text(32,867,'DESIGN POSES ONLY. Actual hinge calibration, falling contact and stability must be tested in the event app.',22);
  await sharp({create:{width:2880,height:900,channels:4,background:'#17292F'}}).composite([...shots,{input:svg(2880,900,labels),left:0,top:0}]).png().toFile(path.join(p,'fold-storyboard.png'));
  overview.push({input:await sharp(path.join(p,'hero.png')).resize(960,640).toBuffer(),left:i*960,top:100});
 }
 const board=names.map((n,i)=>text(i*960+32,60,`${i+1} / ${spec.stages[i].name}`,30)).join('')+text(32,790,'ACTUAL 3D ASSET RENDERS / FLUFFY KAPRAO V3 / COZY CYBERPUNK NIGHT CITY / NOT GAMEPLAY FOOTAGE',22);
 await sharp({create:{width:2880,height:830,channels:4,background:'#17292F'}}).composite([...overview,{input:svg(2880,830,board),left:0,top:0}]).png().toFile(path.join(R,'three-stages.png'));
 console.log('STAGE_DESIGN_RENDERS_COMPLETE');
}
main().catch(e=>{console.error(e);process.exit(1)});
