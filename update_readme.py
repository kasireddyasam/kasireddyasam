import requests

def fetch_leetcode_stats(username):
    url = f"https://leetcode-stats-api.herokuapp.com/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def update_readme(leetcode_stats):
    readme_path = "README.md"
    with open(readme_path, "r") as file:
        content = file.readlines()

    # Update LeetCode stats
    leetcode_start_idx = content.index("## LeetCode Progress\n") + 1
    leetcode_end_idx = leetcode_start_idx + 4

    leetcode_content = [
        f"![LeetCode Progress](https://img.shields.io/badge/Easy-{leetcode_stats['easySolved']}-green?style=flat-square)\n",
        f"![LeetCode Progress](https://img.shields.io/badge/Medium-{leetcode_stats['mediumSolved']}-yellow?style=flat-square)\n",
        f"![LeetCode Progress](https://img.shields.io/badge/Hard-{leetcode_stats['hardSolved']}-red?style=flat-square)\n",
        f"![LeetCode Progress](https://img.shields.io/badge/Total-{leetcode_stats['totalSolved']}-blue?style=flat-square)\n"
    ]

    content = content[:leetcode_start_idx] + leetcode_content + content[leetcode_end_idx:]

    with open(readme_path, "w") as file:
        file.writelines(content)

if __name__ == "__main__":
    leetcode_username = "kasireddy_13177"  # LeetCode username

    leetcode_stats = fetch_leetcode_stats(leetcode_username)

    if leetcode_stats:
        update_readme(leetcode_stats)
    else:
        print("Failed to fetch LeetCode stats")





