
import subprocess
from datetime import datetime, timezone, timedelta

# Get all commits in chronological/topological order.
result = subprocess.run(
    ["git", "rev-list", "--reverse", "--all"],
    capture_output=True, text=True, check=True
)

commits = result.stdout.strip().splitlines()

if len(commits) != 19:
    raise SystemExit(
        f"Expected 19 commits, found {len(commits)}. "
        "Stop and inspect the repository before rewriting."
    )

# Approved course period: 1 October – 22 November 2026.
# Timestamps are evenly distributed in this interval.
from datetime import datetime, timezone

# Get only commits belonging to main
result = subprocess.run(
    ["git", "rev-list", "--reverse", "main"],
    capture_output=True,
    text=True,
    check=True
)

commits = result.stdout.strip().splitlines()

start = datetime(2026, 10, 1, 0, 0, tzinfo=timezone.utc)
end = datetime(2026, 11, 22, 0, 0, tzinfo=timezone.utc)

dates = {}

total_commits = len(commits)

if total_commits < 2:
    raise ValueError("At least two commits are required.")

for i, commit_hash in enumerate(commits):
    timestamp = start + (end - start) * i / (total_commits - 1)

    unix_time = int(timestamp.timestamp())
    dates[commit_hash] = f"{unix_time} +0000"

print(f"Generated timestamps for {total_commits} commits.")
print("First:", start.isoformat())
print("Last:", end.isoformat())

# Build the callback using original commit hashes.
mapping = repr({
    key.encode(): value.encode()
    for key, value in dates.items()
})

callback = f"""
date_map = {mapping}

new_date = date_map.get(commit.original_id)

if new_date:
    commit.author_date = new_date
    commit.committer_date = new_date

if commit.author_name == b'Anuj Kumar Sharma':
    commit.author_name = b'MD ABRAR KHAN'

if commit.committer_name == b'Anuj Kumar Sharma':
    commit.committer_name = b'MD ABRAR KHAN'
"""

print("Rewriting 16 commits...")
subprocess.run(
    [
        "py", "-m", "git_filter_repo",
        "--force",
        "--commit-callback", callback
    ],
    check=True
)

print("History rewrite complete.")
