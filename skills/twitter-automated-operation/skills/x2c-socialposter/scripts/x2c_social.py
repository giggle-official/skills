#!/usr/bin/env python3
"""
X2C Social Poster - CLI tool for X2C Social & Media API
Usage: python3 x2c_social.py --action <action> [options]

Supports:
- Pre-signed URL upload (up to 5GB) for large files
- Direct upload (up to ~50MB) for small files
- Auto-detection: local files are uploaded before publishing
- Per-platform validation before publish
"""

import argparse
import json
import os
import sys
import mimetypes

try:
    import requests
except ImportError:
    print(json.dumps({"success": False, "error": "Missing dependency: requests. Run: pip install requests"}))
    sys.exit(1)

BASE_URL = "https://eumfmgwxwjyagsvqloac.supabase.co/functions/v1/open-api"

SUPPORTED_ACTIONS = [
    "check-key", "status", "publish", "posts", "delete-post",
    "comment", "comments", "reply", "delete-comment", "upload"
]

# Size threshold: files above this use pre-signed URL upload
DIRECT_UPLOAD_LIMIT = 50 * 1024 * 1024  # 50MB

# ─── Platform Requirements ───────────────────────────────────────────────────

PLATFORM_RULES = {
    "twitter": {
        "name": "X (Twitter)",
        "text_limit": 280,
        "media_required": False,
        "max_images": 4,
        "max_videos": 1,
        "max_media": 4,
        "supported_types": ["JPEG", "PNG", "GIF", "MP4"],
        "notes": "Images and videos cannot be mixed. Requires BYO Twitter API keys. Use longPost for >280 chars.",
    },
    "instagram": {
        "name": "Instagram",
        "text_limit": 2200,
        "media_required": True,
        "max_images": 10,
        "max_videos": 1,
        "max_media": 10,
        "max_hashtags": 5,
        "max_mentions": 3,
        "supported_types": ["JPEG", "PNG", "MP4"],
        "notes": "Must be Business/Creator. Media required. Max 5 hashtags, 3 @mentions.",
    },
    "tiktok": {
        "name": "TikTok",
        "text_limit": 2200,
        "media_required": True,
        "max_images": 35,
        "max_videos": 1,
        "supported_types": ["MP4", "JPG", "JPEG", "WEBP"],
        "no_png": True,
        "notes": "Images & video can't mix. No PNG. No line breaks. AI content must set --ai-generated.",
    },
    "youtube": {
        "name": "YouTube",
        "text_limit": 5000,
        "title_limit": 100,
        "media_required": True,
        "video_only": True,
        "max_media": 1,
        "supported_types": ["MP4", "MOV", "AVI", "WMV"],
        "auto_title": True,
        "notes": "Video required. Title required (max 100 chars, auto-gen from post text if missing).",
    },
    "facebook": {
        "name": "Facebook",
        "text_limit": 63206,
        "media_required": False,
        "supported_types": ["JPEG", "PNG", "MP4"],
        "notes": "Must be a Page (not personal account).",
    },
    "linkedin": {
        "name": "LinkedIn",
        "text_limit": 3000,
        "media_required": False,
        "max_images": 9,
        "max_media": 9,
        "supported_types": ["JPEG", "PNG", "GIF", "MP4"],
        "notes": "Personal or Company page.",
    },
    "pinterest": {
        "name": "Pinterest",
        "text_limit": 500,
        "media_required": True,
        "max_media": 5,
        "supported_types": ["JPEG", "PNG"],
        "notes": "Image required. Video posts require --thumbnail.",
    },
    "reddit": {
        "name": "Reddit",
        "text_limit": 40000,
        "title_limit": 300,
        "media_required": False,
        "max_media": 1,
        "requires_title": True,
        "requires_subreddit": True,
        "supported_types": ["JPEG", "PNG", "GIF", "MP4"],
        "notes": "Title required (max 300 chars). Subreddit required.",
    },
    "gmb": {
        "name": "Google Business Profile",
        "text_limit": 1500,
        "media_required": False,
        "max_media": 1,
        "supported_types": ["JPEG", "PNG", "MP4"],
        "notes": "Verified business. No phone numbers in text.",
    },
    "bluesky": {
        "name": "Bluesky",
        "text_limit": 300,
        "media_required": False,
        "max_images": 4,
        "max_media": 4,
        "supported_types": ["JPEG", "PNG", "MP4"],
        "notes": "300 chars including links.",
    },
    "threads": {
        "name": "Threads",
        "text_limit": 500,
        "media_required": False,
        "max_images": 10,
        "max_media": 10,
        "supported_types": ["JPEG", "PNG", "MP4"],
        "notes": "Linked to Instagram account.",
    },
    "snapchat": {
        "name": "Snapchat",
        "text_limit": 160,
        "media_required": True,
        "max_media": 1,
        "supported_types": ["JPEG", "PNG", "MP4"],
        "notes": "Exactly 1 media item only.",
    },
    "telegram": {
        "name": "Telegram",
        "text_limit": 4096,
        "media_required": False,
        "max_media": 1,
        "supported_types": ["JPEG", "PNG", "GIF", "MP4"],
        "notes": "Requires Bot + Channel/Group.",
    },
}


