import os
import boto3
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_S3_REGION')
)

BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')

@app.route('/')
def index():
    return render_template('index.html', name="Ashab")

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        s3.upload_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            BUCKET_NAME,
            filename,
            
        )

        return redirect('/')
    return "❌ No file selected", 400

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
