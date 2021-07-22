from flask import Flask, render_template, url_for
app = Flask(__name__)

posts = [
    {
        'author': "PDUB",
        'title': "Blog Post 1",
        'content': 'first post content',
        'date_posted': 'July 20, 2021'
    },
    {
        'author': "Speno",
        'title': "Blog Post 2",
        'content': 'second post content',
        'date_posted': 'July 21, 2021'
    }
]

@app.route("/")
@app.route("/home")
def hello():
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title='About')

if __name__ == "__main__":
    app.run(debug=True)