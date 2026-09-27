import httpx
import os


GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")


headers = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2026-03-10"
}

# goes from 60/hour to 3000/hour if provided
if GITHUB_TOKEN:
    headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"


# Pagination : github's REST API caps the issues to only "per_page" = 30 (by default) issue
# sollution  : loop over all pages untill finding an empty response = []
def list_open_issues(repo: str, max_items: int = 300) -> list[dict]:
    """Fetch ALL open issues for a repo (not pull requests), across as
    many pages as needed, up to max_items as a safety cap.
    """
    issues = []
    page = 1
    while len(issues) < max_items:
        resp = httpx.get(
            f"{GITHUB_API}/repos/{repo}/issues",
            params={"state": "open", "per_page": 100, "page": page},
            headers=headers,
        )
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break  # GitHub returns [] past the last page, not a 404
        issues.extend(i for i in batch if "pull_request" not in i)
        page += 1
    return issues[:max_items]