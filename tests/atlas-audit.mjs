// Offline source-level audit. No browser, network, credentials, or device probes.
// Executes selected application functions with inert output sinks, not the page bootstrap.
// Run: node tests/atlas-audit.mjs [atlas/tr-atlas.html|index.html]
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const target = process.argv[2] || 'atlas/tr-atlas.html';
const html = fs.readFileSync(path.join(root, target), 'utf8');
const source = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const data = JSON.parse(source.match(/^const DATA = (.*);$/m)[1]);
const operatorFixture = JSON.parse(fs.readFileSync(path.join(root,'data/mapdata',`snapshot-${data.snapshot}`,'org-drill','igdauthentication--US.json'),'utf8'));
const blueStreamCount = operatorFixture.orgs.find(org=>org.value==='Blue Stream').count;
function sourceOrgTotal(cc, labels) {
  const record=JSON.parse(fs.readFileSync(path.join(root,'data/mapdata',`snapshot-${data.snapshot}`,'org-drill',`tr069-http-server--${cc}.json`),'utf8'));
  return record.orgs.filter(org=>labels.includes(org.value)).reduce((sum,org)=>sum+org.count,0);
}
const tpgExactTotal=sourceOrgTotal('AU',['TPG Internet Pty Ltd','TPG Internet Pty Ltd.']);
const tpgGroupTotal=sourceOrgTotal('AU',['TPG Internet Pty Ltd','TPG Internet Pty Ltd.','iiNet Limited']);
const windTreTotal=sourceOrgTotal('IT',['WIND TRE S.P.A.']);
const results = [];
function test(id, description, work) {
  try {
    const evidence = work();
    results.push({ id, description, status: 'PASS', evidence });
  } catch (e) {
    results.push({ id, description, status: 'FAIL', evidence: e.message });
  }
}
function expect(ok, evidence) { if (!ok) throw new Error(evidence); return evidence; }
function section(start, end) { return source.slice(source.indexOf(start), source.indexOf(end)); }
function fn(name) {
  const lines = source.split('\n');
  const start = lines.findIndex(l => l.startsWith(`function ${name}(`));
  if (start < 0) throw new Error(`Missing function: ${name}`);
  if (lines[start].endsWith('}')) return lines[start];
  const end = lines.findIndex((l, i) => i > start && /^}\s*;?\s*$/.test(l));
  if (end < 0) throw new Error(`Missing function end: ${name}`);
  return lines.slice(start, end + 1).join('\n');
}
function context({ hash = '', storageBlocked = false, storedLanguage = null, payload = data } = {}) {
  const elements = new Map();
  const element = selector => {
    if (!elements.has(selector)) elements.set(selector, {
      innerHTML: '', textContent: '', value: '', hidden: false, style: {setProperty(){}}, dataset: {},
      classList: { add() {}, remove() {}, toggle() {} },
      focus() {},
      attrs: {}, setAttribute(key,value){this.attrs[key]=value;}, matches(){return false;}, contains(){return false;},
      createSVGPoint() { return {x:0,y:0,matrixTransform(matrix) { return {x:this.x*matrix.scale,y:(this.y-matrix.offsetY)*matrix.scale}; }}; },
      getScreenCTM() { return {inverse:()=>({scale:2,offsetY:150})}; },
      querySelectorAll() { return []; }, querySelector() { return null; },
      getBoundingClientRect() { return { left: 0, top: 0, width: 660, height: 600 }; }
    });
    return elements.get(selector);
  };
  const sandbox = {
    DATA: structuredClone(payload), URLSearchParams, Intl, Blob, console,
    location: { hash, reload() { sandbox.reloaded=true; } }, navigator: { language: 'en' },
    localStorage: {
      getItem() { if (storageBlocked) throw new Error('SecurityError: storage unavailable'); return storedLanguage; },
      setItem() { if (storageBlocked) throw new Error('SecurityError: storage unavailable'); }
    },
    document: { querySelector: element, querySelectorAll: () => [], documentElement: {} },
    history: { replaceState(_a, _b, url) { sandbox.location.hash = url; }, pushState(_a, _b, url) { sandbox.location.hash = url; } },
    setTimeout(callback) { sandbox.timer = callback; return 1; }, clearTimeout() {},
    renderShortcuts() {}, scaleStatics() {}, element,
    dl(blob, name) { sandbox.download = { blob, name }; }
  };
  vm.createContext(sandbox);
  const chunks = [
    section('const I18N =', 'function REG_NAME'),
    section('/* SNAPSHOT LOADER */', '/* SNAPSHOT LOADER END */'),
    'addUncollectedLines();',
    section('const $ =', '/* URL */'),
    fn('snapshotLabel'), fn('renderSnapshotPicker'), fn('chooseSnapshot'),
    fn('REG_NAME'), fn('urlRead'), fn('urlWrite'), fn('geoPass'), fn('orgPass'), fn('computeSlice'),
    'let SLICE, SLICE_FULL, GEOT; const selCountries=()=>[...S.geo].filter(t=>t.startsWith("c:")).map(t=>t.slice(2));',
    'const insp=$("#inspector"),kkL=$("#kkList"); let kkItems=[],kkSel=0,toastT=null;',
    'const W=1320,H=600,svg=$("#world"); let newsIndex=0,newsPaused=false;const newsMotion={matches:false};',
    ...['facetBtnState','renderChips','renderMode','lineGeoTotals','renderLinesTable','card','badgeHtml','serviceBadge','variantHtml',
      'buildDeploymentIndex','dEntity','dAggregate','dFiltered','dCellState','dEvidence','dDetail','dNodeKeys','dNodeInfo','dTouches','dGraphRows','dBuildGraph','dForceLayout','dFlowLayout','dNodeDetail','dNodeBox','dNodePort','dConnection','dPaintConnections','dGraph','dFitGraph','dPaintCamera','dExpandNode','dMatrix','renderDeployments',
      'sourcesHtml','ecoLineLink','ecoText','ecoName','ecoFiltered','ecoLayout','ecoSources','ecoRenderDetail','renderEcosystem',
      'renderInspector','toggleInsp','computeShortcuts','kkBuild','showToast','exportCSV','exportJSON','svgXY',
      'coverageNote','unknownCountryTotal','renderRegistry','renderFindings','renderAbout','renderOverview','renderLegend',
      'newsText','newsDate','renderNewsTicker','renderNews','newsStep','shouldRotateNews'].map(fn),
    'function refreshTest(){SLICE=computeSlice();SLICE_FULL=computeSlice(true);GEOT=lineGeoTotals();}',
    'DNcur=new Intl.DisplayNames([LANG],{type:"region"});'
  ];
  // Each isolated VM indexes the full snapshot. Keep setup separate from the
  // three-second function-call bound, including on busy development machines.
  vm.runInContext(chunks.join('\n'), sandbox, { timeout: 10000 });
  return { run: code => vm.runInContext(code, sandbox, { timeout: 3000 }), sandbox, element };
}

