import nltk
nltk.download('stopwords')
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from collections import Counter
from resParse.resParseCode.resume_parser import ResumeParser
import base64
import re


# Set page configuration and title
st.set_page_config(page_title="ResuMate - Aryans", page_icon=":bar_chart:", layout="wide")

# Title and styling
st.title("ResuMate Miner")
st.markdown('<style>div.block-container{padding-top: 1rem;}</style>', unsafe_allow_html=True)

# Sidebar for navigation
sidebar_options = ['Resume Parser', 'Analytics', 'Ranking', 'Test Score']
selected_option = st.sidebar.radio("Select a Page", sidebar_options)

# ----------------------------- #
# Resume Parser

if selected_option == 'Resume Parser':
    data={}

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upload Your Resume")
        uploaded_file = st.file_uploader("Drag and drop a file here", type=["pdf", "docx"])
    
        if uploaded_file:
            st.write("Uploaded file:", uploaded_file.name)
    
            base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')
            pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000px" type="application/pdf">'
            st.markdown(pdf_display, unsafe_allow_html=True)
    
            data = ResumeParser(uploaded_file).get_extracted_data()
            
            new_skills = []

            for skill_entry in data["Skills"]:
                skills_split = skill_entry.split(":")
                if len(skills_split) == 2:
                    skill_type = skills_split[0].strip()
                    individual_skills = [skill.strip() for skill in skills_split[1].split(",")]
                    new_skills.append(skill_type)
                    new_skills.extend(individual_skills)
                else:
                    new_skills.append(skill_entry.strip())

            data["Skills"] = new_skills

            with open('applicants_data.json', 'r') as file:
                existing_data = json.load(file)

            # Append your new data to the existing list
            existing_data["applicants"].append(data)

            # Write the updated data back to the file
            with open('applicants_data.json', 'w') as file:
                json.dump(existing_data, file, indent=4)
       
    with col2:
        st.header("Resume")
        # Prepare data for the table
        if data!={}:
            for key, values in data.items():
                st.write("------")
                st.subheader(key)  # Use the key as a title
                if isinstance(values, list):
                    for value in values:
                        st.write(value)
                else:
                    st.write(values) 

#------------------------#
#Test Score

elif selected_option == 'Test Score' :
    with open('applicants_data.json') as json_file:
        data = json.load(json_file)
    applicants_df = pd.DataFrame(data['applicants'])
    st.subheader("Test Score")
    st.header("Applicants' Test Score")



    # Search for a name
    name_search = st.text_input("Search for a name:", value="", key="name_search")
    st.markdown('<div style="font-style: italic; color: gray; margin-top: 0.2rem;">Press Enter to Apply</div>', unsafe_allow_html=True)

# ...

# ...

    if name_search:
        # Convert the search query to lowercase
        search_query_lower = name_search.lower()

        # Convert the names in the DataFrame to lowercase and then search
        matching_name = applicants_df[applicants_df['Name'].str.lower().str.contains(search_query_lower)]

        if not matching_name.empty:
            st.subheader("People with Name:")
            st.dataframe(matching_name[['Name', 'test_score']])

            # Display editable score input
            selected_name = st.selectbox("Select a name to edit score:", matching_name['Name'])

            # Get the index of the selected name in the DataFrame
            selected_index = applicants_df[applicants_df['Name'] == selected_name].index[0]

            # Check if the 'test_score' key exists in the JSON data
            if 'test_score' not in data['applicants'][selected_index]:
                data['applicants'][selected_index]['test_score'] = 0  # Add the key and set initial value to 0

            # Display and update the test score
            new_score = st.number_input("Enter new test score:", value=float(data['applicants'][selected_index]['test_score']), key="new_score")
            data['applicants'][selected_index]['test_score'] = new_score

            # Save the updated JSON data to the file
            with open('applicants_data.json', 'w') as json_file:
                json.dump(data, json_file, indent=4)
        else:
            st.subheader("No matching names found.")
# ...



    st.dataframe(applicants_df)
# ...





# ----------------------------- #
# Analytics
    

