from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Enable headless mode
options.add_argument("--disable-gpu")  # Optional, recommended for Windows
options.add_argument("--window-size=1920x1080")  # Optional, set window size

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), options=options
)


results = []

try:
    base_url = "https://owasp.org/www-project-top-ten/"
    driver.get(base_url)
    sleep(2)  # wait 2 seconds to load page

    title = driver.title
    print(f"\nPage Title:  {title}")

    # Find all the search result items
    items = driver.find_elements(By.XPATH, "//ul/li/a[strong]")
    print(f"Found TOP {len(items)} Voulnerabilities.")

    for item in items:
        title = item.text.strip()
        link = item.get_attribute("href").strip()

        results.append({"Title": title, "Link": link})

    df = pd.DataFrame(results)
    print("\nExtracted Data:")
    print(df)

    # output to csv
    df.to_csv("owasp_top_10.csv", index=False)


except Exception as e:
    print(f"An exception occurred: {type(e).__name__} {e}")
finally:
    driver.quit()
