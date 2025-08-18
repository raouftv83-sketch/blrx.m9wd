from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# بيانات الدخول (ممكن تبدلها)
USERNAME = "BLRX"
PASSWORD = "M9WD.BLRX"

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    user = request.form.get("username")
    password = request.form.get("password")
    
    if user == USERNAME and password == PASSWORD:
        return redirect(url_for("player"))
    else:
        return render_template("login.html", error="❌ اسم المستخدم أو كلمة المرور غير صحيحة")

@app.route("/player")
def player():
    return render_template("player.html")

if __name__ == "__main__":
    app.run(debug=True)