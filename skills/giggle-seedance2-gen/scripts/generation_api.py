#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
giggle.pro Seedance 2.0 Generation API 封装脚本
支持文生视频、图生视频（首帧/尾帧）、多模态视频（omni）
API 文档: https://apidocs.giggle.pro/
"""

import os
import sys
import json
import time
import argparse
import requests
from typing import Optional, Dict, Any, List
from enum import Enum


class TaskStatus(str, Enum):
    COMPLETED  = "completed"
    FAILED     = "failed"
    PROCESSING = "processing"
    PENDING    = "pending"


SUPPORTED_MODELS    = ("seedance-2.0-pro", "seedance-2.0-fast")
SUPPORTED_DURATIONS = list(range(4, 16))   # 4–15 秒
SUPPORTED_RATIOS    = ("16:9", "9:16", "1:1", "3:4", "4:3")
SUPPORTED_RESOLUTIONS = ("480p", "720p")
DEFAULT_MODEL       = "seedance-2.0-pro"
DEFAULT_DURATION    = 5
BASE_URL            = "https://giggle.pro"
KEY_FILE            = os.path.expanduser("~/.giggle_api_key")


# ---------------------------------------------------------------------------
# API Key 持久化管理
# ---------------------------------------------------------------------------

def _detect_shell_rc() -> str:
    """自动检测当前 shell 的配置文件路径"""
    shell = os.environ.get("SHELL", "")
    home  = os.path.expanduser("~")
    if "zsh" in shell:
        return os.path.join(home, ".zshrc")
    if "bash" in shell:
        rc = os.path.join(home, ".bash_profile")
        return rc if os.path.exists(rc) else os.path.join(home, ".bashrc")
    return os.path.join(home, ".profile")


def setup_api_key(api_key: str) -> None:
    """
    将 GIGGLE_API_KEY 永久保存：
    1. 写入 ~/.giggle_api_key（跨 session 可靠读取）
    2. 写入 shell rc 文件（终端 export，可选）
    """
    # 写入专用配置文件 — 不依赖 shell 是否 source
    with open(KEY_FILE, "w", encoding="utf-8") as f:
        f.write(api_key.strip())
    os.chmod(KEY_FILE, 0o600)

    # 同步写入 shell rc（终端直接用环境变量也能生效）
    rc_path     = _detect_shell_rc()
    export_line = f'export GIGGLE_API_KEY="{api_key}"'
    marker      = "GIGGLE_API_KEY="

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
        lines.append(f"\n# Giggle Seedance 2.0 API Key\n{export_line}\n")

    with open(rc_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    # 当前进程立即生效
    os.environ["GIGGLE_API_KEY"] = api_key

    print(f"✓ API Key 已永久保存（配置一次，永久有效）")
    print(f"  保存位置: {KEY_FILE}  |  {rc_path}")
    print(f"  当前会话已立即生效，可直接开始生成视频。")


def check_api_key() -> Optional[str]:
    """返回已配置的 API Key，优先级: 环境变量 > ~/.giggle_api_key"""
    key = os.environ.get("GIGGLE_API_KEY")
    if key:
        return key
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r", encoding="utf-8") as f:
            key = f.read().strip()
        if key:
            os.environ["GIGGLE_API_KEY"] = key  # 设置到当前进程环境变量
            return key
    return None


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def to_view_url(url: str) -> str:
    """将下载型 URL 转为在线查看 URL"""
    url = url.replace("&response-content-disposition=attachment", "")
    url = url.replace("?response-content-disposition=attachment&", "?")
    url = url.replace("?response-content-disposition=attachment", "")
    url = url.replace("~", "%7E")
    return url


def parse_frame(s: str) -> Dict[str, str]:
    """
    解析帧参数：
      url:<URL>      -> {"url": "..."}
      base64:<DATA>  -> {"base64": "..."}
    """
    if s.startswith("url:"):
        return {"url": s[4:]}
    if s.startswith("base64:"):
        return {"base64": s[7:]}
    raise ValueError(
        f"帧格式错误: {s!r}\n"
        "正确格式: url:<URL>  或  base64:<RAW_BASE64>"
    )


def parse_media(s: str) -> Dict[str, str]:
    """解析多模态素材引用"""
    if s.startswith("url:"):
        return {"url": s[4:]}
    if s.startswith("base64:"):
        return {"base64": s[7:]}
    raise ValueError(
        f"素材格式错误: {s!r}\n"
        "图片支持 url 或 base64，音频/视频仅支持 url:<URL>"
    )


# ---------------------------------------------------------------------------
# API 客户端
# ---------------------------------------------------------------------------

class SeedanceClient:
    """giggle.pro Seedance 2.0 API 客户端"""

    ENDPOINTS = {
        "text":  "/api/v1/generation/text-to-video",
        "image": "/api/v1/generation/image-to-video",
        "omni":  "/api/v1/generation/omni-video",
        "query": "/api/v1/generation/task/query",
    }

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "x-auth": api_key,
            "Content-Type": "application/json",
        })

    def _post(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{BASE_URL}{self.ENDPOINTS[endpoint]}"
        try:
            resp = self.session.post(url, json=payload, timeout=30)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"请求失败: {e}") from e
        result = resp.json()
        if result.get("code") != 200:
            raise RuntimeError(result.get("msg") or result.get("message") or "未知错误")
        return result

    def _validate(self, model: str, duration: int, generating_count: int = 1) -> None:
        if model not in SUPPORTED_MODELS:
            raise ValueError(f"不支持的模型 {model!r}，可用: {', '.join(SUPPORTED_MODELS)}")
        if duration not in SUPPORTED_DURATIONS:
            raise ValueError(f"时长必须为 4–15 秒，当前: {duration}")
        if not (1 <= generating_count <= 4):
            raise ValueError(f"生成数量必须为 1–4，当前: {generating_count}")

    def text_to_video(self, *, prompt: str, model: str, duration: int,
                      aspect_ratio: str, resolution: str,
                      generating_count: int = 1) -> Dict[str, Any]:
        self._validate(model, duration, generating_count)
        return self._post("text", {
            "prompt": prompt, "model": model, "duration": duration,
            "aspect_ratio": aspect_ratio, "resolution": resolution,
            "generating_count": generating_count,
        })

    def image_to_video(self, *, prompt: str, start_frame: Dict[str, str],
                       end_frame: Optional[Dict[str, str]] = None,
                       model: str, duration: int,
                       aspect_ratio: str, resolution: str,
                       generating_count: int = 1) -> Dict[str, Any]:
        self._validate(model, duration, generating_count)
        payload: Dict[str, Any] = {
            "prompt": prompt, "start_frame": start_frame,
            "model": model, "duration": duration,
            "aspect_ratio": aspect_ratio, "resolution": resolution,
            "generating_count": generating_count,
        }
        if end_frame:
            payload["end_frame"] = end_frame
        return self._post("image", payload)

    def omni_video(self, *, prompt: str,
                   images: Optional[List[Dict[str, str]]] = None,
                   audios: Optional[List[Dict[str, str]]] = None,
                   videos: Optional[List[Dict[str, str]]] = None,
                   model: str, duration: int,
                   aspect_ratio: str, resolution: str,
                   generating_count: int = 1) -> Dict[str, Any]:
        self._validate(model, duration, generating_count)
        if not any([images, audios, videos]):
            raise ValueError("omni 模式至少需要 --images、--audios 或 --videos 之一")
        if images and len(images) > 9:
            raise ValueError(f"图片最多 9 张，当前: {len(images)}")
        payload: Dict[str, Any] = {
            "prompt": prompt, "model": model, "duration": duration,
            "aspect_ratio": aspect_ratio, "resolution": resolution,
            "generating_count": generating_count,
        }
        if images: payload["images"] = images
        if audios: payload["audios"] = audios
        if videos: payload["videos"] = videos
        return self._post("omni", payload)

    def query_task(self, task_id: str) -> Dict[str, Any]:
        url = f"{BASE_URL}{self.ENDPOINTS['query']}"
        try:
            resp = self.session.get(url, params={"task_id": task_id}, timeout=30)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"查询失败: {e}") from e
        result = resp.json()
        if result.get("code") != 200:
            raise RuntimeError(result.get("msg") or "查询返回异常")
        return result

    def extract_urls(self, result: Dict[str, Any]) -> List[str]:
        return result.get("data", {}).get("urls", [])


# ---------------------------------------------------------------------------
# 输出处理
# ---------------------------------------------------------------------------

def _print_completed(urls: List[str]) -> None:
    """打印已完成的视频链接"""
    view_urls = [to_view_url(u) for u in urls]
    print("视频已就绪！🎬\n")
    print(f"共 {len(view_urls)} 个视频 ✨\n")
    for i, u in enumerate(view_urls):
        print(f"[查看视频 {i + 1}]({u})")
    print("\n⚠️  以上链接为签名 URL（含 Policy、Key-Pair-Id、Signature），"
          "有效期有限，请及时查看或下载。")
    print("\n如需调整，随时告诉我~")


def handle_query(client: SeedanceClient, task_id: str) -> None:
    """单次查询任务状态"""
    result = client.query_task(task_id)
    data   = result.get("data", {})
    status = data.get("status", "")

    if status == TaskStatus.COMPLETED.value:
        raw_urls = client.extract_urls(result)
        if not raw_urls:
            print("生成完成，但未返回视频链接，建议重新生成。")
            return
        _print_completed(raw_urls)

    elif status in ("failed", "error"):
        err = data.get("err_msg", "未知错误")
        if "sensitive" in str(err).lower():
            err = "输入内容可能含敏感信息，被服务端拦截"
        print(f"生成失败：{err}\n\n建议调整提示词后重试。")

    else:
        print(json.dumps({"status": status, "task_id": task_id}, ensure_ascii=False))


def handle_wait(client: SeedanceClient, task_id: str,
                interval: int = 10, timeout: int = 600) -> None:
    """
    主动轮询，直到任务完成或超时。
    完成后立即输出结果（由调用方主动推送给用户，无需等待用户询问）。
    """
    elapsed = 0
    print(f"轮询中 task_id={task_id}（每 {interval}s 查询一次，最长等待 {timeout}s）...",
          file=sys.stderr)

    while elapsed < timeout:
        try:
            result = client.query_task(task_id)
        except Exception as e:
            print(f"查询异常: {e}，{interval}s 后重试...", file=sys.stderr)
            time.sleep(interval)
            elapsed += interval
            continue

        data   = result.get("data", {})
        status = data.get("status", "")

        if status == TaskStatus.COMPLETED.value:
            raw_urls = client.extract_urls(result)
            if not raw_urls:
                print("生成完成，但未返回视频链接，建议重新生成。")
                return
            _print_completed(raw_urls)
            return

        elif status in ("failed", "error"):
            err = data.get("err_msg", "未知错误")
            if "sensitive" in str(err).lower():
                err = "输入内容可能含敏感信息，被服务端拦截"
            print(f"生成失败：{err}\n\n建议调整提示词后重试。")
            return

        else:
            print(f"  [{elapsed}s] 状态: {status}，继续等待...", file=sys.stderr)
            time.sleep(interval)
            elapsed += interval

    print(f"超时（已等待 {timeout}s），任务仍未完成。\n"
          f"可稍后手动查询: python3 generation_api.py --query --task-id {task_id}")


def handle_submit(client: SeedanceClient, args) -> None:
    mode  = args.mode
    model = args.model
    dur   = args.duration
    ratio = args.aspect_ratio
    res   = args.resolution
    count = args.generating_count

    print(f"提交任务 [模式: {mode} | 模型: {model} | 时长: {dur}s | 比例: {ratio}]...",
          file=sys.stderr)

    if mode == "text":
        result = client.text_to_video(
            prompt=args.prompt, model=model, duration=dur,
            aspect_ratio=ratio, resolution=res, generating_count=count,
        )
    elif mode == "image":
        if not args.start_frame:
            print("错误: image 模式需要 --start-frame", file=sys.stderr)
            sys.exit(1)
        start  = parse_frame(args.start_frame)
        end    = parse_frame(args.end_frame) if args.end_frame else None
        result = client.image_to_video(
            prompt=args.prompt, start_frame=start, end_frame=end,
            model=model, duration=dur,
            aspect_ratio=ratio, resolution=res, generating_count=count,
        )
    else:  # omni
        images = [parse_media(s) for s in args.images] if args.images else None
        audios = None
        if args.audios:
            audios = []
            for s in args.audios:
                if not s.startswith("url:"):
                    raise ValueError(
                        f"音频格式错误: {s!r}，omni 模式下每条音频须为 url:<URL>"
                    )
                audios.append({"url": s[4:]})
        videos = None
        if args.videos:
            videos = []
            for s in args.videos:
                if not s.startswith("url:"):
                    raise ValueError(
                        f"参考视频格式错误: {s!r}，omni 模式下每条视频须为 url:<URL>"
                    )
                videos.append({"url": s[4:]})
        result = client.omni_video(
            prompt=args.prompt, images=images, audios=audios, videos=videos,
            model=model, duration=dur,
            aspect_ratio=ratio, resolution=res, generating_count=count,
        )

    task_id = result.get("data", {}).get("task_id", "")
    print(f"✓ 任务已提交！task_id: {task_id}", file=sys.stderr)
    print(json.dumps({"status": "started", "task_id": task_id}, ensure_ascii=False))

    # 提交后立即开始轮询，完成后主动推送结果
    print("\n正在用 Seedance 2.0 生成，完成后我会主动通知你（约 1–5 分钟）...",
          file=sys.stderr)
    handle_wait(client, task_id)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="generation_api.py",
        description="giggle.pro Seedance 2.0 视频生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 【首次使用】永久配置 API Key（只需一次）
  python3 generation_api.py --setup --api-key sk_your_key

  # 检查 API Key 是否已配置
  python3 generation_api.py --check-key

  # 文生视频
  python3 generation_api.py --mode text --prompt "镜头缓缓推进，橘猫在阳光下玩耍" --duration 5

  # 图生视频（首帧 URL）
  python3 generation_api.py --mode image --prompt "人物缓缓转身" \\
    --start-frame "url:https://example.com/photo.jpg" --duration 5

  # 多模态（图片 + 音频）
  python3 generation_api.py --mode omni --prompt "人物保持微笑，镜头缓缓推进" \\
    --images "url:https://example.com/ref.png" --audios "url:https://example.com/bgm.mp3"

  # 手动单次查询任务进度
  python3 generation_api.py --query --task-id <task_id>

  # 断点续查（--wait 中断后恢复轮询）
  python3 generation_api.py --wait --task-id <task_id>
        """,
    )

    # 配置管理
    parser.add_argument("--setup",     action="store_true",
                        help="【首次使用】永久保存 API Key 到 shell 配置文件")
    parser.add_argument("--check-key", action="store_true",
                        help="检查 GIGGLE_API_KEY 是否已配置")

    # 任务管理
    parser.add_argument("--query",    action="store_true", help="单次查询任务状态")
    parser.add_argument("--wait",     action="store_true",
                        help="提交后自动轮询直到完成，主动推送结果给用户")
    parser.add_argument("--task-id",  type=str, metavar="ID",
                        help="任务 ID（--query 或 --wait 时必填）")

    # 认证
    parser.add_argument("--api-key",  type=str,
                        help="API 密钥（--setup 时必填；生成时可选，优先于环境变量）")

    # 生成参数
    parser.add_argument("--mode",     type=str, choices=["text", "image", "omni"],
                        help="生成模式")
    parser.add_argument("--prompt",   type=str, help="视频描述（已优化的提示词）")
    parser.add_argument("--model",    type=str, default=DEFAULT_MODEL,
                        choices=list(SUPPORTED_MODELS))
    parser.add_argument("--duration", type=int, default=DEFAULT_DURATION,
                        help="视频时长（秒），4–15，默认 5")
    parser.add_argument("--aspect-ratio", type=str, default="16:9",
                        choices=list(SUPPORTED_RATIOS))
    parser.add_argument("--resolution",   type=str, default="720p",
                        choices=list(SUPPORTED_RESOLUTIONS))
    parser.add_argument("--generating-count", type=int, default=1,
                        metavar="N", help="生成数量 1–4，默认 1")

    # image-to-video
    parser.add_argument("--start-frame", type=str,
                        help="首帧: url:<URL> 或 base64:<DATA>")
    parser.add_argument("--end-frame",   type=str,
                        help="尾帧: url:<URL> 或 base64:<DATA>")

    # omni-video（action=extend：可写一次有空格多值，也可多次 --images 合并，避免只保留最后一组）
    parser.add_argument("--images", type=str, action="extend", nargs="+",
                        help="图片引用，url 或 base64；可多值或与多次 --images 合并")
    parser.add_argument("--audios", type=str, action="extend", nargs="+",
                        help="音频引用，仅 url:<URL>；可多值或与多次 --audios 合并")
    parser.add_argument("--videos", type=str, action="extend", nargs="+",
                        help="参考视频，仅 url:<URL>；可多值或与多次 --videos 合并")

    return parser


