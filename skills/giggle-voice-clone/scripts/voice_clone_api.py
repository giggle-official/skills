#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
giggle.pro Voice Clone API wrapper script
Flow: Submit voice-clone with file.url directly -> Poll until audio URL is ready
Usage: python voice_clone_api.py --audio-url "https://..." --text "..." --voice-id "my_voice_01"
"""

import os
import sys
import time
import argparse
import requests
from typing import Dict, Any


class TaskStatus:
    COMPLETED = "completed"
    FAILED = "failed"


def to_view_url(url: str) -> str:
    """Normalize URL for user; keep API query params including response-content-disposition=attachment."""
    url = url.replace("~", "%7E")
    return url


class VoiceCloneAPI:
    """giggle.pro Voice Clone API client"""

    BASE_URL = "https://giggle.pro"
    QUERY_ENDPOINT = "/api/v1/generation/task/query"
    VOICE_CLONE_ENDPOINT = "/api/v1/generation/voice-clone"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "x-auth": api_key,
            "Content-Type": "application/json"
        }

    def query_task(self, task_id: str) -> Dict[str, Any]:
        """Query task status"""
        url = f"{self.BASE_URL}{self.QUERY_ENDPOINT}"
        params = {"task_id": task_id}
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            result = response.json()
            if result.get("code") != 200:
                raise Exception(f"Query failed: {result.get('msg', result.get('message', 'Unknown error'))}")
            return result
        except requests.exceptions.RequestException as e:
            raise Exception(f"Query failed: {str(e)}")

    def voice_clone(
        self,
        text: str,
        audio_url: str,
        voice_id: str,
        need_noise_reduction: bool = False,
        need_volumn_normalization: bool = False
    ) -> Dict[str, Any]:
        """Submit voice clone task with file.url directly"""
        payload = {
            "text": text,
            "voice_id": voice_id,
            "need_noise_reduction": need_noise_reduction,
            "need_volumn_normalization": need_volumn_normalization,
            "file": {"url": audio_url}
        }
        url = f"{self.BASE_URL}{self.VOICE_CLONE_ENDPOINT}"
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            if result.get("code") != 200:
                raise Exception(f"Submit failed: {result.get('msg', result.get('message', 'Unknown error'))}")
            return result
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def wait_for_clone_result(
        self,
        task_id: str,
        max_wait: int = 180,
        poll_interval: int = 5
    ) -> Dict[str, Any]:
        """Poll voice clone task until completed or failed"""
        start = time.time()
        while time.time() - start < max_wait:
            result = self.query_task(task_id)
            data = result.get("data", {})
            status = data.get("status", "")

            if status == TaskStatus.COMPLETED:
                return result
            if status == TaskStatus.FAILED:
                return result

            time.sleep(poll_interval)
        raise Exception(f"Voice clone task timed out ({max_wait}s)")


def load_api_key() -> str:
    """Load GIGGLE_API_KEY from system environment"""
    api_key = os.getenv("GIGGLE_API_KEY")
    if not api_key:
        print("Error: GIGGLE_API_KEY not found. Please set system environment variable:", file=sys.stderr)
        print("  export GIGGLE_API_KEY=your_api_key", file=sys.stderr)
        print("  API Key can be obtained at https://giggle.pro/ account settings.", file=sys.stderr)
        sys.exit(1)
    return api_key


def parse_args():
    parser = argparse.ArgumentParser(
        description="giggle.pro Voice Clone - Clone voice from audio URL and synthesize text",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--audio-url", type=str, required=True, help="Public URL of reference audio to clone")
    parser.add_argument("--text", type=str, required=True, help="Text to synthesize with cloned voice")
    parser.add_argument("--voice-id", type=str, required=True, help="User-defined unique voice_id")
    parser.add_argument(
        "--need-noise-reduction",
        type=lambda x: x.lower() in ("true", "1", "yes"),
        default=False,
        help="Apply noise reduction, default false"
    )
    parser.add_argument(
        "--need-volumn-normalization",
        type=lambda x: x.lower() in ("true", "1", "yes"),
        default=False,
        help="Apply volume normalization, default false"
    )
    parser.add_argument("--max-wait", type=int, default=180, help="Max wait seconds for clone task")
    return parser.parse_args()


def main():
    args = parse_args()
    api_key = load_api_key()
    client = VoiceCloneAPI(api_key)

    try:
        print("Submitting voice clone task...", file=sys.stderr)
        clone_result = client.voice_clone(
            text=args.text,
            audio_url=args.audio_url,
            voice_id=args.voice_id,
            need_noise_reduction=args.need_noise_reduction,
            need_volumn_normalization=args.need_volumn_normalization
        )
        clone_task_id = clone_result.get("data", {}).get("task_id")
        if not clone_task_id:
            raise Exception("Clone response missing task_id")

        data = clone_result.get("data", {})
        if data.get("status") == TaskStatus.FAILED:
            err_msg = data.get("err_msg", "Unknown error")
            if "duplicate" in str(err_msg).lower() or "2039" in str(err_msg):
                print("😔 Voice clone issue\n\nvoice_id already exists (duplicate). Please use a different unique voice_id and retry.")
                sys.exit(1)
            raise Exception(f"Clone task failed: {err_msg}")

        if data.get("status") == TaskStatus.COMPLETED and data.get("urls"):
            urls = data.get("urls", [])
            view_urls = [to_view_url(u) for u in urls]
            print("🎙️ Voice clone complete! ✨\n")
            for i, u in enumerate(view_urls):
                print(f"[Listen audio {i+1}]({u})\n" if len(view_urls) > 1 else f"[Listen]({u})\n")
            for u in view_urls:
                print(u)
            print("\nLet me know if you'd like to adjust anything.")
            sys.exit(0)

        print("Waiting for clone to complete...", file=sys.stderr)
        final = client.wait_for_clone_result(
            clone_task_id,
            max_wait=args.max_wait,
            poll_interval=5
        )
        final_data = final.get("data", {})
        status = final_data.get("status", "")

        if status == TaskStatus.FAILED:
            err_msg = final_data.get("err_msg", "Unknown error")
            if "duplicate" in str(err_msg).lower() or "2039" in str(err_msg):
                print("😔 Voice clone issue\n\nvoice_id already exists (duplicate). Please use a different unique voice_id and retry.")
                sys.exit(1)
            print(f"😔 Voice clone failed: {err_msg}")
            sys.exit(1)

        if status == TaskStatus.COMPLETED:
            urls = final_data.get("urls", [])
            if not urls:
                print("Clone completed but no audio URLs returned. Please retry.")
                sys.exit(1)
            view_urls = [to_view_url(u) for u in urls]
            print("🎙️ Voice clone complete! ✨\n")
            for i, u in enumerate(view_urls):
                line = f"[Listen audio {i+1}]({u})\n" if len(view_urls) > 1 else f"[Listen]({u})\n"
                print(line)
            for u in view_urls:
                print(u)
            print("\nLet me know if you'd like to adjust anything.")
            sys.exit(0)

        raise Exception(f"Unknown status: {status}")

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
