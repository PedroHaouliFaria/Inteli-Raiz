import pytest

from datetime import datetime, timedelta

from app.domain.notices.policy import (
    InitialHandling,
    NoticePolicy,
    MemberResponse,
    ResponseOutcome,
    initial_handling,
    is_expired,
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


def test_it_was_me_goes_to_analyst_when_auto_close_is_off():
    policy = NoticePolicy(auto_close_on_it_was_me=False)
    outcome = outcome_for_response(MemberResponse.IT_WAS_ME, biometrics_ok=True, recent_device=False, policy=policy)

    assert outcome is ResponseOutcome.ROUTE_TO_ANALYST


def test_notice_expires_after_configured_timeout():
    sent_at = datetime(2026, 10, 27, 3, 16)
    policy = NoticePolicy(response_timeout_minutes=10)

    assert not is_expired(sent_at, sent_at + timedelta(minutes=9), policy)
    assert is_expired(sent_at, sent_at + timedelta(minutes=10), policy)


def test_notice_policy_reads_environment(monkeypatch):
    from app.config import get_notice_policy, get_settings

    monkeypatch.setenv("NOTICE_AUTO_CLOSE_ON_IT_WAS_ME", "false")
    monkeypatch.setenv("NOTICE_RESPONSE_TIMEOUT_MINUTES", "15")
    get_settings.cache_clear()
    try:
        policy = get_notice_policy()
    finally:
        get_settings.cache_clear()

    assert policy.auto_close_on_it_was_me is False
    assert policy.response_timeout_minutes == 15
