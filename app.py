from flask import Flask, request, render_template, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = "BLRX_SECRET_KEY"  # مهم للـ session

# بيانات تسجيل الدخول الثابتة
USERNAME = "BLRX"
PASSWORD = "M9WD.BLRX"

# ------------------------
# صفحة تسجيل الدخول
# ------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        user = request.form.get("username")
        pwd = request.form.get("password")
        if user == USERNAME and pwd == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            message = "❌ اسم المستخدم أو كلمة المرور خاطئة"
    return render_template("login.html", message=message)

# ------------------------
# صفحة Home بعد تسجيل الدخول
# ------------------------
@app.route("/home")
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template("home.html")

# ------------------------
# صفحة UID
# ------------------------
@app.route("/uid", methods=["GET", "POST"])
def uid_page():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    player_info = None
    message = ""

    if request.method == "POST":
        uid = request.form.get("uid")
        url = f"https://info-ch9ayfa.vercel.app/{uid}"

        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()  # تأكد أن الرد 200 OK
            data = res.json()
        except requests.exceptions.HTTPError:
            data = {}
            message = "❌ الخطأ: UID غير موجود أو السيرفر رفض الطلب"
        except requests.exceptions.RequestException:
            data = {}
            message = "❌ فشل الاتصال بالـ API"
        except ValueError:
            data = {}
            message = "❌ الرد من الـ API غير صالح"

        def clean(val):
            return str(val) if val not in [None, "", "-", "null"] else "❌ غير متوفر"

        player_info = {
            "uid": uid,
            "name": clean(data.get("AccountName")),
            "level": clean(data.get("AccountLevel")),
            "likes": clean(data.get("AccountLikes")),
            "create_time": clean(data.get("AccountCreateTime")),
        }

        if player_info["name"] == "❌ غير متوفر":
            message = "❌ لا توجد بيانات لهذا UID"
            player_info = None

    return render_template("uid.html", player_info=player_info, message=message)

# ------------------------
# خروج المستخدم
# ------------------------
@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# ------------------------
# تشغيل التطبيق
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)
