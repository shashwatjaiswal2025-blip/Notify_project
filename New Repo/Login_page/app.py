
from flask import Flask, request, render_template
from login import check_login

app = Flask(__name__)


@app.route('/')
def index():
    # Render the login template with no password initially
    return render_template('front_end.html', pwd="")

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username').strip()
    pwd = request.form.get('password').strip()

    # Use check_login to verify credentials
    if check_login(username, pwd):
        result = "Authorised"
    else:
        result = "Invalid username or password."

    # Optionally print or pass result to template
    print(result)
    return render_template('front_end.html', pwd=pwd, result=result)

if __name__ == "__main__":
    app.run(debug=True)