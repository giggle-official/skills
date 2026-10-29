#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HopsAPI MiniMax-H3 媒体任务封装（storyclaw-token-gateway /v1/router）

支持：
  - Txt2Video  文生视频
  - Img2Video  图生 / 首尾帧（images 1 或 2 个公网 URL）
  - OmniVideo  全能参考（images ≤9 / videos ≤3 / audios ≤3）

鉴权：Authorization: Bearer <HOPSAPI_API_KEY> 或 x-api-key
文档：apps/docs/content/docs/media/(video-models)/minimax-h3*.mdx
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional

import requests

SUPPORTED_MODEL = "MiniMax-H3"
SUPPORTED_TASKS = ("Txt2Video", "Img2Video", "OmniVideo")
SUPPORTED_RESOLUTIONS = ("480p", "768p")
SUPPORTED_RATIOS = ("16:9", "9:16", "1:1", "4:3", "3:4", "21:9", "auto")
SUPPORTED_DURATIONS = list(range(4, 16))  # 4–15
DEFAULT_DURATION = 5
DEFAULT_RESOLUTION = "768p"
MAX_IMAGES = 9
MAX_VIDEOS = 3
MAX_AUDIOS = 3

DEFAULT_BASE_URL = "https://hopsapi.com/v1"
DEFAULT_CONSOLE_URL = "https://hopsapi.com"
KEY_FILE = os.path.expanduser("~/.hopsapi_api_key")

STATUS_QUEUED = 0
STATUS_PROCESSING = 1
STATUS_DONE = 2
STATUS_FAILED = 3
STATUS_CANCELLED = 4


# ---------------------------------------------------------------------------
# API Key
# ---------------------------------------------------------------------------

def _detect_shell_rc() -> str:
    shell = os.environ.get("SHELL", "")
    home = os.path.expanduser("~")
    if "zsh" in shell:
        return os.path.join(home, ".zshrc")
    if "bash" in shell:
        rc = os.path.join(home, ".bash_profile")
        return rc if os.path.exists(rc) else os.path.join(home, ".bashrc")
    return os.path.join(home, ".profile")


