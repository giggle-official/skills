#!/usr/bin/env python3
"""Photo-driven talking-head video (wrapped Giggle generation API).

## Agent reminders
- Default to `run`: submit then poll until done.
- If `run` times out but you have task_id: keep polling via `query --task-id`; only final states belong to users.

Three mutually exclusive drives (see references/tv_avatar_video.md):
  A  TTS + voice_over_id (drive_mode=1)
  B  TTS + clone_audio.url (drive_mode=1; omit voice_over_id)
  C  drive_audio.url (drive_mode=2)

Examples:
    python tv_avatar_video.py run --image-url https://... \\
      --tts-script "Hello" --voice-over-id <id>

    python tv_avatar_video.py run --image-url https://... \\
      --tts-script "Hello" --clone-audio-url https://... --voice-speed 1

    python tv_avatar_video.py run --image-url https://... \\
      --drive-audio-url https://...

    python tv_avatar_video.py query --task-id <uuid>
"""

from __future__ import annotations

import argparse
import json as json_mod
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))

from shared.client import GiggleApiError, GiggleClient

DEFAULT_TIMEOUT = 600
DEFAULT_INTERVAL = 5

TTS_SCRIPT_MAX_CHARS = 2700
_BREAK_TAG_RE = re.compile(r'<break\s+time="([^"]+)"\s*/>', re.IGNORECASE)
_BREAK_NUM_PART = re.compile(r"^(\d+(?:\.\d)?)$")


def validate_tts_script_content(text: str, parser: argparse.ArgumentParser) -> None:
    """Gateway-aligned checks for drive_mode=1 copy (chars + break tags)."""
    if not text:
        parser.error("drive_mode=1 requires non-empty --tts-script")
    if len(text) > TTS_SCRIPT_MAX_CHARS:
        parser.error(
            f"--tts-script exceeds {TTS_SCRIPT_MAX_CHARS} characters (got {len(text)})"
        )
    for m in _BREAK_TAG_RE.finditer(text):
        inner = m.group(1).strip()
        low = inner.lower()
        if not low.endswith("s"):
            parser.error(
                f'break tag value must end with s (e.g. time="1.0s"): {m.group(0)!r}'
            )
        num_part = inner[:-1].strip()
        if not _BREAK_NUM_PART.fullmatch(num_part):
            parser.error(
                "break pause must look like N or N.D with at most one decimal "
                f'(e.g. 1.0): {m.group(0)!r}'
            )
        sec = float(num_part)
        if sec < 0.1 or sec > 99.9:
            parser.error(
                "break pause must be between 0.1 and 99.9 seconds inclusive "
                f'(got {sec} in {m.group(0)!r})'
            )


def build_submit_body(args: argparse.Namespace) -> dict:
    """Build JSON body for POST /api/v1/generation/tv-avatar-video."""
    body: dict = {
        "image": {"url": args.image_url.strip()},
    }

    if args.drive_audio_url:
        body["drive_mode"] = 2
        body["drive_audio"] = {"url": args.drive_audio_url.strip()}
        return body

    body["drive_mode"] = 1
    body["tts_script"] = args.tts_script.strip()

    if args.clone_audio_url:
        body["clone_audio"] = {"url": args.clone_audio_url.strip()}
        if args.voice_speed is not None:
            body["voice_speed"] = args.voice_speed
        return body

    body["voice_over_id"] = args.voice_over_id.strip()
    return body


