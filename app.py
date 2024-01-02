from flask import Flask, render_template, request
from dataClean import getText
import os
from ml.infer import infer

app = Flask(__name__)

@app.route('/')
def upload_ui():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file:
            # Save the uploaded file to a folder
            file_path = 'uploads/' + uploaded_file.filename
            uploaded_file.save(file_path)
            file_path = os.getcwd() + "\\" + file_path
            file_path = file_path.replace("/", "\\")
            print(file_path)
            x = getText(file_path)
            preds = infer(x)

            return render_template('result.html', prediction=str(preds), text = x)
    return 'File upload failed.'

if __name__ == '__main__':
    app.run(debug=True)





# from flask import Flask, render_template, request
#
# app = Flask(__name__)
#
# # Define a route to render the upload form
# @app.route('/')
# def upload_form():
#     return render_template('index.html')
#
# # Define a route to handle the uploaded file
# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if request.method == 'POST':
#         uploaded_file = request.files['file']
#         if uploaded_file:
#             # Save the uploaded file to a folder
#             uploaded_file.save('uploads/' + uploaded_file.filename)
#             return 'File uploaded successfully!'
#     return 'File upload failed.'
#
# if __name__ == '__main__':
#     app.run(debug=True)
