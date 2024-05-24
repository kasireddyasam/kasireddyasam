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
        '<div align="center" style="border: 1px solid #e1e4e8; border-radius: 6px; padding: 16px; background-color: #282c34; color: white;">\n',
        '  <h2>Leetcode Data</h2>\n',
        '  <div style="display: flex; flex-direction: column; align-items: center;">\n',
        '    <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 16px;">\n',
        '      <div style="text-align: center; margin-right: 16px;">\n',
        '        <div style="font-size: 24px;">All</div>\n',
        f'        <div style="font-size: 32px; font-weight: bold;">{stats["totalSolved"]}</div>\n',
        f'        <div>{stats["totalQuestions"]}</div>\n',
        '      </div>\n',
        '      <button style="background-color: #ff4d4f; border: none; padding: 10px 20px; border-radius: 4px; color: white; cursor: pointer;">Remove</button>\n',
        '    </div>\n',
        '    <div style="width: 100%; display: flex; justify-content: space-around;">\n',
        '      <div style="display: flex; flex-direction: column; align-items: center;">\n',
        '        <div style="background-color: green; color: white; padding: 4px 8px; border-radius: 4px;">Easy</div>\n',
        f'        <div style="margin-top: 4px;">{stats["easySolved"]} / {stats["totalEasy"]}</div>\n',
        '      </div>\n',
        '      <div style="display: flex; flex-direction: column; align-items: center;">\n',
        '        <div style="background-color: orange; color: white; padding: 4px 8px; border-radius: 4px;">Medium</div>\n',
        f'        <div style="margin-top: 4px;">{stats["mediumSolved"]} / {stats["totalMedium"]}</div>\n',
        '      </div>\n',
        '      <div style="display: flex; flex-direction: column; align-items: center;">\n',
        '        <div style="background-color: red; color: white; padding: 4px 8px; border-radius: 4px;">Hard</div>\n',
        f'        <div style="margin-top: 4px;">{stats["hardSolved"]} / {stats["totalHard"]}</div>\n',
        '      </div>\n',
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