# ─── Helpers ─────────────────────────────────────────────────────────────────

def get_api_key():
    key = os.environ.get("X2C_API_KEY", "").strip()
    return key if key else None


def api_request(action, payload=None, api_key=None):
    if not api_key:
        return {"success": False, "error": "X2C_API_KEY not set"}

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key
    }

    body = {"action": action}
    if payload:
        body.update(payload)

    try:
        resp = requests.post(BASE_URL, headers=headers, json=body, timeout=60)
        return resp.json()
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Request failed: {str(e)}"}
    except json.JSONDecodeError:
        return {"success": False, "error": f"Invalid response (HTTP {resp.status_code})"}


def guess_content_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or "application/octet-stream"


def is_video_mime(content_type):
    return content_type.startswith("video/")


def is_image_mime(content_type):
    return content_type.startswith("image/")


# ─── Upload Methods ──────────────────────────────────────────────────────────

def upload_presigned(file_path, folder, api_key):
    """Upload via pre-signed URL (recommended, up to 5GB)."""
    file_name = os.path.basename(file_path)
    content_type = guess_content_type(file_path)

    # Step 1: Get pre-signed URL
    payload = {
        "action": "media/get-upload-url",
        "file_name": file_name,
        "content_type": content_type,
    }
    if folder:
        payload["folder"] = folder

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key
    }

    try:
        resp = requests.post(BASE_URL, headers=headers, json=payload, timeout=30)
        data = resp.json()
    except Exception as e:
        return {"success": False, "error": f"Failed to get upload URL: {str(e)}"}

    if not data.get("success") or not data.get("upload_url"):
        return {"success": False, "error": data.get("error", "Failed to get pre-signed URL")}

    upload_url = data["upload_url"]
    public_url = data["public_url"]

    # Step 2: PUT file directly to S3
    try:
        file_size = os.path.getsize(file_path)
        with open(file_path, "rb") as f:
            put_resp = requests.put(
                upload_url,
                data=f,
                headers={"Content-Type": content_type},
                timeout=max(300, file_size // (1024 * 1024) * 5)  # ~5s per MB
            )
            if put_resp.status_code != 200:
                return {
                    "success": False,
                    "error": f"S3 upload failed with HTTP {put_resp.status_code}",
                    "details": put_resp.text[:500] if put_resp.text else None
                }
    except requests.exceptions.Timeout:
        return {"success": False, "error": "S3 upload timed out (file may be too large)"}
    except Exception as e:
        return {"success": False, "error": f"S3 upload failed: {str(e)}"}

    return {
        "success": True,
        "url": public_url,
        "key": data.get("key"),
        "file_name": file_name,
        "content_type": content_type,
        "size": file_size,
        "method": "presigned"
    }


def upload_direct(file_path, folder, api_key):
    """Upload via multipart/form-data (small files < 50MB)."""
    headers = {"X-API-Key": api_key}
    content_type = guess_content_type(file_path)

    try:
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f, content_type)}
            data = {}
            if folder:
                data["folder"] = folder
            resp = requests.post(BASE_URL, headers=headers, files=files, data=data, timeout=300)
            result = resp.json()
            result["method"] = "direct"
            return result
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Upload timed out"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Upload failed: {str(e)}"}
    except json.JSONDecodeError:
        return {"success": False, "error": f"Invalid response (HTTP {resp.status_code})"}


