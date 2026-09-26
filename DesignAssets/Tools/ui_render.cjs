// Render the editable UI overlays over the approved concept art.
// Usage: bundled node ui_render.cjs
const fs = require('fs');
const path = require('path');
const sharp = require('/Users/volkthienpreecha/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root = path.resolve(__dirname, '..');
async function main() {
  const world = fs.readFileSync(path.join(root, 'Concepts/workshop-world-concept.png'));
  const background = await sharp(world).resize(1080,720,{fit:'cover'}).png().toBuffer();
  for (const state of ['gameplay','pause','completion']) {
    const p = path.join(root,'UI/States',state+'-overlay.svg');
    const overlay = fs.readFileSync(p,'utf8');
    const body = overlay.slice(overlay.indexOf('</title>')+8,overlay.lastIndexOf('</svg>'));
    const compositeSVG = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1080" height="720" viewBox="0 0 1080 720"><title>Fold &amp; Fetch '+state+' UI concept</title><image x="0" y="0" width="1080" height="720" xlink:href="data:image/png;base64,'+background.toString('base64')+'"/>'+body+'</svg>';
    fs.writeFileSync(path.join(root,'UI/States',state+'-concept.svg'),compositeSVG);
    await sharp(background).composite([{input:Buffer.from(overlay)}]).png().toFile(path.join(root,'UI/States',state+'-concept.png'));
    await sharp(Buffer.from(overlay)).png().toFile(path.join(root,'UI/States',state+'-overlay.png'));
  }
  await sharp(path.join(root,'Palette/material-sheet.svg')).png().toFile(path.join(root,'Palette/material-sheet.png'));
  await sharp(path.join(root,'UI/hint-library.svg')).png().toFile(path.join(root,'UI/hint-library.png'));
  const thumbW=648,thumbH=432;
  const previews=await Promise.all(['gameplay','pause','completion'].map(s=>sharp(path.join(root,'UI/States',s+'-concept.png')).resize(thumbW,thumbH).toBuffer()));
  await sharp({create:{width:thumbW*3+64,height:thumbH+32,channels:4,background:'#17292F'}}).composite(previews.map((input,i)=>({input,left:16+i*(thumbW+16),top:16}))).png().toFile(path.join(root,'UI/ui-contact-sheet.png'));
  console.log('Rendered three concept states, three transparent overlays, palette, hints, and contact sheet.');
}
main().catch(e=>{console.error(e);process.exit(1);});
