# Digitize Handwritten Exams from Students  

In Germany, teachers manually grade handwritten exams, which is time-consuming due to increasing student numbers. This system automates the digitization of handwritten text into digital files, reducing grading workload.  

Features

User Authentication – Register and log in securely.
File Upload & Download – Upload handwritten exam scans and download digitized text.
AI Processing Pipeline – Converts handwriting into digital text.
Submission Management – Handle multiple exam submissions efficiently.
This solution streamlines exam grading, making it faster and more efficient for educators.

## Setup Instructions  

### Install Requirements  
```sh
pip install -r requirements.txt  
python -m spacy download de_core_news_sm  
sudo apt-get install hunspell-de-de  # For German dictionary  
flask shell  
from app import db  
db.create_all()  
python app.py  
Access via Browser
Open http://localhost:5000 in your browser.

Features

User Authentication – Register and log in securely.
File Upload & Download – Upload handwritten exam scans and download digitized text.
AI Processing Pipeline – Converts handwriting into digital text.
Submission Management – Handle multiple exam submissions efficiently.
This solution streamlines exam grading, making it faster and more efficient for educators.
