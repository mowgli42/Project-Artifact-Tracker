def test_index_returns_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"html" in response.data.lower()


def test_create_and_list_projects(client):
    create = client.post(
        "/api/projects",
        json={"name": "Alpha Mission", "description": "Test project", "status": "Active"},
    )
    assert create.status_code == 201
    body = create.get_json()
    assert body["name"] == "Alpha Mission"

    listing = client.get("/api/projects")
    assert listing.status_code == 200
    projects = listing.get_json()
    assert len(projects) == 1
    assert projects[0]["name"] == "Alpha Mission"


def test_create_project_requires_name(client):
    response = client.post("/api/projects", json={"description": "missing name"})
    assert response.status_code == 400


def test_get_update_delete_project(client):
    created = client.post("/api/projects", json={"name": "Bravo"}).get_json()
    project_id = created["id"]

    fetched = client.get(f"/api/projects/{project_id}")
    assert fetched.status_code == 200
    assert fetched.get_json()["name"] == "Bravo"

    updated = client.put(
        f"/api/projects/{project_id}",
        json={"name": "Bravo Updated", "status": "Completed"},
    )
    assert updated.status_code == 200
    assert updated.get_json()["name"] == "Bravo Updated"

    deleted = client.delete(f"/api/projects/{project_id}")
    assert deleted.status_code == 200

    missing = client.get(f"/api/projects/{project_id}")
    assert missing.status_code == 404
