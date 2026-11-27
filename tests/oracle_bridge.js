'use strict';
// Read test inputs as JSON; never execute provided source.
const fs=require('node:fs'),m=require('../extension/core.js'),r=require('../research/core.js'),a=require('../research/advanced.js'),p=require('../research/precision.js'),mc=require('../research/monte.js'),s=require('../research/statistics.js');
const models={M01:m.capacity,M02:m.line,M03:m.experiment,M04:m.takt,R01:r.sensitivity,R02:r.queue,R03:a.simulate,R04:a.optimize,R05:r.protocol,R06:p,R07:mc,R08:s.regression,R09:s.reliability};
const cases=JSON.parse(fs.readFileSync(0,'utf8'));
process.stdout.write(JSON.stringify(cases.map(({model,args})=>models[model](...args))));
