from flask import Flask
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def helloWorld():
  return'{"message" : "Hello, cross-origin-world!"}'


@app.route("/hellotesting")
@cross_origin()
def hiworld():
  return'{"message" : "hi!"}'


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)

