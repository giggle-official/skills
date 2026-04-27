#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Product poster generation script.
Submits image-to-image task, polls until complete, prints plain URL to stdout.

Usage:
  python generate_poster.py \
    --image /path/to/product.jpg \
    --prompt "E-commerce poster for ..." \
    --model nano-banana-2 \
    --aspect-ratio 3:4

Output (stdout): plain URL, one per line
Errors (stderr): status messages
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

import requests


BASE_URL = "https://giggle.pro"


def to_view_url(url: str) -> str:
    url = url.replace("&response-content-disposition=attachment", "")
    url = url.replace("?response-content-disposition=attachment&", "?")
    url = url.replace("?response-content-disposition=attachment", "")
    url = url.replace("~", "%7E")
    return url


def submit(api_key, img_b64, prompt, model, aspect_ratio, generate_count):
    headers = {"x-auth": api_key, "Content-Type": "application/json"}
    payload = {
        "prompt": prompt,
        "reference_images": [{"base64": img_b64}],
        "model": model,
        "aspect_ratio": aspect_ratio,
        "generate_count": generate_count,
        "watermark": False,
    }
    resp = requests.post(f"{BASE_URL}/api/v1/generation/image-to-image",
                         headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 200:
        raise RuntimeError(data.get("msg", "submit failed"))
    return data["data"]["task_id"]


def poll(api_key, task_id, interval=5, max_wait=180):
    headers = {"x-auth": api_key, "Content-Type": "application/json"}
    elapsed = 0
    while elapsed < max_wait:
        time.sleep(interval)
        elapsed += interval
        resp = requests.get(f"{BASE_URL}/api/v1/generation/task/query",
                            headers=headers, params={"task_id": task_id}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 200:
            raise RuntimeError(data.get("msg", "query failed"))
        result = data["data"]
        status = result.get("status", "")
        print(f"[{elapsed}s] status={status}", file=sys.stderr)
        if status == "completed":
            return result.get("urls", [])
        if status in ("failed", "error"):
            raise RuntimeError(result.get("err_msg", "generation failed"))
    raise TimeoutError(f"task did not complete within {max_wait}s")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, help="Local product image path")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--model", default="nano-banana-2",
                        choices=["nano-banana-2", "nano-banana-2-fast", "seedream45", "midjourney"])
    parser.add_argument("--aspect-ratio", default="3:4",
                        choices=["1:1", "3:4", "4:3", "16:9", "9:16", "2:3", "3:2", "21:9"])
    parser.add_argument("--count", type=int, default=1)
    args = parser.parse_args()

    api_key = os.environ.get("GIGGLE_API_KEY")
    if not api_key:
        print("Error: GIGGLE_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    image_path = Path(args.image).expanduser()
    if not image_path.exists():
        print(f"Error: image not found: {image_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Reading image: {image_path}", file=sys.stderr)
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    print("Submitting task...", file=sys.stderr)
    task_id = submit(api_key, img_b64, args.prompt, args.model, args.aspect_ratio, args.count)
    print(f"Task ID: {task_id}", file=sys.stderr)

    print("Polling for result...", file=sys.stderr)
    urls = poll(api_key, task_id)

    if not urls:
        print("Error: no URLs returned", file=sys.stderr)
        sys.exit(1)

    # Output plain URLs to stdout — one per line, no markdown, no formatting
    for url in urls:
        print(to_view_url(url))


if __name__ == "__main__":
    main()
