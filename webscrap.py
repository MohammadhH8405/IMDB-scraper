# Import the necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
import os

# Function to extract the changes
def compare_movie_lists(old_file, new_file):
    # Read old and new movie lists into dictionaries
    with open(old_file, 'r') as f:
        old_movies = {int(row[0]):row[1] for row in csv.reader(f) if row[0] != "time of checking:"}

    with open(new_file, 'r') as f:
        new_movies = {int(row[0]):row[1] for row in csv.reader(f) if row[0] != "time of checking:"}

    # Analyze changes
    added = []
    for i in range(1,251) :
        if old_movies[i] not in new_movies.values() :
            print('The movie',old_movies[i],'has been removed from the list!')
        if new_movies[i] not in old_movies.values() :
            added.append(new_movies[i])
            print('The movie',new_movies[i],'has been add to the list!')
        if old_movies[i] != new_movies[i] :
            if new_movies[i] in added:
                print('+',251-i,new_movies[i])
                continue
            for j in new_movies :
                if new_movies[j] == old_movies[i]:
                    diff = i -j
                    if diff>0:
                        print('-',i-j,old_movies[i])
                    else :
                        print('+',j-i,old_movies[i])

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

    # Get the new list of movies
    with open('temp.csv','w') as t :
        writer = csv.writer(t)

        # Parse the page to find the 250 movies
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        movie_list = soup.find('ul', class_="ipc-metadata-list")
        movies = [i.get_text(strip=True).split('.',1) for i in movie_list.find_all('h3', class_='ipc-title__text')]
        # Save result
        for i in range(0,250) :
            writer.writerow([int(movies[i][0]),movies[i][1]])
        writer.writerow(['time of checking:',time.strftime('%Y-%m-%d %H:%M:%S')])
    # Save and show the changes
    compare_movie_lists('movielist.csv', 'temp.csv')
    os.replace('temp.csv','movielist.csv')

except Exception as e:
    print("An error occurred: ", e)
finally:
    if driver != None:  # Check if driver was created
        driver.quit()  # Ensure browser closes even if error occurs
