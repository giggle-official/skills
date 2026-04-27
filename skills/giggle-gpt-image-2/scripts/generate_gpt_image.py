#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate images using Giggle GPT Image 2 fast.

Supports:
- Text-to-image: calls /api/v1/generation/text-to-image when no reference image is provided
- Image-to-image: calls /api/v1/generation/image-to-image when a reference image is provided

Output:
- stdout: machine-readable result, defaults to fixed-key URL output
- stderr: progress logs and error messages
"""

import argparse
import base64
import os
import sys
import time
from pathlib import Path
from typing import Any, List
from urllib.parse import urlparse

import requests


BASE_URL = "https://giggle.pro"
TEXT_TO_IMAGE_PATH = "/api/v1/generation/text-to-image"
IMAGE_TO_IMAGE_PATH = "/api/v1/generation/image-to-image"
QUERY_TASK_PATH = "/api/v1/generation/task/query"
MODEL_NAME = "gpt-image-2-fast"
VALID_RATIOS = {"auto", "1:1", "9:16", "16:9", "4:3", "3:4"}


def is_remote_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def read_image_as_base64(image_path: str) -> str:
    path = Path(image_path).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"Reference image not found: {path}")
    if not path.is_file():
        raise ValueError(f"Reference image path is not a file: {path}")
    with path.open("rb") as file:
        return base64.b64encode(file.read()).decode("ascii")


def request_json(method: str, path: str, api_key: str, *, payload: Any = None, params: Any = None) -> Any:
    headers = {
        "x-auth": api_key,
        "Content-Type": "application/json",
    }
    response = requests.request(
        method=method,
        url=f"{BASE_URL}{path}",
        headers=headers,
        json=payload,
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    if data.get("code") != 200:
        raise RuntimeError(data.get("msg") or data.get("message") or "Giggle API returned an error")
    return data


def submit_text_to_image(api_key: str, prompt: str, aspect_ratio: str, count: int) -> str:
    payload = {
        "prompt": prompt,
        "generate_count": count,
        "model": MODEL_NAME,
        "aspect_ratio": aspect_ratio,
        "resolution": "2K",
    }
    result = request_json("POST", TEXT_TO_IMAGE_PATH, api_key, payload=payload)
    return result["data"]["task_id"]


def submit_image_to_image(
    api_key: str,
    prompt: str,
    aspect_ratio: str,
    count: int,
    reference_image: str,
) -> str:
    reference: dict[str, str]
    if is_remote_url(reference_image):
        reference = {"url": reference_image}
    else:
        reference = {"base64": read_image_as_base64(reference_image)}

    payload = {
        "prompt": prompt,
        "reference_images": [reference],
        "generate_count": count,
        "model": MODEL_NAME,
        "aspect_ratio": aspect_ratio,
        "watermark": False,
    }
    result = request_json("POST", IMAGE_TO_IMAGE_PATH, api_key, payload=payload)
    return result["data"]["task_id"]


def collect_urls_from_payload(value: Any, found: List[str]) -> None:
    if isinstance(value, dict):
        urls = value.get("urls")
        if isinstance(urls, list):
            for item in urls:
                if isinstance(item, str) and item not in found:
                    found.append(item)

        # Fallback for legacy or undocumented response structures.
        download_url = value.get("download_url")
        if isinstance(download_url, str) and download_url not in found:
            found.append(download_url)

        for nested in value.values():
            collect_urls_from_payload(nested, found)
        return

    if isinstance(value, list):
        for item in value:
            collect_urls_from_payload(item, found)


def extract_result_urls(task_result: Any) -> List[str]:
    found: List[str] = []
    collect_urls_from_payload(task_result, found)
    return found


def poll_task(api_key: str, task_id: str, timeout_seconds: int) -> List[str]:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        time.sleep(5)
        result = request_json("GET", QUERY_TASK_PATH, api_key, params={"task_id": task_id})
        data = result.get("data", {})
        status = data.get("status", "")
        print(f"Task status: {status or 'unknown'}", file=sys.stderr)

        if status == "completed":
            urls = extract_result_urls(result)
            if urls:
                return urls
            raise RuntimeError("Task completed but no data.urls or usable image URL was returned")

        if status in {"failed", "error"}:
            raise RuntimeError(data.get("err_msg") or data.get("msg") or "Generation failed")

    raise TimeoutError(f"Task timed out: did not complete within {timeout_seconds} seconds")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Giggle GPT Image 2 fast image generation script")
    parser.add_argument("--prompt", required=True, help="Final prompt text")
    parser.add_argument(
        "--aspect-ratio",
        default="9:16",
        choices=sorted(VALID_RATIOS),
        help="Image aspect ratio",
    )
    parser.add_argument("--count", type=int, default=1, help="Number of images to generate (1 to 4)")
    parser.add_argument(
        "--reference-image",
        help="Reference image: local file path or remote URL; triggers image-to-image mode when provided",
    )
    parser.add_argument("--timeout", type=int, default=300, help="Maximum wait time in seconds")
    parser.add_argument(
        "--output-format",
        default="kv",
        choices=["kv", "json", "plain"],
        help="stdout output format: kv is best for LLM/script parsing, json for programmatic use, plain for one URL per line",
    )
    return parser.parse_args()


def emit_result(urls: List[str], output_format: str) -> None:
    primary_url = urls[0] if urls else ""

    if output_format == "plain":
        for url in urls:
            print(url)
        return

    if output_format == "json":
        print(
            json.dumps(
                {
                    "success": True,
                    "primary_url": primary_url,
                    "urls": urls,
                    "count": len(urls),
                },
                ensure_ascii=False,
            )
        )
        return

    # Default: kv format with fixed key names for reliable LLM extraction
    print("RESULT_STATUS=success")
    print(f"RESULT_PRIMARY_URL={primary_url}")
    print(f"RESULT_URL_COUNT={len(urls)}")
    for index, url in enumerate(urls, start=1):
        print(f"RESULT_URL_{index}={url}")


def main() -> int:
    args = parse_args()
    api_key = os.environ.get("GIGGLE_API_KEY")
    if not api_key:
        print("Error: GIGGLE_API_KEY environment variable is not set", file=sys.stderr)
        return 1

    if not 1 <= args.count <= 4:
        print("Error: --count must be between 1 and 4", file=sys.stderr)
        return 1

    try:
        if args.reference_image:
            print("Mode: image-to-image", file=sys.stderr)
            task_id = submit_image_to_image(
                api_key=api_key,
                prompt=args.prompt,
                aspect_ratio=args.aspect_ratio,
                count=args.count,
                reference_image=args.reference_image,
            )
        else:
            print("Mode: text-to-image", file=sys.stderr)
            task_id = submit_text_to_image(
                api_key=api_key,
                prompt=args.prompt,
                aspect_ratio=args.aspect_ratio,
                count=args.count,
            )

        print(f"Task submitted: {task_id}", file=sys.stderr)
        urls = poll_task(api_key, task_id, args.timeout)
        emit_result(urls, args.output_format)
        return 0
    except requests.HTTPError as error:
        detail = error.response.text if error.response is not None else str(error)
        print(f"HTTP error: {detail}", file=sys.stderr)
        return 1
    except Exception as error:
        print(f"Generation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
