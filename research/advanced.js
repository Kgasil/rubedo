/* Rubedo Research 1.0.1 candidate: reproducible queue experiments and two-variable continuous LP. */
(function(root){'use strict';
function numeric(v,label,min,max,integer=false){if(typeof v==='string'&&/^[+-]?(?:\d+(?:[.,]\d+)?|[.,]\d+)$/.test(v.trim()))v=Number(v.trim().replace(',','.'));if(typeof v!=='number'||!Number.isFinite(v)||v<min||v>max||(integer&&!Number.isInteger(v)))throw Error(label+': '+min+'–'+max+(integer?' (integer)':''));return v;}
// Mulberry32, deterministic 32-bit generator, not cryptographic.
function rng(seed){let a=seed>>>0;return ()=>{a=(a+0x6D2B79F5)>>>0;let t=a;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return ((t^(t>>>14))>>>0)/4294967296;};}
function exp(rate,random){return -Math.log(1-random())/rate;}
function describe(a){const mean=a.reduce((s,v)=>s+v,0)/a.length;return {mean,sd:a.length>1?Math.sqrt(a.reduce((s,v)=>s+(v-mean)**2,0)/(a.length-1)):null,min:Math.min(...a),max:Math.max(...a)};}
function simulate(arrival,service,warmup,observations,replications,seed){const l=numeric(arrival,'λ',.01,10000),m=numeric(service,'μ',.01,10000),w=numeric(warmup,'Warmup',0,20000,true),n=numeric(observations,'Observations',10,20000,true),r=numeric(replications,'Replications',2,20,true),s=numeric(seed,'Seed',0,4294967295,true);if(l>=m)throw Error('λ < μ required (stable M/M/1).');if((w+n)*r>400000)throw Error('Maximum 400,000 simulated arrivals.');let runs=[];const random=rng(s);for(let j=0;j<r;j++){let arrivalTime=0,completion=0,sumWait=0,sumTotal=0,waited=0;const repSeed=Math.floor(random()*4294967296),u=rng(repSeed);for(let i=0;i<w+n;i++){arrivalTime+=exp(l,u);const start=Math.max(arrivalTime,completion),wait=start-arrivalTime,work=exp(m,u);completion=start+work;if(i>=w){sumWait+=wait;sumTotal+=wait+work;if(wait>0)waited++;}}runs.push({replication:j+1,seed:repSeed,meanWait:60*sumWait/n,meanTotal:60*sumTotal/n,waitFraction:waited/n});}const theoryWait=60*l/(m*(m-l)),theoryTotal=60/(m-l);return {schema:'rubedo.queue.simulation.v1',inputs:{arrival:l,service:m,warmup:w,observations:n,replications:r,seed:s},rho:l/m,theoryWait,theoryTotal,wait:describe(runs.map(x=>x.meanWait)),total:describe(runs.map(x=>x.meanTotal)),waitFraction:describe(runs.map(x=>x.waitFraction)),runs};}
// Maximize vA*x + vB*y, x,y >= 0, two nonnegative resource constraints.
function optimize(values,coefficients,limits){if(!Array.isArray(values)||values.length!==2||!Array.isArray(coefficients)||coefficients.length!==2||!coefficients.every(a=>Array.isArray(a)&&a.length===2)||!Array.isArray(limits)||limits.length!==2)throw Error('Two products and two resources required.');const v=values.map((x,i)=>numeric(x,'Value '+i,0,1e6)),a=coefficients.map((row,i)=>row.map((x,j)=>numeric(x,'Coefficient '+i+','+j,0,1e6))),b=limits.map((x,i)=>numeric(x,'Limit '+i,0,1e6));if(a.some(row=>row.some(x=>x>0&&x<1e-6)))throw Error('Nonzero resource coefficients must be at least 0.000001.');if([0,1].some(j=>!a.some(row=>row[j]>0)))throw Error('Each product must consume at least one resource.');return exactLP(v,a,b);}

// Convert the canonical decimal representation of validated Number inputs to
// integer rows. Feasibility, vertex identity and objective ranking are exact
// for these decimals; floating point is used only to report results.
function decimalParts(n){
  const [mantissa,exp='0']=n.toString().split('e');
  const [whole,fraction='']=mantissa.split('.');
  return [BigInt(whole+fraction),Number(exp)-fraction.length];
}
function integerRow(numbers){
  const parts=numbers.map(decimalParts), exponent=Math.min(0,...parts.map(p=>p[1]));
  return {row:parts.map(([n,e])=>n*10n**BigInt(e-exponent)),scale:10n**BigInt(-exponent)};
}
function ratio(n,d){
  if(n===0n)return 0;
  // 26 significant decimal digits, then one conversion to binary64.
  const exponent=n.toString().length-d.toString().length;
  const shift=26-exponent;
  const digits=shift>=0?n*10n**BigInt(shift)/d:n/(d*10n**BigInt(-shift));
  const result=Number(digits.toString()+'e'+(-shift));
  if(!Number.isFinite(result)||result===0)throw Error('Result outside representable numeric range.');
  return result;
}
function compareFraction(n1,d1,n2,d2){const z=n1*d2-n2*d1;return z<0n?-1:z>0n?1:0;}
function exactLP(v,a,b){
  const resources=a.map((r,i)=>integerRow([...r,b[i]]));
  const cost=integerRow(v);
  const lines=[[1n,0n,0n],[0n,1n,0n],...resources.map(r=>r.row)];
  const vertices=[];
  for(let i=0;i<lines.length;i++)for(let j=i+1;j<lines.length;j++){
    const [p,q,c]=lines[i],[r,s,h]=lines[j];
    let d=p*s-q*r,x=c*s-q*h,y=p*h-c*r;
    if(d===0n)continue;
    if(d<0n){d=-d;x=-x;y=-y;}
    if(x<0n||y<0n)continue;
    const used=resources.map(({row:[u,w]})=>u*x+w*y);
    if(used.some((z,k)=>z>resources[k].row[2]*d))continue;
    if(vertices.some(z=>z.x*d===x*z.d&&z.y*d===y*z.d))continue;
    vertices.push({x,y,d,used,objective:cost.row[0]*x+cost.row[1]*y});
  }
  if(!vertices.length)throw Error('No feasible vertex.');
  vertices.sort((p,q)=>compareFraction(q.objective,q.d,p.objective,p.d)||compareFraction(p.x,p.d,q.x,q.d)||compareFraction(p.y,p.d,q.y,q.d));
  const best=vertices[0];
  const output=vertices.map(z=>({x:ratio(z.x,z.d),y:ratio(z.y,z.d),objective:ratio(z.objective,z.d*cost.scale),used:z.used.map((u,i)=>ratio(u,z.d*resources[i].scale))}));
  return {schema:'rubedo.optimization.lp2.v1',inputs:{values:v,coefficients:a,limits:b},best:output[0],alternativeOptima:vertices.filter(z=>compareFraction(z.objective,z.d,best.objective,best.d)===0).length>1,vertices:output,slack:resources.map((r,i)=>ratio(r.row[2]*best.d-best.used[i],best.d*r.scale))};
}

const api={simulate,optimize};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.RubedoAdvanced=api;})(typeof globalThis!=='undefined'?globalThis:this);
