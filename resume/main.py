import spacy
import re
import pdfminer.high_level
import os
from pdfminer.high_level import extract_text as pdf_extract_text

# Load the English NLP model from spaCy
nlp = spacy.load('en_core_web_sm')


# Define a function to extract text from a PDF file
def extract_text(pdf_path):
    try:
        # Use pdfminer to extract text from the PDF file
        text = pdf_extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None


def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)


# Function to extract email
def extract_email(text):
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else None


# Function to extract phone number
def extract_phone(text):
    phone_pattern = r'(\+?\d{1,2}\s?)?(\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}'
    phones = re.findall(phone_pattern, text)
    return phones[0][0] if phones else None


# Function to extract name (assuming the first proper noun is the name)
def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            return ent.text
    return None


# Function to extract skills (customize as per skill set)
def extract_skills(text):
    skills = ['Python', 'Java', 'Machine Learning', 'Data Science', 'SQL', 'C++', 'Project Management']
    skill_list = []
    for skill in skills:
        if skill.lower() in text.lower():
            skill_list.append(skill)
    return skill_list


# Function to extract education
def extract_education(text):
    education_keywords = ['Bachelors', 'Masters', 'PhD', 'University', 'College', 'Degree']
    education = []
    for keyword in education_keywords:
        if keyword.lower() in text.lower():
            education.append(keyword)
    return education


# Function to extract experience (basic implementation, can be enhanced)
def extract_experience(text):
    experience_pattern = r'(\d+ years? experience|\d{4} to \d{4})'
    experiences = re.findall(experience_pattern, text)
    return experiences


# Function to parse a resume and extract information
def parse_resume(pdf_path):
    # Step 1: Extract text from the PDF
    text = extract_text_from_pdf(pdf_path)

    # Check if text extraction was successful
    if not text:
        return {"Error": "Failed to extract text from the PDF."}

    # Step 2: Extract different details
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)
    education = extract_education(text)
    experience = extract_experience(text)

    # Step 3: Organize the extracted information
    return {
        'Name': name,
        'Email': email,
        'Phone': phone,
        'Skills': skills,
        'Education': education,
        'Experience': experience
    }


# Example usage
if __name__ == "__main__":
    resume_path ="C:\\Users\\YAGESWARAN\\yages resume1[1] (1).pdf"
    parsed_data = parse_resume(resume_path)

    # Print extracted information
    for key, value in parsed_data.items():
        print(f"{key}: {value}")
