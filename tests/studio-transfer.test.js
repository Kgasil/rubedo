'use strict';
const assert=require('node:assert/strict'),s=require('../research/studio-core.js'),r=require('../research/core.js'),a=require('../research/advanced.js'),p=require('../research/precision.js'),mc=require('../research/monte.js'),{regression,reliability}=require('../research/statistics.js');
const date='2026-11-27T20:00:00.000Z',version=s.version;
const cases=[
['R01',{cycle:45},r.sensitivity(480,45,85,97,20),'good','units'],
['R02',{arrival:6,service:10},r.queue(6,10),'Wq','min'],
['R03',{seed:42},a.simulate(6,10,500,3000,5,42),'meanWait','min'],
['R04',{limits:[8,12]},a.optimize([3,5],[[1,2],[3,2]],[8,12]),'objective','points of value'],
['R06',{measurements:'1 2 3'},p('1 2 3'),'sd','mm'],
['R07',{seed:42,target:100},mc(80,100,140,10000,42,100),'probability','fraction'],
['R08',{pairs:[[1,3],[2,5],[3,7]]},regression([[1,3],[2,5],[3,7]]),'slope','kg/h'],
['R09',{rates:[.01,.01],hours:100},reliability([.01,.01],100),'parallel','fraction']];
const rows=cases.map(([model,inputs,result,metric,unit])=>{const snap={model,version,inputs,result,limitations:'Synthetic example'};const row=s.capture(snap,metric,model,unit,date);assert.equal(row.origin,'local-calculation');assert.deepEqual(row.snapshot,snap);assert.equal(row.value,s.metrics(snap).find(x=>x.id===metric).value);return row;});
const imported=s.restore(JSON.stringify(s.pack(rows)));assert.equal(imported.length,8);assert.ok(imported.every(r=>r.origin==='imported-calculation'));
assert.throws(()=>s.pack([{...rows[1],value:999}]));
assert.throws(()=>s.capture(rows[3].snapshot,'objective','A','points',date));
assert.throws(()=>s.capture(rows[1].snapshot,'Wq','A','h',date));
assert.throws(()=>s.capture({...rows[1].snapshot,result:r.queue(10,10)},'Wq','A','min',date));
assert.equal(s.compare([rows[1],{...rows[1],name:'B'}],1).delta,0);
assert.equal(s.compare([rows[1],{...rows[1],origin:'manual'}],1),null);
assert.equal(s.compare([rows[5],{...rows[5],snapshot:{...rows[5].snapshot,inputs:{target:101}}}],1),null);
assert.equal(s.compare([rows[7],{...rows[7],snapshot:{...rows[7].snapshot,inputs:{hours:200}}}],1),null);
assert.throws(()=>s.pack(Array(101).fill(rows[0])));
console.log('8 model transfers plus 10 provenance, comparison and rejection checks passed');
