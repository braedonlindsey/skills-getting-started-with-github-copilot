"""Test suite for the Mergington High School Activities API.

Uses the Arrange-Act-Assert (AAA) pattern for clarity.
"""

import pytest


def test_get_activities_returns_expected_structure(client):
    # Arrange: (nothing special; app starts with default activities)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    new_student = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={new_student}")

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    activities = client.get("/activities").json()
    assert new_student in activities[activity]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity = "Chess Club"
    student = "newstudent@mergington.edu"

    # Act
    first = client.post(f"/activities/{activity}/signup?email={student}")
    second = client.post(f"/activities/{activity}/signup?email={student}")

    # Assert
    assert first.status_code == 200
    assert second.status_code == 400
    assert "already signed up" in second.json()["detail"].lower()


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity = "Nonexistent Club"
    student = "someone@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={student}")

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_removes_participant(client):
    # Arrange
    activity = "Chess Club"
    student = "newstudent@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={student}")

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={student}")

    # Assert
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]

    activities = client.get("/activities").json()
    assert student not in activities[activity]["participants"]


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    activity = "Chess Club"
    student = "missing@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={student}")

    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]
