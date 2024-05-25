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
        
        try:
            easy = soup.find("div", {"class": "profile-progress-card_stat profile-progress-card_stat--easy"}).find_all("span")[1].text.strip()
            medium = soup.find("div", {"class": "profile-progress-card_stat profile-progress-card_stat--medium"}).find_all("span")[1].text.strip()
            hard = soup.find("div", {"class": "profile-progress-card_stat profile-progress-card_stat--hard"}).find_all("span")[1].text.strip()
            total = soup.find("div", {"class": "profile-progress-card_stat profile-progress-card_stat--total"}).find_all("span")[1].text.strip()
            
            stats = {
                "easy": easy,
                "medium": medium,
                "hard": hard,
                "total": total
            }
            return stats

        except AttributeError as e:
            raise AttributeError("Failed to find the necessary elements on the InterviewBit profile page. The page structure might have changed.") from e
    else:
        return None

def update_readme(leetcode_stats, interviewbit_stats):
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
        f'      <div style="font-size: 32px; font-weight: bold;">{leetcode_stats["totalSolved"]}</div>\n',
        f'      <div style="color: #61dafb;">{leetcode_stats["totalQuestions"]}</div>\n',
        '    </div>\n',
        '    <div style="text-align: center;">\n',
        '      <div style="background-color: #27ae60; color: white; padding: 4px 8px; border-radius: 4px;">Easy</div>\n',
        f'      <div style="margin-left: 8px;">{leetcode_stats["easySolved"]} / {leetcode_stats["totalEasy"]}</div>\n',
        '    </div>\n',
        '    <div style="text-align: center;">\n',
        '      <div style="background-color: #f39c12; color: white; padding: 4px 8px; border-radius: 4px;">Medium</div>\n',
        f'      <div style="margin-left: 8px;">{leetcode_stats["mediumSolved"]} / {leetcode_stats["totalMedium"]}</div>\n',
        '    </div>\n',
        '    <div style="text-align: center;">\n',
        '      <div style="background-color: #c0392b; color: white; padding: 4px 8px; border-radius: 4px;">Hard</div>\n',
        f'      <div style="margin-left: 8px;">{leetcode_stats["hardSolved"]} / {leetcode_stats["totalHard"]}</div>\n',
        '    </div>\n',
        '  </div>\n',
        '</div>\n',
        '<br>\n',
        '<div align="center" style="border: 2px solid #e1e4e8; border-radius: 8px; padding: 20px; background-color: #1c1c1c; color: #e1e4e8;">\n',
        '  <h2 style="color: #f0db4f;">InterviewBit Data</h2>\n',
        '  <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; gap: 20px;">\n',
        '    <div style="text-align: center;">\n',
        '      <div style="font-size: 24px; color: #61dafb;">Easy</div>\n',
        f'      <div style="font-size: 32px; font-weight: bold;">{interviewbit_stats["easy"]}</div>\n',
        '    </div>\n',
        '    <div style="text-align: center;">\n',
        '      <div style="font-size: 24px; color: #61dafb;">Medium</div>\n',
        f'      <div style="font-size: 32px; font-weight: bold;">{interviewbit_stats["medium"]}</div>\n',
        '    </div>\n',
        '    <div style="text-align: center;">\n',
        '      <div style="font-size: 24px; color: #61dafb;">Hard</div>\n',
        f'      <div style="font-size: 32px; font-weight: bold;">{interviewbit_stats["hard"]}</div>\n',
        '    </div>\n',
        '    <div style="text-align: center;">\n',
        '      <div style="font-size: 24px; color: #61dafb;">Total</div>\n',
        f'      <div style="font-size: 32px; font-weight: bold;">{interviewbit_stats["total"]}</div>\n',
        '    </div>\n',
        '  </div>\n',
        '</div>\n'
    ]

    content = content[:start_idx] + new_content + content[end_idx:]

    with open(readme_path, "w") as file:
        file.writelines(content)

if __name__ == "__main__":
    leetcode_username = "kasireddy_13177"  # LeetCode username
    interviewbit_username = "kasireddy-asam"  # InterviewBit username

    leetcode_stats = fetch_leetcode_stats(leetcode_username)
    interviewbit_stats = fetch_interviewbit_stats(interviewbit_username)

    if leetcode_stats and interviewbit_stats:
        update_readme(leetcode_stats, interviewbit_stats)
    else:
        print("Failed to fetch LeetCode or InterviewBit stats")


