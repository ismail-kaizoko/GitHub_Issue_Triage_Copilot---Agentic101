from mcp.server.fastmcp import FastMCP
import github_client
from schemas import IssueSummary, summarize

mcp = FastMCP("github_issues")

MAX_ISSUES = 50       # policy constants: yours to tune, not the model's
BODY_PREVIEW = 500
SEARCH_PREVIEW = 200
FULL_BODY = 8000      # still capped: some bodies are pasted logs

@mcp.tool()
def list_open_issues(repo: str) -> list[IssueSummary]:
    f"""List open issues (not pull requests) for a repo as summaries: number,
    title, labels, comment/reaction counts, dates, and the first {BODY_PREVIEW} characters
    of the body. Use get_issue to read one issue in full."""
    return [summarize(i, BODY_PREVIEW)
            for i in github_client.list_open_issues(repo, MAX_ISSUES)]

@mcp.tool()
def get_issue(repo: str, number: int) -> IssueSummary:
    """Fetch one issue with its full body text if more details were needed."""
    return summarize(github_client.get_issue(repo, number), FULL_BODY)

@mcp.tool()
def search_issues(repo: str, keywords: str) -> list[IssueSummary]:
    """Search open AND closed issues in this repo for possible duplicates.
    Pass 2-4 distinctive keywords from the new issue's title, not its whole body."""
    return [summarize(i, SEARCH_PREVIEW)
            for i in github_client.search_issues(repo, keywords)]

if __name__ == "__main__":
    mcp.run()

