from email.policy import default
import json
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import logging
logging.basicConfig(level=logging.INFO)
from flask import Flask, g, request, jsonify, render_template, redirect, send_from_directory, send_file
from flask_login import (current_user, LoginManager,
                             login_user, logout_user,
                             login_required)
from flask_mongoengine import MongoEngine
from mongoengine import *
from matplotlib import collections
from rpy2.robjects import pandas2ri as pr
from rpy2 import robjects as ro
import rpy2.robjects as robjects
from rpy2.robjects.conversion import localconverter as lc
from flask_cors import CORS
from glob import glob
from io import BytesIO
from zipfile import ZipFile
from python_helpers import new_graph_still_image

ALLOWED_EXTENSIONS = {'fcs'} #, "png", "jpg", "txt", "csv", "tsv"
#UPLOAD_FOLDER = "C:/Users/Zuhayr/Desktop/Zuhayr_Web_Data"
app = Flask(__name__, static_url_path='/static')
CORS(app)
#app.config["Upload_Folder"] = UPLOAD_FOLDER

app.config['MONGODB_SETTINGS'] = {
    'db': 'web_application_login',
    'host': '127.0.0.1',
    'port': 27017
}
#'bindip': "0.0.0.0"
app.secret_key = 'some key'
db = MongoEngine()
login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

############################ user_handler ############################
######################################################################

@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

@app.route('/login', methods=['POST'])
def login():
    # info = json.loads(request.data)
    # name = info.get('name', 'guest')
    # password = info.get('password', '')
    name = request.form['name']
    password = request.form['password']
    # info = request.get_json()
    # name = info.get('name', 'guest')
    # password = info.get('password', '')
    user = User.objects(name=name,
                        password=password).first()

    if user:
        print()
        login_user(user)
        return redirect("/dashboard")
        # return jsonify(user.to_json())
    else:
        return jsonify({"status": 401,
                        "reason": "Username or Password Error"})
 
@app.route('/logout', methods=['POST'])
def logout():
    print("logging out")
    logout_user()
    return redirect("/hyperspace")#jsonify(**{'result': 200, 'data': {'message': 'logout success'}})

@app.route('/user_info', methods=['POST'])
def user_info():
    if current_user.is_authenticated:
        resp = {"status": 200,
                "data": current_user.to_json()}
    else:
        resp = {"status": 401,
                "data": {"message": "user no login"}}
    return jsonify(resp)

class Job(db.EmbeddedDocument):
    username = db.StringField()
    job_name = db.StringField()
    # current_step = db.StringField()
        # if (path == None):
        #     self.path = "user_data/" + username + "/" + job_name + "/"
        # else:
        #     self.path = path
    fcs_files = db.StringField()
    path = db.StringField() #default=lambda: "user_data/" + username + job_name
    channels = db.ListField()
    current_step = db.IntField()
    analysis_list = db.ListField()

    def get_name(self):
        return self.job_name
    def set_current_step(self, step):
        self.current_step = step
        return self.current_step
    def add_fcs(self):
        self.fcs_files
        return 42
    def get_fcs_names(self):
        #self.path = "F:/user_data/" + self.username + "/" + self.job_name + "/" #"C:\Users\Zuhayr\Desktop\user_data\tim"
        self.fcs_files = os.listdir(self.path + "upload_fcs/") #"F:\user_data\tom\cool\fcs_files\776_F_SP_QC.fcs"
        return self.fcs_files
    def add_gates(self):
        return 42
    def add_normalized_fcs(self):
        return 42
    def set_channels(self, channels):
        print(channels)
        self.channels = channels
        return self.channels
    def get_channels(self):
        return self.channels
    # def toJSON(self):
    #     print("my own json creation below")
    #     print(json.dumps(self, default=lambda o: o.__dict__, ))
    #     return json.dumps(self, default=lambda o: o.__dict__)


