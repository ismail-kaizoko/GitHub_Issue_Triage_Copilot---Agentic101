import httpx
import os


GITHUB_API = "https://api.github.com"

def headers() -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")

    # goes from 60 requests/hour to 3000 requests/hour if provided
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


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
            headers=headers(),
        )
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break  # GitHub returns [] past the last page, not a 404
        issues.extend(i for i in batch if "pull_request" not in i)
        page += 1
    return issues[:max_items]


def get_issue(repo: str, number: int) -> dict:
    resp = httpx.get(f"{GITHUB_API}/repos/{repo}/issues/{number}", headers=headers())
    resp.raise_for_status()
    return resp.json()


def search_issues(repo: str, query: str) -> list[dict]:
    """query is free text; scoped to this repo automatically."""
    resp = httpx.get(
        f"{GITHUB_API}/search/issues",
        params={"q": f"repo:{repo} is:issue {query}"},
        headers=headers(),
    )
    resp.raise_for_status()
    return resp.json().get("items", [])



