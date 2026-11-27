(function(){'use strict';
const api=RubedoStudio,$=id=>document.getElementById('st-'+id);
const tr=(p,e)=>document.documentElement.lang==='en'?e:p;
let rows=[],busy=false;
function status(p,e){$('status').textContent=tr(p,e);}
function render(){
 const t=document.createElement('table');t.createCaption().textContent=tr('Registros: '+rows.length+' / 100','Records: '+rows.length+' / 100');const head=t.createTHead().insertRow();
 for(const label of [tr('Modelo','Model'),tr('Cenário','Scenario'),tr('Métrica','Metric'),tr('Unidade','Unit'),tr('Valor','Value'),tr('Base','Baseline'),'Δ',tr('Versão declarada','Declared version'),tr('Parâmetros','Parameters'),tr('Fonte','Source'),tr('Limitações','Limitations'),tr('Origem','Origin'),'UTC']){
  const th=document.createElement('th');th.scope='col';th.textContent=label;head.append(th);
 }
 const body=t.createTBody();
 rows.forEach((r,i)=>{const c=api.compare(rows,i),row=body.insertRow();for(const val of [r.model,r.name,r.metric,r.unit,String(r.value),c?c.baseline:'—',c?String(Number(c.delta.toPrecision(12))):'—',r.modelVersion,r.parameters,r.source,r.notes,({manual:tr('Manual','Manual'),'legacy-manual':tr('Legado','Legacy'),'local-calculation':tr('Cálculo local','Local calculation'),'imported-calculation':tr('Cálculo importado (não verificado)','Imported calculation (unverified)')})[r.origin],r.createdAt||'—'])row.insertCell().textContent=val;});
 $('table').replaceChildren(t);
 for(const id of ['json','txt','clear'])$(id).disabled=busy||rows.length===0;
 $('add').disabled=busy||rows.length>=100;$('import').disabled=busy;
}
$('add').onclick=()=>{try{const fields=Object.fromEntries(['model','name','metric','unit','value','notes','parameters','source','modelVersion'].map(k=>[k,$(k).value.trim()]));if(rows.length>=100||busy)throw Error('limit');const next=[...rows,api.record(fields,new Date().toISOString())];api.pack(next);rows=next;render();status('Registro manual adicionado','Manual record added');}catch(e){status('Entrada inválida: preencha os campos obrigatórios e confira os limites.','Invalid input: fill required fields and check limits.');}};
function download(name,body,type){if(!rows.length||busy)return;const u=URL.createObjectURL(new Blob([body],{type})),a=document.createElement('a');a.href=u;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1000);}
$('json').onclick=()=>download('rubedo-results.json',JSON.stringify(api.pack(rows),null,2)+'\n','application/json');
$('txt').onclick=()=>download('rubedo-report.txt','RUBEDO — Experimental research records / Registros experimentais\nLocal calculations, manual or imported claims; not industrially validated.\nStudio '+api.version+'\n\n'+rows.map((r,i)=>String(i+1)+'. '+Object.entries(r).map(([k,v])=>k+': '+(v&&typeof v==='object'?JSON.stringify(v):v??'unknown')).join('\n')).join('\n\n'),'text/plain');
$('import').onclick=async()=>{if(busy)return;busy=true;render();try{const f=$('file').files[0];if(!f||f.size>2097152)throw Error('size');const restored=api.restore(await f.text());if(rows.length&&!confirm(tr('Substituir registros atuais pelos importados?','Replace current records with imported ones?'))){status('Importação cancelada; registros preservados.','Import cancelled; records preserved.');return;}rows=restored;status('Registros restaurados; origem declarada, não verificada.','Records restored; declared provenance, not verified.');}catch(e){status('Arquivo inválido; registros preservados.','Invalid file; records preserved.');}finally{busy=false;render();}};
$('clear').onclick=()=>{if(!busy&&rows.length&&confirm(tr('Limpar todos os registros?','Clear all records?'))){rows=[];render();status('Registros removidos','Records cleared');}};
window.RubedoStudioAdd=function(record){if(busy)throw Error('Studio busy');const next=[...rows,record];api.pack(next);rows=next;render();status('Cálculo registrado no Studio; exporte para preservar.','Calculation recorded in Studio; export to preserve.');};
for(const id of ['pt','en'])document.getElementById(id).addEventListener('click',()=>{render();$('status').textContent='';});render();
})();