class User(db.Document):
    name = db.StringField()
    password = db.StringField()
    meta = {'collection': 'User'}
    email = db.StringField()
    #job_list = []
    current_job = db.StringField()
    #job_list = db.ListField(EmbeddedDocumentField(Job))
    jobs = MapField(field=EmbeddedDocumentField(Job))
# http://docs.mongoengine.org/guide/defining-documents.html?highlight=object%20key%20value#field-arguments
    def to_json(self):
        return {"name": self.name,
                "email": self.email}
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)
    def get_name(self):
        return str(self.name)
    def create_new_job(self, job_name):
        #self.job_list.append(Job(self.name, job_name))
        return 42 #self.job_list
    # def recreate_job_objects_on_login(self):
    #     self.get_job_list_string()
    #     for i in range(len(self.job_list_string)):
    #         job_name = self.job_list_string[i]
    #         #current_step = "cool"
    #         path = "user_data/" + self.name + "/" + job_name + "/"
    #         fcs_file_list = os.listdir(path + "fcs_files/")
    #         #self.job_list.append(Job(self.name, job_name, current_step, path, fcs_file_list))
    #     return self.jobs
    def get_job_list_string(self):
        path =  "C:/Users/Zuhayr/Desktop/user_data/" + current_user.get_name() #"F:/user_data/" "C:/Users/Zuhayr/Desktop/user_data/"
        self.job_list_string = os.listdir(path)
        return self.job_list_string
    def get_job_list(self):
        return self.jobs
    def set_current_job(self, job_name):
        self.current_job = job_name
        return self.current_job
    def get_current_job(self):
        return self.jobs[self.current_job]
        #for job in self.job_list:
        #    print(job.get_name())
        #    if (job.get_name() == self.current_job):
        #       return job
    #def get_job_list(self):
    #    return self.jobs




@app.route('/')
def opening_page():
    return render_template("opening/hyperspace.html")

@app.route('/logged_in')
def logged_in():
    return render_template("/logged_in.html")

@app.route('/', methods=['GET'])
def query_records():
    name = request.args.get('name')
    user = User.objects(name=name).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(user.to_json())

@app.route('/', methods=['PUT'])
@login_required
def create_record():
    record = json.loads(request.data)
    user = User(name=record['name'],
                password=record['password'],
                email=record['email'])

    # try catch if error tell user to try another name
    user.save()
    #collection.insert_one(user)
    #logging.info("trying to create login")
    return jsonify(user.to_json())

@app.route('/', methods=['POST'])
@login_required
def update_record():
    record = json.loads(request.data)
    user = User.objects(name=record['name']).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.update(email=record['email'],
                    password=record['password'])
    return jsonify(user.to_json())

@app.route('/', methods=['DELETE'])
@login_required
def delete_record():
    record = json.loads(request.data)
    user = User.objects(name=record['name']).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.delete()
    return jsonify(user.to_json())

# @app.route("/set_current_job", methods=['POST'])
# @login_required
# def set_current_job():
#     job_name = request.args.get("job_name")
#     current_user.set_current_job(job_name)
#     return job_name

############################ routes ############################
################################################################

############################ general ############################


@app.route("/")
def initial():
    return render_template("opening/hyperspace.html")

@app.route("/about_us")
def about_us():
    return render_template("general/about_us.html", name = current_user.get_name(), job_list = json.dumps(current_user.get_job_list_string()))

@app.route("/account")
def account():
    return render_template("general/account.html", name = current_user.get_name(), job_list = json.dumps(current_user.get_job_list_string()))

@app.route("/dashboard")
def dashboard():
    # current_user.recreate_job_objects_on_login()
    return render_template("general/dashboard.html", name = current_user.get_name(), job_list = json.dumps(current_user.get_job_list_string()))
    
@app.route("/settings")
def settings():
    return render_template("general/settings.html", name = current_user.get_name(), job_list = json.dumps(current_user.get_job_list_string()))

