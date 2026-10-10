// Runs the atlas's actual pointer handlers offline, including SVG letterboxing.
// Run: node --test tests/map-gestures.mjs
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import test from 'node:test';

const html = fs.readFileSync(new URL('../atlas/map-template.html', import.meta.url), 'utf8');
const handlers = html.slice(html.indexOf('const vp='), html.indexOf('/* рендер стран */'));
const ocean = { closest: () => null };
const country = { closest: selector => selector === '[data-cc]' ? { dataset: { cc: 'DE' } } : null };
const cloud = { closest: selector => selector === '[data-cloud]' ? { dataset: { cc: 'DE', slug: 'test-line' } } : null };
const button = { closest: selector => selector === 'button' ? {} : null };
const ratio = 1320 / 355;

function map() {
  const listeners = new Map(), elements = new Map(), captures = new Set(), timers = new Map();
  let time = 0, nextTimer = 0;
  const element = id => {
    if (!elements.has(id)) elements.set(id, {
      attrs: {}, classList: { add() {}, remove() {} },
      setAttribute(key, value) { this.attrs[key] = value; },
      addEventListener(type, callback) { listeners.set(type, callback); },
      setPointerCapture(id) { captures.add(id); },
      hasPointerCapture(id) { return captures.has(id); },
      releasePointerCapture(id) { captures.delete(id); listeners.get('lostpointercapture')({ pointerId: id }); },
      // 355 x 340 stage: the 1320 x 600 SVG is centered vertically.
      createSVGPoint() { return { x: 0, y: 0, matrixTransform() {
        return { x: (this.x - 13) * ratio, y: (this.y - 290) * ratio + 300 };
      } }; },
      getScreenCTM() { return { inverse: () => ({}) }; }
    });
    return elements.get(id);
  };
  const context = vm.createContext({
    $: element, performance: { now: () => time },
    setInterval(fn) { const id = ++nextTimer; timers.set(id, fn); return id; },
    clearInterval(id) { timers.delete(id); }, setTimeout() {}, clearTimeout() {},
    scaleStatics() {}, refreshAll() {}, bboxOf: () => [620, 210, 690, 270]
  });
  const run = code => vm.runInContext(code, context);
  run(`const W=1320,H=600,homeT={k:1,x:0,y:0};let K=1,TX=0,TY=0;
    const S={geo:new Set(),cell:null};
    function selCountries(){return [...S.geo].filter(t=>t.startsWith('c:')).map(t=>t.slice(2));}
    function homeIfNoCountries(){if(!selCountries().length)tween(1,0,0);}
    ${handlers}`);
  return {
    run, element, timers,
    camera: () => Array.from(run('[K,TX,TY]')),
    event(type, id, x, y, target = ocean, extras = {}) {
      listeners.get(type)({ pointerId: id, pointerType: 'touch', button: 0,
        clientX: x, clientY: y, target, ...extras });
    },
    tick(ms) { time += ms; for (const fn of [...timers.values()]) fn(); }
  };
}

function near(actual, expected) {
  expected.forEach((value, i) => assert.ok(Math.abs(actual[i] - value) < 1e-8, `${actual} != ${expected}`));
}

test('tiny tap movement does not move the camera; a country tap still selects', () => {
  const m = map();
  m.event('pointerdown', 1, 190, 290, country);
  m.event('pointermove', 1, 192, 291);
  near(m.camera(), [1, 0, 0]);
  m.event('pointerup', 1, 192, 291);
  assert.equal(m.run('S.geo.has("c:DE")'), true);
  m.tick(600);
  assert.ok(m.camera()[0] > 1);
});

test('cloud tap selects the original hit despite pointer capture', () => {
  const m = map();
  m.event('pointerdown', 1, 190, 290, cloud);
  m.event('pointerup', 1, 190, 290);
  assert.equal(m.run('S.cell.slug'), 'test-line');
});

test('pan uses SVG coordinates and never selects its starting country', () => {
  const m = map();
  m.run('K=2;TX=-660;TY=-300;');
  m.event('pointerdown', 1, 190, 290, country);
  m.event('pointermove', 1, 210, 310);
  near(m.camera(), [2, -660 + 20 * ratio, -300 + 20 * ratio]);
  m.event('pointerup', 1, 210, 310);
  assert.equal(m.run('S.geo.size'), 0);
});

