import pytest

from app.domain.notices.policy import (
    InitialHandling,
    MemberResponse,
    ResponseOutcome,
    initial_handling,
    outcome_for_response,
)


@pytest.mark.parametrize(
    ("score", "expected"),
    [
        (0.41, InitialHandling.NO_ACTION),
        (0.66, InitialHandling.AUTO_SEND_NOTICE),
        (0.80, InitialHandling.ROUTE_TO_ANALYST),
        (0.92, InitialHandling.ROUTE_TO_ANALYST),
    ],
)
def test_medium_risk_sends_notice_and_high_risk_goes_to_analyst(score, expected):
    assert initial_handling(score) is expected


def test_it_was_me_with_biometrics_on_known_device_releases_purchase():
    outcome = outcome_for_response(MemberResponse.IT_WAS_ME, biometrics_ok=True, recent_device=False)

    assert outcome is ResponseOutcome.RELEASE_PURCHASE


@pytest.mark.parametrize(
    ("response", "biometrics_ok", "recent_device"),
    [
        (MemberResponse.IT_WAS_ME, True, True),
        (MemberResponse.IT_WAS_ME, False, False),
        (MemberResponse.NOT_ME, False, False),
        (MemberResponse.TALK_TO_PERSON, False, False),
        (MemberResponse.NO_RESPONSE, False, False),
    ],
)
def test_exceptions_go_to_analyst(response, biometrics_ok, recent_device):
    outcome = outcome_for_response(response, biometrics_ok=biometrics_ok, recent_device=recent_device)

    assert outcome is ResponseOutcome.ROUTE_TO_ANALYST
