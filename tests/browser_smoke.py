"""Exercise the static UI in Chromium. Default HTTP mode tests deployed layout on a
local server; --in-memory verifies HTML/CSS/JS interactions without URL navigation.
Neither mode installs the real browser extension."""
import argparse, base64, functools, http.server, json, re, threading, os
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--in-memory',action='store_true');parser.add_argument('--screenshots',type=Path);args=parser.parse_args()
server=None
if not args.in_memory:
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
count=0
with sync_playwright() as p:
    opts={'headless':True}
    if os.environ.get('RUBEDO_CHROMIUM'):opts['executable_path']=os.environ['RUBEDO_CHROMIUM']
    browser=p.chromium.launch(**opts)
    page=browser.new_page(viewport={'width':1280,'height':900},accept_downloads=True)
    errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
    def check(name,fn):
        global count
        fn();count+=1;print('OK',name)
    def load(path):
        global page
        viewport=page.viewport_size
        page.close()
        page=browser.new_page(viewport=viewport,accept_downloads=True)
        page.on('pageerror',lambda error:errors.append(str(error)))
        if not args.in_memory:
            page.goto(f'http://127.0.0.1:{server.server_port}/{path}');return
        source=ROOT/path;s=source.read_text();d=source.parent
        s=re.sub(r'<script[^>]+src="([^"]+)"[^>]*></script>',lambda m:'<script>'+(d/m[1]).read_text()+'</script>',s)
        s=re.sub(r'<link[^>]+href="([^"]+\.css)"[^>]*>',lambda m:'<style>'+(d/m[1]).read_text()+'</style>',s)
        s=re.sub(r'(<img[^>]+src=")([^"\s]+\.svg)(")',lambda m:m[1]+'data:image/svg+xml;base64,'+base64.b64encode((d/m[2]).read_bytes()).decode()+m[3],s)
        page.set_content(s)
    def shot(name):
        if args.screenshots:
            args.screenshots.mkdir(parents=True,exist_ok=True);page.screenshot(path=str(args.screenshots/name),full_page=False)
    def no_overflow():assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1')
    def lang_en():page.locator('#en').click();expect(page.locator('html')).to_have_attribute('lang','en')
    def lang_pt():page.locator('#pt').click();expect(page.locator('html')).to_have_attribute('lang','pt-BR')
    load('index.html');check('standards mode',lambda:expect(page.locator('html')).to_have_js_property('tagName','HTML'));assert page.evaluate("document.compatMode === 'CSS1Compat'");check('site heading',lambda:expect(page.locator('h1').first).to_contain_text('Ciência e Inovação'));check('site English',lang_en);check('site English heading',lambda:expect(page.locator('h1').first).to_contain_text('Science'));check('site Portuguese',lang_pt);check('desktop layout',no_overflow);check('live demo',lambda:expect(page.locator('#demo-good')).to_contain_text('527,7'));page.locator('#demo-cycle').evaluate("e=>{e.value=30;e.dispatchEvent(new Event('input'))}");check('live demo update',lambda:expect(page.locator('#demo-good')).to_contain_text('791,5'));check('scenario link',lambda:expect(page.locator('#demo-open')).to_have_attribute('href',re.compile(r'cycle=30.*demand=600')));page.locator('#demo-reset').click();shot('rubedo-site.png')
    page.set_viewport_size({'width':390,'height':844});check('site mobile width',no_overflow);shot('rubedo-site-mobile.png');page.set_viewport_size({'width':1280,'height':900})
    load('mini/index.html');page.locator('#run').click();check('capacity result',lambda:expect(page.locator('#result')).to_contain_text('527,68'));check('Mini English',lang_en);check('capacity English formatting',lambda:expect(page.locator('#result')).to_contain_text('527.68'));lang_pt();page.locator('#cycle').fill('0');check('stale result cleared',lambda:expect(page.locator('#result')).to_be_empty());page.locator('#run').click();check('invalid cycle',lambda:expect(page.locator('#export')).to_be_disabled());page.locator('[data-mode="line"]').click();page.locator('#sample').click();check('bottleneck result',lambda:expect(page.locator('#result')).to_contain_text('Estação 2'));page.locator('[data-mode="experiment"]').click();page.locator('#sample').click();check('experiment result',lambda:expect(page.locator('#result')).to_contain_text('2,4'));page.locator('[data-mode="takt"]').click();page.locator('#sample').click();check('takt demand result',lambda:expect(page.locator('#result')).to_contain_text('Não atende'))
    def export_json(button,validate):
        with page.expect_download(timeout=10000) as d:page.locator(button).click()
        record=json.loads(Path(d.value.path()).read_text());validate(record)
    def mini_record(rec):assert rec['schema']=='rubedo.mini.result.v1' and rec['tool']=='takt' and abs(rec['result']['good']-527.68)<1e-8 and rec['version']=='1.0.1'
    check('mini JSON download',lambda:export_json('#export',mini_record));shot('rubedo-mini.png');page.set_viewport_size({'width':390,'height':844});check('Mini mobile width',no_overflow);page.set_viewport_size({'width':1280,'height':900})
    if not args.in_memory:
        page.goto(f'http://127.0.0.1:{server.server_port}/mini/index.html#mode=takt&cycle=30&demand=700&lang=en')
        check('scenario transfer language',lambda:expect(page.locator('html')).to_have_attribute('lang','en'))
        check('scenario transfer demand',lambda:expect(page.locator('#demand')).to_have_value('700'))
        check('scenario transfer cycle',lambda:expect(page.locator('#takt-cycle')).to_have_value('30'))
        check('scenario transfer result',lambda:expect(page.locator('#result')).to_contain_text('791.52'))
    load('research/index.html');check('sensitivity initial',lambda:expect(page.locator('#sensitivity-result')).to_contain_text('527,68'));check('analytical queue initial',lambda:expect(page.locator('#queue-result')).to_contain_text('Espera média'));page.locator('#arrival').fill('10');page.locator('#service').fill('10');page.locator('#queue-run').click();check('saturation notice',lambda:expect(page.locator('#queue-note')).to_contain_text('não existe regime'));page.locator('#simulacao-run').click();check('simulation results',lambda:expect(page.locator('#simulacao-result')).to_contain_text('Repetição 5'));check('simulation graphic',lambda:expect(page.locator('#simulacao-result svg')).to_have_count(1));page.locator('#otimizacao-run').click();check('optimization result',lambda:expect(page.locator('#otimizacao-result')).to_contain_text('21'));check('optimization graphic',lambda:expect(page.locator('#otimizacao-result svg')).to_have_count(1));page.locator('#otimizacao').scroll_into_view_if_needed();shot('rubedo-research.png')
    def lp_record(rec):assert rec['schema']=='rubedo.optimization.lp2.v1' and rec['best']['objective']==21
    check('research JSON download',lambda:export_json('#otimizacao-export',lp_record));
    for field,value in {'lp-va':'1000000','lp-vb':'0','lp-a1':'1000000','lp-b1':'0','lp-limit1':'0.001','lp-a2':'0','lp-b2':'1','lp-limit2':'1'}.items():page.locator('#'+field).fill(value)
    page.locator('#otimizacao-run').click()
    check('tiny LP coordinate visible',lambda:expect(page.locator('#otimizacao-result')).to_contain_text('1.00000e-9'))
    def tiny_lp_record(rec):
        assert abs(rec['best']['objective']-.001)<1e-12 and abs(rec['best']['x']-1e-9)<1e-18 and len(rec['vertices'])==4
    check('tiny LP JSON download',lambda:export_json('#otimizacao-export',tiny_lp_record))
    lang_en();check('research English output',lambda:expect(page.locator('#otimizacao-result')).to_contain_text('Maximum objective'));lang_pt();page.locator('#protocol-sample').click();check('protocol sample',lambda:expect(page.locator('#p-title')).not_to_have_value(''))
    def protocol(rec):assert rec['schema']=='rubedo.research.protocol.v1' and rec['title']
    check('protocol JSON download',lambda:export_json('#protocol-export',protocol));payload={'schema':'rubedo.research.protocol.v1','title':'Restaurado','question':'Q','method':'M'};page.locator('#protocol-file').set_input_files({'name':'sample.json','mimeType':'application/json','buffer':json.dumps(payload).encode()});page.locator('#protocol-import').click();check('protocol import',lambda:expect(page.locator('#p-title')).to_have_value('Restaurado'));page.locator('#protocol-file').set_input_files({'name':'invalid.json','mimeType':'application/json','buffer':b'{"schema":"invalid"}'});page.locator('#protocol-import').click();check('invalid import preserves fields',lambda:expect(page.locator('#protocol-note')).to_contain_text('Campos preservados'));expect(page.locator('#p-title')).to_have_value('Restaurado');page.set_viewport_size({'width':390,'height':844});check('research mobile width',no_overflow)
    page.set_viewport_size({'width':1280,'height':900})
    check('library twelve protocols',lambda:expect(page.locator('#biblioteca article')).to_have_count(12))
    for field,value in {'name':'Case A','metric':'objective','unit':'points','value':'1,5','notes':'synthetic','parameters':'x=1; seed N/A','source':'analytic'}.items():page.locator('#st-'+field).fill(value)
    page.locator('#st-add').click()
    check('Studio manual record',lambda:expect(page.locator('#st-table tbody tr')).to_have_count(1))
    page.locator('#st-name').fill('Case B');page.locator('#st-value').fill('2,5');page.locator('#st-add').click()
    check('Studio baseline delta',lambda:expect(page.locator('#st-table tbody tr').nth(1).locator('td').nth(6)).to_have_text('1'))
    def studio_record(rec):
        assert rec['schema']=='rubedo.studio.v2' and len(rec['records'])==2
        assert rec['records'][0]['origin']=='manual' and rec['records'][0]['modelVersion']=='1.0.1' and rec['records'][0]['createdAt']
    check('Studio JSON provenance',lambda:export_json('#st-json',studio_record))
    page.locator('#st-file').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':b'{"schema":"bad"}'});page.locator('#st-import').click()
    check('Studio invalid import preserves records',lambda:expect(page.locator('#st-status')).to_contain_text('preservados'))
    expect(page.locator('#st-table tbody tr')).to_have_count(2)
    legacy={'schema':'rubedo.studio.v1','records':[{'model':'R04','name':'Legacy','metric':'objective','unit':'points','value':1,'notes':''}]}
    page.locator('#st-file').set_input_files({'name':'legacy.json','mimeType':'application/json','buffer':json.dumps(legacy).encode()})
    page.once('dialog',lambda d:d.accept());page.locator('#st-import').click()
    check('Studio legacy restore',lambda:expect(page.locator('#st-table tbody tr')).to_have_count(1))
    def legacy_record(rec):assert rec['records'][0]['modelVersion']=='unknown' and rec['records'][0]['createdAt'] is None
    check('Studio legacy provenance',lambda:export_json('#st-json',legacy_record))
    lang_en();check('Studio English headings',lambda:expect(page.locator('#st-table th').nth(1)).to_have_text('Scenario'));lang_pt()
    page.locator('#reg-run').click();expect(page.locator('#reg-export')).to_be_enabled()
    page.locator('#reg-pairs').fill('1;3\n2;5\n3;7')
    check('regression stale export disabled',lambda:expect(page.locator('#reg-export')).to_be_disabled())
    page.locator('#rel-run').click();expect(page.locator('#rel-export')).to_be_enabled()
    page.locator('#rel-time').fill('200');check('reliability stale export disabled',lambda:expect(page.locator('#rel-export')).to_be_disabled())
    page.set_viewport_size({'width':390,'height':844});check('Studio mobile width',no_overflow)
    page.set_viewport_size({'width':360,'height':600});load('extension/popup.html');check('popup 4 tools',lambda:expect(page.locator('[data-mode]')).to_have_count(4));page.locator('#run').click();check('popup capacity',lambda:expect(page.locator('#result')).to_contain_text('527,68'));page.locator('[data-mode="takt"]').click();page.locator('#sample').click();check('popup takt',lambda:expect(page.locator('#result')).to_contain_text('Não atende'));lang_en();check('popup English',lambda:expect(page.locator('#result')).to_contain_text('Does not meet'));check('popup width',no_overflow);shot('rubedo-popup.png');assert not errors,errors;browser.close()
if server:server.shutdown()
print(f'{count} browser interface checks passed ({"in-memory" if args.in_memory else "HTTP"}); no page errors.')
