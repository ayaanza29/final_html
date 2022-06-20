import json
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import logging
logging.basicConfig(level=logging.INFO)
from flask import Flask, g, request, jsonify, render_template, redirect
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

ALLOWED_EXTENSIONS = {'fcs', "png", "jpg"}
UPLOAD_FOLDER = "C:/Users/Zuhayr/Desktop/Zuhayr_Web_Data"
app = Flask(__name__, static_url_path='/static')
CORS(app)
app.config["Upload_Folder"] = UPLOAD_FOLDER

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
    logout_user()
    return jsonify(**{'result': 200,
                      'data': {'message': 'logout success'}})

@app.route('/user_info', methods=['POST'])
def user_info():
    if current_user.is_authenticated:
        resp = {"status": 200,
                "data": current_user.to_json()}
    else:
        resp = {"status": 401,
                "data": {"message": "user no login"}}
    return jsonify(resp)

class User(db.Document):
    meta = {'collection': 'User'}
    name = db.StringField()
    password = db.StringField()
    email = db.StringField()
    job_list = []
    current_job = None

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
        self.job_list.append(Job(self.name, job_name))
        return self.job_list
    def recreate_job_objects_on_login(self):
        self.get_job_list()
        for i in range(len(self.job_list_string)):
            job_name = self.job_list_string[i]
            current_step = "cool"
            path = "user_data/" + self.name + "/" + job_name + "/"
            fcs_file_list = os.listdir(path + "fcs_files/")
            self.job_list.append(Job(self.name, job_name, current_step, path, fcs_file_list))
        return self.job_list
    def get_job_list(self):
        path = "user_data/" + current_user.get_name()
        self.job_list_string = os.listdir(path)
        return self.job_list_string
    def set_current_job(self, job_name):
        for job in self.job_list:
            if(job.get_name() == job_name):
                print("set current job to" + job_name)
                self.current_job = job
        return self.current_job
    def get_current_job(self):
        return self.current_job

class Job():
    def __init__(self, username, job_name, current_step = "cool", path = None, fcs_file_list = []): #, job_description, fcs_files, qc_files, normalize_files, normalize_graph, downsample_file
        self.username = username 
        self.job_name = job_name
        self.current_step = current_step
        if (path == None):
            self.path = "user_data/" + username + "/" + job_name + "/"
        else:
            self.path = path
        self.fcs_file_list = fcs_file_list
    def get_name(self):
        return self.job_name
    def add_fcs(self):
        self.fcs_files
        return 42
    def get_fcs_names(self):
        self.fcs_files = os.listdir(self.path + "fcs_files/")
        return self.fcs_file_list
    def add_gates(self):
        return 42
    def add_normalized_fcs(self):
        return 42
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)


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


############################ routes ############################
################################################################

############################ general ############################


@app.route("/")
def initial():
    return render_template("opening/hyperspace.html")

@app.route("/about_us")
def about_us():
    return render_template("general/about_us.html")

@app.route("/account")
def account():
    return render_template("general/account.html")

@app.route("/dashboard")
def dashboard():
    current_user.recreate_job_objects_on_login()
    return render_template("general/dashboard.html", name = current_user.get_name(), job_list = json.dumps(current_user.get_job_list()))
    
@app.route("/settings")
def settings():
    return render_template("general/settings.html")

############################ job_specific ############################ 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload_data/<job_passed_in>", methods=['GET', 'POST'])
def upload_data(job_passed_in = ""):
    if (job_passed_in != ""):
        job_name = job_passed_in #request.args.get('job_name') 
    current_user.set_current_job(job_name)
    current_job = current_user.get_current_job()
    print(type(current_job))
    path = current_job.path + "fcs_files"
    if request.method == 'POST':
        print("entered post request upload data")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits a
        # empty file without a filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #file.save(os.path.join("C:/Users/rkhan/Desktop/Zuhayr_Web_Data", filename))
            file.save(os.path.join(path, filename))
            return redirect(url_for('upload_file', name=filename))
    return render_template("job_specific/upload_data.html", name = current_user.get_name(), job = json.dumps((current_user.get_current_job()).toJSON())) #job = json.dumps(current_user.get_current_job().get_name()), fcs_files = json.dumps(((current_user.get_current_job()).get_fcs_names())

@app.route("/upload_helper")
def upload_helper():
    return render_template("job_specific/upload_data.html", name = current_user.get_name(), job = json.dumps((current_user.get_current_job()).toJSON()))

