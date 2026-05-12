# Credentials and API key

The wrapped API expects an **`x-auth`** header carrying the secret.

## API key

1. Open [giggle.pro](https://giggle.pro/) and sign in.  
2. In the left sidebar, open **API Key**.  
3. Create or copy the key and export it before runs:

```bash
export GIGGLE_API_KEY="<your-key>"
```

If unset, `tv_avatar_video.py` prints a short hint and exits.

Optional **`python-dotenv`**: add `.env` in the project folder (never commit secrets), for example:

```
GIGGLE_API_KEY=...
GIGGLE_API_BASE=https://giggle.pro
```

## Gateway base URL

| Variable | Meaning |
|----------|---------|
| `GIGGLE_API_BASE` | Optional; defaults to `https://giggle.pro`. For private or local gateways use that origin (**no trailing slash**). |

The script hits:

- `POST {GIGGLE_API_BASE}/api/v1/generation/tv-avatar-video`
- `GET {GIGGLE_API_BASE}/api/v1/generation/task/query?task_id=...`
