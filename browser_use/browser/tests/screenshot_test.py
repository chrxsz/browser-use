import os
os.environ["ANONYMIZED_TELEMETRY"] = "false"

import asyncio
import base64
import pytest

from browser_use.browser.browser import Browser, BrowserConfig


async def test_take_full_page_screenshot():
    browser = Browser(config=BrowserConfig(headless=False, disable_security=True))
    try:
        async with await browser.new_context() as context:
            page = await context.get_current_page()
            await page.goto('https://youtube.com')
            await asyncio.sleep(3)

            screenshot_b64 = await context.take_screenshot(full_page=True)
            await asyncio.sleep(3)

            assert screenshot_b64 is not None
            assert isinstance(screenshot_b64, str)
            assert len(screenshot_b64) > 0

            try:
                image_data = base64.b64decode(screenshot_b64)

                # Caminho para salvar a imagem
                output_dir = "/Users/christian/Documents/GitHub/browser-use/browser_use/browser/tests"
                os.makedirs(output_dir, exist_ok=True)
                
                output_path = os.path.join(output_dir, "screenshot.png")

                with open(output_path, "wb") as f:
                    f.write(image_data)
            except Exception as e:
                pytest.fail(f'Failed to decode base64 screenshot: {str(e)}')

            print(f"Screenshot saved at: {output_path}")
    finally:
        await browser.close()


if __name__ == '__main__':
    asyncio.run(test_take_full_page_screenshot())