############################ job_specific ############################ 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload_data", methods=['GET', 'POST'], defaults={'job_passed_in': ""})
@app.route("/upload_data/<job_passed_in>", methods=['GET', 'POST'])
def upload_data(job_passed_in = ""):
    # print(job.path + "upload_fcs")
    if (job_passed_in != ""):
        job_name = job_passed_in #request.args.get('job_name')
        current_user.set_current_job(job_name)
        #current_job = current_user.get_current_job()
        user =  User.objects(id=current_user.id)
        user.update(current_job=job_name)
    #print(type(current_job))
    job = current_user.get_current_job()
    job_name = job.get_name()
    path = job.path + "upload_fcs" #"user_data/" + current_user.get_name() + "/" + job_name + "/" + "fcs_files" #user.job_list["job_name"] 
    if request.method == 'POST':
        # check if the post request has the file part
        # print(request.files)
        if 'file_upload' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file_upload']
        # If the user does not select a file, the browser submits 
        # empty file without a filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # print(path + " got there")
        # print(file.filename)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = filename.replace(" ", "_")
            #file.save(os.path.join("C:/Users/rkhan/Desktop/Zuhayr_Web_Data", filename))
            print("why is it not uploading to " + os.path.join(path, filename))
            file.save(os.path.join(path, filename))
            file.seek(0)
            file.save(os.path.join(job.path + "latest_fcs", filename))
            current_user.get_current_job().get_fcs_names()
            return redirect(url_for('upload_data', name=filename))

    #current_user.get_current_job().set_current_step(1)
    # user.update(current_job=job_name)
    #user.find({"job_list": {"$elemMatch": {"username": current_user.get_name(), "job_name":1975}}})
    current_user.get_current_job().get_fcs_names()
    # print(current_user.get_current_job().fcs_files)
    return render_template("job_specific/upload_data.html", name = current_user.get_name(), job = json.dumps((current_user.get_current_job()).to_json()))

@app.route("/upload_helper")
def upload_helper():
    return render_template("job_specific/upload_data.html", name = current_user.get_name(), job = json.dumps((current_user.get_current_job()).to_json()))

# def update_job(job_name = current_user.get_current_job().job_name, current_step = current_user.get_current_job().current_step, fcs_files = current_user.get_current_job().fcs_files, channels = current_user.get_current_job().channels, analysis_list = current_user.get_current_job().analysis_list):
#     user_name = current_user.get_current_job().username
#     path = current_user.get_current_job().path

#     jobs = Job(username=user_name, job_name=job_name, path=path, fcs_files=fcs_files, current_step=current_step, channels=channels, analysis_list=analysis_list)
#     user =  User.objects(id=current_user.id).get()
#     user.jobs[job_name] = jobs
#     user.save()

#     return "42"

@app.route("/automated_qc")
def automated_qc():
    if current_user.get_current_job().current_step == 1:
        user_name = current_user.get_current_job().username
        job_name = current_user.get_current_job().job_name
        path = current_user.get_current_job().path
        fcs_files = current_user.get_current_job().fcs_files
        channels = current_user.get_current_job().channels
        analysis_list = (current_user.get_current_job().analysis_list)

        jobs = Job(username=user_name, job_name=job_name, path=path, fcs_files=fcs_files, current_step=2, channels=channels, analysis_list=analysis_list)
        user =  User.objects(id=current_user.id).get()
        user.jobs[job_name] = jobs
        user.save()
        #update_job(current_step=2)
    return render_template("job_specific/automated_qc.html", name = current_user.get_name(), job = json.dumps((current_user.get_current_job()).to_json()))