@app.route("/automated_qc")
def automated_qc():
    return render_template("job_specific/automated_qc.html", name = current_user.get_name(), job = json.dumps((current_user.get_current_job()).toJSON()))

@app.route("/gating")
def gating():
    return render_template("job_specific/gating.html", name = current_user.get_name(), job = current_user.get_current_job())

@app.route("/normalization")
def normalization():
    return render_template("job_specific/normalization.html", name = current_user.get_name(), job = current_user.get_current_job())

@app.route("/downsampling")
def downsampling():
    return render_template("job_specific/downsampling.html", name = current_user.get_name(), job = current_user.get_current_job())

@app.route("/dr_clustering")
def dr_clustering():
    return render_template("job_specific/dr_clustering.html", name = current_user.get_name(), job = current_user.get_current_job())

@app.route("/download_results")
def download_results():
    return render_template("job_specific/download_results.html", name = current_user.get_name(), job = current_user.get_current_job())

############################ ajax requests ############################
#######################################################################

@app.route("/create_job")
def add_job():
    job_name = request.args.get("job_name")
    user_name = current_user.get_name()
    directory = "user_data/" + user_name + "/"
    os.makedirs(directory + job_name + "/")
    os.makedirs(directory + job_name + "/fcs_files/")
    os.makedirs(directory + job_name + "/temporary_images/")
    with open(directory + job_name +'/job_description.txt', 'w') as f:
        f.write('')
    current_user.create_new_job(job_name)
    return job_name + " was created"

# @app.route('/set_job')
# def set_job():
#     name = request.args.get('job_name')
#     print(name)
#     current_user.set_current_job(name)
#     return name + " was acessed"

############################ r files ############################

# @app.route("/get_peaqo") 
# def get_peaqo():  

#     path = request.args.get("path")
#     channels = request.args.get("channels")

    # fileName = "peaqo.r"
    # url = "C:\\Users\\Zuhayr\\Documents\\GitHub\\all_together\\R_files\\peaqo.r"
    # with lc(ro.default_converter + pr.converter):
    #     fileName_c = ro.conversion.py2rpy(fileName)
    #     url_c = ro.conversion.py2rpy(url)
    # ro.globalenv['fileName'] = fileName_c
    # ro.globalenv['url'] = url_c

    # r = robjects.r
    # r.source('R_files\\clustering_dr.r')

    # densvis_umap = robjects.globalenv['densvis_umap']
    # print("start qc cool")
    # densvis_umap(path)

    #return 42 (output_path)

# @app.route("/get_peaqo")
# def get_peaqo():

#     path = request.args.get("path")
#     channels = request.args.get("channels")

#     fileName = "peaqo.r"
#     url = "C:\\Users\\Zuhayr\\Documents\\GitHub\\all_together\\R_files\\peaqo.r"
#     with lc(ro.default_converter + pr.converter):
#         fileName_c = ro.conversion.py2rpy(fileName)
#         url_c = ro.conversion.py2rpy(url)
#     ro.globalenv['fileName'] = fileName_c
#     ro.globalenv['url'] = url_c

#     r = robjects.r
#     r.source('R_files\\clustering_dr.r')

#     densvis_umap = robjects.globalenv['densvis_umap']
#     print("start qc cool")
#     densvis_umap(path)

#     return 42 #(output_path)

@app.route("/get_peaqo")
def get_peaqo():
    fileName = "peaqo.r"
    url = "C:\\Users\\Zuhayr\\Documents\\GitHub\\all_together\\R_files\\peaqo.r"
    with lc(ro.default_converter + pr.converter):
        fileName_c = ro.conversion.py2rpy(fileName)
        url_c = ro.conversion.py2rpy(url)
    ro.globalenv['fileName'] = fileName_c
    ro.globalenv['url'] = url_c

    r = robjects.r
    r.source('R_files\\peaqo.r')

    run_QC = robjects.globalenv['run_QC']
    run_QC('C:\\Users\\Zuhayr\\Documents\\GitHub\\front_end_monochrome\\user_data\\Bob\\Job1\\fcs_files\\776 F SP_QC.fcs', output = 'C:\\Users\\Zuhayr\\Documents\\GitHub\\front_end_monochrome\\user_data\\Bob\\Job1\\')
    return 'C:\\Users\\Zuhayr\\Documents\\GitHub\\front_end_monochrome\\user_data\\Bob\\Job1\\'




if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(host='0.0.0.0', port = 5000, debug = True)
