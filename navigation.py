from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'fcs', "png", "jpg"}
UPLOAD_FOLDER = "C:/Users/Zuhayr/Desktop/Zuhayr_Web_Data"
app = Flask(__name__, static_url_path='/static')
app.config["Upload_Folder"] = UPLOAD_FOLDER

############################ general ############################


@app.route("/")
def initial():
    return render_template("general/dashboard.html")

@app.route("/about_us")
def about_us():
    return render_template("general/about_us.html")

@app.route("/account")
def account():
    return render_template("general/account.html")

@app.route("/dashboard")
def dashboard():
    return render_template("general/dashboard.html")
    
@app.route("/settings")
def settings():
    return render_template("general/settings.html")

############################ job_specific ############################

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload_data", methods=['GET', 'POST'])
def upload_data():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #file.save(os.path.join("C:/Users/rkhan/Desktop/Zuhayr_Web_Data", filename))
            file.save(os.path.join("C:/Users/Zuhayr/Desktop/Zuhayr_Web_Data", filename))
            return redirect(url_for('upload_file', name=filename))
    #return render_template("upload_help.html")
    return render_template("job_specific/upload_data.html")

@app.route("/upload_helper")
def upload_helper():
    return render_template("job_specific/upload_helper.html")

@app.route("/automated_qc")
def automated_qc():
    return render_template("job_specific/automated_qc.html")

@app.route("/gating")
def gating():
    return render_template("job_specific/gating.html")

@app.route("/normalization")
def normalization():
    return render_template("job_specific/normalization.html")

@app.route("/downsampling")
def downsampling():
    return render_template("job_specific/downsampling.html")

@app.route("/dr_clustering")
def dr_clustering():
    return render_template("job_specific/dr_clustering.html")

@app.route("/download_results")
def download_results():
    return render_template("job_specific/download_results.html")


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(port = 5000, debug = True)

