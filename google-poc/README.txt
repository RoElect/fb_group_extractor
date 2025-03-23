HOW TO USE:

1. Create a Custom Search Engine:

- Visit Google Custom Search Engine.
- Click "Add" and create a new search engine.
- Set the site to facebook.com/groups or any site you want to restrict searches to, or leave it open to search the entire web.
- After creating, go to Control Panel and copy the CX ID.

2. Get an API Key:

- Go to Google Cloud Console.
- Enable the Custom Search API from the APIs library.
- Go to Credentials, create a new API key, and copy it.

3. Replace your API KEY and CX ID in the python script

4. Run the Script:

- Save your locations in a text file (one per line).
- Save your key_words in another text file (one per line).
- Run the script from the command line:

  ```sh
  python3 scraper.py locations.txt key_words.txt
  ```

- If no files are provided, default values will be used, and the user will be notified.
- The script will generate a CSV file with the extracted Facebook groups.
