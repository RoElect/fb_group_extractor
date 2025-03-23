import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import requests
import csv
import re
import time

# Default values
API_KEY = "Your API KEY ID"
CX_ID = "Your CX ID"

def select_file(entry_widget):
    filename = filedialog.askopenfilename()
    if filename:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, filename)

def update_status(message):
    status_text.config(state=tk.NORMAL)
    status_text.insert(tk.END, message + "\n")
    status_text.see(tk.END)
    status_text.config(state=tk.DISABLED)

def animate_loading():
    symbols = [".", "..", "..."]
    index = 0
    while loading_flag:
        loading_label.config(text=f"Searching{symbols[index]}")
        index = (index + 1) % len(symbols)
        time.sleep(0.5)
        root.update_idletasks()

def run_scraper():
    global loading_flag
    location_file = location_entry.get()
    query_file = query_entry.get()
    
    locations = ["Bucuresti", "Craiova", "Cluj"]  # Default
    queries = ["", "Vanzari", "Meseriasi"]  # Default
    
    if location_file:
        try:
            with open(location_file, "r", encoding="utf-8") as f:
                locations = [line.strip() for line in f if line.strip()]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read location file: {e}")
            return
    
    if query_file:
        try:
            with open(query_file, "r", encoding="utf-8") as f:
                queries = [line.strip() for line in f if line.strip()]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read query file: {e}")
            return
    
    def scrape():
        global loading_flag
        loading_flag = True
        threading.Thread(target=animate_loading, daemon=True).start()

        groups_with_10k_followers = []
        
        for location in locations:
            for query in queries:
                full_query = f"{location} {query} site:facebook.com/groups"
                update_status(f"Searching for groups in {location} with keyword '{query}'...")
                start_index = 1
                while start_index <= 100:
                    response = requests.get(
                        "https://www.googleapis.com/customsearch/v1",
                        params={"key": API_KEY, "cx": CX_ID, "q": full_query, "start": start_index}
                    ).json()
                    
                    results = response.get("items", [])
                    if not results:
                        break
                    
                    for result in results:
                        title = result.get("title")
                        snippet = result.get("snippet", "")
                        url = result.get("link")
                        
                        match = re.search(r'(\d+[,.]?\d*)[ ]?(K|M)?[ ]?(members|followers)', snippet, re.I)
                        if match:
                            count = float(match.group(1).replace(",", ""))
                            unit = match.group(2)
                            if unit and unit.upper() == "K":
                                count *= 1000
                            elif unit and unit.upper() == "M":
                                count *= 1000000
                            if count >= 10000:
                                groups_with_10k_followers.append({'location': location, 'query': query, 'title': title, 'url': url, 'followers': int(count)})
                    start_index += 10
                    time.sleep(1)
        
        with open('facebook_groups_api.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['location', 'query', 'title', 'url', 'followers'])
            writer.writeheader()
            for group in groups_with_10k_followers:
                writer.writerow(group)
        
        loading_flag = False
        loading_label.config(text="Done!")
        messagebox.showinfo("Done", f"Exported {len(groups_with_10k_followers)} groups to facebook_groups_api.csv")
    
    threading.Thread(target=scrape, daemon=True).start()

root = tk.Tk()
root.title("Facebook Group Scraper")
root.geometry("550x350")

# File selectors
tk.Label(root, text="Location File:").pack()
location_entry = tk.Entry(root, width=50)
location_entry.pack()
tk.Button(root, text="Browse", command=lambda: select_file(location_entry)).pack()

tk.Label(root, text="Query File:").pack()
query_entry = tk.Entry(root, width=50)
query_entry.pack()
tk.Button(root, text="Browse", command=lambda: select_file(query_entry)).pack()

# Status Box
status_text = tk.Text(root, height=8, width=60, state=tk.DISABLED)
status_text.pack()

# Loading label
loading_label = tk.Label(root, text="")
loading_label.pack()

# Start button
tk.Button(root, text="Start Scraper", command=run_scraper).pack()

root.mainloop()
