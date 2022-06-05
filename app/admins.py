from app import app #cause __init__.py is present so app folder is a library
import os
import sys
#from io import BytesIO
import shutil
sys.path.append("../webscrape/data_hunter")
# from data_hunter import customFunc
from data_hunter.customFuncMCF import *
from data_hunter.customFunclink import *
from flask import render_template, flash, request, redirect, url_for, session, send_file
import zipfile
import pathlib
from pyresparser import ResumeParser
from werkzeug.utils import secure_filename


### globals ####


UPLOAD_FOLDER ="./resources"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'docx', 'pdf'}

#### functions #############
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


url = "https://www.mycareersfuture.gov.sg/"

driver_loc = "../data_hunter/chromedriver.exe"

#####################

@app.route('/')
def index():
    for i in ["resources","resources.zip"]:
        try:
            if os.path.isdir(i):
                shutil.rmtree(i)
            elif os.path.isfile(i):
                os.remove(i)
        except:
            continue

    return render_template("index.html")

@app.route('/', methods = ["GET","POST"])
def upload_resume():
    if request.method =="POST":
        if 'customFile' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['customFile']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            try:
                os.path.exists(path_to_file)
            except:
                os.mkdir('resources')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'resume.pdf'))

            data = ResumeParser('./resources/resume.pdf').get_extracted_data()
            global data_list
            data_list = data["skills"]
            return redirect(url_for('choices'))



@app.route('/choices')
def choices():
    #data = ResumeParser('./resume.pdf').get_extracted_data()
    #data_list = data["skills"]
    #time.sleep(3)
    #data_list = [1,2,3]
    return render_template("choices.html", items=data_list)
    #return render_template("choices.html")

@app.route('/choices', methods = ["GET","POST"])
def print_shit():
    if request.method == 'POST':
        super_var_unique = request.form.getlist('haro')
        for i in super_var_unique:
            browser_sim(url,i,driver_loc,'./resources/')
            searches = i
            search_linkedin(i,'Singapore',driver_loc,'./resources/')

    return redirect(url_for('results'))

@app.route('/results')
def results():
    # compression_type = zipfile.ZIP_STORED
    directory = pathlib.Path("./resources")
    # with zipfile.ZipFile("resources.zip", mode="w", compression=compression_type) as archive:\
    # with zipfile.ZipFile("resources.zip", mode="w" ) as archive:
        # for file_path in directory.rglob("*"):
        #     archive.write(
        #         file_path,
        #         arcname=file_path.relative_to(directory)
        #     )
    # zipfolder = zipfile.ZipFile('resources.zip','w', compression = zipfile.ZIP_STORED)
    # for root,dirs, files in os.walk('./resources'):
    #     for file in files:
    #         zipfolder.write('./resources/'+file)
    #zipfolder.close()
    

    return render_template("results.html")

@app.route('/download')
def download():
    # memory_file = BytesIO()
    # memory_file.seek(0)
    compression_type = zipfile.ZIP_STORED
    directory = pathlib.Path("./resources")
    with zipfile.ZipFile("resources.zip", mode="w", compression=compression_type) as archive:
    #with zipfile.ZipFile("resources.zip", mode="w" ) as archive:
        for file_path in directory.rglob("*"):
            archive.write(
                file_path,
                arcname=file_path.relative_to(directory)
            )
    return send_file('./resources.zip', attachment_filename= 'resources.zip', as_attachment=True)



    