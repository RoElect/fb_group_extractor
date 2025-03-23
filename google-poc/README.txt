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

3. Replace your API KEY and CX ID in the python scripts

4. Run the GUI Version:

- Run the GUI script with:

  ```sh
  python3 search_from_gui.py
  ```

- A graphical interface will appear, allowing you to select the location and key_words files manually.
- Click the "Run Search" button to start the extraction process.
- The results will be saved in a CSV file automatically.
- If no files are selected, the script will use default values and notify the user.