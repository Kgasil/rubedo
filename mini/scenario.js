/* Optional synthetic scenario transfer from the public demonstration. */
(function(root){'use strict';
function parse(hash){if(typeof hash!=='string'||hash.length>100)return null;const m=/^#mode=takt&cycle=([0-9]{2,3})&demand=([0-9]{3,4})&lang=(pt|en)$/.exec(hash);if(!m)return null;const cycle=Number(m[1]),demand=Number(m[2]);if(cycle<15||cycle>120||cycle%5!==0||demand<100||demand>1000||demand%25!==0)return null;return {cycle,demand,lang:m[3]};}
if(typeof module!=='undefined'&&module.exports){module.exports={parse};return;}
function apply(){const s=parse(root.location.hash);if(!s)return;const $=id=>document.getElementById(id);$(s.lang).click();document.querySelector('[data-mode="takt"]').click();$('takt-cycle').value=String(s.cycle);$('demand').value=String(s.demand);$('run').click();}
apply();root.addEventListener('hashchange',apply);
})(typeof globalThis!=='undefined'?globalThis:this);