def upload_file(file_path, folder, api_key):
    """Smart upload: auto-select method based on file size.
    
    - <= 50MB: direct multipart upload (simple, one request)
    - > 50MB: pre-signed URL upload (two steps, up to 5GB)
    """
    if not os.path.isfile(file_path):
        return {"success": False, "error": f"File not found: {file_path}"}

    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    size_mb = round(file_size / (1024 * 1024), 1)

    if file_size > DIRECT_UPLOAD_LIMIT:
        print(json.dumps({
            "status": "uploading",
            "file": file_name,
            "size_mb": size_mb,
            "method": "presigned",
            "message": f"Uploading {file_name} ({size_mb}MB) via pre-signed URL..."
        }), flush=True)
        return upload_presigned(file_path, folder, api_key)
    else:
        print(json.dumps({
            "status": "uploading",
            "file": file_name,
            "size_mb": size_mb,
            "method": "direct",
            "message": f"Uploading {file_name} ({size_mb}MB) via direct upload..."
        }), flush=True)
        return upload_direct(file_path, folder, api_key)


# ─── Auto Upload for Publish ─────────────────────────────────────────────────

def auto_upload_local_files(file_paths, folder, api_key):
    """Upload local files and return CDN URLs. Remote URLs pass through."""
    urls = []
    errors = []

    for path in file_paths:
        if path.startswith("http://") or path.startswith("https://"):
            urls.append(path)
            continue

        if not os.path.isfile(path):
            errors.append(f"File not found: {path}")
            continue

        result = upload_file(path, folder, api_key)

        if result.get("success") and result.get("url"):
            urls.append(result["url"])
            print(json.dumps({
                "status": "uploaded",
                "file": os.path.basename(path),
                "url": result["url"],
                "method": result.get("method", "unknown")
            }), flush=True)
        else:
            err_msg = result.get("error", "Unknown upload error")
            errors.append(f"Failed to upload {path}: {err_msg}")

    return urls, errors


# ─── Platform Validation ─────────────────────────────────────────────────────

def count_hashtags(text):
    """Count hashtags in text."""
    import re
    return len(re.findall(r'#\w+', text)) if text else 0


def count_mentions(text):
    """Count @mentions in text."""
    import re
    return len(re.findall(r'@\w+', text)) if text else 0


def validate_publish(platforms, post_text, media_urls, args):
    """Validate publish parameters against platform requirements.
    Returns list of warning/error strings. Empty = all good."""
    warnings = []

    for p in platforms:
        rules = PLATFORM_RULES.get(p)
        if not rules:
            warnings.append(f"⚠️  Unknown platform: {p}")
            continue

        name = rules["name"]

        # Text length check
        text_limit = rules.get("text_limit", 0)
        if text_limit and post_text and len(post_text) > text_limit:
            warnings.append(
                f"❌ {name}: Text too long ({len(post_text)} chars, max {text_limit})"
            )

        # Title length check (YouTube max 100, Reddit max 300)
        title_limit = rules.get("title_limit")
        if title_limit and args.title and len(args.title) > title_limit:
            warnings.append(
                f"❌ {name}: Title too long ({len(args.title)} chars, max {title_limit})"
            )

        # Media required check
        if rules.get("media_required") and not media_urls:
            warnings.append(f"❌ {name}: Media is required (image or video)")

        # Video-only check (YouTube)
        if rules.get("video_only") and media_urls:
            has_video = any(
                is_video_mime(guess_content_type(u)) or
                any(u.lower().endswith(ext) for ext in [".mp4", ".mov", ".webm", ".avi", ".wmv"])
                for u in media_urls
            )
            if not has_video:
                warnings.append(f"❌ {name}: Video is required (images not supported)")

        # Title required — but YouTube can auto-gen, so only error for Reddit
        if rules.get("requires_title") and not args.title and not rules.get("auto_title"):
            warnings.append(f"❌ {name}: --title is required")

        # Subreddit required (Reddit)
        if rules.get("requires_subreddit") and not args.subreddit:
            warnings.append(f"❌ {name}: --subreddit is required")

        # Max media count
        max_media = rules.get("max_media")
        if max_media and media_urls and len(media_urls) > max_media:
            warnings.append(
                f"❌ {name}: Only {max_media} media item(s) allowed, got {len(media_urls)}"
            )

        # Instagram: max 5 hashtags, 3 @mentions
        if p == "instagram" and post_text:
            ht_count = count_hashtags(post_text)
            mt_count = count_mentions(post_text)
            max_ht = rules.get("max_hashtags", 999)
            max_mt = rules.get("max_mentions", 999)
            if ht_count > max_ht:
                warnings.append(
                    f"❌ {name}: Too many hashtags ({ht_count}, max {max_ht})"
                )
            if mt_count > max_mt:
                warnings.append(
                    f"⚠️  {name}: Too many @mentions ({mt_count}, max {max_mt})"
                )

        # TikTok: no PNG warning
        if p == "tiktok" and rules.get("no_png") and media_urls:
            has_png = any(u.lower().endswith(".png") for u in media_urls)
            if has_png:
                warnings.append(
                    f"⚠️  {name}: PNG format not supported. Use JPG, JPEG, or WEBP instead."
                )

    return warnings


