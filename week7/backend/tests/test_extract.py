from backend.app.services.extract import extract_action_items


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    - task: fix docs
    - BuG: investigate flaky test
    - TODO:
    - ACTION:      
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "TODO: write tests" in items
    assert "ACTION: review PR" in items
    assert "TASK: fix docs" in items
    assert "BUG: investigate flaky test" in items
    assert "TODO:" not in items
    assert "ACTION:" not in items
    assert "Ship it!" in items


