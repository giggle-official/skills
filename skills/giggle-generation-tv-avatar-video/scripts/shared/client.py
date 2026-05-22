"""Giggle wrapped generation endpoints: x-auth authentication + task polling."""

import sys
import time
from typing import Any, Optional

import requests

from .config import load_config


class GiggleApiError(Exception):
    """Raised whenever business code is not HTTP 200 success envelope."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


class GiggleClient:
    """Talking-head renders: submit and poll."""

    SUBMIT_PATH = "/api/v1/generation/tv-avatar-video"
    VOICE_CLONE_PATH = "/api/v1/generation/tv-voice-clone"
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
            msg = resp_json.get("msg", "Unknown error")
            raise GiggleApiError(str(code), str(msg))
        data = resp_json.get("data")
        if data is None:
            return {}
        if not isinstance(data, dict):
            raise GiggleApiError("INVALID", f"Unexpected data payload: {resp_json!r}")
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
            raise GiggleApiError("INVALID", f"Missing task_id in submit response: {data!r}")
        return task_id

    def submit_tv_voice_clone(self, body: dict[str, Any]) -> str:
        url = f"{self._base}{self.VOICE_CLONE_PATH}"
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
            raise GiggleApiError("INVALID", f"Missing task_id in submit response: {data!r}")
        return task_id

    def query_task(self, task_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
        """Return (data dict, full JSON envelope)."""
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
        """Poll until status is completed, failure, or timeout."""
        start = time.time()
        last_full: dict[str, Any] = {}
        while True:
            elapsed = time.time() - start
            if elapsed > timeout:
                raise TimeoutError(f"Task {task_id} did not finish within {timeout}s")

            data, last_full = self.query_task(task_id)
            status = str(data.get("status", "")).strip().lower()
            err_msg = (data.get("err_msg") or "").strip()

            if verbose:
                print(f"  [{elapsed:.0f}s] status: {status}", file=sys.stderr)

            if status == "completed":
                urls = data.get("urls") or []
                if isinstance(urls, list) and urls:
                    return data, last_full
                raise GiggleApiError("INVALID", "Completed but urls list empty")

            if status in ("failed", "fail", "error") or err_msg:
                raise GiggleApiError(
                    "TASK_FAILED",
                    err_msg or f"Task failed (status={status!r})",
                )

            time.sleep(interval)

    def poll_task_for_voice_clone(
        self,
        task_id: str,
        *,
        interval: float = 5.0,
        timeout: float = 300.0,
        verbose: bool = True,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Poll until status is completed with a non-empty voice_id, failure, or timeout."""
        start = time.time()
        last_full: dict[str, Any] = {}
        while True:
            elapsed = time.time() - start
            if elapsed > timeout:
                raise TimeoutError(f"Task {task_id} did not finish within {timeout}s")

            data, last_full = self.query_task(task_id)
            status = str(data.get("status", "")).strip().lower()
            err_msg = (data.get("err_msg") or "").strip()
            voice_id = str(data.get("voice_id") or "").strip()

            if verbose:
                extra = f", voice_id: {voice_id}" if voice_id else ""
                print(f"  [{elapsed:.0f}s] status: {status}{extra}", file=sys.stderr)

            if status == "completed":
                if voice_id:
                    return data, last_full
                raise GiggleApiError("INVALID", "Completed but voice_id empty")

            if status in ("failed", "fail", "error") or err_msg:
                raise GiggleApiError(
                    "TASK_FAILED",
                    err_msg or f"Task failed (status={status!r})",
                )

            time.sleep(interval)
