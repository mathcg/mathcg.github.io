"""Small Playwright smoke test for the deployed-style static site."""

from pathlib import Path
import os

from playwright.sync_api import sync_playwright


BASE_URL = "http://127.0.0.1:8000"
OUTPUT_DIR = Path("/tmp/gang-site-screenshots")


def check_page(page, viewport, screenshot_name):
    page.set_viewport_size(viewport)
    errors = []
    page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
    page.on("pageerror", lambda error: errors.append(str(error)))
    response = page.goto(BASE_URL, wait_until="networkidle")

    assert response and response.status == 200
    assert page.title() == "Gang Cheng — Research Scientist"
    assert page.locator("h1").inner_text().replace("\n", " ") == "Gang Cheng."
    assert page.locator("#about-heading").inner_text() == "About Me"
    assert page.locator(".publication").count() == 5
    assert page.locator("#software .software-list > li").count() == 2
    assert page.locator("a[href='https://pypi.org/project/accmv/']").count() == 2
    assert "My Ph.D. work sits at the intersection" in page.locator("#about").inner_text()
    assert "including suicide and self-injury content" in page.locator("#about").inner_text()
    assert page.locator("#contact").inner_text() == "Contact\nContact me at mathchenggang [at] gmail [dot] com."
    assert page.locator("a[href='#contact']").count() >= 2
    assert not errors, f"Browser errors: {errors}"

    page.screenshot(path=str(OUTPUT_DIR / screenshot_name), full_page=True)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser_name = os.environ.get("BROWSER", "chromium")
        executable_path = os.environ.get("BROWSER_PATH")
        browser = getattr(playwright, browser_name).launch(executable_path=executable_path)
        page = browser.new_page()
        check_page(page, {"width": 1440, "height": 1000}, "desktop.png")
        check_page(page, {"width": 390, "height": 844}, "mobile.png")

        menu = page.locator(".menu-button")
        menu.click()
        assert menu.get_attribute("aria-expanded") == "true"
        assert "is-open" in (page.locator("#site-nav").get_attribute("class") or "")
        page.keyboard.press("Escape")
        assert menu.get_attribute("aria-expanded") == "false"

        browser.close()

    print("Browser checks passed; screenshots written to", OUTPUT_DIR)


if __name__ == "__main__":
    main()