test('pan at the world view stays centered and cannot become a tap', () => {
  const m = map();
  m.event('pointerdown', 1, 190, 290, country);
  m.event('pointermove', 1, 230, 320);
  m.event('pointermove', 1, 190, 290);
  m.event('pointerup', 1, 190, 290);
  near(m.camera(), [1, 0, 0]);
  assert.equal(m.run('S.geo.size'), 0);
});

test('two fingers zoom around their midpoint; remaining finger pans without a jump', () => {
  const m = map();
  m.run('S.geo.add("c:DE")');
  m.event('pointerdown', 1, 140.5, 290, country);
  m.event('pointerdown', 2, 240.5, 290, country);
  m.event('pointermove', 1, 90.5, 290);
  m.event('pointermove', 2, 290.5, 290);
  near(m.camera(), [2, -660, -300]);
  m.event('pointerup', 2, 290.5, 290);
  near(m.camera(), [2, -660, -300]);
  m.event('pointermove', 1, 100.5, 290);
  near(m.camera(), [2, -660 + 10 * ratio, -300]);
  m.event('pointerup', 1, 100.5, 290);
  assert.equal(m.run('S.geo.has("c:DE")'), true);
  assert.equal(m.run('pointers.size'), 0);
});

test('pinching out respects minimum and maximum scale', () => {
  const m = map();
  m.event('pointerdown', 1, 180, 290);
  m.event('pointerdown', 2, 200, 290);
  m.event('pointermove', 2, 1000, 290);
  assert.equal(m.camera()[0], 24);
  m.event('pointermove', 2, 181, 290);
  near(m.camera(), [1, 0, 0]);
});

test('a third finger and cancellation never produce a selection or stale drag', () => {
  const m = map();
  m.event('pointerdown', 1, 140, 290, country);
  m.event('pointerdown', 2, 240, 290, country);
  m.event('pointerdown', 3, 280, 300, country);
  m.event('pointerup', 3, 280, 300);
  m.event('pointercancel', 1, 140, 290);
  m.event('pointermove', 2, 250, 290);
  m.event('pointerup', 2, 250, 290);
  assert.equal(m.run('S.geo.size'), 0);
  assert.equal(m.run('pointers.size'), 0);
  m.event('pointerdown', 4, 190, 290, cloud);
  m.event('lostpointercapture', 4, 190, 290);
  m.event('pointerup', 4, 190, 290);
  assert.equal(m.run('S.cell'), null);
});

test('grabbing the map stops an in-progress camera animation', () => {
  const m = map();
  m.run('tween(3,-1000,-600)');
  m.tick(100);
  m.event('pointerdown', 1, 190, 290);
  const before = m.camera();
  assert.equal(m.timers.size, 0);
  m.tick(500);
  near(m.camera(), before);
});

test('zoom controls, right click and unrelated pointer events preserve selection', () => {
  const m = map();
  m.run('S.geo.add("c:DE")');
  m.event('pointerdown', 1, 30, 350, button);
  m.event('pointerup', 1, 30, 350, button);
  m.element('#zin').onclick();
  m.tick(300);
  assert.ok(m.camera()[0] > 1);
  m.event('pointerdown', 2, 190, 290, ocean, { button: 2, pointerType: 'mouse' });
  m.event('pointerup', 2, 190, 290);
  m.event('pointermove', 99, 210, 300);
  m.event('pointerup', 99, 210, 300);
  assert.equal(m.run('S.geo.has("c:DE")'), true);
});

test('zooming out off center ends at the centered world view', () => {
  const m = map();
  m.run('K=2;TX=-100;TY=-50;zoomAt(0.1,1000,500)');
  m.tick(300);
  near(m.camera(), [1, 0, 0]);
});

test('a release far from its start is not a tap even without a move event', () => {
  const m = map();
  m.event('pointerdown', 1, 190, 290, country);
  m.event('pointerup', 1, 250, 330);
  assert.equal(m.run('S.geo.size'), 0);
});

test('the map owns touch gestures so the browser does not cancel vertical pans', () => {
  assert.match(html, /\.stage\{touch-action:none[;}]/);
});
