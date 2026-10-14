// Geometry regressions for the graph's visible card borders and connection ports.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import test from 'node:test';
const source=fs.readFileSync(new URL('../atlas/map-template.html',import.meta.url),'utf8');
const geometry=source.slice(source.indexOf('function dNodeBox('),source.indexOf('function dGraph('));
const c=vm.createContext({});vm.runInContext(geometry,c);
const node={kind:'line',x:300,y:300};
function near(actual,expected){assert.ok(Math.abs(actual-expected)<1e-8,`${actual} != ${expected}`);}
test('connections use the facing side, including neighbors above and below',()=>{
 for(const [x,y,px,py,nx,ny] of [[600,300,378,300,1,0],[0,300,222,300,-1,0],[300,0,300,270,0,-1],[300,600,300,330,0,1]]){
  const p=c.dNodePort(node,{x,y},'graph');near(p.x,px);near(p.y,py);near(p.nx,nx);near(p.ny,ny);
 }
});
test('ports stay on flat borders outside rounded corners for every angle and node shape',()=>{
 for(const kind of ['line','operator','country'])for(let angle=0;angle<360;angle++){
  const a={...node,kind},b={x:a.x+400*Math.cos(angle*Math.PI/180),y:a.y+400*Math.sin(angle*Math.PI/180)};
  const p=c.dNodePort(a,b,'graph'),box=c.dNodeBox(a,'graph');
  if(p.nx){near(Math.abs(p.x-a.x),box.w/2);assert.ok(Math.abs(p.y-a.y)<=box.h/2-box.r+1e-8);}
  else{near(Math.abs(p.y-a.y),box.h/2);assert.ok(Math.abs(p.x-a.x)<=box.w/2-box.r+1e-8);}
  assert.ok((b.x-a.x)*p.nx+(b.y-a.y)*p.ny>0);
 }
});
test('curve endpoints coincide with ports and controls leave both cards outward',()=>{
 const a=node,b={kind:'operator',x:520,y:70},g=c.dConnection(a,b,'graph');
 const n=g.path.match(/-?\d+(?:\.\d+)?/g).map(Number);
 near(n[0],g.start.x);near(n[1],g.start.y);near(n[6],g.end.x);near(n[7],g.end.y);
 assert.ok((n[2]-n[0])*g.start.nx+(n[3]-n[1])*g.start.ny>0);
 assert.ok((n[4]-n[6])*g.end.nx+(n[5]-n[7])*g.end.ny>0);
});
test('flow endpoints follow enlarged labels at every supported label scale',()=>{
 for(const scale of [1,1.5,2.5]){
  const a={kind:'line',x:110,y:50},b={kind:'operator',x:800,y:400};
  const g=c.dConnection(a,b,'flows',scale);
  near(g.start.x,110+78*scale);near(g.start.y,50);near(g.end.x,800-78*scale);near(g.end.y,400);
 }
});
test('drag and zoom repaint visual paths, hit areas and both ports from the same geometry',()=>{
 const a={id:'a',...node},b={id:'b',kind:'operator',x:600,y:100};
 const item=dataset=>({dataset,attrs:{},style:{},setAttribute(k,v){this.attrs[k]=v;}});
 const paths=[item({dWire:'0'}),item({dWire:'0'})],ports=[item({dPort:'0',end:'start'}),item({dPort:'0',end:'end'})];
 c.DG={layout:{nodes:[a,b],edges:[{source:'a',target:'b'}]},camera:{k:1}};c.DS={view:'graph'};c.$$=selector=>selector.includes('data-d-wire')?paths:ports;
 for(const [view,k,x,y] of [['graph',1,500,650],['graph',2,100,50],['flows',.4,110,50]]){
  Object.assign(c.DS,{view});c.DG.camera.k=k;Object.assign(a,{x,y});c.dPaintConnections();
  const g=c.dConnection(a,b,view,Math.max(1,Math.min(2.5,1/k)));
  for(const path of paths)assert.equal(path.attrs.d,g.path);
  for(const [i,end] of ['start','end'].entries()){const node=i?b:a;assert.equal(ports[i].style.left,`calc(50% + ${g[end].x-node.x}px)`);assert.equal(ports[i].style.top,`calc(50% + ${g[end].y-node.y}px)`);}
 }
});
