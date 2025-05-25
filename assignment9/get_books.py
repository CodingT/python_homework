import json
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

# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), options=options
)

# <un class="results">
# <li class="row cp-search-result-item"
# data-test-id="searchResultItem"
# <a href="/item/show/18011361981"
# data-key="bib-image-link">
# <img alt="Real-World Spanish: The Conversation Learning System - Camila Vega Rivera"
# src="https://cover.hoopladigital.com/dvf_9798347721009_270.jpeg"
# class="cp-jacket-cover img-responsive"
# <a href="/item/show/18011361981"
# title="Real-World Spanish: The Conversation Learning System"


# <span aria-hidden="true"
# class="title-content">Real-World Spanish: The Conversation Learning System</span>

# Author
# <a target="_parent" rel="noopener noreferrer"
# class="author-link" data-key="author-link"
# href="/v2/search?origin=core-catalog-explore&amp;query=Camila%20Vega%20Rivera&amp;searchType=author">Camila Vega Rivera</a>


# format and year
# <div class="cp-format-info">
# <span aria-hidden="true" class="display-info">
# <span class="display-info-primary">eAudiobook<!-- --> - 2025</span>
# <span class="call-number"></span>
# </span><span class="cp-screen-reader-message">eAudiobook, 2025</span></div>


results = []


try:
    base_url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"
    driver.get(base_url)
    sleep(2)  # wait 2 seconds to load page

    # extracting data:
    title = driver.title
    print(f"\nPage Title:  {title}")

    while True:

        # Find all the search result items
        items = driver.find_elements(
            By.CSS_SELECTOR,
            "li.row.cp-search-result-item[data-test-id='searchResultItem']",
        )
        print(f"Found {len(items)} book entries.")

        for item in items:
            # Extract book title
            title_element = item.find_element(By.CSS_SELECTOR, "span.title-content")
            title = title_element.text.strip()

            # Extract the author
            author_elements = item.find_elements(By.CSS_SELECTOR, "a.author-link")
            authors = "; ".join([author.text.strip() for author in author_elements])

            # Extract the format and year
            format_info_element = item.find_element(
                By.CSS_SELECTOR, "div.cp-format-info span.display-info-primary"
            )
            format_year = format_info_element.text.strip()

            results.append(
                {"Title": title, "Author": authors, "Format-Year": format_year}
            )

        try:
            next_button = driver.find_element(
                By.CSS_SELECTOR,
                "li.cp-pagination-item.pagination__next-chevron a.cp-link.pagination-item__link",
            )
            next_url = next_button.get_attribute("href")
            print(f"Navigating to next page: {next_url}")
            driver.get(next_url)
            sleep(2)  # Wait for the next page to load
        except Exception as e:
            print("No more pages to load. Stopping.")
            break

    df = pd.DataFrame(results)
    print("\nExtracted Data:")
    print(df)

    # output to csv and json files
    df.to_csv("get_books.csv", index=False)
    print("\nData saved to get_books.csv")

    df.to_json("get_books.json", index=False)
    print("\nData saved to get_books.json")

except Exception as e:
    print(f"An exception occurred: {type(e).__name__} {e}")
finally:
    driver.quit()
