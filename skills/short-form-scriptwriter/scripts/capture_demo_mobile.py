from playwright.sync_api import sync_playwright
import time
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--disable-gpu'])
    c=b.new_context(viewport={'width':390,'height':844},device_scale_factor=3,is_mobile=True,has_touch=True)
    pg=c.new_page(); pg.goto('https://tendaapp.onrender.com/app?version=20261001-v4',wait_until='networkidle',timeout=90000); time.sleep(4)
    pg.screenshot(path='m_overview.png')
    print([t for t in pg.locator('button').all_inner_texts()][:25])
    for name in ['Inbox','Approve']:
        try:
            pg.get_by_role('button',name=name).first.click(timeout=4000); time.sleep(2); pg.screenshot(path=f'm_{name.lower()}.png'); print('ok',name)
        except Exception as e: print('fail',name,str(e)[:80])
    b.close()
