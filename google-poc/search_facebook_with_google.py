import requests
import csv
import re
import time

# Your Custom Search API credentials
API_KEY = "Your API KEY ID"
CX_ID = "Your CX ID"

# Variables
locations = ["Bucuresti", "Craiova", "Cluj"]
query_params = ["", "Vanzari", "Meseriasi"]

# Function to call the Google Custom Search API
def google_search(query, api_key, cx_id, start_index=1):
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX_ID}&q={query}&start={start}"
    import requests
    response = requests.get(url=url).json()
    return response.get("items", [])

groups_with_10k_followers = []

for location in locations:
    for query in query_params:
        full_query = f"{location} {query} site:facebook.com/groups"

        start_index = 1
        while start_index <= 100:  # Google Custom Search API allows maximum 100 results (10 pages, 10 results each)
            response = requests.get(
                f"https://www.googleapis.com/customsearch/v1",
                params={
                    "key": API_KEY,
                    "cx": CX_ID,
                    "q": full_query,
                    "start": start_index
                }
            ).json()

            results = response.get("items", [])
            if not results:
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

            start_index += 10  # Next page (each page returns max 10 results)
            time.sleep(1)  # delay to respect API rate limit

# Export results to CSV
with open('facebook_groups_api.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['location', 'query', 'title', 'url', 'followers']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for group in groups_with_10k_followers:
        writer.writerow(group)

print(f"Exported {len(groups_with_10k_followers)} groups to facebook_groups_api.csv")

