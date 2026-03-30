def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_update_note(client):
    r = client.post("/notes/", json={"title": "Original", "content": "Old content"})
    assert r.status_code == 201
    note_id = r.json()["id"]

    r = client.put(f"/notes/{note_id}", json={"title": "Updated", "content": "New content"})
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["id"] == note_id
    assert data["title"] == "Updated"
    assert data["content"] == "New content"


def test_update_note_not_found(client):
    r = client.put("/notes/9999", json={"title": "X", "content": "Y"})
    assert r.status_code == 404


def test_update_note_validation_empty_title(client):
    r = client.post("/notes/", json={"title": "Valid", "content": "Content"})
    note_id = r.json()["id"]

    r = client.put(f"/notes/{note_id}", json={"title": "", "content": "Content"})
    assert r.status_code == 422


def test_update_note_validation_title_too_long(client):
    r = client.post("/notes/", json={"title": "Valid", "content": "Content"})
    note_id = r.json()["id"]

    r = client.put(f"/notes/{note_id}", json={"title": "x" * 201, "content": "Content"})
    assert r.status_code == 422


def test_update_note_validation_empty_content(client):
    r = client.post("/notes/", json={"title": "Valid", "content": "Content"})
    note_id = r.json()["id"]

    r = client.put(f"/notes/{note_id}", json={"title": "Valid", "content": ""})
    assert r.status_code == 422


def test_delete_note(client):
    r = client.post("/notes/", json={"title": "To Delete", "content": "Bye"})
    assert r.status_code == 201
    note_id = r.json()["id"]

    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404


def test_delete_note_not_found(client):
    r = client.delete("/notes/9999")
    assert r.status_code == 404


def test_create_note_validation(client):
    r = client.post("/notes/", json={"title": "", "content": "Content"})
    assert r.status_code == 422

    r = client.post("/notes/", json={"title": "Title", "content": ""})
    assert r.status_code == 422

    r = client.post("/notes/", json={"title": "x" * 201, "content": "Content"})
    assert r.status_code == 422
