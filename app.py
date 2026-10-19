from flask import Flask, render_template, request, redirect, url_for, flash
from stack import stack_bp, to_value
from linkedlist import linkedlist_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.register_blueprint(stack_bp) 
app.register_blueprint(linkedlist_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/works')
def works():
    return render_template('works.html')

@app.route('/works/convert/touppercase', methods=['GET', 'POST'])
def touppercase():
    result = None
    error = None
    if request.method == 'POST':
        input_string = request.form.get('inputString', '').strip()
        if input_string == '':
            error = "Type something first."
        else:
            result = input_string.upper()
    return render_template('touppercase.html', result=result, error=error)
 
@app.route('/works/area/circle', methods=['GET', 'POST'])
def circle():
    result = None
    error = None
    if request.method == 'POST':
        try:
            radius = float(request.form.get('radius', ''))
            result = f"{3.14 * radius * radius:.2f}"
        except ValueError:
            error = "Enter a number, like 5 or 2.5."
    return render_template('circle.html', result=result, error=error)
 
@app.route('/works/area/triangle', methods=['GET', 'POST'])
def triangle():
    result = None
    error = None
    if request.method == 'POST':
        try:
            base = float(request.form.get('base', ''))
            height = float(request.form.get('height', ''))
            result = f"{0.5 * base * height:.2f}"
        except ValueError:
            error = "Enter numbers only, like 5 or 2.5."
    return render_template('triangle.html', result=result, error=error)
 
 
# @app.route('/areaOfcirle', methods=['GET', 'POST'])
# def areaOfcirle():
#     result = None
#     name=request.get('name','')
#     print(name)
#     if request.method == 'POST':
#         input_string = request.form.get('inputradius', '')
#         result = int(input_string) * int(input_string) * 3.14
#     return render_template('areaCircle.html', result=result)
 
@app.route('/contact')
def contact():
    return render_template('contact.html')
 
if __name__ == "__main__":
    app.run(debug=True)