# ─── Commands ────────────────────────────────────────────────────────────────

def cmd_check_key():
    key = get_api_key()
    if key:
        masked = key[:8] + "..." + key[-4:] if len(key) > 12 else "***"
        print(json.dumps({"success": True, "configured": True, "key_preview": masked}))
    else:
        print(json.dumps({"success": True, "configured": False, "message": "X2C_API_KEY is not set"}))


def cmd_status(api_key):
    result = api_request("social/status", api_key=api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_publish(args, api_key):
    """Publish a post with auto-upload and per-platform validation."""
    if not args.post:
        print(json.dumps({"success": False, "error": "Missing --post parameter"}))
        return
    if not args.platforms:
        print(json.dumps({"success": False, "error": "Missing --platforms parameter"}))
        return

    # Collect all media sources
    all_media_paths = []
    if args.media_urls:
        all_media_paths.extend(args.media_urls)
    if args.media_files:
        all_media_paths.extend(args.media_files)

    # Auto-upload local files (smart: presigned for large, direct for small)
    final_urls = []
    if all_media_paths:
        urls, errors = auto_upload_local_files(all_media_paths, args.folder, api_key)
        if errors:
            print(json.dumps({
                "success": False,
                "error": "Some media files failed to upload",
                "details": errors
            }))
            return
        final_urls = urls

    # Per-platform validation
    warnings = validate_publish(args.platforms, args.post, final_urls, args)
    fatal = [w for w in warnings if w.startswith("❌")]
    if fatal:
        print(json.dumps({
            "success": False,
            "error": "Platform validation failed",
            "details": warnings
        }, ensure_ascii=False))
        return
    if warnings:
        for w in warnings:
            print(json.dumps({"warning": w}, ensure_ascii=False), flush=True)

    # Build payload
    payload = {
        "post": args.post,
        "platforms": args.platforms,
    }

    if final_urls:
        payload["media_urls"] = final_urls
    if args.schedule:
        payload["schedule_date"] = args.schedule
    if args.shorten_links:
        payload["shorten_links"] = True

    # Build platform_options
    platform_options = {}

    # YouTube options — auto-generate title if missing (max 100 chars)
    if "youtube" in args.platforms:
        yt_opts = {}
        if args.title:
            yt_opts["title"] = args.title[:100]
        else:
            # Auto-gen title from post text (first 100 chars)
            auto_title = (args.post or "Untitled")[:100]
            yt_opts["title"] = auto_title
            print(json.dumps({
                "info": f"YouTube: Auto-generated title from post text: \"{auto_title}\""
            }, ensure_ascii=False), flush=True)
        yt_opts["visibility"] = args.visibility if args.visibility else "public"
        platform_options["youTubeOptions"] = yt_opts

    # Reddit options
    if "reddit" in args.platforms:
        rd_opts = {}
        if args.title:
            rd_opts["title"] = args.title[:300]
        if args.subreddit:
            rd_opts["subreddit"] = args.subreddit
        if rd_opts:
            platform_options["redditOptions"] = rd_opts

    # TikTok options
    if "tiktok" in args.platforms:
        tt_opts = {}
        if args.ai_generated:
            tt_opts["isAIGenerated"] = True
        if args.visibility:
            tt_opts["visibility"] = args.visibility
        if tt_opts:
            platform_options["tikTokOptions"] = tt_opts

    # Pinterest thumbnail
    if "pinterest" in args.platforms and args.thumbnail:
        platform_options["thumbNail"] = args.thumbnail

    if platform_options:
        payload["platform_options"] = platform_options

    result = api_request("social/publish", payload, api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_posts(args, api_key):
    payload = {}
    if args.platform:
        payload["platform"] = args.platform
    result = api_request("social/posts", payload, api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_delete_post(args, api_key):
    if not args.post_id:
        print(json.dumps({"success": False, "error": "Missing --post-id parameter"}))
        return
    payload = {"post_id": args.post_id}
    if args.bulk:
        payload["bulk"] = True
    result = api_request("social/delete-post", payload, api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_comment(args, api_key):
    if not args.post_id:
        print(json.dumps({"success": False, "error": "Missing --post-id parameter"}))
        return
    if not args.comment:
        print(json.dumps({"success": False, "error": "Missing --comment parameter"}))
        return
    payload = {"post_id": args.post_id, "comment": args.comment}
    if args.platforms:
        payload["platforms"] = args.platforms
    result = api_request("social/comment", payload, api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_comments(args, api_key):
    if not args.post_id:
        print(json.dumps({"success": False, "error": "Missing --post-id parameter"}))
        return
    payload = {"post_id": args.post_id}
    if args.platform:
        payload["platform"] = args.platform
    result = api_request("social/comments", payload, api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_reply(args, api_key):
    if not args.comment_id:
        print(json.dumps({"success": False, "error": "Missing --comment-id parameter"}))
        return
    if not args.comment:
        print(json.dumps({"success": False, "error": "Missing --comment parameter"}))
        return
    payload = {"comment_id": args.comment_id, "comment": args.comment}
    if args.platforms:
        payload["platforms"] = args.platforms
    if args.platform:
        payload["platform"] = args.platform
    result = api_request("social/reply", payload, api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_delete_comment(args, api_key):
    if not args.comment_id:
        print(json.dumps({"success": False, "error": "Missing --comment-id parameter"}))
        return
    payload = {"comment_id": args.comment_id}
    result = api_request("social/delete-comment", payload, api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_upload(args, api_key):
    if not args.file:
        print(json.dumps({"success": False, "error": "Missing --file parameter"}))
        return
    result = upload_file(args.file, args.folder, api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="X2C Social Poster CLI")
    parser.add_argument("--action", required=True, choices=SUPPORTED_ACTIONS)

    # Publishing
    parser.add_argument("--post", type=str, help="Post text content")
    parser.add_argument("--platforms", nargs="+", type=str, help="Target platforms")
    parser.add_argument("--platform", type=str, help="Single platform filter")
    parser.add_argument("--media-urls", nargs="+", type=str, help="Media URLs or local paths (auto-uploaded)")
    parser.add_argument("--media-files", nargs="+", type=str, help="Local files to auto-upload and attach")
    parser.add_argument("--schedule", type=str, help="ISO 8601 schedule date")
    parser.add_argument("--shorten-links", action="store_true", help="Shorten URLs in post")

    # Platform-specific
    parser.add_argument("--title", type=str, help="Title (required for YouTube/Reddit)")
    parser.add_argument("--subreddit", type=str, help="Target subreddit (required for Reddit)")
    parser.add_argument("--visibility", type=str, help="Post visibility (platform-specific)")
    parser.add_argument("--thumbnail", type=str, help="Thumbnail URL (required for Pinterest video)")
    parser.add_argument("--ai-generated", action="store_true", help="Mark content as AI-generated (TikTok)")

    # Comment/Reply
    parser.add_argument("--post-id", type=str, help="Post ID")
    parser.add_argument("--comment-id", type=str, help="Comment ID")
    parser.add_argument("--comment", type=str, help="Comment text")
    parser.add_argument("--bulk", action="store_true", help="Bulk delete")

    # Upload
    parser.add_argument("--file", type=str, help="Local file path for upload")
    parser.add_argument("--folder", type=str, default="uploads", help="Upload subfolder")

    args = parser.parse_args()
    action = args.action

    if action == "check-key":
        cmd_check_key()
        return

    api_key = get_api_key()
    if not api_key:
        print(json.dumps({
            "success": False,
            "error": "X2C_API_KEY not set. Please set the environment variable.",
            "setup_url": "https://www.x2creel.ai/social-accounts"
        }))
        sys.exit(1)

    action_map = {
        "status": lambda: cmd_status(api_key),
        "publish": lambda: cmd_publish(args, api_key),
        "posts": lambda: cmd_posts(args, api_key),
        "delete-post": lambda: cmd_delete_post(args, api_key),
        "comment": lambda: cmd_comment(args, api_key),
        "comments": lambda: cmd_comments(args, api_key),
        "reply": lambda: cmd_reply(args, api_key),
        "delete-comment": lambda: cmd_delete_comment(args, api_key),
        "upload": lambda: cmd_upload(args, api_key),
    }

    handler = action_map.get(action)
    if handler:
        handler()
    else:
        print(json.dumps({"success": False, "error": f"Unknown action: {action}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
