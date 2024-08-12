import streamlit as st
import requests
from bs4 import BeautifulSoup

def scrape_doctor_count(location, specialization):
    # Construct the URL based on location and specialization
    url = f"https://www.practo.com/{location}/doctors?specialization={specialization}"
    
    response = requests.get(url)
    if response.status_code != 200:
        st.error("Failed to retrieve data from Practo. Please check your inputs.")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the total number of doctors
    count_div = soup.find('h1')
    if count_div:
        count_text = count_div.get_text()
        # Example: "1,234 doctors found in Bangalore"
        count_number = ''.join(filter(str.isdigit, count_text))
        return int(count_number) if count_number else None
    else:
        return None

def count():  
    st.title("PaidIntern Project Assessment")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
     st.image(
        "logo.jfif", 
        width=300  
    )
    st.header('Doctor Count Scraper')
    location = st.text_input("Enter Location (e.g., Indore)")
    
    # Dropdown for specialization
    specializations = [
        'General Physician',
        'Dermatologist',
        'Cardiologist',
        'Dentist',
        'Gynecologist',
        'Pediatrician',
        'Orthopedist',
        'Ophthalmologist',
        'ENT Specialist',
        'Psychiatrist'
    ]
    specialization = st.selectbox("Select Specialization", specializations)
    
    # Scrape button
    if st.button("Scrape"):
        if location.strip() == "":
            st.error("Please enter a valid location.")
        else:
            with st.spinner('Scraping data...'):
                doctor_count = scrape_doctor_count(location.lower().replace(' ', '-'), specialization.lower().replace(' ', '-'))
                
                if doctor_count is not None:
                    st.success(f"Total number of {specialization} in {location.title()}: {doctor_count}")
                else:
                    st.error("Could not find the number of doctors. Please try again with different inputs.")
        st.success('Scrapping Done')
if __name__ == "__main__":
    count()
