import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User
from preprocess import preprocess_image
from ocr import extract_text
from postprocess import correct_text
import cv2
from PIL import Image
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Create upload directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            return "Username already exists!"
            
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('home'))
        
    return render_template('register.html'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
            
        return "Invalid credentials!"
        
    return render_template('login.html'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('upload.html'))

@app.route('/process', methods=['POST'])
@login_required
def process():
    if 'file' not in request.files:
        return "No file uploaded!"
        
    file = request.files['file']
    if file.filename == '':
        return "No file selected!"

    # Save original file
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(current_user.id))
    os.makedirs(user_folder, exist_ok=True)
    file_path = os.path.join(user_folder, file.filename)
    file.save(file_path)

    # Process image
    try:
        preprocessed = preprocess_image(file_path)
        processed_path = os.path.join(app.config['PROCESSED_FOLDER'], f"processed_{file.filename}")
        cv2.imwrite(processed_path, preprocessed)

        # OCR and correction
        text = extract_text(Image.open(processed_path))
        corrected_text = correct_text(text)

        # Save result
        output_filename = f"digitized_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        output_path = os.path.join(user_folder, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(corrected_text)

        return render_template('result.html',
                             original=text,
                             corrected=corrected_text,
                             filename=output_filename)

    except Exception as e:
        return f"Error processing file: {str(e)}"

@app.route('/download/<filename>')
@login_required
def download(filename):
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(current_user.id))
    return send_file(os.path.join(user_folder, filename), as_attachment=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)