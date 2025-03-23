import requests
import csv
import re
import time
import sys

# Your Custom Search API credentials
API_KEY = "AIzaSyAiZYKvcyz5AVUqS07BnhAmcsuGiYqjbwY"
CX_ID = "024efef60ebdf492d"

# Default values
DEFAULT_LOCATIONS = ["Bucuresti", "Craiova", "Cluj"]
DEFAULT_QUERY_PARAMS = ["", "Vanzari", "Meseriasi"]

# Function to read data from file
def read_from_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"⚠️  Fișierul '{filename}' nu a fost găsit. Se folosesc valorile implicite.")
        return None

# Read file names from command-line arguments
locations_file = sys.argv[1] if len(sys.argv) > 1 else None
queries_file = sys.argv[2] if len(sys.argv) > 2 else None

# Load locations and query params from files or use defaults
locations = read_from_file(locations_file) if locations_file else DEFAULT_LOCATIONS
query_params = read_from_file(queries_file) if queries_file else DEFAULT_QUERY_PARAMS

if locations_file is None or queries_file is None:
    print("\nℹ️  Poți rula scriptul cu parametrii pentru a folosi liste personalizate:")
    print("   python3 search_facebook_with_google.py <locations_file> <queries_file>\n")

groups_with_10k_followers = []

for location in locations:
    for query in query_params:
        full_query = f"{location} {query} site:facebook.com/groups"

        print(f"\n🔍 Searching for groups in '{location}' with keyword '{query}'...\n")

        start_index = 1
        while start_index <= 100:
            loading_animation = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
            print(f"   {loading_animation[start_index % len(loading_animation)]} Querying page {start_index // 10 + 1}...", end="\r", flush=True)

            response = requests.get(
                "https://www.googleapis.com/customsearch/v1",
                params={
                    "key": API_KEY,
                    "cx": CX_ID,
                    "q": full_query,
                    "start": start_index
                }
            ).json()

            results = response.get("items", [])
            if not results:
                print(f"⚠️  No more results found for '{location}' with '{query}'\n")
                break  # No more results

            for result in results:
                title = result.get("title")
                snippet = result.get("snippet", "")
                url = result.get("link")

                # Check snippet for follower/member count
                match = re.search(r'(\d+[,.]?\d*)[ ]?(K|M)?[ ]?(members|followers)', snippet, re.I)
                if match:
                    count = match.group(1)
                    unit = match.group(2)

                    count = float(count.replace(",", ""))

                    # Convert to number
                    if unit and unit.upper() == "K":
                        count *= 1000
                    elif unit and unit.upper() == "M":
                        count *= 1000000

                    # Filter groups with more than 10k followers
                    if count >= 10000:
                        groups_with_10k_followers.append({
                            'location': location,
                            'query': query,
                            'title': title,
                            'url': url,
                            'followers': int(count)
                        })

            start_index += 10
            time.sleep(1)  # delay to respect API rate limit

# Export results to CSV
with open('facebook_groups_api.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['location', 'query', 'title', 'url', 'followers']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for group in groups_with_10k_followers:
        writer.writerow(group)

print(f"\n✅ Exported {len(groups_with_10k_followers)} groups to facebook_groups_api.csv\n")
