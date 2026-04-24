#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调用 Giggle GPT Image 2 fast 生成图片。

支持：
- 文生图：无参考图时调用 /api/v1/generation/text-to-image
- 图生图：有参考图时调用 /api/v1/generation/image-to-image

输出：
- stdout: 机器可读结果，默认输出带固定键名的 URL
- stderr: 进度日志与错误信息
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
        raise FileNotFoundError(f"参考图不存在: {path}")
    if not path.is_file():
        raise ValueError(f"参考图不是文件: {path}")
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
        raise RuntimeError(data.get("msg") or data.get("message") or "Giggle API 返回错误")
    return data


def submit_text_to_image(api_key: str, prompt: str, aspect_ratio: str, count: int) -> str:
    payload = {
        "prompt": prompt,
        "generate_count": count,
        "model": MODEL_NAME,
        "aspect_ratio": aspect_ratio,
        "resolution": "1K",
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

        # 兼容历史或非文档化返回结构。
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
        print(f"任务状态: {status or 'unknown'}", file=sys.stderr)

        if status == "completed":
            urls = extract_result_urls(result)
            if urls:
                return urls
            raise RuntimeError("任务已完成，但未返回 data.urls 或可用图片 URL")

        if status in {"failed", "error"}:
            raise RuntimeError(data.get("err_msg") or data.get("msg") or "生成失败")

    raise TimeoutError(f"任务超时，{timeout_seconds} 秒内未完成")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Giggle GPT Image 2 fast 图片生成脚本")
    parser.add_argument("--prompt", required=True, help="最终提示词")
    parser.add_argument(
        "--aspect-ratio",
        default="9:16",
        choices=sorted(VALID_RATIOS),
        help="图片比例",
    )
    parser.add_argument("--count", type=int, default=1, help="生成数量，1 到 4")
    parser.add_argument(
        "--reference-image",
        help="参考图，本地路径或远程 URL；提供后自动走图生图",
    )
    parser.add_argument("--timeout", type=int, default=300, help="最长等待秒数")
    parser.add_argument(
        "--output-format",
        default="kv",
        choices=["kv", "json", "plain"],
        help="stdout 输出格式：kv 最适合 LLM/脚本提取，json 适合程序消费，plain 为每行一个 URL",
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

    print("RESULT_STATUS=success")
    print(f"RESULT_PRIMARY_URL={primary_url}")
    print(f"RESULT_URL_COUNT={len(urls)}")
    for index, url in enumerate(urls, start=1):
        print(f"RESULT_URL_{index}={url}")


def main() -> int:
    args = parse_args()
    api_key = os.environ.get("GIGGLE_API_KEY")
    if not api_key:
        print("错误: 未设置 GIGGLE_API_KEY 环境变量", file=sys.stderr)
        return 1

    if not 1 <= args.count <= 4:
        print("错误: --count 只能在 1 到 4 之间", file=sys.stderr)
        return 1

    try:
        if args.reference_image:
            print("模式: 图生图", file=sys.stderr)
            task_id = submit_image_to_image(
                api_key=api_key,
                prompt=args.prompt,
                aspect_ratio=args.aspect_ratio,
                count=args.count,
                reference_image=args.reference_image,
            )
        else:
            print("模式: 文生图", file=sys.stderr)
            task_id = submit_text_to_image(
                api_key=api_key,
                prompt=args.prompt,
                aspect_ratio=args.aspect_ratio,
                count=args.count,
            )

        print(f"任务已提交: {task_id}", file=sys.stderr)
        urls = poll_task(api_key, task_id, args.timeout)
        emit_result(urls, args.output_format)
        return 0
    except requests.HTTPError as error:
        detail = error.response.text if error.response is not None else str(error)
        print(f"HTTP 错误: {detail}", file=sys.stderr)
        return 1
    except Exception as error:
        print(f"生成失败: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
