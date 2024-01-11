import pytest
from flask import url_for

from app.factories import UserBJourneyFactory, SessionsFactory, faker


@pytest.mark.integration
def test_get_alignment(client):
    user_b_journey = UserBJourneyFactory()
    alignment_scores = user_b_journey.alignment_scores
    session = SessionsFactory()

    faked_uuid = faker.uuid4()
    error_response = client.get(
        url_for(
            "alignment.get_alignment",
            alignment_scores_uuid=faked_uuid,
        ),
        headers=[("X-Session-Id", session.session_uuid)],
    )
    assert error_response.status_code == 404

    response = client.get(
        url_for(
            "alignment.get_alignment",
            alignment_scores_uuid=alignment_scores.alignment_scores_uuid,
        ),
        headers=[("X-Session-Id", session.session_uuid)],
    )
    assert response.status_code == 200

    # The exact values are tested in UT
    expected_response_keys = {
        "overallSimilarityScore",
        "topMatchPercent",
        "topMatchValue",
        "valueAlignment",
        "userAName",
        "userBName",
    }
    assert (
        set(response.json.keys()) == expected_response_keys
    ), "Response contain all keys we need"


@pytest.mark.integration
def test_get_alignment(client):
    user_b_journey = UserBJourneyFactory()
    alignment_scores = user_b_journey.alignment_scores
    session = SessionsFactory()

    response = client.get(
        url_for(
            "alignment.get_alignment",
            alignment_scores_uuid=alignment_scores.alignment_scores_uuid,
        ),
        headers=[("X-Session-Id", session.session_uuid)],
    )
    assert response.status_code == 200
    assert "overallSimilarityScore" in response.json
    assert "topMatchPercent" in response.json
    assert "topMatchValue" in response.json
    assert "valueAlignment" in response.json
    assert "userAName" in response.json
    assert "userBName" in response.json


@pytest.mark.integration
def test_get_shared_impacts(client):
    user_b_journey = UserBJourneyFactory()
    alignment_scores = user_b_journey.alignment_scores
    session = SessionsFactory()

    response = client.get(
        url_for(
            "alignment.get_shared_impacts",
            alignment_scores_uuid=alignment_scores.alignment_scores_uuid,
        ),
        headers=[("X-Session-Id", session.session_uuid)],
    )
    assert response.status_code == 200


@pytest.mark.integration
def test_get_shared_solutions(client):
    user_b_journey = UserBJourneyFactory()
    alignment_scores = user_b_journey.alignment_scores
    session = SessionsFactory()

    response = client.get(
        url_for(
            "alignment.get_shared_solutions",
            alignment_scores_uuid=alignment_scores.alignment_scores_uuid,
        ),
        headers=[("X-Session-Id", session.session_uuid)],
    )
    assert response.status_code == 200


@pytest.mark.integration
def test_post_shared_impact_selection(client):
    user_b_journey = UserBJourneyFactory()
    alignment_scores = user_b_journey.alignment_scores
    session = SessionsFactory()

    response = client.post(
        url_for(
            "alignment.post_shared_impact_selection",
            alignment_scores_uuid=alignment_scores.alignment_scores_uuid,
        ),
        json={"sharedImpacts": [{"effectId": "example_effect_id"}]},
        headers=[("X-Session-Id", session.session_uuid)],
    )
    assert response.status_code == 201
