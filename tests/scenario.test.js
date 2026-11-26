'use strict';
const assert=require('node:assert/strict'),{parse}=require('../mini/scenario.js');
const base='#mode=takt&cycle=30&demand=700&lang=en';
assert.deepEqual(parse(base),{cycle:30,demand:700,lang:'en'});
for(const invalid of ['',base+'&cycle=35',base+'&x=1',base.replace('30','0'),base.replace('30','31'),base.replace('700','1001'),base.replace('700','701'),base.replace('en','xx'),base.replace('takt','line'),base.replace('700','<script>')])assert.equal(parse(invalid),null);
console.log('11 scenario transfer checks passed');