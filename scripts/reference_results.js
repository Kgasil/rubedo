'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');const mini=require('../extension/core.js'),research=require('../research/core.js'),advanced=require('../research/advanced.js');
const report={schema:'rubedo.reference.results.v1',release:'1.0.1-candidate',data:'synthetic',cases:[
{id:'capacity',inputs:[480,45,85,97],result:mini.capacity(480,45,85,97),limitations:'Simplified continuous flow; no setups or material limits.'},
{id:'takt',inputs:[480,600,45,85,97],result:mini.takt(480,600,45,85,97),limitations:'Constant availability and yield; demand in good units.'},
{id:'queue',inputs:[6,10],result:research.queue(6,10),limitations:'Stationary M/M/1 under analytical assumptions.'},
{id:'queue-seeded',inputs:[6,10,500,3000,5,42],result:advanced.simulate(6,10,500,3000,5,42),limitations:'Fixed seed; warmup bias may remain; replication spread is not a confidence interval.'},
{id:'resource-allocation',inputs:[[3,5],[[1,2],[3,2]],[8,12]],result:advanced.optimize([3,5],[[1,2],[3,2]],[8,12]),limitations:'Continuous LP; no integer quantities.'}]};
const output=path.join(__dirname,'../examples/reference-results.json');if(process.argv.includes('--check')){assert.deepEqual(JSON.parse(fs.readFileSync(output,'utf8')),report);console.log(report.cases.length+' reference cases reproduced');}else{fs.writeFileSync(output,JSON.stringify(report,null,2)+'\n');console.log('Reference cases generated.');}
