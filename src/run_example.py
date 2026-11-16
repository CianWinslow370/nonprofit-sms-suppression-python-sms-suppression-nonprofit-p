import os

from nonprofit_sms import CampaignReport, DonorReceipt, VolunteerReminder, run_campaign


def demo_sender(phone: str, message: str) -> str:
    return f"queued {phone}: {message}"


def main() -> CampaignReport:
    api_key = os.environ.get("INFRAI_API_KEY")
    if not api_key:
        raise RuntimeError("INFRAI_API_KEY is required")
    report = run_campaign(
        DonorReceipt("+15550001", "Mina", "$25"),
        VolunteerReminder("+15550002", "Ravi", "Saturday 09:00"),
        {"+15550001"},
        demo_sender,
    )
    print(report)
    return report


if __name__ == "__main__":
    main()
