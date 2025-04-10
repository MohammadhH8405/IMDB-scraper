from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv

driver = None  # Initialize driver variable
try:
    # Open chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Load the IMDb Top 250 page
    driver.get("https://www.imdb.com/chart/top/")

    # Scroll to load all movies
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)  # Will not work without!
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    movies = []
    # Save and show results
    with open('movielist.csv','w') as file :
        writer = csv.writer(file)

        # Parse the page to find the 250 movies
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        movie_list = soup.find('ul', class_="ipc-metadata-list")
        for i in movie_list.find_all('h3', class_='ipc-title__text') :
            i = i.get_text(strip=True)
            movies.append(i)
            writer.writerow([i])

        # Show results
        print(*movies[:], sep="\n")
        print(f"\nTotal movies scraped: {len(movies)}")  # Should be 250
        print(time.strftime('%Y-%m-%d %H:%M:%S'))

except Exception as e:
    print("An error occurred: ", e)
finally:
    if driver != None:  # Check if driver was created
        driver.quit()  # Ensure browser closes even if error occurs
