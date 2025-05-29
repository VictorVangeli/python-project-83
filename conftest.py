from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

_orig_screenshot = Page.screenshot


def _screenshot_with_timeout(self, *args, **kwargs):
    kwargs.setdefault("timeout", 10_000)
    try:
        return _orig_screenshot(self, *args, **kwargs)
    except PlaywrightTimeoutError:
        return b""


Page.screenshot = _screenshot_with_timeout
__all__: list = []
