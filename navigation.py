from flask import Flask, flash, request, render_template

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

@app.route("/help")
def help():
    return render_template("general/help.html")

@app.route("/settings")
def settings():
    return render_template("general/settings.html")

############################ job_specific ############################


@app.route("/upload_data")
def upload_data():
    return render_template("job_specific/upload_data.html")

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

