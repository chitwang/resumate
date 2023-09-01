# Resume Parser

```
A simple resume parser used for extracting information from resumes
```

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

#we are using streamlit to display page
pip install streamlit
```

# Documentation

Official documentation is available at: 

# Supported File Formats

- PDF on all Operating Systems

# Usage

- clone this repo in your system
- download necessary packages
- Use below command to launch the site

```bash

```

# CLI

For running the resume extractor you can also use the `cli` provided

```bash
usage: pyresparser [-h] [-f FILE] [-d DIRECTORY] [-r REMOTEFILE]
                   [-re CUSTOM_REGEX] [-sf SKILLSFILE] [-e EXPORT_FORMAT]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  resume file to be extracted
  -d DIRECTORY, --directory DIRECTORY
                        directory containing all the resumes to be extracted
  -r REMOTEFILE, --remotefile REMOTEFILE
                        remote path for resume file to be extracted
  -re CUSTOM_REGEX, --custom-regex CUSTOM_REGEX
                        custom regex for parsing mobile numbers
  -sf SKILLSFILE, --skillsfile SKILLSFILE
                        custom skills CSV file against which skills are
                        searched for
  -e EXPORT_FORMAT, --export-format EXPORT_FORMAT
                        the information export format (json)
```

# Notes:

- If you are running the app on windows, then you can only extract .docs and .pdf files

# Result

The module would return a list of dictionary objects with result as follows:

```
[
  {
    'college_name': ['Marathwada Mitra Mandal’s College of Engineering'],
    'company_names': None,
    'degree': ['B.E. IN COMPUTER ENGINEERING'],
    'designation': ['Manager',
                    'TECHNICAL CONTENT WRITER',
                    'DATA ENGINEER'],
    'email': 'omkarpathak27@gmail.com',
    'mobile_number': '8087996634',
    'name': 'Omkar Pathak',
    'no_of_pages': 3,
    'skills': ['Operating systems',
              'Linux',
              'Github',
              'Testing',
              'Content',
              'Automation',
              'Python',
              'Css',
              'Website',
              'Django',
              'Opencv',
              'Programming',
              'C',
              ...],
    'total_experience': 1.83
  }
]
```

# References that helped me get here

- [https://www.kaggle.com/nirant/hitchhiker-s-guide-to-nlp-in-spacy](https://www.kaggle.com/nirant/hitchhiker-s-guide-to-nlp-in-spacy)

- [https://www.analyticsvidhya.com/blog/2017/04/natural-language-processing-made-easy-using-spacy-%E2%80%8Bin-python/](https://www.analyticsvidhya.com/blog/2017/04/natural-language-processing-made-easy-using-spacy-%E2%80%8Bin-python/)

- [https://medium.com/@divalicious.priya/information-extraction-from-cv-acec216c3f48](https://medium.com/@divalicious.priya/information-extraction-from-cv-acec216c3f48)

- **Special thanks** to dataturks for their [annotated dataset](https://dataturks.com/blog/named-entity-recognition-in-resumes.php)

# Donation

If you have found my softwares to be of any use to you, do consider helping me pay my internet bills. This would encourage me to create many such softwares :smile:

| PayPal | <a href="https://paypal.me/omkarpathak27" target="_blank"><img src="https://www.paypalobjects.com/webstatic/mktg/logo/AM_mc_vs_dc_ae.jpg" alt="Donate via PayPal!" title="Donate via PayPal!" /></a> |
|:-------------------------------------------:|:-------------------------------------------------------------:|
| ₹ (INR)  | <a href="https://www.instamojo.com/@omkarpathak/" target="_blank"><img src="https://www.soldermall.com/images/pic-online-payment.jpg" alt="Donate via Instamojo" title="Donate via instamojo" /></a> |

# Stargazer over time
[![Stargazers over time](https://starchart.cc/OmkarPathak/pyresparser.svg)](https://starchart.cc/OmkarPathak/pyresparser)
