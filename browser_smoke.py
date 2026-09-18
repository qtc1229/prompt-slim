"""Real browser + local model smoke check; run manually after starting app.py."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={'width':1280,'height':1000})
    errors=[]
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto('http://127.0.0.1:8765')
    page.locator('#model option[value="qwen3:4b"]').wait_for(state='attached')
    page.locator('#model').select_option('qwen3:4b')
    case=json.loads(Path('evals/cases.json').read_text(encoding='utf-8'))[1]
    page.locator('#source').fill(case['text'])
    page.locator('#protected').fill('\n'.join(case['protected']))
    page.get_by_role('button',name='保守压缩').click()
    page.wait_for_function("document.querySelector('#output').value.length > 0",timeout=180000)
    result=page.locator('#output').input_value()
    assert all(fragment in result for fragment in case['protected'])
    assert '参考 token' in page.locator('#status').inner_text()
    page.locator('#protected').fill('THIS IS NOT IN THE SOURCE')
    page.get_by_role('button',name='保守压缩').click()
    page.wait_for_function("!document.querySelector('#compress').disabled")
    assert page.locator('#output').input_value()==''
    assert '必须存在于原文' in page.locator('#status').inner_text()
    assert not errors, errors
    page.locator('#protected').fill('\n'.join(case['protected']))
    page.get_by_role('button',name='保守压缩').click()
    page.wait_for_function("document.querySelector('#output').value.length > 0",timeout=180000)
    Path('artifacts').mkdir(exist_ok=True)
    page.screenshot(path='artifacts/desktop.png',full_page=True)
    page.set_viewport_size({'width':390,'height':844})
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
    page.screenshot(path='artifacts/mobile.png',full_page=True)
    print('PASS: model selection, real compression, literals, stale-output clearing, validation error, mobile overflow, JS errors')
    browser.close()