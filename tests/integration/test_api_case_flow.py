from __future__ import annotations


def test_health_endpoints(client):
    for path in ["/", "/health/live", "/health/ready"]:
        response = client.get(path)
        assert response.status_code == 200


def test_create_and_read_case_and_job(client):
    create_response = client.post(
        "/cases",
        json={
            "title": "Cannot login to dashboard",
            "description": "User cannot access the dashboard after a password reset.",
        },
    )
    assert create_response.status_code == 201

    payload = create_response.json()
    case_id = payload["case"]["id"]
    job_id = payload["job"]["id"]

    assert payload["case"]["status"] == "queued"
    assert payload["case"]["source"] is None
    assert payload["job"]["status"] == "pending"
    assert payload["job"]["job_type"] == "triage_case"
    assert payload["job"]["case_id"] == case_id

    list_response = client.get("/cases")
    assert list_response.status_code == 200
    assert any(item["id"] == case_id for item in list_response.json())

    case_response = client.get(f"/cases/{case_id}")
    assert case_response.status_code == 200
    assert case_response.json()["title"] == "Cannot login to dashboard"

    job_response = client.get(f"/jobs/{job_id}")
    assert job_response.status_code == 200
    assert job_response.json()["case_id"] == case_id


def test_create_case_with_optional_source(client):
    create_response = client.post(
        "/cases",
        json={
            "title": "Payment issue",
            "description": "Customer was charged twice.",
            "source": "email",
        },
    )
    assert create_response.status_code == 201

    payload = create_response.json()
    case_id = payload["case"]["id"]

    assert payload["case"]["source"] == "email"

    case_response = client.get(f"/cases/{case_id}")
    assert case_response.status_code == 200
    assert case_response.json()["source"] == "email"

    list_response = client.get("/cases")
    assert list_response.status_code == 200
    listed_case = next(item for item in list_response.json() if item["id"] == case_id)
    assert listed_case["source"] == "email"
