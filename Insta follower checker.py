import json
import sys
from pathlib import Path
 
 
def load_following(filepath: Path) -> set[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
 
    usernames = set()
    for item in data.get("relationships_following", []):
        title = item.get("title")
        if title:
            usernames.add(title)
    return usernames
 
 
def load_followers(filepath: Path) -> set[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
 
    usernames = set()
    for item in data:
        for entry in item.get("string_list_data", []):
            value = entry.get("value")
            if value:
                usernames.add(value)
    return usernames
 
 
def find_files(pattern: str) -> list[Path]:
    matches = list(Path(__file__).parent.rglob(pattern))
    if not matches:
        print(f"Error: Could not find any file matching '{pattern}' in the current directory or subfolders.")
        sys.exit(1)
    return matches
 
 
def main():
    following_files = find_files("following.json")
    followers_files = find_files("followers_*.json")
 
    following = set()
    for path in following_files:
        following |= load_following(path)
        print(f"Loaded following file:  {path}")
 
    followers = set()
    for path in followers_files:
        followers |= load_followers(path)
        print(f"Loaded followers file:  {path}")
 
    print(f"\nYou follow:       {len(following)} accounts")
    print(f"Followers of you: {len(followers)} accounts\n")
 
    not_following_back = sorted(following - followers)
 
    print(f"{'='*45}")
    print(f"  People who don't follow you back: {len(not_following_back)}")
    print(f"{'='*45}")
 
    if not_following_back:
        for username in not_following_back:
            print(f"  @{username}")
    else:
        print("  Everyone you follow also follows you back!")
 
    print(f"{'='*45}")
 
 
if __name__ == "__main__":
    main()
