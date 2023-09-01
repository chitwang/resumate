import os
import multiprocessing as mp
import io
import spacy
import pprint
from spacy.matcher import Matcher
from . import utils
import re


class ResumeParser(object):

    def __init__(
        self,
        resume,
        skills_file=None,
        custom_regex=None
    ):
        nlp = spacy.load('en_core_web_sm')
        custom_nlp = spacy.load(os.path.dirname(os.path.abspath(__file__)))
        self.__skills_file = skills_file
        self.__custom_regex = custom_regex
        self.__matcher = Matcher(nlp.vocab)
        self.__details = {
            'Name': None,
            'Email': None,
            'Mobile number': None,
            'College name': None,
            'Degree': None,
            'CPI':None,
            'Skills': None,
            'Experience': None,
            'Projects' : None,
            'Designation' : None,
            'Courses' :None,
            'Position of responsibilities' : None,
            'no_of_pages': None,
        }
        self.__resume = resume
        if not isinstance(self.__resume, io.BytesIO):
            ext = os.path.splitext(self.__resume)[1].split('.')[1]
        else:
            ext = self.__resume.name.split('.')[1]
        self.__text_raw = utils.extract_text(self.__resume, '.' + ext)
        self.__text = ' '.join(self.__text_raw.split())
        self.__nlp = nlp(self.__text)
        self.__custom_nlp = custom_nlp(self.__text_raw)
        self.__noun_chunks = list(self.__nlp.noun_chunks)
        self.__get_basic_details()

    def get_extracted_data(self):
        return self.__details

    def __get_basic_details(self):
        cust_ent = utils.extract_entities_wih_custom_model(
                            self.__custom_nlp
                        )
        name = utils.extract_name(self.__nlp, matcher=self.__matcher)
        email = utils.extract_email(self.__text)
        mobile = utils.extract_mobile_number(self.__text, self.__custom_regex)
        skills = utils.extract_skills(
                    self.__nlp,
                    self.__noun_chunks,
                    self.__skills_file
                )
        # edu = utils.extract_education(
        #               [sent.string.strip() for sent in self.__nlp.sents]
        #       )
        print(self.__text_raw)
        entities = utils.extract_entity_sections_grad(self.__text_raw)
        # print("Here are the entities:", entities)

        cpi_pattern = r"(?:CPI/%|Score)\s*([\d.]+)"
        cpi_matches = re.findall(cpi_pattern, self.__text_raw, re.IGNORECASE)
        # print("This are the matches: ",matches)

        institute_pattern = r"(?:Institution|Institute)\s+(.+)\s*"
        institue_matches = re.findall(institute_pattern, self.__text_raw, re.IGNORECASE)
        # print("This are the matches: ",institue_matches)

        degree_pattern = r"(?:Degree/Certiﬁcate|Degree/Certificate|Degree)\s+(.+)\s*"
        degree_matches = re.findall(degree_pattern, self.__text_raw, re.IGNORECASE)
        # print("This are the matches: ",matches)

        relevant_courses_labels = ["relevant courses", "coursework", "relevant coursework"]
        relevant_courses_index = -1
        por_index_label = ["positions of responsibility", "positions of responsibilities", "extra-curricular", "extra curricular activity", "extra-curricular activities"]
        por_index = -1

        if entities.get("skills") is not None:
            for label in relevant_courses_labels:
                if label.lower() in [item.lower() for item in entities["skills"]]:
                    relevant_courses_index = [item.lower() for item in entities["skills"]].index(label)
                    break
                
            for label in por_index_label:
                if label.lower() in [item.lower() for item in entities["skills"]]:
                    por_index = [item.lower() for item in entities["skills"]].index(label)
                    break

            if relevant_courses_index!=-1 and por_index!=-1:
                # Function to find the index of the first string with the specified format
                def find_index_with_substring(lst, start_index):
                    for i in range(start_index, len(lst)):
                        match = re.search(r'(?:Jan|Feb|Mar|Apr|May|Jun|July|Aug|Sep|Oct|Nov|Dec)\’\d{2}', lst[i])
                        if match:
                            return i
                    return -1  # Return -1 if no match is found

                # Find the index of the first matching string in the list starting from the specified index
                index = find_index_with_substring(entities["skills"], por_index)
                if index!=-1 and index!=por_index:
                    skills = entities["skills"][:relevant_courses_index]
                    relevant_courses = entities["skills"][relevant_courses_index + 1 : por_index] + entities["skills"][por_index + 1 : index-1]
                    position_of_responsibilities = entities["skills"][index-1:]
                else:
                    skills = entities["skills"][:relevant_courses_index]
                    relevant_courses = entities["skills"][relevant_courses_index + 1 : por_index]
                    position_of_responsibilities = entities["skills"][por_index + 1 :]

                entities["skills"] = skills
                entities["courses"] = relevant_courses
                entities["responsibilities"] = position_of_responsibilities
            elif relevant_courses_index != -1:
                skills = entities["skills"][:relevant_courses_index]
                relevant_courses = entities["skills"][relevant_courses_index + 1:]

                # Update the existing JSON object
                entities["skills"] = skills
                entities["courses"] = relevant_courses
            elif por_index != -1:
                skills = entities["skills"][:por_index]
                position_of_responsibilities = entities["skills"][por_index + 1:]

                # Update the existing JSON object
                entities["skills"] = skills
                entities["responsibilities"] = position_of_responsibilities

        if cust_ent.get("Degree") is not None:
            deg_val = cust_ent["Degree"][0]
            if deg_val.startswith("Degree/Certificate"):
                deg_val = deg_val[len("Degree/Certificate"):]

            # Update the "degree" value in the JSON object
            cust_ent["Degree"][0] = deg_val

        # print(cust_ent)

        try:
            self.__details['Name'] = cust_ent['Name'][0]
        except (IndexError, KeyError):
            self.__details['Name'] = name

        # extract email
        self.__details['Email'] = email

        # extract mobile number
        self.__details['Mobile number'] = mobile

        # extract skills
        self.__details['Skills'] = skills

        # extract college name
        try:
            if institue_matches:
                self.__details['College name'] = institue_matches[0]
        except KeyError:
            pass

        try:
            self.__details['Designation'] = cust_ent['Designation']
        except KeyError:
            pass

        # extract education Degree
        try:
            if degree_matches:
                self.__details['Degree'] = degree_matches[0]
        except KeyError:
            pass

        try:
            self.__details['Projects'] = entities['projects']
        except KeyError:
            pass

        try:
            self.__details['Courses'] = entities['courses']
        except KeyError:
            pass

        try:
            self.__details['Position of responsibilities'] = entities['responsibilities']
        except KeyError:
            pass

        try:
            self.__details['Experience'] = entities['experience']
        except KeyError:
            pass

        try:
            if cpi_matches:
                self.__details['CPI'] = float(cpi_matches[0])
        except KeyError:
            pass

        self.__details['no_of_pages'] = utils.get_number_of_pages(
                                            self.__resume
                                        )
        return


def resume_result_wrapper(resume):
    parser = ResumeParser(resume)
    return parser.get_extracted_data()


if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())

    resumes = []
    data = []
    for root, directories, filenames in os.walk('resumes'):
        for filename in filenames:
            file = os.path.join(root, filename)
            resumes.append(file)

    results = [
        pool.apply_async(
            resume_result_wrapper,
            args=(x,)
        ) for x in resumes
    ]

    results = [p.get() for p in results]

    pprint.pprint(results)