@app.route("/gating")
def gating():
    if current_user.get_current_job().current_step == 2:
        user_name = current_user.get_current_job().username
        job_name = current_user.get_current_job().job_name
        path = current_user.get_current_job().path
        fcs_files = current_user.get_current_job().fcs_files
        channels = current_user.get_current_job().channels
        analysis_list = (current_user.get_current_job().analysis_list)

        jobs = Job(username=user_name, job_name=job_name, path=path, fcs_files=fcs_files, current_step=3, channels=channels, analysis_list=analysis_list)
        user =  User.objects(id=current_user.id).get()
        user.jobs[job_name] = jobs
        user.save()
    return render_template("job_specific/gating.html", name = current_user.get_name(), job = json.dumps((current_user.get_current_job()).to_json()))

@app.route("/normalization")
def normalization():
    if current_user.get_current_job().current_step == 3:
        user_name = current_user.get_current_job().username
        job_name = current_user.get_current_job().job_name
        path = current_user.get_current_job().path
        fcs_files = current_user.get_current_job().fcs_files
        channels = current_user.get_current_job().channels
        analysis_list = (current_user.get_current_job().analysis_list)

        jobs = Job(username=user_name, job_name=job_name, path=path, fcs_files=fcs_files, current_step=4, channels=channels, analysis_list=analysis_list)
        user =  User.objects(id=current_user.id).get()
        user.jobs[job_name] = jobs
        user.save()
    return render_template("job_specific/normalization.html", name = current_user.get_name(), job = json.dumps((current_user.get_current_job()).to_json()))

@app.route("/downsampling")
def downsampling():
    if current_user.get_current_job().current_step == 4:
        user_name = current_user.get_current_job().username
        job_name = current_user.get_current_job().job_name
        path = current_user.get_current_job().path
        fcs_files = current_user.get_current_job().fcs_files
        channels = current_user.get_current_job().channels
        analysis_list = (current_user.get_current_job().analysis_list)

        jobs = Job(username=user_name, job_name=job_name, path=path, fcs_files=fcs_files, current_step=5, channels=channels, analysis_list=analysis_list)
        user =  User.objects(id=current_user.id).get()
        user.jobs[job_name] = jobs
        user.save()
    return render_template("job_specific/downsampling.html", name = current_user.get_name(), job = json.dumps((current_user.get_current_job()).to_json()))

@app.route("/dr_clustering")
def dr_clustering():
    if current_user.get_current_job().current_step == 5:
        user_name = current_user.get_current_job().username
        job_name = current_user.get_current_job().job_name
        path = current_user.get_current_job().path
        fcs_files = current_user.get_current_job().fcs_files
        channels = current_user.get_current_job().channels
        analysis_list = (current_user.get_current_job().analysis_list)

        jobs = Job(username=user_name, job_name=job_name, path=path, fcs_files=fcs_files, current_step=6, channels=channels, analysis_list=analysis_list)
        user =  User.objects(id=current_user.id).get()
        user.jobs[job_name] = jobs
        user.save()
    return render_template("job_specific/dr_clustering.html", name = current_user.get_name(), job = json.dumps((current_user.get_current_job()).to_json()))

@app.route("/download_results")
def download_results():
    if current_user.get_current_job().current_step == 6:
        user_name = current_user.get_current_job().username
        job_name = current_user.get_current_job().job_name
        path = current_user.get_current_job().path
        fcs_files = current_user.get_current_job().fcs_files
        channels = current_user.get_current_job().channels
        analysis_list = (current_user.get_current_job().analysis_list)
        current_step = current_user.get_current_job().current_step

        jobs = Job(username=user_name, job_name=job_name, path=path, fcs_files=fcs_files, current_step=current_step, channels=channels, analysis_list=analysis_list)
        user =  User.objects(id=current_user.id).get()
        user.jobs[job_name] = jobs
        user.save()
    return render_template("job_specific/download_results.html", name = current_user.get_name(), job = json.dumps((current_user.get_current_job()).to_json()))

############################ ajax requests ############################
#######################################################################

