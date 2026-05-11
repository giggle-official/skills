"""Giggle 封装生成接口：x-auth 鉴权与任务轮询。"""

import sys
import time
from typing import Any, Optional

import requests

from .config import load_config


class GiggleApiError(Exception):
    """业务 code 非 200 时抛出。"""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


class GiggleClient:
    """照片数字人口播视频：提交任务并轮询查询。"""

    SUBMIT_PATH = "/api/v1/generation/tv-avatar-video"
    QUERY_PATH = "/api/v1/generation/task/query"

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        cfg = load_config()
        self._api_key = api_key if api_key is not None else cfg["api_key"]
        self._base = (base_url if base_url is not None else cfg["base_url"]).rstrip("/")

    def _headers_json(self) -> dict[str, str]:
        return {
            "x-auth": self._api_key,
            "Content-Type": "application/json",
        }

    def _headers_simple(self) -> dict[str, str]:
        return {"x-auth": self._api_key}

    @staticmethod
    def _unwrap(resp_json: dict[str, Any]) -> dict[str, Any]:
        code = resp_json.get("code")
        if code != 200:
            msg = resp_json.get("msg", "未知错误")
            raise GiggleApiError(str(code), str(msg))
        data = resp_json.get("data")
        if data is None:
            return {}
        if not isinstance(data, dict):
            raise GiggleApiError("INVALID", f"响应 data 异常: {resp_json!r}")
        return data

    def submit_tv_avatar(self, body: dict[str, Any]) -> str:
        url = f"{self._base}{self.SUBMIT_PATH}"
        resp = requests.post(
            url,
            headers=self._headers_json(),
            json=body,
            timeout=120,
        )
        resp.raise_for_status()
        data = self._unwrap(resp.json())
        task_id = data.get("task_id", "")
        if not task_id:
            raise GiggleApiError("INVALID", f"提交响应缺少 task_id: {data!r}")
        return task_id

    def query_task(self, task_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
        """返回 (data, 完整响应 JSON)。"""
        url = f"{self._base}{self.QUERY_PATH}"
        resp = requests.get(
            url,
            headers=self._headers_simple(),
            params={"task_id": task_id},
            timeout=60,
        )
        resp.raise_for_status()
        full = resp.json()
        data = self._unwrap(full)
        return data, full

    def poll_task(
        self,
        task_id: str,
        *,
        interval: float = 5.0,
        timeout: float = 600.0,
        verbose: bool = True,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """轮询直至 status 为 completed，或失败/超时。"""
        start = time.time()
        last_full: dict[str, Any] = {}
        while True:
            elapsed = time.time() - start
            if elapsed > timeout:
                raise TimeoutError(f"任务 {task_id} 在 {timeout}s 内未完成")

            data, last_full = self.query_task(task_id)
            status = str(data.get("status", "")).strip().lower()
            err_msg = (data.get("err_msg") or "").strip()

            if verbose:
                print(f"  [{elapsed:.0f}s] 状态: {status}", file=sys.stderr)

            if status == "completed":
                urls = data.get("urls") or []
                if isinstance(urls, list) and urls:
                    return data, last_full
                raise GiggleApiError("INVALID", "已完成但 urls 为空")

            if status in ("failed", "fail", "error") or err_msg:
                raise GiggleApiError(
                    "TASK_FAILED",
                    err_msg or f"任务失败（status={status!r}）",
                )

            time.sleep(interval)
