# Digitize-Handwritten-Exams-from-Students
Teachers in Germany manually grade handwritten exams, which is time-consuming due to increasing student numbers. The system aims to automate digitization of handwritten text into digital files, reducing grading workload.

Setup Instructions

Install Requirements

pip install -r requirements.txt
python -m spacy download de_core_news_sm
sudo apt-get install hunspell-de-de  # For German dictionary
Initialize Database

flask shell
>>> from app import db
>>> db.create_all()
Run Application

python app.py
Access via Browser
http://localhost:5000

This complete solution includes user authentication, file upload/download functionality, and the full AI processing pipeline. Teachers can:

Register and login
Upload handwritten exam scans
View processing results
Download digitized text files
Manage multiple submissions