@app.route("/new")
def new(): 
    path = request.args.get("path")
    point_list = request.args.get("list_points")
    x_axis = request.args.get("x_axis")
    y_axis = request.args.get("y_axis")
    # print(x_axis, y_axis)
    
    #logging.info("new flask " + point_list)
    #path = "C:/Users/Zuhayr/Documents/GitHub/r_background_app/PeacoQC_results/fcs_files/776 F SP_QC.fcs"
    if (x_axis != None and y_axis != None):
        new_graph_still_image.createBokeh(path, channel1 = x_axis, channel2 = y_axis, points_array = point_list, output_path = (current_user.get_current_job()).path + "/gating/temporary_images/mark1.png")
    else:
        new_graph_still_image.createBokeh(path, points_array = point_list, output_path = (current_user.get_current_job()).path + "/gating/temporary_images/mark1.png")

    # b = request.args.get("b")
    # return jsonify(result = returned_image)
    print("did it update")
    return render_template("job_specific/gating.html")


@app.route("/create_job")
def add_job():
    job_name = request.args.get("job_name")
    user_name = current_user.get_name()
    directory = "C:/Users/Zuhayr/Desktop/user_data/" + user_name + "/" #"C:/Users/Zuhayr/Desktop/user_data/"  F:/user_data/
    # os.makedirs(directory + job_name + "/")
    # os.makedirs(directory + job_name + "/fcs_files/")
    # os.makedirs(directory + job_name + "/qc_cleaned_fcs/")
    # os.makedirs(directory + job_name + "/temporary_images/")
    # os.makedirs(directory + job_name + "/normalized_fcs/")
    # os.makedirs(directory + job_name + "/clustering_results/")
    # os.makedirs(directory + job_name + "/available_for_download/")
    # with open(directory + job_name +'/job_description.txt', 'w') as f:
    #     f.write('')

    os.makedirs(directory + job_name + "/")
    os.makedirs(directory + job_name + "/upload_fcs/")
    os.makedirs(directory + job_name + "/automated_qc/")
    os.makedirs(directory + job_name + "/gating/")
    os.makedirs(directory + job_name + "/gating/temporary_images/")
    os.makedirs(directory + job_name + "/normalization/")
    os.makedirs(directory + job_name + "/downsampling/")
    os.makedirs(directory + job_name + "/dr_clustering/")
    os.makedirs(directory + job_name + "/latest_fcs/")

    jobs = Job(username=user_name, job_name=job_name, path="C:/Users/Zuhayr/Desktop/user_data/" + user_name + "/" + job_name + "/", current_step=1, analysis_list=[]) # "C:/Users/Zuhayr/Desktop/user_data/" F:/user_data/
    user =  User.objects(id=current_user.id).get()
    user.jobs[job_name] = jobs
    user.save()

    return job_name + " was created"

def delete_files(directory):
    for f in os.listdir(directory):
        if not os.path.isdir(os.path.join(directory, f)):
            os.remove(os.path.join(directory, f))
        #else:
           # raise ValueError('You tried to delete a non empty directory bozo')
    return directory

##################################      Neeed lots of changes to get edit button to work with latest files


@app.route('/edit_anyway')
def edit_anyway():
    step_to_edit = int(request.args.get("step_to_edit"))
    step_list = ["upload_data", "automated_qc", "gating", "normalization", "downsampling", "dr_clustering"] #, "download_results"   
    # edit_index = step_list[step_to_edit]

    user_name = current_user.get_current_job().username
    job_name = current_user.get_current_job().job_name
    directory = "C:/Users/Zuhayr/Desktop/user_data/" + user_name + "/" + job_name

    for step in range(len(step_list)):
        if step_to_edit < step + 1:
            if (step + 1 == 2):
                delete_files(directory + "/automated_qc/")
            if (step + 1 == 3):
                delete_files(directory + "/gating/temporary_images/")
            if (step + 1 == 4):
                delete_files(directory + "/normalization/")
            if (step + 1 == 5):
                delete_files(directory + "/downsampling/")
            if (step + 1 == 6):
                delete_files(directory + "/dr_clustering/")
            if (step + 1 == 7):
                delete_files(directory + "/download_results/")

    user_name = current_user.get_current_job().username
    job_name = current_user.get_current_job().job_name
    path = current_user.get_current_job().path
    fcs_files = current_user.get_current_job().fcs_files
    channels = current_user.get_current_job().channels
    analysis_list = (current_user.get_current_job().analysis_list)
    # current_step = current_user.get_current_job().current_step

    jobs = Job(username=user_name, job_name=job_name, path=path, fcs_files=fcs_files, current_step=step_to_edit, channels=channels, analysis_list=analysis_list)
    user =  User.objects(id=current_user.id).get()
    user.jobs[job_name] = jobs
    user.save()

    return "cool" #step_to_edit


