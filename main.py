from flask import Flask, render_template, request
from post import Post
import requests
import smtplib


blog_url = "https://api.npoint.io/43644ec4f0013682fc0d"
posts = requests.get(blog_url).json()
post_objects = []
username = "46uday.d@gmail.com"
password = "uday1998"


for post in posts:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["date"], post["body"], post["image_url"])
    post_objects.append(post_obj)


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html", all_blogs=post_objects)


@app.route('/index.html')
def get_all_posts():
    return render_template("index.html")


@app.route('/contact.html')
def contacts():
    return render_template("contact.html")


@app.route('/contact', methods=["POST","GET"])
def received_data():
    if request.method == "POST":
        data = request.form
        print(data["name"])
        print(data["email"])
        print(data["phone"])
        print(data["message"])
        send_mail(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    else:
        return render_template("contact.html", msg_sent=False)


def send_mail(name, email, phone, message):
    email_msg = f"Subject : New Message\n\nName : {name}\nEmail : {email}\nPhone no : {phone}\nMessage : {message}"
    with smtplib.SMTP("smtp.gmail.com",587) as connection:
        connection.starttls()
        connection.login(user=username,password=password)
        connection.sendmail(from_addr=username,to_addrs=username,msg=email_msg)

@app.route('/about.html')
def about():
    return render_template("about.html")


@app.route('/post.html')
def sample_post():
    return render_template("post.html")


@app.route('/home')
def return_home():
    x = get_all_posts()
    return x


@app.route('/post.html/<int:index>')
def show_post(index):
    requested_post = None
    for blog_post in post_objects:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)
