from flask import Flask, render_template
import requests

app = Flask(__name__)

# api data for blog content
blog_json = requests.get("https://api.npoint.io/976e5c713a2e420613d3").json()


@app.route("/")
def home():
    return render_template("index.html", blog_json=blog_json)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/blog/<int:blog_id>")
def blog(blog_id):
    for blog_content in blog_json:
        if blog_content["id"] == blog_id:
            target_blog = blog_content
    return render_template("blog.html", target_blog=target_blog)


if __name__ == "__main__":
    app.run(debug=True)
