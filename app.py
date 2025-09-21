from flask import Flask, request, render_template

app = Flask(__name__)

user_input = []
password = []

@app.route('/')
def index():
    # Render the login template with no password initially
    return render_template('front_end.html', pwd="")

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    pwd = request.form.get('password')

    if username:
        user_input.append(username)
    if pwd:
        password.append(pwd)
    
    print('Usernames:', user_input)
    print('Passwords:', password)

    # Render the template again, passing the latest password for display
    return render_template('front_end.html', pwd=pwd)

if __name__ == "__main__":
    app.run(debug=True)
