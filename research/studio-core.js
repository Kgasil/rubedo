/* Local, versioned research records. No network or persistence. */
(function(root){'use strict';
const schema='rubedo.studio.v2',version='1.0.1',models=new Set(['R01','R02','R03','R04','R06','R07','R08','R09']);
function str(v,name,required=false,max=500){if(typeof v!=='string'||v.length>max||required&&!v.trim())throw Error('Invalid '+name);return v.trim();}
function decimal(v){if(typeof v==='string'&&/^[+-]?(?:\d+(?:[.,]\d+)?|[.,]\d+)$/.test(v.trim()))v=Number(v.trim().replace(',','.'));if(typeof v!=='number'||!Number.isFinite(v)||Math.abs(v)>1e12)throw Error('Invalid value');return v;}
function normalized(r){
  if(!r||typeof r!=='object'||Array.isArray(r)||!models.has(r.model))throw Error('Invalid record/model');
  const origin=r.origin;if(origin!=='manual'&&origin!=='legacy-manual')throw Error('Invalid origin');
  const modelVersion=str(r.modelVersion,'model version',true,40);
  const createdAt=r.createdAt;
  if(origin==='legacy-manual'){if(createdAt!==null||modelVersion!=='unknown')throw Error('Invalid legacy provenance');}
  else if(typeof createdAt!=='string'||!/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$/.test(createdAt)||!Number.isFinite(Date.parse(createdAt))||new Date(createdAt).toISOString()!==createdAt)throw Error('Invalid timestamp');
  return {model:r.model,name:str(r.name,'scenario',true),metric:str(r.metric,'metric',true),unit:str(r.unit,'unit',true),value:decimal(r.value),notes:str(r.notes,'notes'),parameters:str(r.parameters,'parameters',origin==='manual'),source:str(r.source,'source',origin==='manual'),modelVersion,origin,createdAt};
}
function record(fields,createdAt){return normalized({...fields,origin:'manual',createdAt});}
function pack(rows){if(!Array.isArray(rows)||rows.length>100)throw Error('Invalid record count');return {schema,studioVersion:version,records:rows.map(normalized)};}
function restore(text){
  if(typeof text!=='string'||text.length>2097152)throw Error('Invalid file size');
  const data=JSON.parse(text);if(!data||!Array.isArray(data.records)||data.records.length>100)throw Error('Invalid records');
  if(data.schema===schema){str(data.studioVersion,'studio version',true,40);return pack(data.records).records;}
  if(data.schema==='rubedo.studio.v1')return data.records.map(r=>normalized({...r,parameters:'',source:'',modelVersion:'unknown',origin:'legacy-manual',createdAt:null}));
  throw Error('Unsupported schema');
}
function compare(rows,i){const r=rows[i];if(r.modelVersion==='unknown')return null;const first=rows.slice(0,i).find(x=>x.model===r.model&&x.metric===r.metric&&x.unit===r.unit&&x.modelVersion===r.modelVersion);return first?{baseline:first.name,delta:r.value-first.value}:null;}
const api={version,record,pack,restore,compare};if(typeof module==='object'&&module.exports)module.exports=api;else root.RubedoStudio=api;
})(typeof globalThis==='object'?globalThis:this);
