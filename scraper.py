import streamlit as st 
from bs4 import BeautifulSoup
import requests

# Set Page configuration
st.set_page_config(page_title="Unsplash Web Scraper", layout="wide")

# page title
st.title('Unsplash Scraper')

with st.form('Search'):
    keyword = st.text_input("Enter your keyword")
    search = st.form_submit_button("Search")
    displayed_urls = set()
    
placeholder = st.empty()
if search:
    page = requests.get(f"https://unsplash.com/s/photos/{keyword}")
    soup = BeautifulSoup(page.content,features='html.parser')
    rows = soup.find_all('div',class_ = "ripi6")
    
    # Divide the screen into three columns
    col1, col2, col3 = placeholder.columns(3)
    
    # Iterate over the images and display them in three columns
    for row in rows:
        imgdiv = row.find_all("div",class_='MorZF')
        
        for i in range(len(imgdiv)):
            img = imgdiv[i].find("img")
            list_alttext = img['alt']
            list_url = img['srcset'].split(',')[-1].split(' ')[-2]
            
            # Check if the URL has already been displayed
            if list_url not in displayed_urls:
                displayed_urls.add(list_url)  # Add the URL to the set
                
                # Determine which column to display the image in based on the count of displayed URLs
                if len(displayed_urls) % 3 == 1:  
                    with col1:
                        st.image(list_url)
                        st.caption(list_alttext)
                elif len(displayed_urls) % 3 == 2:
                    with col2:
                        st.image(list_url)
                        st.caption(list_alttext)
                else:
                    with col3:
                        st.image(list_url)
                        st.caption(list_alttext)
