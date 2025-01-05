### pip install requests beautifulsoup4 ###

import requests
import re
from bs4 import BeautifulSoup

# TODO add all URLs of the wanted muscle group exercises list
URLS = [
    "https://fitnessprogramer.com/exercise-primary-muscle/neck/",
    "https://fitnessprogramer.com/exercise-primary-muscle/trapezius/",
    "https://fitnessprogramer.com/exercise-primary-muscle/shoulders/",
    "https://fitnessprogramer.com/exercise-primary-muscle/chest/",
    "https://fitnessprogramer.com/exercise-primary-muscle/back/",
    "https://fitnessprogramer.com/exercise-primary-muscle/erector-spinae/",
    "https://fitnessprogramer.com/exercise-primary-muscle/biceps/",
    "https://fitnessprogramer.com/exercise-primary-muscle/triceps/",
    "https://fitnessprogramer.com/exercise-primary-muscle/forearm/",
    "https://fitnessprogramer.com/exercise-primary-muscle/abs/",
    "https://fitnessprogramer.com/exercise-primary-muscle/leg/",
    "https://fitnessprogramer.com/exercise-primary-muscle/calf/",
    "https://fitnessprogramer.com/exercise-primary-muscle/hip/",
    "https://fitnessprogramer.com/exercise-primary-muscle/cardio/",
    "https://fitnessprogramer.com/exercise-primary-muscle/full-body/",
]

def scrape_exercises(base_url):
    page = 1
    exercises = []

    while True:
        # Construct the URL for the current page
        url = f"{base_url}page/{page}/" if page > 1 else base_url
        print(f"Scraping {url}...")  # Optional: Track progress

        # Fetch the webpage content
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

        # Break the loop if the page does not exist or cannot be retrieved
        if response.status_code != 200:
            print(f"Reached end of pages or encountered an error. Status code: {response.status_code}")
            break

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all articles with IDs starting with 'exercise-'
        exercise_articles = soup.find_all('article', id=re.compile(r'^exercise-\d+$'))

        # Break the loop if no exercises are found on the page
        if not exercise_articles:
            print("No more exercises found on this page.")
            break

        # Extract exercise details
        for article in exercise_articles:
            # Extract the exercise title
            title_tag = article.find('h2', class_='title')
            title = title_tag.get_text(strip=True) if title_tag else 'Unknown Title'

            # Extract the GIF link
            img_tag = article.find('img')
            gif_link = img_tag['src'] if img_tag else 'No GIF Link'

            # Store the data
            exercises.append({'title': title, 'gif_link': gif_link})

        # Increment the page counter
        page += 1

    return exercises

def generate_lower_name(title):
    # Remove non-alphanumeric characters and replace spaces with hyphens
    normalized = re.sub(r'[^a-zA-Z0-9\s]', '', title)  # Remove special characters
    normalized = re.sub(r'\s+', '-', normalized.strip())  # Replace spaces with hyphens
    return normalized.lower()

# Step 1: Scrape all exercises
all_exercises = []
for url in URLS:
    all_exercises.extend(scrape_exercises(url))

# Step 2: Remove duplicates from the global list
unique_exercises = {generate_lower_name(ex['title']): ex for ex in all_exercises}.values()

# Step 3: Generate the EXERCISE_CHOICES list
with open('EXERCISE_CHOICES.txt', 'w') as file:
    file.write("EXERCISE_CHOICES = [\n")
    for exercise in unique_exercises:
        entry = f'\tapp_commands.Choice(name="{exercise["title"]}", value="{generate_lower_name(exercise["title"])}"),\n'
        file.write(entry)
    file.write("]")

# Step 4: Generate the EXERCISE_META dict
with open('EXERCISE_META.txt', 'w') as file:
    file.write("EXERCISE_META = {\n")
    for exercise in unique_exercises:
        file.write(f'\t\"{generate_lower_name(exercise["title"])}\"')
        file.write(": {\n")
        file.write(f"\t\t\"image\": \"{exercise['gif_link']}\",\n")
        file.write(f"\t\t\"pretty-name\": \"{exercise['title']}\",\n")
        file.write("\t},\n")
    file.write("}")

print(f"generated {len(unique_exercises)} unique exercises")
