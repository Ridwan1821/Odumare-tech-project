# Streamlit dependencies
import streamlit as st
from streamlit_option_menu import option_menu

# Data handling dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import folium
import PIL
from PIL import Image
import zipfile
from zipfile import ZipFile
import os
import pickle

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
# Data loading
file = pd.ExcelFile('skills.xlsx')
data = file.parse('skills')
courses = list(data['Label'].unique())

# App declaration
def streamlit_menu(example=1):
    # Display average values in a horizontal layout using Streamlit columns

    if example == 3:
        # 2. horizontal menu with custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Home","Chatbot","About","Contact"],  # required
            icons=["house", "people", "graph-down","telephone"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "12px"},
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "4px",
                    "--hover-color": "#fafa",
                },
                "nav-link-selected": {"background-color": "blue"},
            },
        )
        return selected


selected = streamlit_menu(example=3)

if selected == "Home":
    # Set up the Streamlit app layout
    st.title("OdumareTech Trainees")

    # Sidebar controls for selecting time range and location
    #st.sidebar.title("Filter Options")
    course = st.sidebar.selectbox('Course', data['Label'].unique())
    st.subheader(f"**Educational Background of {course} Students**")

    # Filter the data based on user selection
    filtered_data = data[data['Label'] == course]
    # Plot a bar chart for students' educational background
    filtered_data = data[data['Label'] == course]
    plot1 = pd.DataFrame(filtered_data['Course of Study'].value_counts())
    plot1 = plot1.reset_index().rename(columns={'index':'course_of_study', 'Course of Study': 'count'})
    plot1 = plot1.sort_values(by = 'count')
    plt.figure(figsize=(5,6))
    plt.barh(plot1['course_of_study'], plot1['count'])
    fig1 = plt.show()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(fig1, clear_figure=None, use_container_width=True)

    # Plot a bar chart for students' soft skills
    st.markdown(f"**Soft Skills of {course} Students**")
    plot2 = pd.DataFrame(filtered_data['Soft Skills'].value_counts())
    plot2 = plot2.reset_index().rename(columns={'index':'soft_skills', 'Soft Skills': 'count'})
    plot2 = plot2.sort_values(by = 'count')
    plt.figure(figsize=(5,6))
    plt.barh(plot2['soft_skills'], plot2['count'])
    #plt.xticks(rotation = 45)
    fig2 = plt.show()
    st.pyplot(fig2, clear_figure=None, use_container_width=True)

if selected == "Chatbot":
    #locations = sorted(data['location'].unique())
    #selected_location = st.sidebar.selectbox("Select Location", locations)
    
    # Load the trained Random Forest Regression model from the pickle file
    with open('rf_model.pkl', 'rb') as f:
        model = pickle.load(f)

    # Define the Streamlit app
    st.title("Course Recommender")
    st.write("Welcome to OdumareTech")
    st.write("We understand you are confused on what tech course to enrol in. We are here to assist you.")

    # Input fields for the features
    background = st.text_input("**What is your Educational Background**")
    skills = st.text_input("**What are your soft skills**")

    # Vectorizing the data using countVectorizer
    vect = pickle.load(open("vectorizer.pkl", "rb"))
    df = pd.DataFrame({'background':[background], 'skills':[skills]})
    data_vect1 = vect.transform(df['background'].values.astype(str))
    data_vect2 = vect.transform(df['skills'].values.astype(str))
    data_vect = data_vect1 + data_vect2

    # Converting the vectorized data to array
    x_vect = data_vect.toarray()

    if st.button("Submit"):
        # Make prediction using the loaded model
        prediction = model.predict(x_vect)
        if prediction == 0:
            st.write("The most suited course for you is Data Analytics")
        elif prediction == 1:
            st.write("The most suited course for you is Data Science")
        else:
            st.write("The most suited course for you is Web Development Front End")

if selected == "About":
    def about():
        # About the project
        st.header("About This Platform")
        st.markdown('We are tackling an issue that aspiring techies are facing: the challenge of selecting the right tech course.'+
                    ' We have recognized the time-consuming nature of individual consultations, hence the implementation of this chatbot solution.'+
                    ' This chatbot aims to provide personalized recommendations, helping aspiring techies navigate the sea of course options more efficiently.'+
                    ' The chatbot only recommends courses offered by Odumaretech which are Data Analytics, Data Science and Web Development Front End.')
        
        # Meet Our Team section
        st.header("Meet The Team")
        
        col1, col2, col3 = st.columns(3)
        with col1:
                st.image('Adebayo.jpg', caption='Adebayo Akinleye - Data Analyst', use_column_width=True)
        with col2:
                st.image('AMAKA.jpg', caption='AMAKA ADEWOYE - Data Analyst', use_column_width=True)
        with col3:
                st.image('Deborah.jpg', caption='Deborah Oshamehin - Data Analyst', use_column_width=True)

        col1, col2 = st.columns(2)
        with col1:
                st.image('Olawale.jpg', caption='Olawale Quadry - Data Analyst', use_column_width=True)
        with col2:
                st.image('Patrick.jpg', caption='Patrick Okonkwo - ML model Developer', use_column_width=True)
        
    about()


if selected == "Contact":
    def contact_form():
        st.title("Contact Us")
        
        # Input fields for name, email, and phone number
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone_number = st.text_input("Phone Number")
        
        # Text area for the message
        message = st.text_area("Review message")
        
        # Submit button
        if st.button("Submit"):
            # Validate form inputs
            if not name:
                st.error("Please enter your name")
            elif not email:
                st.error("Please enter your email")
            elif not phone_number:
                st.error("Please enter your phone number")
            elif not message:
                st.error("Please enter a message")
            else:
                # Process the form submission
                # You can add your own logic here, such as sending an email or storing the form data in a database
                st.success("Thank you! Your message has been submitted.")
                # Clear form fields after submission
                name = ""
                email = ""
                phone_number = ""
                message = ""
    contact_form()
