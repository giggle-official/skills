# Error handling

Classify retries before surfacing failures to avoid dumping long stack traces.

## HTTP layer

| Situation | Suggestion |
|-----------|--------------|
| 4xx / 5xx | One line: upstream unavailable or denied; optionally retry shortly. |
| Timeouts | If nothing was created yet, retry submit; if `task_id` exists, **`query`** to avoid duplicate billable jobs. |

## Envelope fields `code` / `msg`

Typical envelope:

```json
{ "code": 200, "msg": "success", "data": { ... } }
```

| code | Meaning | Suggestion |
|------|---------|------------|
| `200` | OK | Continue parsing `data`. |
| non-200 | Error | Relay `msg`; infer quota/param/compliance issues from wording. |

Exact codes belong in gateway docs.

## Task status

`data.status` from `task/query`:

| Example status | Meaning | Suggestion |
|----------------|---------|-------------|
| (in progress) | Not done | Poll until deadline or terminal state. |
| `completed` | Success | Output is `urls[0]`. |
| `failed` / `fail` / `error` or nonempty `err_msg` | Failure | Read `err_msg`; fix URLs / script / drives and `run` again. |

## After timeout

If `run` or `query` hits `--timeout` before `completed`:

1. Do **not** blindly resubmit the same render (might double billing).  
2. Use **`query --task-id <existing id>`** with a longer `--timeout`.

## Common input pitfalls

| Issue | Mitigation |
|-------|-------------|
| Image/audio URL inaccessible | HTTPS, referrer rules, expiry for signed URLs. |
| Mixing drives | CLI rejects overlaps; handwritten JSON cannot mix `drive_audio` with TTS fields. |
| `clone_audio` with `voice_over_id` both set | Against gateway rules—clone mode skips `voice_over_id`. |
| `tts_script` empty / whitespace-only (`drive_mode=1`) | Non-empty copy required; CLI rejects before submit. |
| `tts_script` over 2700 characters | Shorten copy; CLI rejects before submit. |
| Invalid `<break time="…"/>` values | Pause must be 0.1–99.9 s with ≤1 decimal; fix markup or gateway may fail. |
| TTS playback > ~180 s | Gateway may reject despite character limit; shorten script or reduce breaks. |
| `drive_audio` longer than 120 s | Use a shorter clip; CLI cannot validate remote duration. |
