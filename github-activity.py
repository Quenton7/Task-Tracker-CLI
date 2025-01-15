import sys
import urllib.request
import json

def fetch_github_activity(username):
    """
    Fetch and display the recent activity of a GitHub user.
    """
    url = f"https://api.github.com/users/{username}/events"
    try:
        # Make the HTTP request to the GitHub API
        with urllib.request.urlopen(url) as response:
            # Parse the JSON response
            data = json.load(response)
            display_activity(data)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: User '{username}' not found.")
        else:
            print(f"Error: Unable to fetch data from GitHub. (HTTP {e.code})")
    except urllib.error.URLError as e:
        print(f"Error: Failed to connect to GitHub API. ({e.reason})")
    except Exception as e:
        print(f"Unexpected error: {e}")

def display_activity(events):
    """
    Parse and display user activity from the GitHub API response.
    """
    if not events:
        print("No recent activity found.")
        return
    
    for event in events:
        event_type = event.get("type", "UnknownEvent")
        repo_name = event["repo"]["name"]
        
        # Match event type to display a meaningful message
        if event_type == "PushEvent":
            commit_count = len(event["payload"]["commits"])
            print(f"- Pushed {commit_count} commits to {repo_name}")
        elif event_type == "CreateEvent":
            ref_type = event["payload"].get("ref_type", "repository")
            ref = event["payload"].get("ref", "")
            if ref_type == "repository":
                print(f"- Created a new repository: {repo_name}")
            elif ref_type == "branch":
                print(f"- Created a branch '{ref}' in {repo_name}")
            else:
                print(f"- Created a new {ref_type} in {repo_name}")
        elif event_type == "IssuesEvent":
            action = event["payload"].get("action", "performed")
            print(f"- {action.capitalize()} an issue in {repo_name}")
        elif event_type == "WatchEvent":
            print(f"- Starred {repo_name}")
        else:
            print(f"- Performed {event_type} on {repo_name}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: github-activity <username>")
        sys.exit(1)

    username = sys.argv[1]
    fetch_github_activity(username)