test('syntax', 'Application JavaScript parses', () => { new vm.Script(source); return 'Parsed'; });
test('daily-snapshot-picker', 'One best snapshot per day; archived shared links retain exact dates', () => {
  const c=context();c.run('renderSnapshotPicker()');
  const choices=[...c.element('#snapshotSelect').innerHTML.matchAll(/<option value="([^"]+)"([^>]*)>/g)];
  const visible=choices.filter(match=>!match[2].includes('hidden')).map(match=>match[1]);
  expect(new Set(visible.map(id=>id.slice(0,8))).size===visible.length,'Duplicate daily choices');
  expect(visible.includes('20261008-2227')&&visible.includes('20261010-102121'),'Best historical runs absent');
  c.run('DATA.snapshot="20261010-083331";renderSnapshotPicker()');
  expect(c.element('#snapshotSelect').value==='20261010-083331','Archived selection lost');
  expect(c.element('#snapshotSelect').innerHTML.includes('value="20261010-083331" hidden'),'Archived run entered daily menu');
  return visible;
});
test('snapshot-filter-roundtrip', 'Date selection preserves map, language, registry and network filters in the URL', () => {
  const hash='#'+new URLSearchParams({lang:'es',lines:'tr069-http-server',geo:'c:AU',mode:'countries',tab:'ecosystem',eco_view:'networks',net_view:'matrix',net_country:'AU',net_line:'tr069-http-server',net_operator:'o:tpg',net_group:'1',net_q:'TPG',reg_q:'Huawei',reg_service:'cpe',cc_q:'Australia'})+'&org='+encodeURIComponent('raw:TPG Internet Pty Ltd.')+'&org='+encodeURIComponent('raw:TPG Internet Pty Ltd');
  const c=context({hash});c.run('urlRead();urlWrite()');
  const before=new URLSearchParams(c.sandbox.location.hash.slice(1));
  c.run('chooseSnapshot("20261010-102121")');
  const after=new URLSearchParams(c.sandbox.location.hash.slice(1));
  expect(c.sandbox.reloaded&&after.get('snapshot')==='20261010-102121','Date selection did not navigate');
  for(const [key] of before)if(key!=='snapshot')expect(JSON.stringify(before.getAll(key))===JSON.stringify(after.getAll(key)),`Lost ${key}`);
  const old=JSON.parse(fs.readFileSync(path.join(root,'atlas/snapshots/20261010-102121.json'),'utf8'));
  const restored=context({hash:c.sandbox.location.hash,payload:{...data,...old}});
  restored.run('urlRead();refreshTest();renderOverview();renderSnapshotPicker();urlWrite()');
  expect(restored.run('S.lines.has("tr069-http-server")&&S.geo.has("c:AU")&&S.orgs.size===2&&LANG==="es"&&DS.operator==="o:tpg"&&DS.view==="matrix"'),'Filters changed after historical data was loaded');
  expect(restored.element('#overviewPark').title===new Intl.NumberFormat('es').format(old.denominators.park.total),'Current measurements leaked into history');
  return 'Snapshot URL, repeated organization parameters, language and both views survive';
});
test('historical-uncollected-line', 'New signatures remain selected on old dates without importing current counts', () => {
  const old=JSON.parse(fs.readFileSync(path.join(root,'atlas/snapshots/20261008-1651.json'),'utf8'));
  expect(!old.lines['freeacs'],'Fixture unexpectedly collected FreeACS');
  const c=context({hash:'#lang=en&lines=freeacs&geo=c:IT&org=raw%3ABlue+Stream',payload:{...data,...old}});
  c.run('urlRead();refreshTest();renderSnapshotPicker();renderLegend();renderInspector();urlWrite()');
  expect(c.run('S.lines.has("freeacs")&&S.geo.has("c:IT")&&S.orgs.size===1'),'Unavailable filter discarded');
  expect(c.run('DATA.lines["freeacs"].total===null&&!DISJOINT.includes("freeacs")'),'Missing line gained a current count');
  expect(c.element('#sliceSum').textContent==='—'&&!c.element('#snapshotStatus').hidden,'Missing data shown as zero');
  expect(c.element('#snapshotStatus').textContent.includes('not collected'),'Missing collection note');
  expect(!c.element('#inspector').innerHTML.includes('undefined'),'Invalid historical inspector');
  return 'Filter kept, unavailable counts marked, absent line excluded from the core';
});
test('overview-count-scopes', 'Worldwide port and signature counts remain distinct from a filtered map selection', () => {
  const c=context();
  const coreTotal=Object.entries(data.lines).filter(([slug])=>!data.excluded.includes(slug)).reduce((sum,[,line])=>sum+line.total,0);
  c.run('refreshTest();renderOverview();renderLegend();');
  expect(c.element('#overviewPark').title===new Intl.NumberFormat('en').format(data.denominators.park.total), 'Port baseline lost');
  expect(c.element('#overviewSignatures').title===new Intl.NumberFormat('en').format(coreTotal), 'Core total must include unknown geography');
  const allSignatures=c.element('#overviewSignatures').textContent;
  c.run('S.lines=new Set(["huaweihomegateway"]);S.geo.add("c:US");refreshTest();renderOverview();renderLegend();');
  expect(c.run('SLICE.total')===data.lines.huaweihomegateway.countries.US, 'Filtered Huawei slice differs from all-port query');
  expect(c.element('#overviewSignatures').textContent===allSignatures, 'Worldwide total changed with filters');
  const date=data.snapshot.slice(0,8).replace(/(\d{4})(\d{2})(\d{2})/,'$1-$2-$3');
  expect(c.element('#sliceSub').textContent.includes(date), 'Slice date must show the calendar date');
  for(const lang of ['en','ru','es','zh'])c.run(`LANG=${JSON.stringify(lang)};renderOverview();`);
  return `Port baseline ${data.denominators.park.total}; core ${coreTotal}; selection scoped separately`;
});
test('ecosystem-views', 'Filters, neighborhoods and shared graph state preserve evidence scope', () => {
  const c=context({hash:'#lang=es&tab=ecosystem&eco_node=gateway&eco_focus=gateway&eco_hyp=1&eco_depth=2'});
  c.run('urlRead();renderEcosystem();urlWrite();');
  expect(c.run('S.tab')==='ecosystem', 'Graph route lost');
  expect(c.run('ecoFiltered().length')===2, 'Gateway neighborhood should contain observation and hypothesis');
  expect(c.sandbox.location.hash.includes('eco_focus=gateway'), 'Shared focus lost');
  expect(c.sandbox.location.hash.includes('eco_depth=2'), 'Shared depth lost');
  c.run('E.hyp=false');
  expect(c.run('ecoFiltered().length')===1, 'Hypothesis visible while disabled');
  c.run('E.focus="";E.q="MiFibra";E.kind="deployment"');
  expect(c.run('ecoFiltered()[0].id')==='mifibra-zte-deployment', 'Search or evidence filter failed');
  c.run('E.q="missing-component";renderEcosystem()');
  expect(c.element('#ecoEmpty').hidden===false, 'Empty results missing');
  c.sandbox.location.hash='#tab=ecosystem&eco_node=__proto__&eco_edge=missing&eco_depth=999&eco_kind=invalid';
  c.run('urlRead()');
  expect(c.run('E.node===""&&E.edge===""&&E.depth===1&&E.kind==="all"'), 'Invalid graph route accepted');
  return 'Valid filters and share state; invalid IDs rejected';
});
test('ecosystem-localization', 'All graph cards render in four languages with dated map counts', () => {
  const c=context();
  for(const lang of ['en','ru','es','zh']) {
    c.run(`LANG=${JSON.stringify(lang)};E.view="evidence";E.node="genieacs";E.edge="";renderEcosystem()`);
    const text=c.element('#ecoDetail').innerHTML;
    expect(text.includes(data.lines['genieacs-admin-ui'].taken), 'Snapshot date missing');
    expect(text.includes('data-eco-map="genieacs-admin-ui"'), 'Map link missing');
    for(const edge of data.ecosystem.edges) {
      c.run(`E.node="";E.edge=${JSON.stringify(edge.id)};E.hyp=true;renderEcosystem()`);
      const html=c.element('#ecoDetail').innerHTML;
      expect(html.includes(edge.reviewed), 'Evidence review date missing');
      expect(!/eco_[a-z_]+/.test(html.replace(/data-eco-[a-z]+/g,'')), 'Untranslated graph key');
      if(lang!=='ru')expect(!/[А-Яа-яЁё]/.test(html), `Russian fallback in ${lang}/${edge.id}`);
    }
  }
  return 'Node and edge cards translated; counts use the selected snapshot';
});
test('network-combinations', 'Country-scoped operator aliases preserve many-to-many observations', () => {
  const c=context();
  c.run('DS.country="IT";DS.operator="o:windtre"');
  const rows=c.run('dFiltered()');
  expect(rows.length>=5, 'WindTre combinations collapsed');
  expect(windTreTotal>0&&rows.find(r=>r.line==='tr069-http-server').count===windTreTotal,'WindTre differs from its source count');
  c.run('DS.country="AU";DS.operator="o:tpg"');
  const tpg=c.run('dFiltered().find(r=>r.line==="tr069-http-server")');
  expect(tpgExactTotal>0&&tpg.count===tpgExactTotal&&tpg.raws.length===2,'TPG aliases did not retain exact source members');
  c.run('DS.group=true;DS.operator="g:tpg-telecom"');
  const grouped=c.run('dFiltered().find(r=>r.line==="tr069-http-server")');
  expect(tpgGroupTotal>tpgExactTotal&&grouped.count===tpgGroupTotal&&grouped.raws.length===3,'TPG group failed');
  c.run('DS.operator="";DS.q="iiNet"');
  expect(c.run('dFiltered().find(r=>r.line==="tr069-http-server").count')===tpgGroupTotal,'Search matched a partial group');
  const idx=c.run('buildDeploymentIndex({"x--GB":{orgs:[{value:"IP pools",count:2}]},"x--IT":{orgs:[{value:"IP pools",count:3}]}},{x:{}},DATA.operatorCatalog)');
  expect(idx.observations[0].operator!==idx.observations[1].operator,'Countries merged');
  expect(idx.entities[idx.observations[0].operator].kind==='raw','Generic pool inferred as BT');
  return 'WindTre branches, exact aliases, group membership and country boundaries verified';
});
test('network-roles-evidence', 'Service roles and ACS evidence retain their original scope', () => {
  const c=context();
  expect(c.run('dFiltered().every(r=>DATA.lines[r.line].service==="cpe")'),'Default includes ACS');
  c.run('DS.role="acs"');
  expect(c.run('dFiltered().length>0&&dFiltered().every(r=>DATA.lines[r.line].service==="acs")'),'ACS filter failed');
  c.run('DS.role="cpe";DS.country="GB";DS.line="icwmp-iopsys"');
  const mapped=c.run('dEvidence(dFiltered().find(r=>r.operator==="o:bt"))');
  expect(mapped.length===1&&mapped[0].kind==='operator','BT observation missing');
  expect(c.run('dEvidence(dFiltered().find(r=>r.operator==="u:GB:IP pools")).length')===0,'Raw pool inherited BT evidence');
  c.run('DS.country="US";DS.line="easycwmp-vanilla"');
  expect(c.run('dFiltered().every(r=>dEvidence(r).length===0)'),'Generic interop assigned to production network');
  return 'CPE and ACS separated; operator and interop evidence not propagated';
});
test('matrix-coverage', 'Matrix distinguishes zero, truncated tail, uncollected and measured cells', () => {
  const c=context(), full=Object.entries(data.orgdrill).find(([,v])=>v.facet_meta.org.remainder===0),tail=Object.entries(data.orgdrill).find(([,v])=>v.facet_meta.org.remainder>0);
  for(const [record,expected] of [[full,'zero'],[tail,'tail']]) {
    const i=record[0].lastIndexOf('--'),line=record[0].slice(0,i),cc=record[0].slice(i+2);
    expect(c.run(`dCellState(${JSON.stringify(line)},${JSON.stringify(cc)},"nonexistent",[]).kind`)===expected,expected);
  }
  expect(c.run('dCellState("uncollected","AU","o:tpg",[]).kind')==='missing','Missing is not zero');
  c.run('DS.country="AU";DS.operator="o:tpg";DS.view="matrix";renderDeployments()');
  expect(c.element('#dMatrix').innerHTML.includes('data-d-cell='),'Measured matrix cell absent');
  return 'All four measurement states verified';
});
test('network-map-roundtrip', 'Exact raw organization selections survive map URLs without broadening or double counting', () => {
  const c=context();
  c.run('S.lines=new Set(["tr069-http-server"]);S.geo=new Set(["c:AU"]);S.orgs=new Set(["raw:TPG Internet Pty Ltd","raw:TPG Internet Pty Ltd."]);urlWrite(true);S.orgs.clear();urlRead()');
  expect(tpgExactTotal>0&&c.run('computeSlice().total')===tpgExactTotal,'Exact TPG map total failed');
  c.run('S.orgs.add(normOrg("TPG Internet Pty Ltd","AU"))');
  const actual=c.run('computeSlice().total');
  const expected=data.orgdrill['tr069-http-server--AU'].orgs.reduce((n,o)=>n+(c.run(`S.orgs.has("raw:"+${JSON.stringify(o.value)})||S.orgs.has(normOrg(${JSON.stringify(o.value)},"AU"))`)?o.count:0),0);
  expect(actual===expected,'Broad and exact labels double-counted');
  return {exact:tpgExactTotal,withAlias:actual};
});
test('network-share-localization', 'Graph and matrix links restore filters, selection and four languages', () => {
  const c=context({hash:'#tab=ecosystem&eco_view=networks&net_country=IT&net_operator=o%3Awindtre&net_view=matrix'});
  c.run('urlRead();DS.selected=dFiltered()[0].id;urlWrite();DS.operator="";DS.selected="";urlRead()');
  expect(c.run('DS.operator==="o:windtre"&&DS.country==="IT"&&DS.view==="matrix"&&Boolean(DS.selected)'),'Shared selection lost');
  for(const lang of ['en','ru','es','zh']) {
    c.run(`LANG=${JSON.stringify(lang)};DNcur=new Intl.DisplayNames([LANG],{type:"region"});renderEcosystem()`);
    const html=c.element('#dDetail').innerHTML;
    expect(html.includes('WIND TRE S.P.A.')&&html.includes('/org-drill/'),'Source labels or dated evidence absent');
    expect(!/\bd_[a-z_]+\b/.test(html),'Untranslated deployment key');
    if(lang!=='ru')expect(!/[А-Яа-яЁё]/.test(html),'Russian fallback');
    c.run('DS.view="graph";renderDeployments();DS.view="matrix"');
    expect(c.element('#dWorld').innerHTML.includes('data-d-cell='),'Graph edges absent');
    c.run(`DNcur=new Intl.DisplayNames([${JSON.stringify(lang)}],{type:'region'});renderDeployments()`);
    expect(c.element('#dWorld').innerHTML.includes(new Intl.DisplayNames([lang],{type:'region'}).of('IT')),'Cached node labels did not change language');
  }
  c.sandbox.location.hash='#tab=ecosystem&net_operator=__proto__&net_line=constructor&net_country=XX&net_role=invalid';
  c.run('urlRead()');
  expect(c.run('DS.operator===""&&DS.line===""&&DS.country===""&&DS.role==="cpe"'),'Invalid network URL accepted');
  return 'Shared state, graph, matrix, sources and translations verified';
});
test('network-exploration', 'Node expansion keeps the graph context, country scope and exact records', () => {
  const c=context();
  c.run('DS.country="AU";const before=dGraphRows(dFiltered());dExpandNode("l:igdauthentication")');
  expect(c.run('DS.line===""&&DS.operator===""&&DS.country==="AU"'),'Expanding silently applied a filter');
  expect(c.run('dGraphRows(dFiltered()).some(r=>r.line!=="igdauthentication")'),'Expansion discarded graph context');
  expect(c.run('dGraphRows(dFiltered()).filter(r=>r.line==="igdauthentication").length>=8'),'Neighbors not expanded');
  expect(c.run('dGraphRows(dFiltered()).every(r=>r.cc==="AU")'),'Country scope widened');
  c.run('S.tab="ecosystem";urlWrite();DS.expanded=[];DS.node="";urlRead()');
  expect(c.run('DS.node==="l:igdauthentication"&&DS.expanded[0][1]===8'),'Shared expansion lost');
  c.run('dExpandNode("l:igdauthentication",true)');
  expect(c.run('DS.expanded[0][1]')===16,'More neighbors failed');
  return 'Expansion reveals real neighbors without replacing filters; URLs preserve it';
});
test('network-layout-and-flows', 'Layouts retain measurements, pinned nodes and country-scoped operator identities', () => {
  const c=context();
  const output=c.run(`(()=>{
    DS.country="AU";const rows=dGraphRows(dFiltered()),m=dBuildGraph(rows),p=new Map(),pins=new Set();
    const first=dForceLayout(m,p,pins),id=first.nodes[0].id;p.set(id,{x:333,y:222});pins.add(id);
    const next=dForceLayout(m,p,pins),flow=dFlowLayout(m);
    return {pinned:next.nodes.find(n=>n.id===id),finite:next.nodes.every(n=>Number.isFinite(n.x)&&Number.isFinite(n.y)),
      counts:flow.edges.filter(e=>e.row).map(e=>e.row.count),expected:rows.map(r=>r.count),geo:flow.edges.filter(e=>e.geo).length,operators:m.nodes.filter(n=>n.kind==="operator").length};
  })()`);
  expect(output.pinned.x===333&&output.pinned.y===222&&output.finite,'Force layout moved a pin or produced invalid coordinates');
  expect(JSON.stringify(output.counts)===JSON.stringify(output.expected),'Flow transformed source counts');
  expect(output.geo===output.operators,'An operator lost its country in flows');
  c.sandbox.location.hash='#tab=ecosystem&net_view=flows&net_node=__proto__&net_expand=%5B%5B%22l%3Aconstructor%22%2C999%5D%5D';
  c.run('urlRead();renderEcosystem()');
  expect(c.run('DS.view==="flows"&&DS.node===""&&DS.expanded.length===0'),'Unsafe expansion accepted');
  return 'Stable finite layout; original weights and country-scoped flow edges';
});
test('source-links', 'Evidence links resolve from both entry points and reject unsafe paths', () => {
  const c=context();
  for(const [pathname,prefix] of [['/index.html',''],['/atlas/tr-atlas.html','../'],['/project/atlas/tr-atlas.html','../']]) {
    c.sandbox.location.pathname=pathname;
    const output=c.run('sourcesHtml([{file:"NOTES.md",anchor:"section-9.29"}])');
    expect(output.includes(`href="${prefix}NOTES.md#section-9.29"`),output);
  }
  const rejected=c.run('sourcesHtml([{file:"../private.md"},{file:"https://example.com"},{file:"/etc/passwd"}])');
  expect(!rejected.includes('<a '),rejected);
  c.sandbox.location.pathname='/index.html';
  const escaped=c.run('sourcesHtml([{file:"NOTES.md",title:"<img src=x>",anchor:"\\\" onmouseover=alert(1)"}])');
  return expect(!escaped.includes('<img')&&!escaped.includes('" onmouseover='),escaped);
});
test('snapshot', 'All embedded lines match their source snapshot', () => {
  const mismatches=[];
  for(const [slug,line] of Object.entries(data.lines)) {
    const raw=JSON.parse(fs.readFileSync(path.join(root,'data/mapdata',`snapshot-${data.snapshot}`,`${slug}.json`),'utf8'));
    const countries=Object.fromEntries(raw.countries.map(c=>[c.value,c.count]));
    if(JSON.stringify(countries)!==JSON.stringify(line.countries)||raw.total!==line.total||raw.dork!==line.dork) mismatches.push(slug);
  }
  return expect(!mismatches.length, JSON.stringify({lines:Object.keys(data.lines).length,mismatches}));
});
test('observation-counts', 'Observation counts and dates come from exact collected queries', () => {
  let collected=0,missing=0;
  for(const items of Object.values(data.facts)) for(const fact of items) {
    if(fact.collection_status!=='ok') {
      expect(fact.count===null,`Uncollected fact leaked a historical count: ${fact.label}`);
      missing++;continue;
    }
    const ref=fact.collection_ref;
    expect(ref&&ref.id,`Missing collection reference: ${fact.label}`);
    const raw=JSON.parse(fs.readFileSync(path.join(root,'data/mapdata',`snapshot-${data.snapshot}`,ref.kind==='variant'?'variants':'',`${ref.id}.json`),'utf8'));
    expect(raw.dork===fact.dork&&raw.total===fact.count&&raw.taken===fact.taken,`Fact result differs: ${fact.label}`);
    collected++;
  }
  return {collected,missing};
});
test('http-bounds', 'HTTP counts stay within port 7547 denominators', () => {
  const bad=Object.entries(data.http).filter(([cc,n])=>n<0||n>data.park[cc]);
  return expect(!bad.length,JSON.stringify(bad));
});
test('ident', 'Default country sums equal embedded ident', () => {
  const c=context(); const actual=c.run('computeSlice()');
  const bad=[...actual.ccs].filter(([cc,v])=>v.base!==data.ident[cc]);
  return expect(!bad.length,JSON.stringify({total:actual.total,countries:actual.ccs.size,mismatches:bad}));
});
test('line-country-sweep', 'Every line and country filter preserves source counts', () => {
  const c=context(); let cases=0;
  for(const [slug,line] of Object.entries(data.lines)) for(const [cc,n] of Object.entries(line.countries)) {
    c.run(`S.lines=new Set([${JSON.stringify(slug)}]);S.geo=new Set([${JSON.stringify('c:'+cc)}]);`);
    const actual=c.run('computeSlice().total');
    expect(actual===n,`${slug}/${cc}: ${actual} != ${n}`); cases++;
  }
  return `${cases} line-country cases`;
});
test('region-country', 'Selecting Italy inside Europe narrows the slice to Italy', () => {
  const c=context();c.run('S.geo=new Set(["c:IT"]);');const italy=c.run('computeSlice().total');
  c.run('S.geo.add("r:Europe");');const combined=c.run('computeSlice().total');
  return expect(combined===italy,JSON.stringify({italy,combined,countries:[...c.run('computeSlice().ccs.keys()')].length}));
});
test('operator-counts', 'Operator filter uses selected operator facet counts', () => {
  const c=context();c.run('S.lines.add("igdauthentication");S.geo.add("c:US");S.orgs.add("Blue Stream");');
  const actual=c.run('computeSlice().total'); const expected=data.orgdrill['igdauthentication--US'].orgs.find(o=>o.value==='Blue Stream').count;
  return expect(actual===expected,JSON.stringify({actual,expected,ratio:actual/expected}));
});
test('operator-normalization', 'Specific Jersey operator is not captured by a generic foreign DSL rule', () => {
  const c=context();const actual=c.run('normOrg("WAVE RESIDENTIAL DSL SERVICE")');
  return expect(actual==='JT (Jersey)',JSON.stringify({raw:'WAVE RESIDENTIAL DSL SERVICE',actual,expected:'JT (Jersey)'}));
});
test('disjoint-overlap', 'Default core selection excludes a documented overlapping nonce class', () => {
  const c=context();const selected=c.run('DISJOINT');
  return expect(!(selected.includes('decimal-nonce-class')&&selected.includes('sercomm-cpe-authentication')),
    JSON.stringify({included:selected.filter(s=>['decimal-nonce-class','sercomm-cpe-authentication'].includes(s)),classCount:data.lines['decimal-nonce-class'].total,evidence:data.meta.lines['decimal-nonce-class'].findings}));
});
test('facet-coverage', 'Operator drill retains the coverage metadata required to explain its truncated tail', () => {
  const cell=data.orgdrill['igdauthentication--US'];
  return expect(Boolean(cell.facet_meta),JSON.stringify({embeddedFields:Object.keys(cell),sumTopOrgs:cell.orgs.reduce((s,o)=>s+o.count,0)}));
});
test('geo-html', 'A malformed country URL is escaped before HTML insertion', () => {
  const marker='<em data-audit-marker=1>AUDIT</em>';
  const c=context({hash:'#'+new URLSearchParams({geo:'c:'+marker})});c.run('urlRead();facetBtnState();');
  const output=c.element('#fv-geo').innerHTML;
  return expect(!output.includes(marker),output);
});
test('invalid-region', 'Unknown regions in URLs do not crash suggestions', () => {
  const c=context({hash:'#geo=r%3ANotARegion'});c.run('urlRead();refreshTest();computeShortcuts();');return 'No exception';
});
test('prototype-line', 'Inherited object properties are rejected as line slugs', () => {
  const c=context({hash:'#lines=constructor'});c.run('urlRead();computeSlice();');return 'No exception';
});
test('language-url', 'URL roundtrip preserves language', () => {
  const c=context({hash:'#lang=es'});c.run('urlRead();urlWrite();');
  return expect(new URLSearchParams(c.sandbox.location.hash.slice(1)).get('lang')==='es',c.sandbox.location.hash);
});
test('language-priority', 'Explicit URL language overrides stored preference', () => {
  const c=context({hash:'#lang=es',storedLanguage:'ru'});return expect(c.run('LANG')==='es',`LANG=${c.run('LANG')}`);
});
test('storage-blocked', 'Storage restrictions do not prevent initialization', () => {context({storageBlocked:true});return 'No exception';});
test('org-url-roundtrip', 'Operator names containing commas survive URL roundtrip', () => {
  const c=context();const org=Object.values(data.orgdrill).flatMap(x=>x.orgs).map(x=>c.run(`normOrg(${JSON.stringify(x.value)})`)).find(x=>x.includes(','));
  c.run(`S.orgs.add(${JSON.stringify(org)});urlWrite();S.orgs.clear();urlRead();`);
  const actual=[...c.run('S.orgs')];return expect(actual.length===1&&actual[0]===org,JSON.stringify({org,actual}));
});
test('chips', 'Selection labels contain translated text, not source fragments', () => {
  const c=context();c.run('renderChips();');const text=c.element('#chipsRow').innerHTML;
  return expect(!text.includes("t('sel_none')"),text);
});
test('pair-title', 'Opening a pair updates the map title', () => {
  const c=context();c.run('S.cell={cc:"IT",slug:"cpe-server-1-0"};renderMode();');
  return expect(c.element('#mapTitle').textContent.includes('CPE-SERVER'),JSON.stringify({title:c.element('#mapTitle').textContent,wrongTarget:c.run('t.textContent')}));
});
test('pair-outside-selection', 'Visible dimmed map pairs keep their real count in inspector', () => {
  const c=context();c.run('S.lines.add("cpe-server-1-0");S.geo.add("c:GB");S.cell={cc:"IT",slug:"cpe-server-1-0"};refreshTest();renderInspector();');
  const output=c.element('#inspector').innerHTML;const count=output.match(/class="bignum num">([^<]+)/)?.[1]?.trim();
  return expect(count!=='0',JSON.stringify({displayed:count,source:data.lines['cpe-server-1-0'].countries.IT}));
});
test('lines-in-slice', 'In-slice line table respects selected country', () => {
  const c=context();c.run('S.lines.add("cpe-server-1-0");S.geo.add("c:GB");refreshTest();');
  const actual=c.run('GEOT.get("cpe-server-1-0")');const expected=c.run('SLICE.lines.get("cpe-server-1-0").total');
  return expect(actual===expected,JSON.stringify({actual,expected}));
});
test('top-countries', 'Line table populates top-country column', () => {
  const c=context();c.run('refreshTest();renderLinesTable();');const output=c.element('#linesBody').innerHTML;
  const blank=(output.match(/<td class="vendorcell"><\/td>/g)||[]).length;
  return expect(blank===0,`${blank} empty top-country cells`);
});
test('toast-timeout', 'Toast disappears after its timeout callback', () => {
  const c=context();c.run('showToast("audit");');c.sandbox.timer();return expect(c.element('#toast').hidden===true,'Toast hidden after timer');
});
test('inspector-reopen', 'Inspector collapse leaves a reachable reopening control', () => {
  const c=context();c.run('toggleInsp();');
  expect(c.element('#inspector').hidden&&!c.element('#inspReopen').hidden,'Reopen control must remain visible outside the hidden inspector');
  c.run('toggleInsp();');
  return expect(!c.element('#inspector').hidden&&c.element('#inspReopen').hidden,'Inspector reopens');
});
test('shortcut-labels', 'Shortcut labels interpolate country and line names', () => {
  const c=context();c.run('refreshTest();');const labels=c.run('computeShortcuts().map(x=>x.title)');
  return expect(labels.every(s=>!s.includes('\\$\\{')),JSON.stringify(labels));
});
test('operator-search', 'Quick search finds collected operators outside the first twelve', () => {
  const c=context();c.run('refreshTest();kkBuild("Blue Stream");');const items=c.run('kkItems');
  return expect(items.some(x=>x.t==='Blue Stream'),JSON.stringify(items));
});
test('svg-coordinates', 'Pointer coordinates account for SVG aspect-ratio letterboxing', () => {
  const c=context();const actual=c.run('svgXY({clientX:330,clientY:150})');
  return expect(actual[0]===660&&actual[1]===0,JSON.stringify({svgBox:'660x600',viewBox:'1320x600',actual,expected:[660,0]}));
});
test('copy-dork', 'Country copy action matches the adjacent Shodan link query', () => {
  const c=context();c.run('S.lines.add("cpe-server-1-0");S.geo.add("c:IT");refreshTest();renderInspector();');
  const output=c.element('#inspector').innerHTML;
  const href=output.match(/href="https:\/\/www\.shodan\.io\/search\?query=([^"]+)/)[1];
  const copy=output.match(/data-copy="([^"]+)/)[1].replaceAll('&quot;','"').replaceAll('&#39;',"'").replaceAll('&amp;','&');
  return expect(decodeURIComponent(href)===copy,JSON.stringify({link:decodeURIComponent(href),copy}));
});
test('map-all-countries', 'Every country with line data has a map anchor', () => {
  const geo=new Set(data.geo.features.map(f=>f.properties.cc));
  const c=context();const micro=c.run('Object.keys(MICRO)');micro.forEach(cc=>geo.add(cc));
  const missing=Object.entries(data.ident).filter(([cc,n])=>n>0&&!geo.has(cc));
  return expect(!missing.length,JSON.stringify(missing));
});
test('country-picker-coverage', 'Country selector can discover countries present outside the 7547 denominator', () => {
  const all=new Set(Object.values(data.lines).flatMap(l=>Object.keys(l.countries)));
  const missing=[...all].filter(cc=>!Object.hasOwn(data.park,cc));
  const pickerUsesOnlyPark=fn('buildPanel').includes('const ccs=Object.keys(DATA.park)');
  return expect(!missing.length||!pickerUsesOnlyPark,JSON.stringify(missing));
});
test('geo-duplicates', 'Map rendering does not overwrite paths sharing a country code', () => {
  const counts={};data.geo.features.forEach(f=>{const cc=f.properties.cc;if(cc)counts[cc]=(counts[cc]||0)+1;});
  const duplicates=Object.entries(counts).filter(([,n])=>n>1);
  return expect(!duplicates.length||!source.includes('pathMap.set(el.dataset.cc,el)'),JSON.stringify(duplicates));
});
test('json-export', 'JSON export creates a nonempty downloadable blob', () => {
  const c=context();c.run('S.lines.add("cpe-server-1-0");S.geo.add("c:IT");refreshTest();exportJSON();');
  return expect(c.sandbox.download.name==='tron-069-slice.json'&&c.sandbox.download.blob.size>0,'JSON blob generated');
});
test('snapshot-only-fetch', 'Only the selected same-origin archive can be fetched at runtime', () => {
  const external=/<script\b[^>]*\bsrc=|new\s+(?:XMLHttpRequest|WebSocket)\s*\(/.test(html);
  expect(!external,'No external scripts, XHR or WebSocket');
  expect((source.match(/\bfetch\s*\(/g)||[]).length===1&&source.includes('fetch(snapshotURL(id)'), 'Unexpected fetch outside snapshot loader');
  return 'One allowlisted snapshot request; the embedded date needs no network';
});

test('all-locales-content', 'All line inspectors, registry, observations and methodology render without Russian fallback in EN/ES/ZH', () => {
  let checked=0;
  for(const lang of ['en','es','zh']) {
    const c=context({hash:'#lang='+lang});
    c.run('refreshTest();renderRegistry();renderFindings();renderAbout();');
    const check=(selector,label)=>{
      const visible=c.element(selector).innerHTML.replace(/<[^>]*>/g,'');
      expect(!/[А-Яа-яЁё]/.test(visible),`${lang}/${label}: ${visible.match(/[А-Яа-яЁё][^<]*/)?.[0]}`);checked++;
    };
    for(const id of ['#regBody','#fndGrid','#aboutBody'])check(id,id);
    for(const slug of Object.keys(data.lines)) {
      c.run(`S.lines=new Set([${JSON.stringify(slug)}]);S.cell=null;refreshTest();renderInspector();`);
      check('#inspector',slug);
    }
  }
  return `${checked} localized sections/inspectors`;
});
test('operator-shortcuts', 'Suggested largest line stays within the selected operator data', () => {
  const c=context();c.run('S.orgs.add("Blue Stream");refreshTest();');
  const totals=new Map();
  const directory=path.join(root,'data/mapdata',`snapshot-${data.snapshot}`,'org-drill');
  for(const file of fs.readdirSync(directory).filter(file=>file.endsWith('.json'))) {
    const slug=file.slice(0,-5).split('--')[0];
    if(data.excluded.includes(slug))continue;
    const record=JSON.parse(fs.readFileSync(path.join(directory,file),'utf8'));
    const count=record.orgs.filter(org=>org.value==='Blue Stream').reduce((sum,org)=>sum+org.count,0);
    totals.set(slug,(totals.get(slug)||0)+count);
  }
  const [expectedSlug,expectedCount]=[...totals].sort((a,b)=>b[1]-a[1])[0];
  const shortcut=c.run('computeShortcuts()[0]');
  return expect(shortcut.act.slug===expectedSlug&&shortcut.val===c.run(`fmtF(${expectedCount})`),JSON.stringify(shortcut));
});
test('invalid-cell', 'Malformed pair URL cannot inject HTML or access inherited line keys', () => {
  for(const value of ['IT,constructor','<em>AUDIT</em>,cpe-server-1-0','IT,__proto__']) {
    const c=context({hash:'#'+new URLSearchParams({cell:value})});c.run('urlRead();refreshTest();renderInspector();');
    expect(c.run('S.cell')===null,value);
  }
  return '3 invalid cells rejected';
});
test('state-roundtrip', 'A shared URL restores multiple operators, geography, pair, mode and tab', () => {
  const c=context();
  c.run('S.lines.add("igdauthentication");S.geo.add("c:US");S.orgs.add("Blue Stream");S.orgs.add("D&P Communications, Inc.");S.cell={cc:"US",slug:"igdauthentication"};S.mode="countries";S.tab="findings";urlWrite();');
  const before=c.run('JSON.stringify({lines:[...S.lines],geo:[...S.geo],orgs:[...S.orgs],cell:S.cell,mode:S.mode,tab:S.tab})');
  c.run('urlRead();');
  const after=c.run('JSON.stringify({lines:[...S.lines],geo:[...S.geo],orgs:[...S.orgs],cell:S.cell,mode:S.mode,tab:S.tab})');
  return expect(before===after,after);
});
test('service-classification', 'ACS roles are explicit and excluded from the core set', () => {
 const c=context();const acs=Object.keys(data.lines).filter(s=>data.lines[s].service==='acs');
 expect(acs.length>=4, 'Expected existing ACS lines plus Telefónica');
 expect(acs.every(s=>!c.run('DISJOINT').includes(s)), 'ACS entered core sum');
 c.element('#regService').value='acs';c.run('renderRegistry()');
 const rows=c.element('#regBody').innerHTML;
 expect(acs.every(s=>rows.includes('data-slug="'+s+'"')), 'ACS filter lost a line');
 expect(!rows.includes('data-slug="cpe-server-1-0"'),'ACS filter includes CPE');
 return {acs,unknown:data.lines['cwmp-server'].service,mixed:data.lines['gsoap-park'].service};
});
test('variant-counts', 'Research variants stay outside map sums and render in all languages', () => {
 const c=context();const total=c.run('computeSlice().total');let rendered=0;
 for(const lang of ['ru','en','es','zh']){
  c.run(`LANG=${JSON.stringify(lang)};`);
  for(const [slug,variants] of Object.entries(data.variants||{})){
   const html=c.run(`variantHtml(${JSON.stringify(slug)})`);
   expect(html.includes('variant-card'), 'Missing variant card');
   if(lang!=='ru')expect(!/[А-Яа-яЁё]/.test(html),'Russian fallback in variants');
   expect(variants.every(v=>html.includes(v.label[lang].replaceAll('&','&amp;'))),'Missing variant label');
   rendered+=variants.length;
  }
 }
 expect(rendered>0,'No collected variants');
 expect(total===c.run('computeSlice().total'),'Variants changed core sum');
 return {rendered,total};
});
test('news-locales', 'Every news item renders in all four languages without Russian fallback outside RU', () => {
  for(const lang of ['ru','en','es','zh']){
    const c=context({hash:'#lang='+lang});c.run('renderNews();');
    const output=c.element('#newsGrid').innerHTML;
    expect((output.match(/<article /g)||[]).length===data.news.length,lang+' missing cards');
    if(lang!=='ru')expect(!/[А-Яа-яЁё]/.test(output),lang+' Russian fallback');
  }
  return `${data.news.length} news items × 4 languages`;
});
test('news-navigation', 'News previous/next wraps and news tab survives a shared URL', () => {
  const c=context();c.run('newsStep(-1,true);');
  expect(c.run('newsIndex')===data.news.length-1,'Previous did not wrap');
  c.run('newsStep(1,true);');expect(c.run('newsIndex')===0,'Next did not wrap');
  c.run('S.tab="news";urlWrite();S.tab="map";urlRead();');
  return expect(c.run('S.tab')==='news','News tab restored');
});
test('manifesto-first', 'Manifesto leads the news list and initial ticker, with readable paragraphs and tool links', () => {
  expect(data.news[0].id==='tron-069-manifesto'&&data.news[0].pinned,'Manifesto is not pinned first');
  const c=context();c.run('renderNews();');
  const grid=c.element('#newsGrid').innerHTML;
  expect(grid.startsWith('<article class="news-card" id="news-tron-069-manifesto"'),'Wrong first card');
  const card=grid.slice(0,grid.indexOf('</article>'));
  expect((card.match(/<p>/g)||[]).length===3,'Manifesto lost paragraph structure');
  for(const repo of ['rust-in-peace','reproof'])expect(card.includes(`href="https://github.com/scadastrangelove/${repo}"`),repo+' link missing');
  expect(c.element('#newsHeadline').innerHTML.includes(data.news[0].title.en),'Initial ticker does not show manifesto');
  return 'Pinned first card and ticker; three paragraphs; two HTTPS project links';
});
test('news-pause', 'News rotation stops on pause, reduced motion, hidden tab, hover and keyboard focus', () => {
  const c=context();expect(c.run('shouldRotateNews()'),'Rotation disabled unexpectedly');
  for(const statement of ['newsPaused=true','newsMotion.matches=true','document.hidden=true','S.tab="news"']){
    c.run('newsPaused=false;newsMotion.matches=false;document.hidden=false;S.tab="map";'+statement);
    expect(!c.run('shouldRotateNews()'),statement);
  }
  c.run('S.tab="map";');const ticker=c.element('#newsTicker');
  ticker.matches=()=>true;expect(!c.run('shouldRotateNews()'),'Hover ignored');
  ticker.matches=()=>false;ticker.contains=()=>true;expect(!c.run('shouldRotateNews()'),'Focus ignored');
  return 'All six pause conditions respected';
});
const exportedContext=context();
exportedContext.run('S.lines.add("igdauthentication");S.geo.add("c:US");S.orgs.add("Blue Stream");refreshTest();exportJSON();');
const exportedJSON=JSON.parse(await exportedContext.sandbox.download.blob.text());
test('export-operator-total', 'Export preserves the filtered operator count and coverage scope', () => {
  return expect(exportedJSON.countries.US.base===blueStreamCount && exportedJSON.operatorScope==='collected top-N facets' && exportedJSON.unknownCountry===null,JSON.stringify(exportedJSON));
});
exportedContext.run('exportCSV();');
const exportedCSV=await exportedContext.sandbox.download.blob.text();
test('csv-format', 'CSV uses quoted fields and CRLF with the selected operator count', () => {
  return expect(exportedCSV.includes(`"US";"United States";"${blueStreamCount}";`) && exportedCSV.includes('\r\n'),exportedCSV);
});

const report={target,sourceSha256:createHash('sha256').update(html).digest('hex'),snapshot:data.snapshot,testedAt:new Date().toISOString(),method:'Offline source-function tests with inert output sinks; no browser rendering',pass:results.filter(r=>r.status==='PASS').length,fail:results.filter(r=>r.status==='FAIL').length,results};
const reportJSON=JSON.stringify(report,null,2);
const outputIndex=process.argv.indexOf('--json');
if(outputIndex>=0){fs.writeFileSync(process.argv[outputIndex+1],reportJSON+'\n');console.log(`${target}: ${report.pass} PASS, ${report.fail} FAIL`);for(const r of results.filter(r=>r.status==='FAIL'))console.log(r);}
else console.log(reportJSON);
process.exitCode=report.fail?1:0;