# @app.route('/download_file')
# def download_file():
#     path = os.listdir(request.args.get("path"))

#     return send_file(path, as_attachment=True)

##################################    maybe make a download one file and download everything in directory
@app.route('/download_file')
def download_file():
    # target = 'dir1/dir2'
    path = request.args.get("path")
    files = os.listdir(path)
    #files = [] ############### remove this line when trying to actually run
    print(path)
    print(files)
    if files != []:
        stream = BytesIO()
        with ZipFile(stream, 'w') as zf:
            for file in files:#glob(os.path.join(target, '*.sql'))
                print(path + file)
                zf.write(file, path + file) #os.path.basename os.path.join

                # data = zipfile.ZipInfo(individualFile['fileName'])
                # data.date_time = time.localtime(time.time())[:6]
                # data.compress_type = zipfile.ZIP_DEFLATED
                # zf.writestr(data, individualFile['fileData'])
        stream.seek(0)
        return send_file(stream, as_attachment=True, attachment_filename='cleaned_fcs.zip')
    return "42"

# @app.route('/set_job')
# def set_job():
#     name = request.args.get('job_name')
#     print(name)
#     current_user.set_current_job(name)
#     return name + " was acessed"

#def change_job_attributes(user_name = current_user.get_current_job().username, job_name = current_user.get_current_job().job_name, path = current_user.get_current_job().path, fcs_files = current_user.get_current_job().fcs_files, current_step = current_user.get_current_job().current_step, analysis_list = (current_user.get_current_job().analysis_list), channels=current_user.get_current_job().channels):
def change_job_attributes(channels):
    user_name = current_user.get_current_job().username
    job_name = current_user.get_current_job().job_name
    path = current_user.get_current_job().path
    fcs_files = current_user.get_current_job().fcs_files
    current_step = current_user.get_current_job().current_step
    analysis_list = (current_user.get_current_job().analysis_list)
    channels = channels #current_user.get_current_job().channels
    steps_ran = {"qc": False, "gating": {},"normalization": False, "downsampling": "", "dr_clustering": []}
    
    jobs = Job(username=user_name, job_name=job_name, path=path, fcs_files=fcs_files, current_step=current_step, channels=channels, analysis_list=analysis_list)
    user =  User.objects(id=current_user.id).get()
    user.jobs[job_name] = jobs
    user.save()

############################ r files ############################

