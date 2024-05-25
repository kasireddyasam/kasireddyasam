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
    
    if response.status_code != 200:
        raise ConnectionError(f"Failed to connect to InterviewBit. Status code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    try:
        easy_div = soup.find("div", class_="profile-progress-card_stat profile-progress-card_stat--easy")
        medium_div = soup.find("div", class_="profile-progress-card_stat profile-progress-card_stat--medium")
        hard_div = soup.find("div", class_="profile-progress-card_stat profile-progress-card_stat--hard")
        total_div = soup.find("div", class_="profile-progress-card_stat profile-progress-card_stat--total")
        
        if easy_div is None or medium_div is None or hard_div is None or total_div is None:
            raise AttributeError("Failed to find one or more elements on the InterviewBit profile page.")
        
        easy_solved = easy_div.find_all("span")[1].text.strip()
        medium_solved = medium_div.find_all("span")[1].text.strip()
        hard_solved = hard_div.find_all("span")[1].text.strip()
        total_solved = total_div.find_all("span")[1].text.strip()
        
        stats = {
            "easy": easy_solved,
            "medium": medium_solved,
            "hard": hard_solved,
            "total": total_solved
        }
        return stats

    except AttributeError as e:
        raise AttributeError("Failed to find the necessary elements on the InterviewBit profile page. The page structure might have changed.") from e

def update_readme(leetcode_stats, interviewbit_stats):
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

    # Update InterviewBit stats
    interviewbit_start_idx = content.index("## InterviewBit Progress\n") + 1
    interviewbit_end_idx = interviewbit_start_idx + 4

    interviewbit_content = [
        f"![InterviewBit Progress](https://img.shields.io/badge/Easy-{interviewbit_stats['easy']}-green?style=flat-square)\n",
        f"![InterviewBit Progress](https://img.shields.io/badge/Medium-{interviewbit_stats['medium']}-yellow?style=flat-square)\n",
        f"![InterviewBit Progress](https://img.shields.io/badge/Hard-{interviewbit_stats['hard']}-red?style=flat-square)\n",
        f"![InterviewBit Progress](https://img.shields.io/badge/Total-{interviewbit_stats['total']}-blue?style=flat-square)\n"
    ]

    content = content[:interviewbit_start_idx] + interviewbit_content + content[interviewbit_end_idx:]

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




