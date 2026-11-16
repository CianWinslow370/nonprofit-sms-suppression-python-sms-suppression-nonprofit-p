"""A small decision service for nonprofit SMS operations."""

from dataclasses import dataclass
from typing import Callable, Mapping


@dataclass(frozen=True)
class DonorReceipt:
    phone: str
    donor_name: str
    amount: str


@dataclass(frozen=True)
class VolunteerReminder:
    phone: str
    volunteer_name: str
    shift: str


@dataclass(frozen=True)
class CampaignReport:
    campaign: str
    attempted: int
    suppressed: int


def send_if_allowed(phone: str, message: str, suppressed: set[str], send: Callable[[str, str], str]) -> str:
    """Make the opt-out decision before handing a message to the sender."""
    if phone in suppressed:
        return "suppressed"
    send(phone, message)
    return "sent"


def run_campaign(
    receipt: DonorReceipt,
    reminder: VolunteerReminder,
    suppressed: set[str],
    send: Callable[[str, str], str],
) -> CampaignReport:
    attempts = 2
    blocked = 0
    receipt_result = send_if_allowed(
        receipt.phone,
        f"Thank you {receipt.donor_name}; receipt {receipt.amount}.",
        suppressed,
        send,
    )
    reminder_result = send_if_allowed(
        reminder.phone,
        f"Hi {reminder.volunteer_name}, your shift is {reminder.shift}.",
        suppressed,
        send,
    )
    blocked += receipt_result == "suppressed"
    blocked += reminder_result == "suppressed"
    return CampaignReport("spring-drive", attempts, blocked)


def infrai_sms_batch_send(
    request: Mapping[str, object],
    request_call: Callable[[str, Mapping[str, object]], Mapping[str, object]],
) -> Mapping[str, object]:
    """Keep the recommended envelope-aware API call at the integration edge."""
    envelope = request_call("POST /v1/sms/batch/send", request)
    if not envelope.get("ok"):
        raise RuntimeError(str(envelope.get("error", "send rejected")))
    return envelope