@app.route("/get_peaqo")
def get_peaqo():
    job_path = request.args.get("job_path")
    #print(job_path)
    fcs_files_path = job_path + "latest_fcs/"

    fileName = "R_files\\peaqo.r"
    url = "C:\\Users\\rkhan\\Documents\\GitHub\\front_end_flow\\R_files\\peaqo.r" # C:\\Users\\Zuhayr\\Documents\\GitHub\\tutorial\\r_files\\peaqo.r
    with lc(ro.default_converter + pr.converter):
        fileName_c = ro.conversion.py2rpy(fileName)
        url_c = ro.conversion.py2rpy(url)
    ro.globalenv['fileName'] = fileName_c
    ro.globalenv['url'] = url_c

    r = robjects.r
    r.source('R_files\\peaqo.r') # lowercase r

    run_QC = robjects.globalenv['run_QC']
    for fcs in os.listdir(fcs_files_path):
        print(fcs_files_path + fcs)
        markernames = run_QC(fcs_files_path + fcs, output = job_path + "/automated_qc/")
        print(markernames)
        markernames = list(markernames)
        print(markernames)
        print(type(markernames))

    print(os.listdir(fcs_files_path))

    if os.listdir(fcs_files_path) == []:
        markernames = []

    print(markernames)
    print(type(markernames))

    # user_name = current_user.get_current_job().username
    # job_name = current_user.get_current_job().job_name
    # path = current_user.get_current_job().path
    # fcs_files = current_user.get_current_job().fcs_files
    # current_step = current_user.get_current_job().current_step
    # analysis_list = (current_user.get_current_job().analysis_list)
    # #steps_ran = {"qc": False, "gating": {},"normalization": False, "downsampling": "", "dr_clustering": []}
    
    # jobs = Job(username=user_name, job_name=job_name, path=path, fcs_files=fcs_files, current_step=current_step, channels=markernames, analysis_list=analysis_list)
    # user =  User.objects(id=current_user.id).get()
    # user.jobs[job_name] = jobs
    # user.save()

    change_job_attributes(channels=markernames)

    return job_path + "/automated_qc/"

@app.route("/get_normalize")
def get_normalize():
    selected_channels = request.args.get("selected_channels")
    print(selected_channels)
    job_path = request.args.get("job_path")
    fcs_files_path = job_path + "automated_qc/PeacoQC_results/fcs_files"#"gated_fcs_files/"

    fileName = "R_files\\gaussNorm.r"
    url = "C:\\Users\\rkhan\\Documents\\GitHub\\front_end_flow\\R_files\\gaussNorm.r" #"C:\\Users\\Zuhayr\\Documents\\GitHub\\tutorial\\r_files\\gaussNorm.r" #C:\Users\rkhan\Documents\GitHub\front_end_flow\R_files\gaussNorm.r
    with lc(ro.default_converter + pr.converter):
        fileName_c = ro.conversion.py2rpy(fileName)
        url_c = ro.conversion.py2rpy(url)
    ro.globalenv['fileName'] = fileName_c
    ro.globalenv['url'] = url_c

    r = robjects.r
    r.source('R_files\\gaussNorm.r')

    gaussNorm = robjects.globalenv['run_norm']
    path = fcs_files_path
    files_vector = os.listdir(path)
    channels_vector = selected_channels
    gaussNorm(path, files_vector) #normalize_peaks_graph =  #channels_vector #'C:\\Users\\Zuhayr\\Documents\\GitHub\\front_end_monochrome\\user_data\\Bob\\Job1\\fcs_files\\776 F SP_QC.fcs'
    return "42" #(normalize_peaks_graph)


@app.route("/get_random_downsampling")
def get_random_downsampling():
    output_path = request.args.get("job_path")
    fcs_path = output_path + "latest_fcs"#"qc_cleaned_fcs\\PeacoQC_results\\fcs_files\\776_F_SP_QC_QC.fcs" #"F:\user_data\tom\wow\qc_cleaned_fcs\PeacoQC_results\fcs_files\776_F_SP_QC_QC.fcs"
    # channels = request.args.get("channels")

    fileName = "R_files\\downsampling.r"
    url = "C:\\Users\\rkhan\\Documents\\GitHub\\front_end_flow\\R_files\\downsampling.r"
    with lc(ro.default_converter + pr.converter):
        fileName_c = ro.conversion.py2rpy(fileName)
        url_c = ro.conversion.py2rpy(url)
    ro.globalenv['fileName'] = fileName_c
    ro.globalenv['url'] = url_c

    r = robjects.r
    r.source('R_files\\downsampling.r')

    random_downsample = robjects.globalenv['simple_random_sampling']
    for path in os.listdir(fcs_path):
        random_downsample(path, output_path)
    return "42"#(spade_graph)


