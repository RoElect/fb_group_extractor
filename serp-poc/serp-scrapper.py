from serpapi import GoogleSearch
import pandas as pd
import time

# Introdu API Key-ul tău de la SerpAPI
API_KEY = "YOUR_API_KEY"

def google_search(query):
    params = {
        "q": query,
        "hl": "ro",
        "gl": "ro",
        "api_key": API_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    data = []
    for result in results.get("organic_results", []):
        link = result.get("link", "")
        title = result.get("title", "")
        data.append((title, link))

    return data

# Lista orașelor și cuvintelor cheie
locations = ["Bucuresti", "Cluj-Napoca", "Timisoara", "Iasi", "Brasov"]
keywords = ["grup Facebook", "comunitate", "locuitori", "forum"]

data = []
for location in locations:
    for keyword in keywords:
        query = f"{location} {keyword} site:facebook.com/groups"
        print(f"Searching: {query}")
        results = google_search(query)
        for title, link in results:
            data.append([location, title, link])
        time.sleep(1)  # Evită să trimiți prea multe cereri simultan

# Salvare în CSV
if data:
    df = pd.DataFrame(data, columns=["Location", "Title", "Link"])
    df.to_csv("facebook_groups.csv", index=False)
    print("Results saved to facebook_groups.csv")
else:
    print("No results found.")
