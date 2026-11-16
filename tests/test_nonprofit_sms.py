from src.nonprofit_sms import DonorReceipt, VolunteerReminder, run_campaign


def test_opted_out_donor_is_suppressed_and_volunteer_is_sent():
    sent = []
    report = run_campaign(
        DonorReceipt("+1", "Asha", "$30"),
        VolunteerReminder("+2", "Noah", "Tuesday 18:00"),
        {"+1"},
        lambda phone, message: sent.append((phone, message)) or "message-1",
    )
    assert report == report.__class__("spring-drive", 2, 1)
    assert [phone for phone, _ in sent] == ["+2"]
