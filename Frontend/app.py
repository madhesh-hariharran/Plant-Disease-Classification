import os
from flask import Flask, flash, render_template, request, redirect, url_for
from connect import predict_disease, crop, get_recommendation, get_cause

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

users = {}

def create_user_directory(user_id):
    user_directory = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)
    return user_directory

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file:
        user_id = request.form.get('user_id')
        user_directory = create_user_directory(user_id)
        filename = file.filename
        file_path = os.path.join(user_directory, filename)
        file.save(file_path)
        
        if user_id not in users:
            users[user_id] = []
        users[user_id].append(filename)

        img = crop(file_path)
        if img is False:
            return render_template('error.html')
        else:
            index, predicted_class, confidence = predict_disease(image_data=img)
            recommendation = get_recommendation(predicted_class)
            cause = get_cause(predicted_class)
            prediction = [index, predicted_class.replace('_', ' '), confidence]
            return render_template('result.html', prediction=prediction, recommendation=recommendation, cause=cause)

if __name__ == '__main__':
    app.run(debug=True)