elif selected_option == 'Analytics':
    st.subheader("Analytics Page")

    # Sidebar for analytics options
    analytics_options = ['CPI Comparison', 'Top Mentioned Skills', 'Most Projects or Experience']
    selected_analytics_option = st.sidebar.radio("Select a Chart", analytics_options)

    # Load JSON data and create DataFrame for analytics
    with open('applicants_data.json') as json_file:
        data = json.load(json_file)
    applicants_df = pd.DataFrame(data['applicants'])

    if selected_analytics_option == 'CPI Comparison':
        st.header("Applicants' CPI Comparison")
        st.write("Comparison of Cumulative Performance Index (CPI) among applicants")

        # Filter by CPI range
        min_cpi, max_cpi = st.slider("CPI Range", min_value=min(applicants_df['CPI']), max_value=max(applicants_df['CPI']),
                                     value=(min(applicants_df['CPI']), max(applicants_df['CPI'])))
        filtered_applicants_df = applicants_df[(applicants_df['CPI'] >= min_cpi) & (applicants_df['CPI'] <= max_cpi)]

        # Calculate median and average CPI
        median_cpi = np.median(filtered_applicants_df['CPI'])
        average_cpi = np.mean(filtered_applicants_df['CPI'])

        # Create a bar chart to compare CPIs
        fig, ax = plt.subplots(figsize=(8, 4))
        bars = ax.barh(filtered_applicants_df['Name'], filtered_applicants_df['CPI'], color='skyblue', label='CPI')
        ax.set_xlabel('CPI (Cumulative Performance Index)')
        ax.set_title('CPI Comparison')

        # Display the exact CPI value on hovering over the chart
        for bar in bars:
            yval = bar.get_y() + bar.get_height() / 2
            ax.text(bar.get_width(), yval, f'{bar.get_width():.2f}', va='center')

        # Display median and average CPI lines
        ax.axvline(median_cpi, color='red', linestyle='dashed', linewidth=1, label=f'Median CPI: {median_cpi:.2f}')
        ax.axvline(average_cpi, color='green', linestyle='dashed', linewidth=1, label=f'Average CPI: {average_cpi:.2f}')
        ax.legend()

        # Display the bar chart using matplotlib
        st.pyplot(fig)
    
    elif selected_analytics_option == 'Top Mentioned Skills':
        st.header("Top Mentioned Skills")
        st.write("Chart showing the frequency of top mentioned skills among applicants")

        # Search bar for skills
        st.markdown('<style>div.css-1v4eu6x{font-weight:bold;}div.st-dd{width:50%;}</style>', unsafe_allow_html=True)
        skill_search = st.text_input("Search for a skill:", value="", key="skill_search")
        st.markdown('<div style="font-style: italic; color: gray; margin-top: 0.2rem;">Press Enter to Apply</div>', unsafe_allow_html=True)

        if skill_search:
            matching_people = applicants_df[applicants_df['Skills'].apply(lambda skills: skill_search.lower() in [skill.lower() for skill in skills])]
            if not matching_people.empty:
                st.subheader("People with Matching Skill:")
                st.dataframe(matching_people[['Name', 'Skills']])
            else:
                st.subheader("No matching skills found.")

        # Combine all skills into a single list
        all_skills = []
        for skills_list in applicants_df['Skills']:
            all_skills.extend(skills_list)

        # Count the frequency of each skill
        skills_counter = Counter(all_skills)

        # Get the top mentioned skills and their frequencies
        top_skills = skills_counter.most_common(10)  # Change the number as needed

        # Extract skill names and frequencies
        skill_names = [skill[0] for skill in top_skills]
        skill_frequencies = [skill[1] for skill in top_skills]

        # Create a smaller bar chart to show skill frequencies
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(skill_names, skill_frequencies, color='lightblue')
        ax.set_xlabel('Skills')
        ax.set_ylabel('Frequency')
        ax.set_title('Top Mentioned Skills')

        # Rotate x-axis labels, adjust spacing, and set font size
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.tight_layout()

        # Display the smaller bar chart using matplotlib
        st.pyplot(fig)

    elif selected_analytics_option == 'Most Projects or Experience':
        st.header("Most Projects or Experience")
        st.write("Applicants with the most number of projects or experience")

        # Search bar for projects and experience keywords
        keyword_search = st.text_input("Search for keywords in projects or experience:")

        # Filter applicants based on keyword search
        if keyword_search:
            matching_applicants = applicants_df[applicants_df['Experience'].apply(lambda exp: any(keyword_search.lower() in project.lower() for project in exp))]

            if not matching_applicants.empty:
                st.subheader("Applicants with Matching Keywords in Projects or Experience:")
                st.dataframe(matching_applicants[['Name', 'Experience']])
            else:
                st.subheader("No matching applicants found.")

        # If no keyword is provided, show the default graph
        else:
            # Count the number of projects or experiences
            regex_pattern = r'(?:Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sep|September|Oct|October|Nov|November|Dec|December)[ ]?[\'’]\d{2,4}'
            matched_counts = []
            for experience_list in applicants_df['Experience']:
                # Initialize count for each applicant
                applicant_count = 0
                for experience in experience_list:
                    # Replace \u2019 with a regular single quote ' in the experience text
                    cleaned_experience = experience.replace('\u2019', "’")
                    # Use regex to find matches
                    if re.search(regex_pattern, cleaned_experience):
                        applicant_count += 1
                # Append the count to the matched_counts list
                matched_counts.append(applicant_count)

            # Add the matched_counts list as a new column 'score' in the DataFrame
            applicants_df['Experience'] = matched_counts
            applicants_df = applicants_df.sort_values(by='Experience', ascending=False)

            # Create a smaller bar chart to show most projects or experience
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.barh(applicants_df['Name'], applicants_df['Experience'], color='salmon')
            ax.set_xlabel('Number of Projects or Experience')
            ax.set_title('Most Projects or Experience')

            # Display the smaller bar chart using matplotlib
            st.pyplot(fig)

