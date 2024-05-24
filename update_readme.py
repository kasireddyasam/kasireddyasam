import requests
from bs4 import BeautifulSoup

def fetch_leetcode_stats(username):
    url = f"https://leetcode-stats-api.herokuapp.com/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def fetch_interviewbit_stats(username):
    url = f"https://www.interviewbit.com/profile/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        stats = {
            "rank": soup.find("div", {"class": "stat"})[0].text.strip(),
            "score": soup.find("div", {"class": "stat"})[1].text.strip(),
            "problems_solved": soup.find("div", {"class": "stat"})[2].text.strip(),
            "streak": soup.find("div", {"class": "stat"})[3].text.strip()
        }
        return stats
    else:
        return None

def update_readme(leetcode_stats, interviewbit_stats):
    readme_path = "README.md"
    with open(readme_path, "r") as file:
        content = file.readlines()

    start_idx = content.index("<!-- LEETCODE-STATS:START -->\n") + 1
    end_idx = content.index("<!-- LEETCODE-STATS:END -->\n")

    new_content = [
        '<div align="center" style="border: 2px solid #e1e4e8; border-radius: 8px; padding: 20px; background-color: #1e1e2e; color: #e1e4e8;">\n',
        '  <h2 style="color: #f0db4f;">Leetcode Data</h2>\n',
        '  <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; gap: 20px;">\n',
        '    <div style="text-align: center; color: #61dafb;">\n',
        '      <div style="font-size: 24px;">All</div>\n',
        f'      <div style="font-size: 32px; font-weight: bold;">{leetcode_stats["totalSolved"]}</div>\n',
        f'      <div>{leetcode_stats["totalQuestions"]}</div>\n',
        '    </div>\n',
        '    <button style="background-color: #e74c3c; border: none; padding: 10px 20px; border-radius: 4px; color: white; cursor: pointer;">Remove</button>\n',
        '  </div>\n',
        '  <div style="margin-top: 16px;">\n',
        '    <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 8px;">\n',
        '      <div style="background-color: #27ae60; color: white; padding: 4px 8px; border-radius: 4px;">Easy</div>\n',
        f'      <div style="margin-left: 8px;">{leetcode_stats["easySolved"]} / {leetcode_stats["totalEasy"]}</div>\n',
        '    </div>\n',
        '    <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 8px;">\n',
        '      <div style="background-color: #f39c12; color: white; padding: 4px 8px; border-radius: 4px;">Medium</div>\n',
        f'      <div style="margin-left: 8px;">{leetcode_stats["mediumSolved"]} / {leetcode_stats["totalMedium"]}</div>\n',
        '    </div>\n',
        '    <div style="display: flex; justify-content: center; align-items: center;">\n',
        '      <div style="background-color: #c0392b; color: white; padding: 4px 8px; border-radius: 4px;">Hard</div>\n',
        f'      <div style="margin-left: 8px;">{leetcode_stats["hardSolved"]} / {leetcode_stats["totalHard"]}</div>\n',
        '    </div>\n',
        '  </div>\n',
        '</div>\n',
        '<br>\n',
        '<div align="center" style="border: 2px solid #e1e4e8; border-radius: 8px; padding: 20px; background-color: #1e1e2e; color: #e1e4e8;">\n',
        '  <h2 style="color: #f0db4f;">InterviewBit Data</h2>\n',
        '  <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; gap: 20px;">\n',
        '    <div style="text-align: center; color: #61dafb;">\n',
        '      <div style="font-size: 24px;">Rank</div>\n',
        f'      <div style="font-size: 32px; font-weight: bold;">{interviewbit_stats["rank"]}</div>\n',
        '    </div>\n',
        '    <div style="text-align: center; color: #61dafb;">\n',
        '      <div style="font-size: 24px;">Score</div>\n',
        f'      <div style="font-size: 32px; font-weight: bold;">{interviewbit_stats["score"]}</div>\n',
        '    </div>\n',
        '    <div style="text-align: center; color: #61dafb;">\n',
        '      <div style="font-size: 24px;">Problems Solved</div>\n',
        f'      <div style="font-size: 32px; font-weight: bold;">{interviewbit_stats["problems_solved"]}</div>\n',
        '    </div>\n',
        '    <div style="text-align: center; color: #61dafb;">\n',
        '      <div style="font-size: 24px;">Streak</div>\n',
        f'      <div style="font-size: 32px; font-weight: bold;">{interviewbit_stats["streak"]}</div>\n',
        '    </div>\n',
        '  </div>\n',
        '</div>\n'
    ]

    content = content[:start_idx] + new_content + content[end_idx:]

    with open(readme_path, "w") as file:
        file.writelines(content)

if __name__ == "__main__":
    leetcode_username = "kasireddy_13177"  # LeetCode username
    interviewbit_username = "Kasireddy Asam"  # InterviewBit username

    leetcode_stats = fetch_leetcode_stats(leetcode_username)
    interviewbit_stats = fetch_interviewbit_stats(interviewbit_username)

    if leetcode_stats and interviewbit_stats:
        update_readme(leetcode_stats, interviewbit_stats)
    else:
        print("Failed to fetch LeetCode or InterviewBit stats")

