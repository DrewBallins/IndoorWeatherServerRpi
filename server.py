from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
   temperature = 24  # TODO: replace hard-coded temperature with temp from Arduino
   humidity = 75     # TODO: replace hard-coded temperature with temp from Arduino
   return render_template('index.html', temperature = temperature, humidity = humidity)

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0')
