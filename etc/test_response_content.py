# test_api_snapshots.py
import json
from pathlib import Path
from difflib import unified_diff

# Define paths (replace with your actual snapshot storage)
SNAPSHOT_DIR = Path(__file__).parent.parent / "responses"

def get_normalized_response_lines(response_data):
    """Parses, normalizes (sorts JSON keys), and returns response as lines."""
    # Assuming response_data is a JSON string or dict
    if isinstance(response_data, str):
        data = json.loads(response_data)
    else:
        data = response_data # Assume it's already a dict/list

    # Normalize JSON by sorting keys
    normalized_json = json.dumps(data, sort_keys=True, indent=2)
    return normalized_json.splitlines(keepends=True) # Keepends is good for diff

def test_get_users_snapshot(api_client, user_id):
    """Tests /users/{user_id} endpoint against a snapshot."""
    response = api_client.get(f"/users/{user_id}")
    response.raise_for_status() # Check for HTTP errors

    # Get current response lines
    current_lines = get_normalized_response_lines(response.json())

    # Define snapshot file path
    snapshot_file = SNAPSHOT_DIR / f"user_{user_id}.json.snap"

    # Load or create snapshot
    if snapshot_file.exists():
        expected_lines = snapshot_file.read_text().splitlines(keepends=True)
    else:
        # First run: Create the snapshot (no diff to check)
        print(f"Creating snapshot: {snapshot_file}")
        snapshot_file.write_text("".join(current_lines))
        expected_lines = current_lines # Treat as expected for this run

    # Generate unified diff
    diff_lines = list(unified_diff(
        expected_lines,
        current_lines,
        fromfile='expected',
        tofile='actual',
        lineterm='' # Avoid extra newlines in diff output
    ))

    # Assert no differences (or display diff if failed)
    assert not diff_lines, f"Response changed:\n{''.join(diff_lines)}"

    # If the test passes and you *want* to update the snapshot,
    # you'd manually run a command to update the .snap file
    # or add a flag (e.g., --update

