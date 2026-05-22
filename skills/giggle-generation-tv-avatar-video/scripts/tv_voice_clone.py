#!/usr/bin/env python3
"""TV voice clone (wrapped Giggle generation API).

Flow:
  POST /api/v1/generation/tv-voice-clone → data.task_id
  GET  /api/v1/generation/task/query?task_id=... (poll up to 5 minutes)

Success:
  data.status == "completed" and data.voice_id is non-empty
"""

from __future__ import annotations

import argparse
import json as json_mod
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))

from shared.client import GiggleApiError, GiggleClient

DEFAULT_TIMEOUT = 300
DEFAULT_INTERVAL = 5

TTS_SCRIPT_MAX_CHARS = 2700
_BREAK_TAG_RE = re.compile(r'<break\s+time="([^"]+)"\s*/>', re.IGNORECASE)
_BREAK_NUM_PART = re.compile(r"^(\d+(?:\.\d)?)$")


def _normalize_url(value: str) -> str:
    return value.strip().strip("`").strip()


def validate_tts_script_content(text: str, parser: argparse.ArgumentParser) -> None:
    if not text:
        parser.error("requires non-empty --tts-script")
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
    body: dict = {
        "tts_script": args.tts_script.strip(),
        "clone_audio": {"url": _normalize_url(args.clone_audio_url)},
    }
    if args.voice_speed is not None:
        body["voice_speed"] = args.voice_speed
    return body


def add_submit_args(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--tts-script",
        required=True,
        help=f"TTS copy; non-empty; max {TTS_SCRIPT_MAX_CHARS} chars",
    )
    p.add_argument(
        "--clone-audio-url",
        required=True,
        help="Reference audio URL mapped to body clone_audio.url",
    )
    p.add_argument(
        "--voice-speed",
        type=float,
        default=1.0,
        help="Speech rate (default 1.0)",
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
    p.add_argument("--json", action="store_true", help="Print last query response JSON in full")
    p.add_argument("-q", "--quiet", action="store_true", help="Suppress progress output")


def _print_completed(data: dict, args: argparse.Namespace, full_json: dict | None) -> None:
    if args.json and full_json is not None:
        print(json_mod.dumps(full_json, indent=2, ensure_ascii=False))
        return
    print(str(data.get("voice_id") or "").strip())


def cmd_run(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    validate_tts_script_content(args.tts_script.strip(), parser)
    body = build_submit_body(args)
    client = GiggleClient(base_url=args.base_url) if args.base_url else GiggleClient()

    if not args.quiet:
        print("Submitting voice-clone job...", file=sys.stderr)
    try:
        task_id = client.submit_tv_voice_clone(body)
    except GiggleApiError as e:
        print(f"Submit failed: {e}", file=sys.stderr)
        sys.exit(1)

    if not args.quiet:
        print(f"Submitted. task_id: {task_id}", file=sys.stderr)

    try:
        data, full = client.poll_task_for_voice_clone(
            task_id,
            interval=args.interval,
            timeout=args.timeout,
            verbose=not args.quiet,
        )
    except TimeoutError as e:
        if not args.quiet:
            print(f"Poll timeout: {e}", file=sys.stderr)
            print("Resume with: python tv_voice_clone.py query --task-id ...", file=sys.stderr)
        sys.exit(2)
    except GiggleApiError as e:
        print(f"Task failed: {e}", file=sys.stderr)
        sys.exit(1)

    _print_completed(data, args, full)


def cmd_submit(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    validate_tts_script_content(args.tts_script.strip(), parser)
    body = build_submit_body(args)
    client = GiggleClient(base_url=args.base_url) if args.base_url else GiggleClient()
    try:
        task_id = client.submit_tv_voice_clone(body)
    except GiggleApiError as e:
        print(f"Submit failed: {e}", file=sys.stderr)
        sys.exit(1)
    print(task_id)


def cmd_query(args: argparse.Namespace, _: argparse.ArgumentParser) -> None:
    client = GiggleClient(base_url=args.base_url) if args.base_url else GiggleClient()
    try:
        data, full = client.poll_task_for_voice_clone(
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
        voice_id = data.get("voice_id", "")
        if args.json:
            print(json_mod.dumps(full, indent=2, ensure_ascii=False))
        else:
            print(f"Status: {status}  voice_id: {voice_id}  task_id: {args.task_id}", file=sys.stderr)
        sys.exit(2)
    except GiggleApiError as e:
        print(f"Task failed: {e}", file=sys.stderr)
        sys.exit(1)

    _print_completed(data, args, full)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="TV voice clone — Giggle wrapped API (submit + poll).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment:
  GIGGLE_API_KEY   Required — sidebar → API Key
  GIGGLE_API_BASE  Optional — defaults to https://giggle.pro
""",
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)

    p_run = sub.add_parser("run", help="Submit and poll to completion")
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