@app.route("/get_spade_downsampling")
def get_spade_downsampling():
    output_path = request.args.get("job_path")
    fcs_path = output_path + "latest_fcs" #"qc_cleaned_fcs\\PeacoQC_results\\fcs_files\\776_F_SP_QC_QC.fcs" #"F:\user_data\tom\wow\qc_cleaned_fcs\PeacoQC_results\fcs_files\776_F_SP_QC_QC.fcs"
    # channels = request.args.get("channels")

    fileName = "R_files\\downsampling.r"
    url = "C:\\Users\\rkhan\\Documents\\GitHub\\front_end_flow\\R_files\\downsampling.r"
    with lc(ro.default_converter + pr.converter):
        fileName_c = ro.conversion.py2rpy(fileName)
        url_c = ro.conversion.py2rpy(url)
    ro.globalenv['fileName'] = fileName_c
    ro.globalenv['url'] = url_c

    r = robjects.r
    r.source('R_files\\downsampling.r')

    spade_downsample = robjects.globalenv['spade_downsample']
    for path in os.listdir(fcs_path):
        spade_downsample(path, output_path)
    return "42"#(spade_graph)


@app.route("/get_clustering_dr")
def get_clustering():
    analysis_method = request.args.get("analysis_method")
    # path = request.args.get("path")
    channels = request.args.get("channels")
    #num_pcs = request.args.get("num_pcs")

    fileName = "clustering_dr.r"
    url = "C:\\Users\\Zuhayr\\Documents\\GitHub\\all_together\\R_files\\clustering_dr.r"
    with lc(ro.default_converter + pr.converter):
        fileName_c = ro.conversion.py2rpy(fileName)
        url_c = ro.conversion.py2rpy(url)
    ro.globalenv['fileName'] = fileName_c
    ro.globalenv['url'] = url_c

    user_name = current_user.get_current_job().username
    job_name = current_user.get_current_job().job_name
    path = current_user.get_current_job().path
    fcs_files = current_user.get_current_job().fcs_files
    current_step = current_user.get_current_job().current_step
    analysis_list = (current_user.get_current_job().analysis_list).append(analysis_method)

    jobs = Job(username=user_name, job_name=job_name, path=path, fcs_files=fcs_files, current_step=current_step, analysis_list=analysis_list)
    user =  User.objects(id=current_user.id).get()
    user.jobs[job_name] = jobs
    user.save()

    r = robjects.r
    r.source('R_files\\clustering_dr.r')
    print("got to analysis")
    if (analysis_method == "pca"):
        print("pca")
        pca = robjects.globalenv['graph_scree']
        path = path + "upload_fcs"
        for file in os.listdir(path):
            print(path + "/" + file)
            pca_plot = pca(path + "/" + file, current_user.get_current_job().path + "dr_clustering/", file) #, channels = channels
        return(pca_plot)
    if (analysis_method == "umap"):
        print("umap")
        umap = robjects.globalenv['umap']
        path = path + "upload_fcs"
        for file in (os.listdir(path))[0]:
            print(path + "/" + file)
            umap_plot = umap(path + "/" + file, current_user.get_current_job().path + "dr_clustering/") #, channels = channels , current_user.get_current_job().path + "dr_clustering/", file
        return "umap" #(pca_plot)
    if (analysis_method == "tsne"):
        print("tsne")
        tsne = robjects.globalenv['tsne']
        path = path + "upload_fcs"
        for file in os.listdir(path):
            print(path + "/" + file)
            tsne_plot = tsne(path + "/" + file, current_user.get_current_job().path + "dr_clustering/") #, channels = channels  , current_user.get_current_job().path + "dr_clustering/", file
        return "tsne" #(pca_plot)
    r.q(save="no")


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(host='0.0.0.0', port = 5000, debug = True)
