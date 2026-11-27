'use strict';
const assert=require('node:assert/strict'),s=require('../research/studio-core.js'),r=require('../research/core.js');
let n=0;function test(name,fn){fn();n++;console.log('OK '+name);}
const when='2026-11-27T20:00:00.000Z',snap={model:'R02',version:s.version,inputs:{arrival:6,service:10},result:r.queue(6,10),limitations:'Synthetic'};
const row=s.capture(snap,'Wq','A','min',when);
test('reject forged metric value',()=>assert.throws(()=>s.pack([{...row,value:1}])));
test('reject unsafe snapshot key',()=>assert.throws(()=>s.validateSnapshot({...snap,inputs:JSON.parse('{"__proto__":{"polluted":true}}')})));
test('reject nested constructor key',()=>assert.throws(()=>s.validateSnapshot({...snap,inputs:{a:{constructor:{prototype:{polluted:true}}}}})));
test('reject invalid numbers',()=>assert.throws(()=>s.validateSnapshot({...snap,result:{Wq:Infinity}})));
test('reject excessive depth',()=>{let x={a:1};for(let i=0;i<14;i++)x={x};assert.throws(()=>s.validateSnapshot({...snap,inputs:x}));});
test('reject over-limit UTF-8 studio data',()=>assert.throws(()=>s.restore('é'.repeat(1100000))));
test('reject over-limit UTF-8 protocol',()=>assert.throws(()=>r.importProtocol('é'.repeat(70000))));
test('reject prototype key protocol',()=>assert.throws(()=>r.importProtocol('{"schema":"rubedo.research.protocol.v1","title":"T","question":"Q","method":"M","__proto__":{}}')));
test('restored calculation labelled unverified',()=>assert.equal(s.restore(JSON.stringify(s.pack([row])))[0].origin,'imported-calculation'));
test('invalid schema cannot execute HTML',()=>{const q=r.importProtocol(JSON.stringify({schema:'rubedo.research.protocol.v1',title:'<b>test</b>',question:'Q',method:'M'}));assert.equal(q.title,'<b>test</b>');});
test('reject malformed legacy record',()=>assert.throws(()=>s.restore('{"schema":"rubedo.studio.v1","records":[null]}')));
test('valid imported record remains unchanged in value',()=>assert.equal(s.restore(JSON.stringify(s.pack([row])))[0].value,row.value));
console.log(n+' security boundary checks passed');
