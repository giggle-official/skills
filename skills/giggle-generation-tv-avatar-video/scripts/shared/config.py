"""读取 Giggle _generation API 配置。

环境变量：
- GIGGLE_API_KEY（必填）：控制台侧边栏 → API 密钥
- GIGGLE_API_BASE（可选）：默认 https://giggle.pro，本地联调可设为 http://localhost:8090
"""

import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def load_config() -> dict:
    """返回 api_key 与 base_url。"""
    api_key = os.environ.get("GIGGLE_API_KEY", "").strip()
    base_url = (
        os.environ.get("GIGGLE_API_BASE", "").strip().rstrip("/")
        or "https://giggle.pro"
    )

    if not api_key:
        print(
            "错误：未配置 GIGGLE_API_KEY。\n\n"
            "请在登录 https://giggle.pro/ 后，于左侧边栏打开「API Key / API 密钥」生成密钥，"
            "并设置环境变量：\n\n"
            '  export GIGGLE_API_KEY="<你的密钥>"\n\n'
            "可选：自定义网关地址（默认 https://giggle.pro）\n"
            '  export GIGGLE_API_BASE="http://localhost:8090"\n',
            file=sys.stderr,
        )
        sys.exit(1)

    return {"api_key": api_key, "base_url": base_url}
