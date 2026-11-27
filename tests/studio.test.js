'use strict';
const assert=require('node:assert/strict'),s=require('../research/studio-core.js');
const base={model:'R04',name:'A',metric:'objective',unit:'points',value:'1,5',notes:'synthetic',parameters:'a=1; seed not applicable',source:'analytical',modelVersion:'1.0.1'};
const date='2026-11-27T20:00:00.000Z';let n=0;
function t(name,fn){fn();n++;console.log('OK '+name);}
const a=s.record(base,date),b=s.record({...base,name:'B',value:2.5},date);
t('v2 round trip',()=>assert.deepEqual(s.restore(JSON.stringify(s.pack([a,b]))),[a,b]));
t('comparison version and unit guard',()=>{assert.deepEqual(s.compare([a,b],1),{baseline:'A',delta:1});for(const patch of [{modelVersion:'1.0.0'},{metric:'other'},{unit:'kg'},{model:'R01'}])assert.equal(s.compare([a,{...b,...patch}],1),null);});
t('legacy data does not acquire invented provenance',()=>{const old={model:'R04',name:'old',metric:'objective',unit:'points',value:1,notes:''};const r=s.restore(JSON.stringify({schema:'rubedo.studio.v1',records:[old]}))[0];assert.equal(r.createdAt,null);assert.equal(r.modelVersion,'unknown');assert.equal(r.origin,'legacy-manual');assert.equal(s.compare([r,r],1),null);});
t('invalid schema',()=>assert.throws(()=>s.restore('{"schema":"bad","records":[]}')));
t('record limits',()=>{assert.throws(()=>s.pack(Array(101).fill(a)));assert.throws(()=>s.record({...base,source:'x'.repeat(501)},date));assert.throws(()=>s.restore('x'.repeat(2097153)));});
t('invalid number and fields',()=>{for(const patch of [{value:'NaN'},{value:Infinity},{value:1e13},{model:'bad'},{source:''},{parameters:''},{name:''}])assert.throws(()=>s.record({...base,...patch},date));});
t('timestamp and origin validation',()=>{assert.throws(()=>s.record(base,'2026-02-30T00:00:00.000Z'));assert.throws(()=>s.pack([{...a,origin:'verified'}]));});
t('untrusted strings remain data',()=>{const r=s.record({...base,name:'<img src=x onerror=alert(1)>'},date);assert.equal(s.restore(JSON.stringify(s.pack([r])))[0].name,r.name);});
console.log(n+' Studio core checks passed');
