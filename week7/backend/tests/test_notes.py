import time


def _create_note(client, title: str, content: str = "Hello world") -> dict:
    response = client.post("/notes/", json={"title": title, "content": content})
    assert response.status_code == 201, response.text
    return response.json()


def test_create_list_and_patch_notes(client):
    note = _create_note(client, title="Test", content="Hello world")
    assert note["title"] == "Test"
    assert "created_at" in note and "updated_at" in note

    response = client.get("/notes/")
    assert response.status_code == 200
    assert len(response.json()) >= 1

    response = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert response.status_code == 200
    assert len(response.json()) >= 1

    note_id = note["id"]
    response = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


def test_list_notes_pagination_with_skip_and_limit(client):
    for i in range(1, 6):
        _create_note(client, title=f"Note {i:02d}", content=f"Content {i}")

    response = client.get("/notes/", params={"sort": "title", "skip": 1, "limit": 2})
    assert response.status_code == 200

    items = response.json()
    assert len(items) == 2
    assert [item["title"] for item in items] == ["Note 02", "Note 03"]


def test_list_notes_pagination_skip_beyond_total_returns_empty(client):
    for i in range(1, 4):
        _create_note(client, title=f"Item {i}")

    response = client.get("/notes/", params={"skip": 10, "limit": 5})
    assert response.status_code == 200
    assert response.json() == []


def test_list_notes_limit_upper_bound_accepts_200(client):
    for i in range(1, 4):
        _create_note(client, title=f"Limit OK {i}")

    response = client.get("/notes/", params={"limit": 200})
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_list_notes_limit_above_upper_bound_returns_422(client):
    response = client.get("/notes/", params={"limit": 201})
    assert response.status_code == 422

    errors = response.json()["detail"]
    assert any(error["loc"][-1] == "limit" for error in errors)


def test_list_notes_sort_title_ascending(client):
    _create_note(client, title="bravo")
    _create_note(client, title="alpha")
    _create_note(client, title="charlie")

    response = client.get("/notes/", params={"sort": "title"})
    assert response.status_code == 200

    titles = [item["title"] for item in response.json()]
    assert titles == ["alpha", "bravo", "charlie"]


def test_list_notes_sort_title_descending(client):
    _create_note(client, title="bravo")
    _create_note(client, title="alpha")
    _create_note(client, title="charlie")

    response = client.get("/notes/", params={"sort": "-title"})
    assert response.status_code == 200

    titles = [item["title"] for item in response.json()]
    assert titles == ["charlie", "bravo", "alpha"]


def test_list_notes_invalid_sort_falls_back_to_created_at_desc(client):
    first = _create_note(client, title="First")
    time.sleep(0.01)
    second = _create_note(client, title="Second")
    time.sleep(0.01)
    third = _create_note(client, title="Third")

    response = client.get("/notes/", params={"sort": "not_a_field"})
    assert response.status_code == 200

    ids = [item["id"] for item in response.json()]
    assert ids == [third["id"], second["id"], first["id"]]


