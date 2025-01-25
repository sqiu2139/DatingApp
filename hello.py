from markupsafe import escape

from flask import Flask
from flask import url_for
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"

@app.route('/users/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route("/id/<int:post_id>")
def handle_id(post_id):
    return f"Handle {post_id}"

@app.route("/test/<string:user>")
def handle_user(user):
    return f"Handle {user}"

with app.test_request_context():
    #print(url_for('user', username='John Doe'))
    print(url_for('handle_user', user="gechang"))
