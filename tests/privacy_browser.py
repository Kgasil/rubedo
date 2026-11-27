"""Local HTTP privacy checks and a real unpacked extension load in isolated Chromium.
Not a test in branded Chrome/Edge, Windows or antivirus.
"""
import functools,http.server,threading,tempfile,subprocess,sys,json,hashlib
from pathlib import Path
from zipfile import ZipFile
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
origin=f'http://127.0.0.1:{server.server_port}'
with sync_playwright() as p:
    browser=p.chromium.launch()
    context=browser.new_context(accept_downloads=True)
    outside=[]
    def route(r):
        if r.request.url.startswith(origin+'/'): r.continue_()
        else: outside.append(r.request.url);r.abort()
    context.route('**/*',route)
    page=context.new_page()
    for path,button in [('index.html',None),('mini/index.html','#run'),('research/index.html','#otimizacao-run')]:
        page.goto(origin+'/'+path);page.wait_for_load_state('networkidle')
        if button:page.locator(button).click()
        assert page.locator('meta[http-equiv="Content-Security-Policy"]').count()==1
        # A same-origin fetch is also denied by connect-src; no request should reach the server.
        assert page.evaluate("""async () => {try {await fetch('/privacy-probe');return false;}catch(e){return true;}}""")
        print('PASS local-only subresources and blocked fetch',path)
    assert not outside,outside
    page.goto(origin+'/research/index.html')
    payload={'schema':'rubedo.research.protocol.v1','title':'<img src=x onerror=alert(1)>','question':'Q','method':'M'}
    page.locator('#protocol-file').set_input_files({'name':'synthetic.json','mimeType':'application/json','buffer':json.dumps(payload).encode()})
    page.locator('#protocol-import').click()
    expect(page.locator('#p-title')).to_have_value(payload['title'])
    assert page.locator('img[src="x"]').count()==0
    print('PASS imported markup treated as text')
    context.close();browser.close()
    with tempfile.TemporaryDirectory() as tmp:
        temp=Path(tmp);stage=temp/'stage';profile=temp/'profile';ext=temp/'extension'
        subprocess.run([sys.executable,str(ROOT/'scripts/package_extension.py'),'--output-dir',str(stage)],check=True)
        archive=stage/'Rubedo-Mini-v1.0.1-install.zip'
        with ZipFile(archive) as z:z.extractall(ext)
        # Chromium permits extension loading in the bundled channel; use a fresh persistent profile.
        context=p.chromium.launch_persistent_context(str(profile),channel='chromium',headless=True,args=[f'--disable-extensions-except={ext}',f'--load-extension={ext}'],accept_downloads=True)
        try:
            page=context.new_page();page.goto('chrome://extensions/')
            item=page.locator('extensions-item').filter(has_text='Rubedo Mini')
            expect(item).to_have_count(1,timeout=15000)
            extension_id=item.evaluate('e=>e.data.id')
            assert extension_id and len(extension_id)==32
            page.goto(f'chrome-extension://{extension_id}/popup.html')
            expect(page.locator('[data-mode]')).to_have_count(4)
            page.locator('#run').click();expect(page.locator('#result')).to_contain_text('527,68')
            for mode in ['line','experiment','takt']:
                page.locator(f'[data-mode="{mode}"]').click();page.locator('#sample').click()
                expect(page.locator('#result')).not_to_be_empty()
            with page.expect_download() as d:page.locator('#export').click()
            data=json.loads(Path(d.value.path()).read_text());assert data['version']=='1.0.1' and data['tool']=='takt'
            assert page.evaluate("chrome.runtime.getManifest().version")=='1.0.1'
            assert page.evaluate("!chrome.runtime.getManifest().permissions && !chrome.runtime.getManifest().host_permissions")
            assert page.evaluate("""async()=>{try{await fetch('https://example.invalid');return false}catch(e){return true}}""")
            print('PASS unpacked Chromium extension registered, all four tools and JSON export')
            print('Installed candidate SHA-256:',hashlib.sha256(archive.read_bytes()).hexdigest())
        finally:context.close()
server.shutdown()
print('Privacy and isolated Chromium installation checks passed')
