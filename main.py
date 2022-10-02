from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import io, os
import PyPDF2

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# export FLASK_APP=main
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/upload', methods = ['GET', 'POST'])
def uploaded_file():
    if request.method == 'POST':
        f = request.files['file']
        print(f)
        print(f.filename)
        # f.save(f.filename, "local_paper.pdf")
        
        f.readlines()
        # new_f = open(f, "r")
        # print(new_f.read())

        # with io.BytesIO(f) as opened_file:
        #     print(opened_file.getvalue())
    return 'file uploaded successfully'


@app.route('/upload2', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/pdf_to_text', methods=['GET'])
def pdf_to_text():
    pdffileobj=open('neural_ner_acl.pdf','rb')

    pdfreader=PyPDF2.PdfFileReader(pdffileobj)
    num_pages=pdfreader.numPages

    file1=open(r"neural_ner_acl.txt","a")

    for i in range(num_pages):
        print("On pdf page: ", i)
        pageobj=pdfreader.getPage(i)
        text=pageobj.extractText()
        file1.writelines(text)

    return "txt coverted successfully"

@app.route('/call_nemo_llm', methods=['GET'])
def call_nemo_llm():
    print("We are in")

    headers = {
                "Accept": "application/octet-stream", 
                "Content-Type": "application/json",
                "Authorization": "Bearer OW44MDUwc3NxbmU4Y3RhcW5jMm4yNmU0OXA6NWVjNTY4YWItODNlYy00NGFmLWI4N2ItMTE5MDY3ZWJkNTU3"
                }
    body = {
            "prompt": "Once upon a time",
            "tokens_to_generate": 50,
            "logprobs": true,
            "temperature": 1,
            "top_p": 0,
            "top_k": 2,
            "stop": [
                "\n"
            ],
            "random_seed": 0,
            "repetition_penalty": 1,
            "beam_search_diversity_rate": 1,
            "beam_width": 1,
            "length_penalty": 1
            }
    response = request.post(f"http://localhost:9009/completions", headers=headers, json=body)

