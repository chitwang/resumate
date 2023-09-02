# ResuMate Miner - Aryans

```
A simple resume miner used for extracting information from resumes
```

# Deployed Site

- Link to the deployed site : http://aryans.tech/

# Features

- Extract name
- Extract email
- Extract mobile numbers
- Extract college name
- Extract degree
- Extract CPI
- Extract skills
- Extract experience
- Extract projects
- Extract designation
- Extract relevant courses
- Extract PORs

# Installation

- You have to install some packages

```bash

#For NLP operations we use spacy and nltk.
pip install nltk

python -m nltk.downloader words
python -m nltk.downloader stopwords

pip install spacy==2.3.5

pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz

pip install pyresparser

pip install matplotlib

#we are using streamlit to display page
pip install streamlit
```

# Usage

- clone this repo in your system
- download necessary packages
- Use below command to launch the site

```bash
streamlit run app.py
```

# Supported File Formats

- PDF on all Operating Systems

# Result

The module would return a list of dictionary objects with result as follows:

```json
"applicants": [
        {
            "Name": "Chitwan Goel",
            "Email": "chitwang21@iitk.ac.in",
            "Mobile number": "+91-7310826277",
            "College name": "Indian Institute of Technology Kanpur",
            "Degree": "Bachelor of Technology",
            "CPI": 9.73,
            "Skills": [
                "\u2022 Programming Skills",
                "C",
                "C++",
                "Python",
                "Bash script",
                "Verilog HDL",
                "MIPS assembly language",
                "Dart*",
                "\u2022 Frameworks/Libraries",
                "Numpy",
                "Pandas",
                "Matplotlib",
                "Keras",
                "Tensorflow",
                "Sklearn",
                "Selenium",
                "Gradio",
                "Flutter*",
                "\u2022 Web",
                "HTML",
                "CSS",
                "JavaScript",
                "ReactJS",
                "NodeJS",
                "Express",
                "TypeScript",
                "MongoDB",
                "NextJS",
                "Firebase*",
                "\u2022 Miscellaneous",
                "Git",
                "LATEX",
                "AutoCAD",
                "Tkinter",
                "Google Colab",
                "Jupyter Notebook",
                "Pinecone",
                "Qdrant",
                "Weaviate"
            ],
            "Experience": [
                "AI Intern, AI Northstar Tech",
                "(May \u201923 - Jul \u201923 )",
                "\u2022 Conducted extensive research on state-of-the-art AI techniques, and used it to solve real-world problems",
                "\u2022 Curated terabyte-scale image dataset through web scraping using Selenium, for multiple semantic search engines",
                "\u2022 Developed a prototype web app for searching and browsing the dataset using images and text as input",
                "\u2022 Integrated embeddings from large multi-modal models like CLIP, and transformer models like ViT, into",
                "the prototype, using Huggingface hub and transformers library",
                "Full Stack Developer Intern, Vizuara",
                "(Mar \u201923 - Jul \u201923 )",
                "\u2022 Developed a full-stack MERN course portal, featuring integrated payment gateway and user authentication",
                "\u2022 Implemented a search system using TensorFlow.js, enabling advanced search based on semantic understanding",
                "\u2022 Automated an uploading process to Firebase, drastically reducing the time required from hours to seconds",
                "\u2022 Created an innovative resume generation portal utilizing AI and human expertise for polished resumes"
            ],
            "Projects": [
                "CSE Bubble (cid:135) (CS220 Course Project)",
                "Mentor: Professor Urbi Chatterjee (CSE, Indian Institute of Technology Kanpur)",
                "(Mar \u201923 - Apr \u201923 )",
                "\u2022 Implemented CSE-BUBBLE processor with separate 32-bit sized Instruction and Data Memory sections",
                "\u2022 Developed op-code formats and modules for instruction handling, including ALU and branching operations",
                "\u2022 Generated machine code for Bubble Sort from MIPS code, and stored output in data memory through simulation",
                "What\u2019s Next (cid:135) (CS253 Course Project)",
                "Mentor: Professor Indranil Saha (CSE, Indian Institute of Technology Kanpur)",
                "(Jan \u201923 - Apr \u201923 )",
                "\u2022 Developed an event management MERN app for IITK, featuring registration, like/dislike functionality & notification",
                "\u2022 Created an intuitive interface with interactive elements like event details pages, and personalized user dashboards",
                "\u2022 Integrated a payment portal enabling organizers to make direct seamless payments to Lecture Hall Complex",
                "Jal Jeevan Mission (Water-Life Mission)",
                "Mentor: Professor Priyanka Bagade (CSE, Indian Institute of Technology Kanpur)",
                "(Nov \u201922 - Apr \u201923 )",
                "\u2022 Contributed to a government-funded project addressing water pipe leakage detection using sensors and hydrophones",
                "\u2022 Extensively analyzed state-of-the-art techniques and integrated hardware and software approaches in the project",
                "\u2022 Simulated a water pipeline to collect data and employed KNN-SVM ensemble methods, for accurate predictions"
            ],
            "Designation": null,
            "Courses": [
                "A*: Exceptional Performance",
                "*Basic Knowledge",
                "*: Ongoing",
                "Data Structures & Algorithms (A*)",
                "Discrete Mathematics for Computer Science",
                "Real Analysis and Multivariable Calculus",
                "Introduction to Machine Learning*",
                "Computer Organization (A*)",
                "Probability for Computer Science",
                "Linear Algebra and ODE",
                "Operating Systems*",
                "Fundamentals of Computing",
                "Logic for Computer Science",
                "Software Development and Ops",
                "Image Processing*"
            ],
            "Position of responsibilities": [
                "\u2022 Leading the website development as Web Head at Techkriti, IITK, providing guidance to the team of executives",
                "\u2022 Coordinated internship and placement drive of more than 2000 students as Company Coordinator at SPO, IITK"
            ],
            "no_of_pages": 1,
            "test_score": 95.0
        }
]
```
