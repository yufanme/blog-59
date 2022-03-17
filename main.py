from flask import Flask, render_template, request
import requests
import smtplib

EMAIL = "562937707@qq.com"
PASSWORD = "bpyjiqjylklcbdhe"


def send_email(name, email, phone, message):
    email_message = f"Subject:USER MESSAGE FROM BLOG!\n\n" \
                    f"NAME: {name}\n" \
                    f"EMAIL: {email}\n" \
                    f"PHONE: {phone}\n" \
                    f"MESSAGE: {message}\n".encode("utf-8")
    with smtplib.SMTP("smtp.qq.com") as connection:
        connection.starttls()
        connection.login(user=EMAIL,
                         password=PASSWORD
                         )
        connection.sendmail(from_addr=EMAIL,
                            to_addrs=EMAIL,
                            msg=email_message
                            )


app = Flask(__name__)

# api data for blog content
blog_json = requests.get("https://api.npoint.io/976e5c713a2e420613d3").json()


@app.route("/")
def home():
    return render_template("index.html", blog_json=blog_json)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        name = data["username"]
        email = data["useremail"]
        phone = data["userphone"]
        message = data["usermessage"]
        send_email(name, email, phone, message)
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


@app.route("/blog/<int:blog_id>")
def blog(blog_id):
    for blog_content in blog_json:
        if blog_content["id"] == blog_id:
            target_blog = blog_content
    return render_template("blog.html", target_blog=target_blog)


if __name__ == "__main__":
    app.run(debug=True)
