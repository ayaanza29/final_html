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
    return render_template("general_about_us.html")

@app.route("/account")
def account():
    return render_template("general_account.html")

@app.route("/dashboard")
def dashboard():
    return render_template("general/dashboard.html")

@app.route("/help")
def help():
    return render_template("general_help.html")

@app.route("/settings")
def settings():
    return render_template("general_settings.html")

############################ job_specific ############################


@app.route("/upload_data")
def upload_data():
    return render_template("job_specific/upload_data.html")

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(port = 5000, debug = True)
    
