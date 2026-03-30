import os
import pytest

from ..app.services.extract import extract_action_items


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


from ..app.services.extract import extract_action_items_llm


def test_llm_simple_sentences():
    text = "Finish homework. Email professor."
    items = extract_action_items_llm(text)

    assert isinstance(items, list)
    assert any("Finish homework" in item for item in items)
    assert any("Email professor" in item for item in items)


def test_llm_bullet_list():
    text = """
    - Set up database
    - Implement endpoint
    """
    items = extract_action_items_llm(text)

    assert isinstance(items, list)
    assert any("Set up database" in item for item in items)
    assert any("Implement endpoint" in item for item in items)


def test_llm_empty_input():
    items = extract_action_items_llm("")
    assert isinstance(items, list)
