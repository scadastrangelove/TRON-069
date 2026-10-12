// Actual graph gesture handlers, with pointer capture and node-drag offsets.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import test from 'node:test';
const source=fs.readFileSync(new URL('../atlas/map-template.html',import.meta.url),'utf8');
const start=source.indexOf('function createNetworkGestures('),code=source.slice(start,source.indexOf('\n}\n',start)+2);
const background={closest:()=>null},node={closest:s=>s==='[data-d-node]'?{dataset:{dNode:'node'}}:null};
function graph(){
 const events=new Map(),captures=new Set(),moves=[],activated=[];let camera={k:1,x:0,y:0},position={x:120,y:160},draggable=true;
 const stage={getBoundingClientRect:()=>({left:10,top:20}),setPointerCapture:id=>captures.add(id),hasPointerCapture:id=>captures.has(id),releasePointerCapture:id=>captures.delete(id),addEventListener:(type,fn)=>events.set(type,fn)};
 const api={camera:()=>camera,setCamera:c=>camera=c,position:()=>position,draggable:()=>draggable,activate:target=>activated.push(target),moveNode:(id,x,y)=>{moves.push({id,x,y});position={x,y};},zoom:(factor,x,y)=>{const k=Math.max(.12,Math.min(3,camera.k*factor));camera={k,x:x-(x-camera.x)*k/camera.k,y:y-(y-camera.y)*k/camera.k};}};
 const context=vm.createContext({stage,api});vm.runInContext(code+';createNetworkGestures(stage,api);',context);
 return {camera:()=>camera,setCamera:c=>camera=c,position:()=>position,moves,activated,flow:()=>draggable=false,
 event(type,id,x,y,target=background,extra={}){events.get(type)({pointerId:id,button:0,clientX:x+10,clientY:y+20,target,preventDefault(){},stopPropagation(){},...extra});}};
}
function near(c,expected){for(const key of ['k','x','y'])assert.ok(Math.abs(c[key]-expected[key])<1e-7,`${key}: ${c[key]} != ${expected[key]}`);}
test('small movement selects the captured node without moving it or the camera',()=>{
 const g=graph();g.event('pointerdown',1,108,143,node);g.event('pointermove',1,110,144);g.event('pointerup',1,110,144);assert.deepEqual(g.activated,[node]);assert.equal(g.moves.length,0);near(g.camera(),{k:1,x:0,y:0});
});
test('node drag preserves the grab offset and stays continuous across moves at any zoom',()=>{
 const g=graph();g.setCamera({k:2,x:-100,y:50});g.event('pointerdown',1,125,360,node);g.event('pointermove',1,145,390);assert.deepEqual(g.position(),{x:130,y:175});g.event('pointermove',1,165,400);assert.deepEqual(g.position(),{x:140,y:180});g.event('pointerup',1,165,400);assert.equal(g.activated.length,0);
});
test('background pan has no tap side effect, including a returning drag',()=>{
 const g=graph();g.event('pointerdown',1,100,100);g.event('pointermove',1,180,140);near(g.camera(),{k:1,x:80,y:40});g.event('pointermove',1,100,100);g.event('pointerup',1,100,100);assert.equal(g.activated.length,0);
});
test('pinch keeps its world anchor and remaining finger continues without a jump',()=>{
 const g=graph();g.event('pointerdown',1,100,200,node);g.event('pointerdown',2,200,200);g.event('pointermove',1,50,200);g.event('pointermove',2,250,200);near(g.camera(),{k:2,x:-150,y:-200});g.event('pointerup',2,250,200);g.event('pointermove',1,60,220);near(g.camera(),{k:2,x:-140,y:-180});g.event('pointerup',1,60,220);assert.equal(g.activated.length,0);assert.equal(g.moves.length,0);
});
test('cancel, third finger and lost capture never select',()=>{
 for(const cancel of ['pointercancel','lostpointercapture']){const g=graph();g.event('pointerdown',1,100,200,node);g.event(cancel,1,100,200);g.event('pointerup',1,100,200);assert.equal(g.activated.length,0);}
 const g=graph();g.event('pointerdown',1,100,200,node);g.event('pointerdown',2,200,200);g.event('pointerdown',3,250,200);g.event('pointerup',3,250,200);g.event('pointerup',2,200,200);g.event('pointerup',1,100,200);assert.equal(g.activated.length,0);
});
test('flow nodes pan instead of changing the layer arrangement',()=>{
 const g=graph();g.flow();g.event('pointerdown',1,100,200,node);g.event('pointermove',1,140,230);g.event('pointerup',1,140,230);assert.equal(g.moves.length,0);near(g.camera(),{k:1,x:40,y:30});assert.equal(g.activated.length,0);
});
test('wheel zoom anchors the cursor and clamps zoom levels',()=>{
 const g=graph();g.event('wheel',0,100,200,background,{deltaY:-10000});near(g.camera(),{k:3,x:-200,y:-400});g.event('wheel',0,100,200,background,{deltaY:10000});near(g.camera(),{k:.12,x:88,y:176});
});
test('release beyond the tap threshold never selects even without a move event',()=>{
 const g=graph();g.event('pointerdown',1,100,200,node);g.event('pointerup',1,140,200);assert.equal(g.activated.length,0);
});

test('replacing one pinch finger rebases the gesture without a camera jump',()=>{
 const g=graph();g.event('pointerdown',1,100,200);g.event('pointerdown',2,200,200);g.event('pointerdown',3,300,200);g.event('pointerup',1,100,200);const before={...g.camera()};g.event('pointermove',3,300,200);near(g.camera(),before);g.event('pointerup',2,200,200);g.event('pointerup',3,300,200);assert.equal(g.activated.length,0);
});
