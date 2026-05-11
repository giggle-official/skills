#!/usr/bin/env python3
"""照片驱动数字人口播视频（封装生成 API）。

## Agent 必读
- 默认使用 `run`：提交后自动轮询直至完成。
- `run` 超时且已有 task_id 时，用 `query --task-id` 续查；须持续轮询至终态。
- 勿将未完成任务的 task_id 当作最终结果交给用户。

三种驱动（互斥，详见 references/tv_avatar_video.md）：
  A  TTS + voice_over_id（drive_mode=1）
  B  TTS + clone_audio.url（drive_mode=1，勿填 voice_over_id）
  C  drive_audio.url（drive_mode=2）

用法示例：
    python tv_avatar_video.py run --image-url https://... \\
      --tts-script "你好" --voice-over-id <id>

    python tv_avatar_video.py run --image-url https://... \\
      --tts-script "你好" --clone-audio-url https://... --voice-speed 1

    python tv_avatar_video.py run --image-url https://... \\
      --drive-audio-url https://...

    python tv_avatar_video.py query --task-id <uuid>
"""

from __future__ import annotations

import argparse
import json as json_mod
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from shared.client import GiggleApiError, GiggleClient

DEFAULT_TIMEOUT = 600
DEFAULT_INTERVAL = 5


def build_submit_body(args: argparse.Namespace) -> dict:
    """构造 POST /api/v1/generation/tv-avatar-video 的请求体。"""
    body: dict = {
        "image": {"url": args.image_url.strip()},
        "mode_type": str(args.mode_type),
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
    """校验三种驱动互斥且必填齐全。"""
    has_tts = bool(args.tts_script)
    has_voice = bool(args.voice_over_id)
    has_clone = bool(args.clone_audio_url)
    has_drive_audio = bool(args.drive_audio_url)

    if has_drive_audio:
        if has_tts or has_voice or has_clone:
            parser.error("音频驱动（--drive-audio-url）不能与 --tts-script / --voice-over-id / --clone-audio-url 同时使用")
        return

    if has_clone:
        if not has_tts:
            parser.error("使用 --clone-audio-url 时必须提供 --tts-script")
        if has_voice:
            parser.error("使用 --clone-audio-url 时不要填写 --voice-over-id")
        return

    if has_voice:
        if not has_tts:
            parser.error("使用 --voice-over-id 时必须提供 --tts-script")
        return

    parser.error(
        "请指定一种驱动："
        "（1）--tts-script + --voice-over-id；"
        "（2）--tts-script + --clone-audio-url；"
        "（3）--drive-audio-url"
    )


def add_submit_args(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--image-url",
        required=True,
        help="人像图片公网可访问 URL（对应请求体 image.url）",
    )
    p.add_argument(
        "--mode-type",
        default="1",
        help='画质/模式枚举，默认 "1"（与网关约定一致）',
    )
    p.add_argument("--tts-script", default=None, help="TTS 口播文案（drive_mode=1 时必填其一组合）")
    p.add_argument("--voice-over-id", default=None, help="已有音色 ID（与 clone_audio 互斥）")
    p.add_argument(
        "--clone-audio-url",
        default=None,
        help="克隆/参考音色音频 URL（填写后勿填 voice_over_id）",
    )
    p.add_argument(
        "--voice-speed",
        type=float,
        default=None,
        help="配合 clone_audio 时的语速（可选，例如 1）",
    )
    p.add_argument(
        "--drive-audio-url",
        default=None,
        help="整段驱动音频 URL（drive_mode=2，与 TTS 相关字段互斥）",
    )
    p.add_argument(
        "--base-url",
        default=None,
        help="覆盖 GIGGLE_API_BASE（默认 https://giggle.pro）",
    )


def add_poll_args(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"最长轮询时间（秒），默认 {DEFAULT_TIMEOUT}",
    )
    p.add_argument(
        "--interval",
        type=float,
        default=DEFAULT_INTERVAL,
        help=f"轮询间隔（秒），默认 {DEFAULT_INTERVAL}",
    )


def add_output_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--output", default=None, help="将成片 URL 下载到本地路径")
    p.add_argument("--json", action="store_true", help="打印完整查询 JSON（最后一次轮询响应）")
    p.add_argument("-q", "--quiet", action="store_true", help="静默进度输出")


def download_url(url: str, output: str, quiet: bool) -> None:
    import requests as req

    if not quiet:
        print(f"正在下载到 {output}...", file=sys.stderr)
    resp = req.get(url, stream=True, timeout=300)
    resp.raise_for_status()
    with open(output, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    if not quiet:
        mb = os.path.getsize(output) / (1024 * 1024)
        print(f"已保存：{output}（{mb:.1f} MB）", file=sys.stderr)


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
        print("正在提交数字人口播任务...", file=sys.stderr)
    try:
        task_id = client.submit_tv_avatar(body)
    except GiggleApiError as e:
        print(f"提交失败：{e}", file=sys.stderr)
        sys.exit(1)

    if not args.quiet:
        print(f"已提交。task_id: {task_id}", file=sys.stderr)

    try:
        data, full = client.poll_task(
            task_id,
            interval=args.interval,
            timeout=args.timeout,
            verbose=not args.quiet,
        )
    except TimeoutError as e:
        if not args.quiet:
            print(f"轮询超时：{e}", file=sys.stderr)
            print("可执行：python tv_avatar_video.py query --task-id ...", file=sys.stderr)
        sys.exit(2)
    except GiggleApiError as e:
        print(f"任务失败：{e}", file=sys.stderr)
        sys.exit(1)

    print_completed(data, args, full)


def cmd_submit(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    validate_drive_args(args, parser)
    body = build_submit_body(args)
    client = GiggleClient(base_url=args.base_url) if args.base_url else GiggleClient()
    try:
        task_id = client.submit_tv_avatar(body)
    except GiggleApiError as e:
        print(f"提交失败：{e}", file=sys.stderr)
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
            print(f"轮询超时：{e}", file=sys.stderr)
            print("正在拉取当前状态...", file=sys.stderr)
        try:
            data, full = client.query_task(args.task_id)
        except GiggleApiError as err:
            print(f"查询失败：{err}", file=sys.stderr)
            sys.exit(1)
        status = data.get("status", "")
        if args.json:
            print(json_mod.dumps(full, indent=2, ensure_ascii=False))
        else:
            print(f"状态: {status}  task_id: {args.task_id}", file=sys.stderr)
        sys.exit(2)

    except GiggleApiError as e:
        print(f"任务失败：{e}", file=sys.stderr)
        sys.exit(1)

    print_completed(data, args, full)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="照片数字人口播视频 — Giggle 封装生成 API（提交后轮询）。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
环境变量：
  GIGGLE_API_KEY   必填，控制台左侧栏 → API Key（API 密钥）
  GIGGLE_API_BASE  可选，默认 https://giggle.pro

流程：
  POST .../tv-avatar-video → data.task_id → GET .../task/query?task_id=...
  轮询至 data.status == completed，成片地址为 data.urls[0]
""",
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)

    p_run = sub.add_parser("run", help="提交并轮询至完成（默认首选）")
    add_submit_args(p_run)
    add_poll_args(p_run)
    add_output_args(p_run)

    p_sub = sub.add_parser("submit", help="仅提交，打印 task_id")
    add_submit_args(p_sub)
    add_output_args(p_sub)

    p_q = sub.add_parser("query", help="按 task_id 继续轮询（超时恢复）")
    p_q.add_argument("--task-id", required=True, help="提交接口返回的 task_id")
    add_poll_args(p_q)
    add_output_args(p_q)
    p_q.add_argument("--base-url", default=None, help="覆盖 GIGGLE_API_BASE")

    ns = parser.parse_args()

    if ns.subcommand == "run":
        cmd_run(ns, parser)
    elif ns.subcommand == "submit":
        cmd_submit(ns, parser)
    else:
        cmd_query(ns, parser)


if __name__ == "__main__":
    main()