# ----------------------------- #
# Ranking of Applicants
else:
    # Load JSON data and create DataFrame for ranking
    with open('applicants_data.json') as json_file:
        data = json.load(json_file)
    applicants_df = pd.DataFrame(data['applicants'])

    # Calculate the ranking score based on criteria
    applicants_df['score'] = (applicants_df['CPI'] * 0.5) + (applicants_df['Skills'].apply(len) * 0.2)
    regex_pattern = r'(?:Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sep|September|Oct|October|Nov|November|Dec|December)[ ]?[\'’]\d{2,4}'
    matched_counts = []

    # Iterate through the 'Experience' column in the DataFrame
    for experience_list in applicants_df['Experience']:
        # Initialize count for each applicant
        applicant_count = 0
        for experience in experience_list:
            # Replace \u2019 with a regular single quote ' in the experience text
            cleaned_experience = experience.replace('\u2019', "’")
            # Use regex to find matches
            if re.search(regex_pattern, cleaned_experience):
                applicant_count += 1
        # Append the count to the matched_counts list
        matched_counts.append(applicant_count*0.1)

    # Add the matched_counts list as a new column 'score' in the DataFrame
    applicants_df['score'] = applicants_df['score'] + matched_counts
    
    # Add points if designation matches a skill or experience
    for index, row in applicants_df.iterrows():
        if row['Designation'] in row['Skills']:
            applicants_df.at[index, 'score'] += 0.3
        if row['Designation'] in row['Experience']:
            applicants_df.at[index, 'score'] += 0.3

    st.subheader("Ranking Page")
    st.write("Ranking applicants based on the provided criteria")

    # Sort applicants by score in descending order
    ranked_applicants_df = applicants_df.sort_values(by='score', ascending=False)

    # Display the ranked applicants
    st.dataframe(ranked_applicants_df[['Name', 'score', 'CPI', 'Experience', 'Skills', 'Designation']])

    # Additional ranking visualization: Bar chart of top ranked applicants
    top_ranked_applicants = ranked_applicants_df.head(10)  # Change the number as needed
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(top_ranked_applicants['Name'], top_ranked_applicants['score'], color='green')
    ax.set_xlabel('Applicant Name')
    ax.set_ylabel('Ranking Score')
    ax.set_title('Top Ranked Applicants')

    # Rotate x-axis labels, adjust spacing, and set font size
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.tight_layout()

    # Display the bar chart using matplotlib
    st.pyplot(fig)