def main() -> None:
    parser = build_parser()
    args   = parser.parse_args()

    # ------------------------------------------------------------------ setup
    if args.setup:
        if not args.api_key:
            print("错误: --setup 需要提供 --api-key sk_your_key", file=sys.stderr)
            print("获取 API Key：打开 giggle.pro/developer → API 密钥 → + 新建 API Key",
                  file=sys.stderr)
            sys.exit(1)
        try:
            setup_api_key(args.api_key)
        except Exception as e:
            print(f"写入失败: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # --------------------------------------------------------------- check-key
    if args.check_key:
        key = check_api_key()
        if key:
            masked = key[:8] + "..." + key[-4:] if len(key) > 12 else "***"
            print(json.dumps({
                "status": "ok",
                "message": f"GIGGLE_API_KEY 已配置: {masked}"
            }, ensure_ascii=False))
        else:
            rc = _detect_shell_rc()
            print(json.dumps({
                "status": "missing",
                "message": (
                    "未找到 GIGGLE_API_KEY，请完成一次性配置：\n"
                    "1. 打开 giggle.pro/developer → 点击左侧「API 密钥」\n"
                    "2. 点击右上角「+ 新建 API Key」，复制 Key\n"
                    f"3. 运行: python3 generation_api.py --setup --api-key sk_你的密钥\n"
                    f"   Key 将永久保存到 {rc}，之后无需再次配置。"
                )
            }, ensure_ascii=False))
        return

    # ------------------------------------------------------------ 获取 API Key
    api_key = args.api_key or check_api_key()
    if not api_key:
        print(
            "错误: 未配置 GIGGLE_API_KEY\n"
            "请先完成一次性配置:\n"
            "  python3 generation_api.py --setup --api-key sk_你的密钥\n"
            "  Key 获取地址: giggle.pro/developer → API 密钥 → + 新建 API Key",
            file=sys.stderr,
        )
        sys.exit(1)

    client = SeedanceClient(api_key)

    # ------------------------------------------------------------------ query
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

    # ------------------------------------------------------------------- wait
    if args.wait:
        if not args.task_id:
            print("错误: --wait 需要 --task-id", file=sys.stderr)
            sys.exit(1)
        try:
            handle_wait(client, args.task_id)
        except Exception as e:
            print(f"轮询失败: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # ----------------------------------------------------------------- submit
    if not args.mode:
        print("错误: 需要 --mode (text / image / omni)", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(1)
    if not args.prompt:
        print("错误: 需要 --prompt", file=sys.stderr)
        sys.exit(1)

    try:
        handle_submit(client, args)
    except Exception as e:
        print(f"生成失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
