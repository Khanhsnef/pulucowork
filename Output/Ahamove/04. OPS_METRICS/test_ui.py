from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.on("console", lambda msg: print(f"Console {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"Page Error: {err}"))
        
        print("Navigating to http://localhost:8080/Index.html")
        page.goto("http://localhost:8080/Index.html")
        page.wait_for_timeout(2000)
        
        print("Taking screenshot...")
        page.screenshot(path="screenshot.png")
        print("Screenshot saved to screenshot.png")
        
        print("Clicking tab-master...")
        page.click("#tab-btn-master")
        page.wait_for_timeout(1000)
        
        is_active = page.evaluate("document.getElementById('tab-master').classList.contains('active')")
        print(f"Is tab-master active? {is_active}")
        
        browser.close()

if __name__ == "__main__":
    run()
