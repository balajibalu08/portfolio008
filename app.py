from flask import Flask, request, render_template, redirect, url_for,flash
import sqlite3
import os
import smtplib
from email.mime.text import MIMEText
app = Flask(__name__)
DATABASE = 'contacts.db'
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
app.secret_key = os.urandom(24)  
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_table() #Create the table if it doesnt exist

@app.route("/", methods=['GET', 'POST'])

def index():
    social_links = {
        'insta' : "https://www.instagram.com/balajicharmpaws?igsh=aGVsMTFzc2Nmdm1t ",
        'twitter' : "https://x.com/tadisettybalaji?s=11",
        'linkedin' :"https://www.linkedin.com/in/balaji-tadisetty-907bba242/"
    }
    educations = [
        {'date': '2023-2025', 'degree': 'Master of Computer Applications', 'institution': 'KL University', 'description': 'Focus on Artificial Intelligence.', 'cgpa': '8.6'},
        {'date': '2019-2022', 'degree': 'Bachelor of Science in Computer Science', 'institution': 'Annai Violet Arts and Science College', 'cgpa': '7.1'},
        {'date': '2016-2018', 'degree': 'Intermediate (MPC)', 'institution': 'KBN JR College', 'cgpa': '81%'},
        {'date': '2015-2016', 'degree': 'SSC', 'institution': 'MSREMH SCHOOL', 'cgpa': '7.8'},
        ]
    projects = [
        {'title': 'Disease Prediction', 'image': 'disease.png','description': 'Developed an innovative application leveraging advanced algorithms trained on extensive medical datasets, achieving 91% accuracy in providing preliminary diagnostic suggestions. Enhanced healthcare accessibility by delivering actionable insights for early disease detection and promoting prompt medical consultations. Additionally, created comprehensive technical and functional documentation to ensure the application\'s scalability and ease of use.'},
        {'title': 'Bi-Directional CSV-SQL Converter', 'image': 'import.png', 'description': 'Developed a robust application for bi-directional conversion between CSV files and SQL tables, enabling seamless data transfer and integration. Optimized the system to handle large datasets, including processing CSV files up to 2GB, ensuring scalability and efficiency. Automated data validation and error handling to maintain data integrity during conversions, streamlining workflows for diverse data management needs.'},
        {'title': 'File Sharing', 'image': 'filesharing.jpeg','description': 'Developed a secure file-sharing platform using Tkinter and Socket programming, allowing users to upload, store, and share files efficiently. The platform features file organization into folders, customizable sharing permissions, and the generation of secure links for accessing files. It supports file versioning, large file uploads, and previews for common file types, enhancing the overall user experience. Additionally, real-time notifications and usage analytics were integrated to foster improved collaboration and usability. I focused on ensuring robust data security and optimized performance, making the system capable of handling diverse user needs effectively.'}
    ]
    experience = [
        {
            'title': 'Intern Data Science, Machine Learning, and Artificial Intelligence',
            'company': 'Brain O Vision',  # Added company name
            'start_date': 'MAY 2024',
            'end_date': 'JULY 2024',
            'description': 'As an intern, I worked on developing a disease prediction system using the Multinomial Naive Bayes algorithm to analyze user-reported symptoms and predict potential health conditions. I processed and cleaned large datasets to improve model accuracy, trained and fine-tuned the algorithm, and integrated the system with Flask for seamless deployment. Additionally, I documented the technical aspects of the project to ensure clear knowledge transfer for future development.'
        }
    ]
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", (name, email, message))
            conn.commit()
            conn.close()

            # Send email
            sender_email = "balajibalu088@gmail.com"
            sender_password = "ekfs kmum xtpz fqam" 
            receiver_email = "2301600019mca@gmail.com" # Recipient email (your email)
            email_message = f"Name: {name}\nEmail: {email}\nMessage: {message}"

            msg = MIMEText(email_message)
            msg['Subject'] = "New Contact Form Submission"
            msg['From'] = sender_email
            msg['To'] = receiver_email

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp: # Use appropriate SMTP server
                smtp.login(sender_email, sender_password)
                smtp.send_message(msg)
            flash('Message sent successfully!', 'success')  # Flash success message
            return redirect(url_for('index'))
        except sqlite3.Error as e:
          return f"Database error: {e}"
        except smtplib.SMTPException as e:
          return f"Email error: {e}"
        except Exception as e:
          return f"Unexpected error: {e}"
    return render_template('index.html',social_links=social_links, educations=educations,projects=projects,experience=experience)

if __name__ == "__main__":

    app.run(debug=False,port=1000,host="0.0.0.0")
