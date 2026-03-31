#!/usr/bin/env python3
"""
X2C Social Poster - CLI tool for X2C Social & Media API
Usage: python3 x2c_social.py --action <action> [options]
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


def get_api_key():
    """Get X2C API Key from environment."""
    key = os.environ.get("X2C_API_KEY", "").strip()
    return key if key else None


def api_request(action, payload=None, api_key=None):
    """Make a JSON API request to X2C."""
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


def upload_file(file_path, folder, api_key):
    """Upload a file via multipart/form-data."""
    if not api_key:
        return {"success": False, "error": "X2C_API_KEY not set"}

    if not os.path.isfile(file_path):
        return {"success": False, "error": f"File not found: {file_path}"}

    headers = {
        "X-API-Key": api_key
    }

    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "application/octet-stream"

    try:
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f, mime_type)}
            data = {}
            if folder:
                data["folder"] = folder

            resp = requests.post(BASE_URL, headers=headers, files=files, data=data, timeout=300)
            return resp.json()
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Upload timed out (file may be too large)"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Upload failed: {str(e)}"}
    except json.JSONDecodeError:
        return {"success": False, "error": f"Invalid response (HTTP {resp.status_code})"}


def cmd_check_key():
    """Check if API key is configured."""
    key = get_api_key()
    if key:
        masked = key[:8] + "..." + key[-4:] if len(key) > 12 else "***"
        print(json.dumps({"success": True, "configured": True, "key_preview": masked}))
    else:
        print(json.dumps({"success": True, "configured": False, "message": "X2C_API_KEY is not set"}))


def cmd_status(api_key):
    """Get linked social accounts."""
    result = api_request("social/status", api_key=api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def auto_upload_local_files(file_paths, folder, api_key):
    """Upload local files to S3 and return CDN URLs.
    
    For each path: if it's a local file, upload and return CDN URL.
    If it's already a URL (http/https), keep as-is.
    Returns (urls_list, errors_list).
    """
    urls = []
    errors = []

    for path in file_paths:
        # Already a remote URL — keep as-is
        if path.startswith("http://") or path.startswith("https://"):
            urls.append(path)
            continue

        # Local file — upload to S3
        if not os.path.isfile(path):
            errors.append(f"File not found: {path}")
            continue

        print(json.dumps({
            "status": "uploading",
            "file": os.path.basename(path),
            "message": f"Uploading {os.path.basename(path)} to S3..."
        }), flush=True)

        result = upload_file(path, folder, api_key)

        if result.get("success") and result.get("url"):
            urls.append(result["url"])
            print(json.dumps({
                "status": "uploaded",
                "file": os.path.basename(path),
                "url": result["url"]
            }), flush=True)
        else:
            err_msg = result.get("error", "Unknown upload error")
            errors.append(f"Failed to upload {path}: {err_msg}")

    return urls, errors


def cmd_publish(args, api_key):
    """Publish a post to social platforms.
    
    Supports one-step publish with local files:
    - --media-files: local file paths → auto-upload to S3, then publish
    - --media-urls: remote URLs (used directly) OR local paths (auto-detected and uploaded)
    Both can be combined; all resulting CDN URLs are merged into a single publish call.
    """
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

    # Auto-upload local files, pass through remote URLs
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

    result = api_request("social/publish", payload, api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_posts(args, api_key):
    """Get post history."""
    payload = {}
    if args.platform:
        payload["platform"] = args.platform
    result = api_request("social/posts", payload, api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_delete_post(args, api_key):
    """Delete a post."""
    if not args.post_id:
        print(json.dumps({"success": False, "error": "Missing --post-id parameter"}))
        return

    payload = {"post_id": args.post_id}
    if args.bulk:
        payload["bulk"] = True

    result = api_request("social/delete-post", payload, api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_comment(args, api_key):
    """Post a comment."""
    if not args.post_id:
        print(json.dumps({"success": False, "error": "Missing --post-id parameter"}))
        return
    if not args.comment:
        print(json.dumps({"success": False, "error": "Missing --comment parameter"}))
        return

    payload = {
        "post_id": args.post_id,
        "comment": args.comment,
    }
    if args.platforms:
        payload["platforms"] = args.platforms

    result = api_request("social/comment", payload, api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_comments(args, api_key):
    """Get comments on a post."""
    if not args.post_id:
        print(json.dumps({"success": False, "error": "Missing --post-id parameter"}))
        return

    payload = {"post_id": args.post_id}
    if args.platform:
        payload["platform"] = args.platform

    result = api_request("social/comments", payload, api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_reply(args, api_key):
    """Reply to a comment."""
    if not args.comment_id:
        print(json.dumps({"success": False, "error": "Missing --comment-id parameter"}))
        return
    if not args.comment:
        print(json.dumps({"success": False, "error": "Missing --comment parameter"}))
        return

    payload = {
        "comment_id": args.comment_id,
        "comment": args.comment,
    }
    if args.platforms:
        payload["platforms"] = args.platforms
    if args.platform:
        payload["platform"] = args.platform

    result = api_request("social/reply", payload, api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_delete_comment(args, api_key):
    """Delete a comment."""
    if not args.comment_id:
        print(json.dumps({"success": False, "error": "Missing --comment-id parameter"}))
        return

    payload = {"comment_id": args.comment_id}
    result = api_request("social/delete-comment", payload, api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_upload(args, api_key):
    """Upload a file."""
    if not args.file:
        print(json.dumps({"success": False, "error": "Missing --file parameter"}))
        return

    result = upload_file(args.file, args.folder, api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="X2C Social Poster CLI")
    parser.add_argument("--action", required=True, choices=SUPPORTED_ACTIONS,
                        help="Action to perform")
    parser.add_argument("--post", type=str, help="Post text content")
    parser.add_argument("--platforms", nargs="+", type=str, help="Target platforms (space-separated)")
    parser.add_argument("--platform", type=str, help="Single platform filter")
    parser.add_argument("--media-urls", nargs="+", type=str, help="Media URLs or local file paths (auto-uploaded)")
    parser.add_argument("--media-files", nargs="+", type=str, help="Local file paths to auto-upload and attach")
    parser.add_argument("--schedule", type=str, help="ISO 8601 schedule date")
    parser.add_argument("--shorten-links", action="store_true", help="Shorten URLs in post")
    parser.add_argument("--post-id", type=str, help="Post ID")
    parser.add_argument("--comment-id", type=str, help="Comment ID")
    parser.add_argument("--comment", type=str, help="Comment text")
    parser.add_argument("--bulk", action="store_true", help="Bulk delete from all platforms")
    parser.add_argument("--file", type=str, help="Local file path for upload")
    parser.add_argument("--folder", type=str, default="uploads", help="Upload subfolder")

    args = parser.parse_args()
    action = args.action

    # check-key doesn't need the API key
    if action == "check-key":
        cmd_check_key()
        return

    # All other actions require API key
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
