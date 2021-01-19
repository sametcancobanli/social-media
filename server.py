from flask import Flask, render_template, request, redirect, escape, session, url_for, flash
from flask_mysqldb import MySQL
import views


app = Flask(__name__)
mysql = MySQL(app)

app.config["app"]=app
app.config["mysql"]=mysql

    
app.config['MYSQL_HOST'] = "eu-cdbr-west-03.cleardb.net"
app.config['MYSQL_USER'] = "b7e8ff5203e2fb"
app.config['MYSQL_PASSWORD'] = "c3cf4e2e"
app.config['MYSQL_DB'] = "heroku_3f45dcbe9716bc3"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

app.secret_key = "super secret key"

app.add_url_rule("/", view_func =views.home_page)
app.add_url_rule("/about", view_func =views.about_page)
app.add_url_rule("/contact", view_func =views.contact_page)
app.add_url_rule("/login", view_func =views.login_page)
app.add_url_rule("/register", view_func =views.register_page)
app.add_url_rule("/afterlog", view_func =views.afterlog_page, methods=['GET', 'POST'])
app.add_url_rule("/afterreg", view_func =views.afterreg_page, methods=['POST'])
app.add_url_rule("/logout", view_func=views.logout_page)
app.add_url_rule("/success", view_func=views.success_page)
app.add_url_rule("/login", view_func=views.fail_page)
app.add_url_rule("/afterpost", view_func=views.post_page, methods=['POST'])
app.add_url_rule("/comment/<int:comment_key>", view_func=views.comment_page)
app.add_url_rule("/afterreply/<int:comment_key_2>", view_func=views.afterreply_page, methods=['POST'])
app.add_url_rule("/aftercomment/<int:post_key>", view_func=views.aftercomment_page, methods=['POST'])
app.add_url_rule("/post_up/<int:post_key>", view_func=views.post_up_page, methods=['POST'])
app.add_url_rule("/comment_up/<int:post_key>/<int:comment_num>", view_func=views.comment_up_page, methods=['POST'])
app.add_url_rule("/reply_up/<int:post_key>/<int:comment_num>/<int:reply_num>", view_func=views.reply_up_page, methods=['POST'])
app.add_url_rule("/profile/<int:user_key>", view_func =views.profile_page)
app.add_url_rule("/delete_profile/<int:profile_key>", view_func =views.delete_profile, methods=['GET', 'POST'])

if __name__ == "__main__":
    app.run()