from pathlib import Path


DASHBOARD_JS = (
    Path(__file__).parents[1] / "static" / "app.js"
).read_text(encoding="utf-8")


def test_live_polling_cannot_erase_limits_while_user_is_typing():
    assert "let limitsDirty = false;" in DASHBOARD_JS
    assert "if (!limitsDirty)" in DASHBOARD_JS
    assert "limitsDirty = true;" in DASHBOARD_JS
    assert "limitsDirty = false;" in DASHBOARD_JS
