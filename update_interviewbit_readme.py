from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def fetch_interviewbit_stats(username):
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Initialize the ChromeDriver using webdriver_manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    url = f"https://www.interviewbit.com/profile/{username}"
    driver.get(url)
    
    try:
        # Locate the "Problems Solved" section
        problems_solved_section = driver.find_element(By.CLASS_NAME, 'profile-progress-card__data')

        easy_solved = problems_solved_section.find_element(By.CLASS_NAME, 'profile-progress-card__stat--easy').find_elements(By.TAG_NAME, 'span')[1].text.strip()
        medium_solved = problems_solved_section.find_element(By.CLASS_NAME, 'profile-progress-card__stat--medium').find_elements(By.TAG_NAME, 'span')[1].text.strip()
        hard_solved = problems_solved_section.find_element(By.CLASS_NAME, 'profile-progress-card__stat--hard').find_elements(By.TAG_NAME, 'span')[1].text.strip()
        total_solved = problems_solved_section.find_element(By.CLASS_NAME, 'profile-progress-card__stat--total').find_elements(By.TAG_NAME, 'span')[1].text.strip()
        
        stats = {
            "easy": easy_solved,
            "medium": medium_solved,
            "hard": hard_solved,
            "total": total_solved
        }
        return stats

    except Exception as e:
        print("Failed to fetch the necessary elements on the InterviewBit profile page.")
        print(e)
        return None

    finally:
        driver.quit()

def update_readme(interviewbit_stats):
    readme_path = "README.md"
    with open(readme_path, "r") as file:
        content = file.readlines()

    # Locate the section for InterviewBit Progress
    interviewbit_start_idx = None
    for idx, line in enumerate(content):
        if line.strip() == "## InterviewBit Progress":
            interviewbit_start_idx = idx + 1
            break

    if interviewbit_start_idx is not None:
        interviewbit_end_idx = interviewbit_start_idx + 4
        interviewbit_content = [
            f"![InterviewBit Progress](https://img.shields.io/badge/Easy-{interviewbit_stats['easy']}-green?style=flat-square)\n",
            f"![InterviewBit Progress](https://img.shields.io/badge/Medium-{interviewbit_stats['medium']}-yellow?style=flat-square)\n",
            f"![InterviewBit Progress](https://img.shields.io/badge/Hard-{interviewbit_stats['hard']}-red?style=flat-square)\n",
            f"![InterviewBit Progress](https://img.shields.io/badge/Total-{interviewbit_stats['total']}-blue?style=flat-square)\n"
        ]
        content[interviewbit_start_idx:interviewbit_end_idx] = interviewbit_content

        with open(readme_path, "w") as file:
            file.writelines(content)

# Use your InterviewBit username
interviewbit_username = "kasireddy-asam"

# Fetch InterviewBit stats
interviewbit_stats = fetch_interviewbit_stats(interviewbit_username)

# Update README if stats were fetched successfully
if interviewbit_stats:
    update_readme(interviewbit_stats)
else:
    print("Failed to fetch InterviewBit stats")