def setup_api_key(api_key: str) -> None:
    with open(KEY_FILE, "w", encoding="utf-8") as f:
        f.write(api_key.strip())
    os.chmod(KEY_FILE, 0o600)

    rc_path = _detect_shell_rc()
    export_line = f'export HOPSAPI_API_KEY="{api_key.strip()}"'
    marker = "HOPSAPI_API_KEY="
    lines: List[str] = []
    if os.path.exists(rc_path):
        with open(rc_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    updated = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(f"export {marker}") or stripped.startswith(marker):
            lines[i] = export_line + "\n"
            updated = True
            break
    if not updated:
        if lines and not lines[-1].endswith("\n"):
            lines.append("\n")
        lines.append(f"\n# HopsAPI MiniMax-H3 API Key\n{export_line}\n")
    with open(rc_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    os.environ["HOPSAPI_API_KEY"] = api_key.strip()
    print("✓ API Key 已永久保存（配置一次，永久有效）")
    print(f"  保存位置: {KEY_FILE}  |  {rc_path}")


def check_api_key() -> Optional[str]:
    key = os.environ.get("HOPSAPI_API_KEY")
    if key:
        return key.strip()
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r", encoding="utf-8") as f:
            key = f.read().strip()
        if key:
            os.environ["HOPSAPI_API_KEY"] = key
            return key
    return None


def base_url() -> str:
    return (os.environ.get("HOPSAPI_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")


def console_url() -> str:
    return (os.environ.get("HOPSAPI_CONSOLE_URL") or DEFAULT_CONSOLE_URL).rstrip("/")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def strip_media_ref(value: str) -> str:
    """接受纯 URL，或兼容 url:<URL> / base64:（base64 须先上传，这里直接拒绝）。"""
    s = value.strip()
    if not s:
        raise ValueError("素材引用不能为空")
    if s.startswith("base64:"):
        raise ValueError(
            "MiniMax-H3 网关只接受公网 URL。请先用 --upload-file / --upload-url "
            "转成 fileUrl，再传入。"
        )
    if s.startswith("url:"):
        s = s[4:].strip()
    if not (s.startswith("http://") or s.startswith("https://")):
        raise ValueError(f"素材必须是 http(s) URL，当前: {value!r}")
    return s


def extract_video_urls(payload: Dict[str, Any]) -> List[str]:
    """兼容 result.content.video_url 与 results[].urls 两种终态形态。"""
    urls: List[str] = []
    result = payload.get("result")
    if isinstance(result, dict):
        content = result.get("content")
        if isinstance(content, dict):
            vu = content.get("video_url")
            if isinstance(vu, str) and vu.strip():
                urls.append(vu.strip())
        nested = result.get("urls")
        if isinstance(nested, list):
            urls.extend(u for u in nested if isinstance(u, str) and u.strip())
    results = payload.get("results")
    if isinstance(results, list):
        for item in results:
            if not isinstance(item, dict):
                continue
            for u in item.get("urls") or []:
                if isinstance(u, str) and u.strip():
                    urls.append(u.strip())
    # 去重保序
    seen = set()
    out: List[str] = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

class MinimaxH3Client:
    def __init__(self, api_key: str, api_base: Optional[str] = None, console: Optional[str] = None):
        self.api_key = api_key
        self.api_base = (api_base or base_url()).rstrip("/")
        self.console = (console or console_url()).rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    def _raise_http(self, resp: requests.Response) -> Dict[str, Any]:
        try:
            data = resp.json()
        except Exception:
            raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:500]}") from None
        if resp.status_code >= 400:
            msg = data.get("message") or data.get("msg") or resp.text[:500]
            raise RuntimeError(f"HTTP {resp.status_code}: {msg}")
        return data if isinstance(data, dict) else {"data": data}

    def create_task(self, body: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.api_base}/router/task/create"
        resp = self.session.post(url, json=body, timeout=60)
        return self._raise_http(resp)

    def query_task(self, task_id: str) -> Dict[str, Any]:
        url = f"{self.api_base}/router/tasks/{task_id}"
        resp = self.session.get(url, timeout=30)
        return self._raise_http(resp)

    def stop_task(self, task_id: str) -> Dict[str, Any]:
        url = f"{self.api_base}/router/task/stop"
        resp = self.session.post(url, json={"task_id": task_id}, timeout=30)
        return self._raise_http(resp)

    def upload_from_url(self, file_url: str, upload_path: str = "videos",
                        file_name: Optional[str] = None) -> str:
        url = f"{self.console}/api/file-url-upload"
        payload: Dict[str, Any] = {"fileUrl": file_url, "uploadPath": upload_path}
        if file_name:
            payload["fileName"] = file_name
        resp = self.session.post(url, json=payload, timeout=120)
        data = self._raise_http(resp)
        file_url_out = (data.get("data") or {}).get("fileUrl")
        if not file_url_out:
            raise RuntimeError(f"上传成功但未返回 fileUrl: {data}")
        return str(file_url_out)

    def upload_file(self, path: str, upload_path: str = "videos") -> str:
        url = f"{self.console}/api/file-stream-upload"
        name = os.path.basename(path)
        with open(path, "rb") as f:
            files = {"file": (name, f)}
            data = {"uploadPath": upload_path, "fileName": name}
            # multipart 时不要带 Content-Type: application/json
            headers = {"Authorization": f"Bearer {self.api_key}"}
            resp = requests.post(url, headers=headers, files=files, data=data, timeout=180)
        body = self._raise_http(resp)
        file_url_out = (body.get("data") or {}).get("fileUrl")
        if not file_url_out:
            raise RuntimeError(f"上传成功但未返回 fileUrl: {body}")
        return str(file_url_out)


def build_body(
    *,
    mode: str,
    prompt: Optional[str],
    images: Optional[List[str]],
    videos: Optional[List[str]],
    audios: Optional[List[str]],
    duration: int,
    resolution: str,
    aspect_ratio: Optional[str],
    generate_audio: Optional[bool],
    callback_url: Optional[str],
) -> Dict[str, Any]:
    if duration not in SUPPORTED_DURATIONS:
        raise ValueError(f"duration 须为 4–15 整数，当前: {duration}")
    if resolution not in SUPPORTED_RESOLUTIONS:
        raise ValueError(f"resolution 仅支持 {SUPPORTED_RESOLUTIONS}，当前: {resolution}")

    imgs = [strip_media_ref(x) for x in (images or [])]
    vids = [strip_media_ref(x) for x in (videos or [])]
    auds = [strip_media_ref(x) for x in (audios or [])]

    if mode == "text":
        task = "Txt2Video"
        if not prompt or not prompt.strip():
            raise ValueError("文生视频需要非空 --prompt")
        if imgs or vids or auds:
            raise ValueError("文生视频不要传 images/videos/audios")
    elif mode == "image":
        task = "Img2Video"
        if len(imgs) not in (1, 2):
            raise ValueError("图生/首尾帧需要 1 或 2 个 --images（首帧[,尾帧]）")
        if vids or auds:
            raise ValueError("Img2Video 不要传 videos/audios")
    elif mode == "omni":
        task = "OmniVideo"
        if not (imgs or vids or auds):
            raise ValueError("OmniVideo 至少需要 images / videos / audios 之一")
        if len(imgs) > MAX_IMAGES:
            raise ValueError(f"images 最多 {MAX_IMAGES} 张")
        if len(vids) > MAX_VIDEOS:
            raise ValueError(f"videos 最多 {MAX_VIDEOS} 个")
        if len(auds) > MAX_AUDIOS:
            raise ValueError(f"audios 最多 {MAX_AUDIOS} 个")
    else:
        raise ValueError(f"未知 mode: {mode}")

    inp: Dict[str, Any] = {
        "duration": duration,
        "resolution": resolution,
    }
    if prompt is not None and prompt.strip():
        inp["prompt"] = prompt.strip()
    if imgs:
        inp["images"] = imgs
    if vids:
        inp["videos"] = vids
    if auds:
        inp["audios"] = auds
    if aspect_ratio:
        if aspect_ratio not in SUPPORTED_RATIOS:
            raise ValueError(f"aspect_ratio 须为 {SUPPORTED_RATIOS}")
        inp["aspect_ratio"] = aspect_ratio
    if generate_audio is not None:
        inp["generate_audio"] = bool(generate_audio)

    body: Dict[str, Any] = {
        "task": task,
        "model": SUPPORTED_MODEL,
        "input": inp,
    }
    if callback_url:
        body["callback_url"] = callback_url
    return body


def _print_completed(payload: Dict[str, Any]) -> None:
    urls = extract_video_urls(payload)
    cost = payload.get("cost")
    print("视频已就绪！🎬\n")
    if cost is not None:
        print(f"本次费用（账户积分）: {cost}\n")
    if not urls:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        print("\n生成完成，但未解析到视频 URL，请检查上方原始响应。")
        return
    print(f"共 {len(urls)} 个视频 ✨\n")
    for i, u in enumerate(urls):
        print(f"[查看视频 {i + 1}]({u})")
    print("\n⚠️  媒体 URL 可能过期，请及时查看或下载。")


def handle_query(client: MinimaxH3Client, task_id: str) -> None:
    data = client.query_task(task_id)
    status = data.get("status")
    if status == STATUS_DONE:
        _print_completed(data)
        return
    if status in (STATUS_FAILED, STATUS_CANCELLED) or data.get("code") == 424:
        reason = data.get("fail_reason") or data.get("message") or data.get("msg") or "未知错误"
        print(f"任务失败/取消：{reason}\n\n（失败不扣费）")
        return
    print(json.dumps({
        "status": status,
        "task_id": data.get("task_id", task_id),
        "hint": {0: "queued", 1: "processing"}.get(status, "unknown"),
    }, ensure_ascii=False))


def handle_wait(client: MinimaxH3Client, task_id: str,
                interval: int = 4, timeout: int = 900) -> None:
    elapsed = 0
    print(
        f"轮询中 task_id={task_id}（每 {interval}s，最长 {timeout}s）...",
        file=sys.stderr,
    )
    while elapsed < timeout:
        try:
            data = client.query_task(task_id)
        except Exception as e:
            print(f"查询异常: {e}，{interval}s 后重试...", file=sys.stderr)
            time.sleep(interval)
            elapsed += interval
            continue
        status = data.get("status")
        if status == STATUS_DONE:
            _print_completed(data)
            return
        if status in (STATUS_FAILED, STATUS_CANCELLED) or data.get("code") == 424:
            reason = data.get("fail_reason") or data.get("message") or "未知错误"
            print(f"任务失败/取消：{reason}\n\n（失败不扣费）")
            return
        print(f"  [{elapsed}s] status={status}，继续等待...", file=sys.stderr)
        time.sleep(interval)
        elapsed += interval
    print(
        f"超时（已等待 {timeout}s）。可稍后：\n"
        f"  python3 generation_api.py --query --task-id {task_id}"
    )


def handle_submit(client: MinimaxH3Client, args: argparse.Namespace) -> None:
    images = list(args.images or [])
    # 兼容 --start-frame / --end-frame → images[首,尾]
    if args.start_frame or args.end_frame:
        if args.mode != "image":
            raise ValueError("--start-frame/--end-frame 仅用于 --mode image")
        if images:
            raise ValueError("请勿同时使用 --images 与 --start-frame/--end-frame")
        if not args.start_frame:
            raise ValueError("图生至少需要 --start-frame（或 --images）")
        images = [args.start_frame]
        if args.end_frame:
            images.append(args.end_frame)

    body = build_body(
        mode=args.mode,
        prompt=args.prompt,
        images=images or None,
        videos=list(args.videos) if args.videos else None,
        audios=list(args.audios) if args.audios else None,
        duration=args.duration,
        resolution=args.resolution,
        aspect_ratio=args.aspect_ratio,
        generate_audio=args.generate_audio,
        callback_url=args.callback_url,
    )
    print(
        f"提交任务 [task={body['task']} | model={SUPPORTED_MODEL} | "
        f"{args.duration}s | {args.resolution}]...",
        file=sys.stderr,
    )
    result = client.create_task(body)
    task_id = result.get("task_id") or (result.get("data") or {}).get("task_id")
    if not task_id:
        raise RuntimeError(f"创建成功但未返回 task_id: {result}")
    print(f"✓ 任务已提交！task_id: {task_id}", file=sys.stderr)
    print(json.dumps({"status": "started", "task_id": task_id}, ensure_ascii=False))
    if args.no_wait:
        return
    print("\n正在用 MiniMax-H3 生成，完成后主动通知你...", file=sys.stderr)
    handle_wait(client, str(task_id), interval=args.poll_interval, timeout=args.timeout)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="generation_api.py",
        description="HopsAPI MiniMax-H3 视频生成（/v1/router）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 generation_api.py --setup --api-key sk_your_key
  python3 generation_api.py --check-key

  # 文生
  python3 generation_api.py --mode text --prompt "电影感山间日出" --duration 5

  # 图生
  python3 generation_api.py --mode image --prompt "云层缓缓流动" \\
    --images "https://assets.example.com/a.png" --resolution 480p

  # 首尾帧
  python3 generation_api.py --mode image --prompt "从清晨过渡到黄昏" \\
    --start-frame "https://.../first.png" --end-frame "https://.../last.png"

  # 全能参考
  python3 generation_api.py --mode omni --prompt "保持人物外观，沿用运镜" \\
    --images "https://.../char.png" --videos "https://.../motion.mp4"

  python3 generation_api.py --query --task-id tsk_xxx
  python3 generation_api.py --wait --task-id tsk_xxx
        """,
    )
    p.add_argument("--setup", action="store_true", help="永久保存 API Key")
    p.add_argument("--check-key", action="store_true", help="检查 Key 是否已配置")
    p.add_argument("--query", action="store_true", help="单次查询任务")
    p.add_argument("--wait", action="store_true", help="轮询直到终态")
    p.add_argument("--stop", action="store_true", help="停止排队/处理中任务")
    p.add_argument("--task-id", type=str, metavar="ID")
    p.add_argument("--api-key", type=str, help="API Key（优先于环境变量）")
    p.add_argument("--base-url", type=str, help="覆盖 HOPSAPI_BASE_URL，默认 https://hopsapi.com/v1")
    p.add_argument("--console-url", type=str, help="覆盖控制台根地址（文件上传用）")

    p.add_argument("--mode", choices=["text", "image", "omni"])
    p.add_argument("--prompt", type=str)
    p.add_argument("--model", type=str, default=SUPPORTED_MODEL,
                   help="固定 MiniMax-H3，传入其他值会被拒绝")
    p.add_argument("--duration", type=int, default=DEFAULT_DURATION,
                   help="4–15 秒，默认 5")
    p.add_argument("--resolution", type=str, default=DEFAULT_RESOLUTION,
                   choices=list(SUPPORTED_RESOLUTIONS))
    p.add_argument("--aspect-ratio", type=str, default=None,
                   choices=list(SUPPORTED_RATIOS),
                   help="省略则不传给上游")
    p.add_argument("--generate-audio", dest="generate_audio", action="store_true",
                   default=None, help="显式 true（默认上游亦为 true）")
    p.add_argument("--no-generate-audio", dest="generate_audio", action="store_false",
                   help="显式 false")
    p.add_argument("--callback-url", type=str, default=None)

    p.add_argument("--images", type=str, action="extend", nargs="+",
                   help="公网图片 URL；image 模式 1–2 张；omni ≤9")
    p.add_argument("--videos", type=str, action="extend", nargs="+",
                   help="公网视频 URL；仅 omni，≤3；勿传 video_durations")
    p.add_argument("--audios", type=str, action="extend", nargs="+",
                   help="公网音频 URL；仅 omni，≤3，不计费")
    p.add_argument("--start-frame", type=str, help="首帧 URL（image 模式）")
    p.add_argument("--end-frame", type=str, help="尾帧 URL（image 模式）")

    p.add_argument("--upload-url", type=str, help="把远程 URL 转存为平台临时 fileUrl")
    p.add_argument("--upload-file", type=str, help="本地文件流上传，返回 fileUrl")
    p.add_argument("--upload-path", type=str, default="videos", help="上传逻辑目录")

    p.add_argument("--no-wait", action="store_true", help="只提交不轮询")
    p.add_argument("--poll-interval", type=int, default=4, help="轮询间隔秒，默认 4")
    p.add_argument("--timeout", type=int, default=900, help="最长等待秒，默认 900")
    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.setup:
        if not args.api_key:
            print("错误: --setup 需要 --api-key sk_你的密钥", file=sys.stderr)
            print("在 hopsapi.com 控制台 → API Keys → 创建并授权 MiniMax-H3", file=sys.stderr)
            sys.exit(1)
        setup_api_key(args.api_key)
        return

    if args.check_key:
        key = check_api_key()
        if key:
            masked = key[:8] + "..." + key[-4:] if len(key) > 12 else "***"
            print(json.dumps({"status": "ok", "message": f"HOPSAPI_API_KEY 已配置: {masked}"},
                             ensure_ascii=False))
        else:
            print(json.dumps({
                "status": "missing",
                "message": (
                    "未找到 HOPSAPI_API_KEY。请：\n"
                    "1. 打开 hopsapi.com 控制台 → API Keys → 创建 Key 并勾选 MiniMax-H3\n"
                    "2. python3 generation_api.py --setup --api-key sk_你的密钥"
                ),
            }, ensure_ascii=False))
        return

    api_key = args.api_key or check_api_key()
    if not api_key:
        print(
            "错误: 未配置 HOPSAPI_API_KEY\n"
            "  python3 generation_api.py --setup --api-key sk_你的密钥",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.model and args.model != SUPPORTED_MODEL:
        print(f"错误: 本 skill 仅支持模型 {SUPPORTED_MODEL}，收到: {args.model}", file=sys.stderr)
        sys.exit(1)

    client = MinimaxH3Client(
        api_key,
        api_base=args.base_url or base_url(),
        console=args.console_url or console_url(),
    )

    if args.upload_url:
        try:
            out = client.upload_from_url(args.upload_url, upload_path=args.upload_path)
            print(json.dumps({"status": "ok", "fileUrl": out}, ensure_ascii=False))
        except Exception as e:
            print(f"上传失败: {e}", file=sys.stderr)
            sys.exit(1)
        return

    if args.upload_file:
        try:
            out = client.upload_file(args.upload_file, upload_path=args.upload_path)
            print(json.dumps({"status": "ok", "fileUrl": out}, ensure_ascii=False))
        except Exception as e:
            print(f"上传失败: {e}", file=sys.stderr)
            sys.exit(1)
        return

    if args.query:
        if not args.task_id:
            print("错误: --query 需要 --task-id", file=sys.stderr)
            sys.exit(1)
        try:
            handle_query(client, args.task_id)
        except Exception as e:
            print(f"查询失败: {e}", file=sys.stderr)
            sys.exit(1)
        return

    if args.wait:
        if not args.task_id:
            print("错误: --wait 需要 --task-id", file=sys.stderr)
            sys.exit(1)
        try:
            handle_wait(client, args.task_id, interval=args.poll_interval, timeout=args.timeout)
        except Exception as e:
            print(f"轮询失败: {e}", file=sys.stderr)
            sys.exit(1)
        return

    if args.stop:
        if not args.task_id:
            print("错误: --stop 需要 --task-id", file=sys.stderr)
            sys.exit(1)
        try:
            print(json.dumps(client.stop_task(args.task_id), ensure_ascii=False))
        except Exception as e:
            print(f"停止失败: {e}", file=sys.stderr)
            sys.exit(1)
        return

    if not args.mode:
        print("错误: 需要 --mode text|image|omni", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(1)

    try:
        handle_submit(client, args)
    except Exception as e:
        print(f"生成失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
