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
function context({ hash = '', storageBlocked = false, storedLanguage = null } = {}) {
  const elements = new Map();
  const element = selector => {
    if (!elements.has(selector)) elements.set(selector, {
      innerHTML: '', textContent: '', value: '', hidden: false, style: {}, dataset: {},
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
    DATA: data, URLSearchParams, Intl, Blob, console,
    location: { hash }, navigator: { language: 'en' },
    localStorage: {
      getItem() { if (storageBlocked) throw new Error('SecurityError: storage unavailable'); return storedLanguage; },
      setItem() { if (storageBlocked) throw new Error('SecurityError: storage unavailable'); }
    },
    document: { querySelector: element, querySelectorAll: () => [], documentElement: {} },
    history: { replaceState(_a, _b, url) { sandbox.location.hash = url; } },
    setTimeout(callback) { sandbox.timer = callback; return 1; }, clearTimeout() {},
    renderShortcuts() {}, scaleStatics() {}, element,
    dl(blob, name) { sandbox.download = { blob, name }; }
  };
  vm.createContext(sandbox);
  const chunks = [
    section('const I18N =', 'function REG_NAME'),
    section('const $ =', '/* URL */'),
    fn('REG_NAME'), fn('urlRead'), fn('urlWrite'), fn('geoPass'), fn('orgPass'), fn('computeSlice'),
    'let SLICE, SLICE_FULL, GEOT; const selCountries=()=>[...S.geo].filter(t=>t.startsWith("c:")).map(t=>t.slice(2));',
    'const insp=$("#inspector"),kkL=$("#kkList"); let kkItems=[],kkSel=0,toastT=null;',
    'const W=1320,H=600,svg=$("#world"); let newsIndex=0,newsPaused=false;const newsMotion={matches:false};',
    ...['facetBtnState','renderChips','renderMode','lineGeoTotals','renderLinesTable','card','badgeHtml','serviceBadge','variantHtml',
      'sourcesHtml','renderInspector','toggleInsp','computeShortcuts','kkBuild','showToast','exportCSV','exportJSON','svgXY',
      'coverageNote','unknownCountryTotal','renderRegistry','renderFindings','renderAbout',
      'newsText','newsDate','renderNewsTicker','renderNews','newsStep','shouldRotateNews'].map(fn),
    'function refreshTest(){SLICE=computeSlice();SLICE_FULL=computeSlice(true);GEOT=lineGeoTotals();}',
    'DNcur=new Intl.DisplayNames([LANG],{type:"region"});'
  ];
  vm.runInContext(chunks.join('\n'), sandbox, { timeout: 2000 });
  return { run: code => vm.runInContext(code, sandbox, { timeout: 3000 }), sandbox, element };
}

test('syntax', 'Application JavaScript parses', () => { new vm.Script(source); return 'Parsed'; });
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
test('no-runtime-fetch', 'HTML has no external runtime scripts or automatic network requests', () => {
  const external=/<script\b[^>]*\bsrc=|\bfetch\s*\(|new\s+(?:XMLHttpRequest|WebSocket)\s*\(/.test(html);
  return expect(!external,'No external scripts, fetch, XHR, or WebSocket');
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
