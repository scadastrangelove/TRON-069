// Exercise the real archive loader offline, including failed and invalid responses.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const html=fs.readFileSync(new URL('../index.html',import.meta.url),'utf8');
const template=fs.readFileSync(new URL('../atlas/map-template.html',import.meta.url),'utf8');
const embedded=JSON.parse(html.match(/^const DATA = (.*);$/m)[1]);
const loader=template.split('/* SNAPSHOT LOADER */')[1].split('/* SNAPSHOT LOADER END */')[0];
const old=JSON.parse(fs.readFileSync(new URL('../atlas/snapshots/20261010-102121.json',import.meta.url),'utf8'));
function setup(response={ok:true,json:async()=>structuredClone(old)},pathname='/TRON-069/index.html'){
  const requests=[],status={hidden:true,textContent:''};
  const context=vm.createContext({DATA:structuredClone(embedded),URL,URLSearchParams,AbortSignal,
    location:{pathname,href:'https://example.test'+pathname,hash:''},
    document:{querySelector:()=>status},t:key=>key,
    fetch:async(url,options)=>{requests.push({url,options});if(response instanceof Error)throw response;return response;}});
  vm.runInContext(loader,context);
  return {context,requests,status,run:code=>vm.runInContext(code,context)};
}
test('embedded snapshot works offline without a request',async()=>{
  const c=setup(new Error('offline'));
  assert.equal(await c.run('loadSnapshot(snapshotTarget())'),true);
  assert.equal(c.requests.length,0);
});
test('historical archive replaces every measurement field without replacing editorial data',async()=>{
  const c=setup();const news=c.context.DATA.news,wanted=c.context.DATA.wanted;
  assert.equal(await c.run('loadSnapshot("20261010-102121")'),true);
  for(const key of Object.keys(old))assert.deepEqual(c.context.DATA[key],old[key],key);
  assert.equal(c.context.DATA.news,news);
  assert.equal(c.context.DATA.wanted,wanted);
  assert.equal(c.requests[0].url,'https://example.test/TRON-069/atlas/snapshots/20261010-102121.json');
  assert.equal(c.status.hidden,true);
  assert.equal(c.requests[0].options.signal.aborted,false);
});
test('archive paths work from both HTML entry points and the Pages directory URL',async()=>{
  for(const pathname of ['/TRON-069/','/TRON-069/atlas/tr-atlas.html']){
    const c=setup(undefined,pathname);
    await c.run('loadSnapshot("20261010-102121")');
    assert.equal(c.requests[0].url,'https://example.test/TRON-069/atlas/snapshots/20261010-102121.json');
  }
});
test('unknown, interrupted and external snapshot IDs never cause a request',async()=>{
  for(const id of ['20261010-101524','20261008-1451','https://elsewhere.test/data','../../private','constructor']){
    const c=setup();assert.equal(await c.run(`loadSnapshot(${JSON.stringify(id)})`),false);
    assert.equal(c.requests.length,0);assert.equal(c.context.DATA.snapshot,embedded.snapshot);
    assert.equal(c.run('snapshotError'),'snapshot_unknown');
  }
});
test('HTTP, offline, parse and incomplete payload failures leave current measurements intact',async()=>{
  const invalid={...old};delete invalid.orgdrill;
  const failed={...old,denominators:{...old.denominators,park:{collection_status:'error'}}};
  for(const response of [{ok:false,status:404},new Error('offline'),{ok:true,json:async()=>{throw new Error('invalid JSON');}},
    {ok:true,json:async()=>({...old,snapshot:'wrong-date'})},{ok:true,json:async()=>invalid},{ok:true,json:async()=>failed}]){
    const c=setup(response),before=JSON.stringify(c.context.DATA);
    assert.equal(await c.run('loadSnapshot("20261010-102121")'),false);
    assert.equal(JSON.stringify(c.context.DATA),before);
    assert.equal(c.run('snapshotError'),'snapshot_load_error');assert.equal(c.status.hidden,true);
  }
});
