import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Facebook credentials (Replace with your actual credentials)
EMAIL = "Your Account"
PASSWORD = "Your Password"

# List of all Romania's counties (județe) + București
judete = [
    "Dolj" 
]

# Setup WebDriver with WebDriver Manager (No need to manually download ChromeDriver)
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Open browser in full screen
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=chrome_options)

def facebook_login():
    """Logs into Facebook using the provided email and password."""
    driver.get("https://www.facebook.com")
    time.sleep(3)  # Allow page to load

    email_input = driver.find_element(By.ID, "email")
    password_input = driver.find_element(By.ID, "pass")
    login_button = driver.find_element(By.NAME, "login")

    email_input.send_keys(EMAIL)
    password_input.send_keys(PASSWORD)
    login_button.click()

    time.sleep(20)  # Wait for login to complete

def scroll_down():
    """Scrolls down the page to load more results and checks for new groups."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    new_groups_found = True
    
    while new_groups_found:
        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)  # Wait for the page to load more results
        
        # Get the new height and compare it with the last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # If the height has not changed, break the loop
        if new_height == last_height:
            new_groups_found = False
        last_height = new_height

def search_facebook_groups(region):
    """Searches Facebook for public groups related to a specific region (județ) and returns a list of valid groups."""
    driver.get(f"https://www.facebook.com/search/groups/?q={region}")
    time.sleep(5)

    scroll_down()  # Scroll down to load more groups

    groups = driver.find_elements(By.CSS_SELECTOR, "a[href*='/groups/']")
    group_data = []

    for g in groups:
        name = g.text.strip()
        url = g.get_attribute("href")

        if name and url:
            # Check if the group is public and has 10k+ members by clicking and examining the group page
            if "Public" in g.text:  # Checking if the word 'Public' appears in the group name/description
                group_data.append([region, name, url])

    return group_data

def check_group_members(group_url):
    """Checks the number of members in a Facebook group by opening the group page."""
    driver.get(group_url)
    time.sleep(5)
    
    try:
        # Wait for the group member count to be visible (may need adjustment depending on the page load time)
        member_count_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'sexy-header')]//span[contains(text(), 'members')]"))
        )
        member_count_text = member_count_elem.text
        if 'K' in member_count_text:
            # Extract the number of members and check if it's greater than 10,000
            members = member_count_text.split(' ')[0].replace(',', '')
            if 'K' in members and float(members.replace('K', '')) >= 10:
                return True
        return False
    except Exception as e:
        print(f"Error checking member count for {group_url}: {e}")
        return False

# Log in to Facebook
facebook_login()

# Prepare CSV file
csv_filename = "facebook_groups_romania_filtered.csv"

with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Judet", "Name of Group", "URL of Group"])  # Write headers

    # Iterate through all counties and fetch groups
    for judet in judete:
        print(f"Searching for groups in {judet}...")
        groups = search_facebook_groups(judet)

        if groups:
            for group in groups:
                name, url = group[1], group[2]
                if check_group_members(url):  # Check if the group has 10k+ members
                    csv_writer.writerow([judet, name, url])  # Write to CSV
                    print(f"✔ Found {name} with 10k+ members for {judet}")
                else:
                    print(f"❌ {name} does not have 10k+ members or is not public.")
        else:
            print(f"❌ No public groups found for {judet}")

# Close the browser
driver.quit()

print(f"\n✅ Data saved to {csv_filename}")
