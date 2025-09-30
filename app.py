from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # your HTML form page

@app.route('/submit_appointment', methods=['POST'])
def submit_appointment():
    # Get data from form
    fullName = request.form.get('fullName')
    age = request.form.get('age')
    bloodGroup = request.form.get('bloodGroup')
    phone = request.form.get('phone')
    email = request.form.get('email')
    appointmentDate = request.form.get('appointmentDate')
    comments = request.form.get('comments')

    # Basic backend validation
    if not fullName or not age or not bloodGroup or not phone or not email or not appointmentDate:
        return "Missing required fields", 400

    # Save to SQLite
    conn = sqlite3.connect('bloodbank.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO appointments
        (fullName, age, bloodGroup, phone, email, appointmentDate, comments)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (fullName, age, bloodGroup, phone, email, appointmentDate, comments))
    conn.commit()
    conn.close()

    # Redirect to thanks page
    return redirect('/thanks')

@app.route('/thanks')
def thanks():
    return "<h2>Thank you! Your appointment has been booked.</h2><a href='/'>Return Home</a>"

@app.route('/view_appointments')
def view_appointments():
    # Just to confirm data is saved
    conn = sqlite3.connect('bloodbank.db')
    c = conn.cursor()
    c.execute('SELECT * FROM appointments')
    data = c.fetchall()
    conn.close()

    html = "<h2>All Appointments</h2><table border='1'><tr><th>ID</th><th>Name</th><th>Age</th><th>Blood Group</th><th>Phone</th><th>Email</th><th>Date</th><th>Comments</th></tr>"
    for row in data:
        html += "<tr>" + "".join(f"<td>{x}</td>" for x in row) + "</tr>"
    html += "</table><br><a href='/'>Back Home</a>"
    return html

if __name__ == '__main__':
    app.run(debug=True)
