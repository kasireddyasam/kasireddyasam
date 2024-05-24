import requests

def fetch_leetcode_stats(username):
    url = f"https://leetcode-stats-api.herokuapp.com/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def update_readme(stats):
    readme_path = "README.md"
    with open(readme_path, "r") as file:
        content = file.readlines()

    start_idx = content.index("<!-- LEETCODE-STATS:START -->\n") + 1
    end_idx = content.index("<!-- LEETCODE-STATS:END -->\n")

    new_content = [
        '<div align="center" style="border: 2px solid #e1e4e8; border-radius: 8px; padding: 20px; background-color: #1c1c1c; color: #e1e4e8;">\n',
        '  <h2 style="color: #f0db4f;">Leetcode Data</h2>\n',
        '  <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; gap: 20px;">\n',
        '    <div style="text-align: center;">\n',
        '      <div style="font-size: 24px; color: #61dafb;">All</div>\n',
        f'      <div style="font-size: 32px; font-weight: bold;">{stats["totalSolved"]}</div>\n',
        f'      <div style="color: #61dafb;">{stats["totalQuestions"]}</div>\n',
        '    </div>\n',
        '    <button style="background-color: #e74c3c; border: none; padding: 10px 20px; border-radius: 4px; color: white; cursor: pointer;">Remove</button>\n',
        '  </div>\n',
        '  <div style="margin-top: 16px;">\n',
        '    <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 8px;">\n',
        '      <div style="background-color: #27ae60; color: white; padding: 4px 8px; border-radius: 4px;">Easy</div>\n',
        f'      <div style="margin-left: 8px;">{stats["easySolved"]} / {stats["totalEasy"]}</div>\n',
        '    </div>\n',
        '    <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 8px;">\n',
        '      <div style="background-color: #f39c12; color: white; padding: 4px 8px; border-radius: 4px;">Medium</div>\n',
        f'      <div style="margin-left: 8px;">{stats["mediumSolved"]} / {stats["totalMedium"]}</div>\n',
        '    </div>\n',
        '    <div style="display: flex; justify-content: center; align-items: center;">\n',
        '      <div style="background-color: #c0392b; color: white; padding: 4px 8px; border-radius: 4px;">Hard</div>\n',
        f'      <div style="margin-left: 8px;">{stats["hardSolved"]} / {stats["totalHard"]}</div>\n',
        '    </div>\n',
        '  </div>\n',
        '</div>\n'
    ]

    content = content[:start_idx] + new_content + content[end_idx:]

    with open(readme_path, "w") as file:
        file.writelines(content)

if __name__ == "__main__":
    username = "kasireddy_13177"  # LeetCode username
    stats = fetch_leetcode_stats(username)
    if stats:
        update_readme(stats)
    else:
        print("Failed to fetch LeetCode stats")



