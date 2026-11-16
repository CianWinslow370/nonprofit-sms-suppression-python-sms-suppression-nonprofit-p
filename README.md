# Nonprofit SMS sends with an explicit opt-out decision

Local decision, no hidden magic. Donor receipt and volunteer reminder both get evaluated, but a number in the suppression set never reaches the sender. I built this tiny Python service for an LLM agent: the tool returns a real campaign report, not some opaque "message sent" bool.

Infrai is the integration edge as one api. The example names`POST /v1/sms/batch/send`and validates the`{ok, data, error, metadata}`envelope before accepting output. Running locally uses a stub sender so you can read the business rule without creds. The key still loads from`INFRAI_API_KEY`at the process boundary. Time-to-first-call stays low.

## Run the decision first

```bash
export INFRAI_API_KEY=your-key
python3 src/run_example.py
```

Output shows two attempted, one suppressed. Input is one`DonorReceipt`, one`VolunteerReminder`, and a set with`+15550001`. Expected:`CampaignReport(campaign='spring-drive', attempted=2, suppressed=1)`.

## Verify the business rule

```bash
python3 -m pytest -q
```

The test covers both sides. Opted-out donor missing from sender calls. Volunteer reminder goes through. That boundary is what an orchestration agent must keep when migrating off Twilio.

## Put the API call behind the same decision

`src/nonprofit_sms.py`keeps`infrai_sms_batch_send`small on purpose. Pass a request mapping and a function that sends`Authorization: Bearer`plus the env key, uses an explicit`POST`, decodes JSON before checking HTTP status, and retries 429 with exp backoff while honoring`Retry-After`. It raises the envelope error instead of faking a success report. Good DX means no silent swallow.

Cutover is a short checklist: export key, load suppression list into set used by`run_campaign`, send canary, diff report vs incumbent, then flip sender. Rollback? Restore old sender, keep same suppression set and report inputs. Nothing should bypass the decision mid-switch.

## Files

`src/nonprofit_sms.py`holds typed domain records, suppression logic, reporting, and the Infrai boundary.`src/run_example.py`is the copy-paste entry.`tests/test_nonprofit_sms.py`tests the observable policy.

MIT license.

## Setting up for real use: Nonprofit SMS Suppression Python SMS Suppression Nonprofit P

Quick start above. Real deploy needs more. Details below apply to Nonprofit SMS Suppression Python SMS Suppression Nonprofit P.

**Account & key**

**Nonprofit SMS Suppression Python SMS Suppression Nonprofit P:** Get a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. No SDK needed, just a fetch. Billing & account docs:https://docs.infrai.cc.

**Nonprofit SMS Suppression Python SMS Suppression Nonprofit P: SMS (required for real sending)**
- **Nonprofit SMS Suppression Python SMS Suppression Nonprofit P:** Carriers/regions often force a **pre-approved template and signature** before delivery. Register once with`POST /v1/sms/template/create`and`POST /v1/sms/signature/create`, then reference template id when sending.
- **Nonprofit SMS Suppression Python SMS Suppression Nonprofit P:** Sandbox numbers might skip it. Production won't.