def validate_drive_args(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    """Ensure exactly one valid drive combination."""
    tts_raw = args.tts_script
    has_tts_nonempty = bool(tts_raw and tts_raw.strip())
    has_voice = bool(args.voice_over_id)
    has_clone = bool(args.clone_audio_url)
    has_drive_audio = bool(args.drive_audio_url)

    if has_drive_audio:
        if has_tts_nonempty or has_voice or has_clone:
            parser.error(
                "Audio drive (--drive-audio-url) cannot be combined with "
                "--tts-script / --voice-over-id / --clone-audio-url"
            )
        return

    if tts_raw is not None and not str(tts_raw).strip():
        parser.error("--tts-script cannot be empty for drive_mode=1")

    if has_clone:
        if not has_tts_nonempty:
            parser.error("--clone-audio-url requires non-empty --tts-script")
        if has_voice:
            parser.error("Do not combine --clone-audio-url with --voice-over-id")
        validate_tts_script_content(tts_raw.strip(), parser)
        return

    if has_voice:
        if not has_tts_nonempty:
            parser.error("--voice-over-id requires non-empty --tts-script")
        validate_tts_script_content(tts_raw.strip(), parser)
        return

    parser.error(
        "Choose one drive: "
        "(1) --tts-script + --voice-over-id; "
        "(2) --tts-script + --clone-audio-url; "
        "(3) --drive-audio-url"
    )


def add_submit_args(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--image-url",
        required=True,
        help="HTTPS portrait URL mapped to body image.url",
    )
    p.add_argument(
        "--tts-script",
        default=None,
        help=f"TTS copy for drive_mode=1 only; non-empty; max {TTS_SCRIPT_MAX_CHARS} chars",
    )
    p.add_argument(
        "--voice-over-id",
        default=None,
        help="Preset voice catalog id (mutually exclusive with clone_audio)",
    )
    p.add_argument(
        "--clone-audio-url",
        default=None,
        help="Reference / clone tone URL—omit voice_over_id when present",
    )
    p.add_argument(
        "--voice-speed",
        type=float,
        default=None,
        help="Speech rate paired with clone_audio (optional, e.g. 1)",
    )
    p.add_argument(
        "--drive-audio-url",
        default=None,
        help="Full clip URL for drive_mode=2; mutually exclusive with TTS fields",
    )
    p.add_argument(
        "--base-url",
        default=None,
        help="Override GIGGLE_API_BASE (default https://giggle.pro)",
    )


def add_poll_args(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"Max poll duration in seconds (default {DEFAULT_TIMEOUT})",
    )
    p.add_argument(
        "--interval",
        type=float,
        default=DEFAULT_INTERVAL,
        help=f"Poll interval in seconds (default {DEFAULT_INTERVAL})",
    )


def add_output_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--output", default=None, help="Download rendered URL to this path")
    p.add_argument("--json", action="store_true", help="Print last query response JSON in full")
    p.add_argument("-q", "--quiet", action="store_true", help="Suppress progress output")


def download_url(url: str, output: str, quiet: bool) -> None:
    import requests as req

    if not quiet:
        print(f"Downloading to {output}...", file=sys.stderr)
    resp = req.get(url, stream=True, timeout=300)
    resp.raise_for_status()
    with open(output, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    if not quiet:
        mb = os.path.getsize(output) / (1024 * 1024)
        print(f"Saved {output} ({mb:.1f} MB)", file=sys.stderr)


def print_completed(data: dict, args: argparse.Namespace, full_json: dict | None) -> None:
    urls = data.get("urls") or []
    primary = urls[0] if urls else ""
    if args.output and primary:
        download_url(primary, args.output, args.quiet)
    if args.json and full_json is not None:
        print(json_mod.dumps(full_json, indent=2, ensure_ascii=False))
    elif primary:
        print(primary)
    else:
        print("", end="")


def cmd_run(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    validate_drive_args(args, parser)
    body = build_submit_body(args)
    client = GiggleClient(base_url=args.base_url) if args.base_url else GiggleClient()

    if not args.quiet:
        print("Submitting talking-head job...", file=sys.stderr)
    try:
        task_id = client.submit_tv_avatar(body)
    except GiggleApiError as e:
        print(f"Submit failed: {e}", file=sys.stderr)
        sys.exit(1)

    if not args.quiet:
        print(f"Submitted. task_id: {task_id}", file=sys.stderr)

    try:
        data, full = client.poll_task(
            task_id,
            interval=args.interval,
            timeout=args.timeout,
            verbose=not args.quiet,
        )
    except TimeoutError as e:
        if not args.quiet:
            print(f"Poll timeout: {e}", file=sys.stderr)
            print("Resume with: python tv_avatar_video.py query --task-id ...", file=sys.stderr)
        sys.exit(2)
    except GiggleApiError as e:
        print(f"Task failed: {e}", file=sys.stderr)
        sys.exit(1)

    print_completed(data, args, full)


def cmd_submit(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    validate_drive_args(args, parser)
    body = build_submit_body(args)
    client = GiggleClient(base_url=args.base_url) if args.base_url else GiggleClient()
    try:
        task_id = client.submit_tv_avatar(body)
    except GiggleApiError as e:
        print(f"Submit failed: {e}", file=sys.stderr)
        sys.exit(1)
    print(task_id)


def cmd_query(args: argparse.Namespace, _: argparse.ArgumentParser) -> None:
    client = GiggleClient(base_url=args.base_url) if args.base_url else GiggleClient()
    try:
        data, full = client.poll_task(
            args.task_id,
            interval=args.interval,
            timeout=args.timeout,
            verbose=not args.quiet,
        )
    except TimeoutError as e:
        if not args.quiet:
            print(f"Poll timeout: {e}", file=sys.stderr)
            print("Fetching latest snapshot...", file=sys.stderr)
        try:
            data, full = client.query_task(args.task_id)
        except GiggleApiError as err:
            print(f"Query failed: {err}", file=sys.stderr)
            sys.exit(1)
        status = data.get("status", "")
        if args.json:
            print(json_mod.dumps(full, indent=2, ensure_ascii=False))
        else:
            print(f"Status: {status}  task_id: {args.task_id}", file=sys.stderr)
        sys.exit(2)

    except GiggleApiError as e:
        print(f"Task failed: {e}", file=sys.stderr)
        sys.exit(1)

    print_completed(data, args, full)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Photo-driven talking-head video — Giggle wrapped API (submit + poll).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment:
  GIGGLE_API_KEY   Required — sidebar → API Key
  GIGGLE_API_BASE  Optional — defaults to https://giggle.pro

Flow:
  POST .../tv-avatar-video → data.task_id → GET .../task/query?task_id=...
  Poll until data.status == completed; output URL is data.urls[0]
""",
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)

    p_run = sub.add_parser("run", help="Submit and poll to completion (default path)")
    add_submit_args(p_run)
    add_poll_args(p_run)
    add_output_args(p_run)

    p_sub = sub.add_parser("submit", help="Submit only; print task_id")
    add_submit_args(p_sub)
    add_output_args(p_sub)

    p_q = sub.add_parser("query", help="Resume polling by task_id (timeout recovery)")
    p_q.add_argument("--task-id", required=True, help="task_id from submit response")
    add_poll_args(p_q)
    add_output_args(p_q)
    p_q.add_argument("--base-url", default=None, help="Override GIGGLE_API_BASE")

    ns = parser.parse_args()

    if ns.subcommand == "run":
        cmd_run(ns, parser)
    elif ns.subcommand == "submit":
        cmd_submit(ns, parser)
    else:
        cmd_query(ns, parser)


if __name__ == "__main__":
    main()
