from flask import Flask, render_template, request, redirect, escape, session, url_for, flash, current_app
from flask_mysqldb import MySQL
from base64 import b64encode
from passlib.hash import pbkdf2_sha256 as hasher

def home_page():
    mysql = current_app.config["mysql"]
    cur = mysql.connection.cursor()
    if 'mail' in session:
        mail_session = escape(session['mail']).capitalize()

        sorgu = "SELECT * FROM post ORDER BY post_id DESC"
        cur.execute(sorgu)
        info = cur.fetchall()

        sorgu_2 = "SELECT * FROM user_profile"
        cur.execute(sorgu_2)
        info_2 = cur.fetchall()

        cur.execute("SELECT student_id FROM user WHERE mail = %s", [mail_session])
        student_id = cur.fetchone()
        student_id = student_id["student_id"]

        cur.execute("SELECT COUNT(student_id) AS user_num FROM user")
        user_num = cur.fetchone()
        user_num = user_num["user_num"]

        cur.execute("SELECT COUNT(student_id) AS post_num FROM post")
        post_num = cur.fetchone()
        post_num = post_num["post_num"]

        cur.execute("SELECT COUNT(student_id) AS comment_num FROM comment")
        comment_num = cur.fetchone()
        comment_num = comment_num["comment_num"]

        cur.execute("SELECT COUNT(student_id) AS reply_num FROM reply")
        reply_num = cur.fetchone()
        reply_num = reply_num["reply_num"]

        return render_template('home.html',student_id = student_id , id = info, id_2 = info_2, session_mail=mail_session, user_num = user_num, post_num = post_num,comment_num = comment_num, reply_num=reply_num)
    
    return render_template("login.html")

def about_page():
    mysql = current_app.config["mysql"]
    cur = mysql.connection.cursor()
    if 'mail' in session:
        mail_session = escape(session['mail']).capitalize()

        cur.execute("SELECT student_id FROM user WHERE mail = %s", [mail_session])
        student_id = cur.fetchone()
        student_id = student_id["student_id"]
        return render_template('about.html', student_id = student_id , session_mail=mail_session)

    return render_template("login.html")

def contact_page():
    mysql = current_app.config["mysql"]
    cur = mysql.connection.cursor()
    if 'mail' in session:
        mail_session = escape(session['mail']).capitalize()

        cur.execute("SELECT student_id FROM user WHERE mail = %s", [mail_session])
        student_id = cur.fetchone()
        student_id = student_id["student_id"]
        return render_template('contact.html',student_id = student_id , session_mail=mail_session)
    
    return render_template("login.html")

def login_page():
    return render_template("login.html")

def afterlog_page():
    mysql = current_app.config["mysql"]
    cursor = mysql.connection.cursor()
    if 'mail' in session:
        return redirect(url_for('home_page'))
    if request.method == 'POST':
        form_mail  = request.form['mail_2']
        form_password  = request.form['password_2']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT password FROM user WHERE mail  = %s', (form_mail,))

        password = cursor.fetchone()

        if hasher.verify(form_password,password['password']):

            session['loggedin'] = True
            session['mail'] = form_mail
            session['password'] = password

            return redirect(url_for('home_page'))

    return redirect(url_for('login_page'))

def register_page():
    return render_template("register.html")

def afterreg_page():
    mysql = current_app.config["mysql"]
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        name = request.form.get('name')
        surname = request.form.get('surname')
        department = request.form.get('department')
        clas = request.form.get('class')

        mail = request.form.get('mail')
        password = request.form.get('password')
        hashed_password = hasher.hash(password)
          
        about = request.form.get('about')

        cursor = mysql.connection.cursor()
        file = request.files['fileToUpload']
        img_1 = file.read()

        cursor.execute("SELECT * FROM user WHERE mail = %s" , [mail])
        temp_mail = cursor.fetchall()

        if temp_mail:
            flash("This E-mail address is used, try again.", "danger")
            return redirect(url_for('register_page'))
        
        cursor.execute("SELECT * FROM user WHERE student_id = %s" , [student_id])
        temp_id = cursor.fetchall()

        if temp_id:
            flash("This Student ID is used, try again.", "danger")
            return redirect(url_for('register_page'))


        cursor = mysql.connection.cursor()

        sorgu = "INSERT INTO user_profile VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sorgu,(student_id,name,surname,department, clas,about,0,0,img_1))
        mysql.connection.commit()

        sorgu = "INSERT INTO user VALUES(%s,%s,%s)"
        cursor.execute(sorgu,(student_id,mail,hashed_password))
        mysql.connection.commit()
        cursor.close()
      
        return redirect(url_for('success_page'))
    else:
        return redirect(url_for('fail_page'))

def logout_page():
    session.pop('loggedin', None)
    session.pop('mail', None)
    session.pop('password', None)
    # Redirect to login page
    return redirect(url_for('login_page'))

def success_page():
    return render_template("success.html")

def fail_page():
    return render_template("fail.html")

def post_page():
    mysql = current_app.config["mysql"]
    if request.method == 'POST':
        content = request.form.get('p_content')
        mail_session = escape(session['mail'])
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT student_id FROM user WHERE mail = %s", [mail_session])
        student_id = cursor.fetchone()
        student_id = student_id["student_id"]

        sorgu = "INSERT INTO post VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(sorgu,(student_id,None,content,0,0))
        mysql.connection.commit()

        

        cursor.close()
      
        return redirect(url_for('home_page'))
    else:
        return redirect(url_for('fail_page'))

def comment_page(comment_key):
    mysql = current_app.config["mysql"]
    cur = mysql.connection.cursor()
    if 'mail' in session:
        mail_session = escape(session['mail']).capitalize()

        cur.execute("SELECT * FROM post WHERE post_id = %s", [comment_key])
        info_1 = cur.fetchone()

        cur.execute("SELECT * FROM comment WHERE post_id = %s", [comment_key])
        info_2 = cur.fetchall()

        sorgu_3 = "SELECT * FROM reply ORDER BY comment_id"
        cur.execute(sorgu_3)
        info_3 = cur.fetchall()

        sorgu_4 = "SELECT * FROM user_profile"
        cur.execute(sorgu_4)
        info_4 = cur.fetchall()

        cur.execute("SELECT * FROM post WHERE post_id=%s", [comment_key])
        temp = cur.fetchone()
        temp = temp['student_id']
        
        cur.execute("SELECT * FROM user_profile WHERE student_id=%s", [temp])
        temp_2 = cur.fetchone()

        img_blob = temp_2['image_id']
        image = b64encode(img_blob).decode("utf-8")

        cur.execute("SELECT student_id FROM user WHERE mail = %s", [mail_session])
        student_id = cur.fetchone()
        student_id = student_id["student_id"]

        return render_template('comment.html',student_id = student_id , id_1 = info_1, id_2 = info_2, id_3 = info_3, id_4 = info_4, session_mail=mail_session, image=image, obj=img_blob)
    
    return render_template("login.html")

def afterreply_page(comment_key_2):
    mysql = current_app.config["mysql"]
    if request.method == 'POST':
        content = request.form.get('r_content')
        mail_session = escape(session['mail'])
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT student_id FROM user WHERE mail = %s", [mail_session])
        student_id = cursor.fetchone()
        student_id = student_id["student_id"]

        sorgu = "INSERT INTO reply VALUES(%s,%s,%s,%s,%s,%s)"
        cursor.execute(sorgu,(student_id,comment_key_2,None,content,0,0))
        mysql.connection.commit()

        cursor.execute("SELECT post_id FROM comment WHERE comment_id = %s", [comment_key_2])
        post_id = cursor.fetchone()
        post_id = post_id["post_id"]

        cursor.close()
      
        return redirect(url_for('comment_page', comment_key =post_id))
    else:
        return redirect(url_for('fail_page'))

def aftercomment_page(post_key):
    mysql = current_app.config["mysql"]
    if request.method == 'POST':
        content = request.form.get('c_content')
        mail_session = escape(session['mail'])
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT student_id FROM user WHERE mail = %s", [mail_session])
        student_id = cursor.fetchone()
        student_id = student_id["student_id"]

        sorgu = "INSERT INTO comment VALUES(%s,%s,%s,%s,%s,%s)"
        cursor.execute(sorgu,(student_id,post_key,None,content,0,0))
        mysql.connection.commit()

        cursor.close()
      
        return redirect(url_for('comment_page', comment_key =post_key))
    else:
        return redirect(url_for('fail_page'))

def post_up_page(post_key):
    mysql = current_app.config["mysql"]
    if request.method == 'POST':
        mail_session = escape(session['mail'])
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT student_id FROM user WHERE mail = %s", [mail_session])
        student_id = cursor.fetchone()
        student_id = student_id["student_id"]

        cursor.execute("UPDATE post SET p_up_vote = p_up_vote + 1 WHERE post_id = %s", [post_key])
        mysql.connection.commit()

        cursor.close()
      
        return redirect(url_for('comment_page', comment_key =post_key))
    else:
        return redirect(url_for('fail_page'))

def comment_up_page(post_key, comment_num):
    mysql = current_app.config["mysql"]
    if request.method == 'POST':
        mail_session = escape(session['mail'])
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT student_id FROM user WHERE mail = %s", [mail_session])
        student_id = cursor.fetchone()
        student_id = student_id["student_id"]

        cursor.execute("UPDATE comment SET c_up_vote = c_up_vote + 1 WHERE post_id = %s AND comment_id =%s", ([post_key],[comment_num]))
        mysql.connection.commit()

        cursor.close()
      
        return redirect(url_for('comment_page', comment_key =post_key))
    else:
        return redirect(url_for('fail_page'))

def reply_up_page(post_key, comment_num, reply_num):
    mysql = current_app.config["mysql"]
    if request.method == 'POST':
        mail_session = escape(session['mail'])
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT student_id FROM user WHERE mail = %s", [mail_session])
        student_id = cursor.fetchone()
        student_id = student_id["student_id"]

        cursor.execute("UPDATE reply SET r_up_vote = r_up_vote + 1 WHERE comment_id =%s AND reply_id =%s", ([comment_num],[reply_num] ))
        mysql.connection.commit()
    
        cursor.close()
      
        return render_template(url_for('comment_page', comment_key =post_key))
    else:
        return redirect(url_for('fail_page'))

def profile_page(user_key):
    mysql = current_app.config["mysql"]
    cur = mysql.connection.cursor()
    if 'mail' in session:
        mail_session = escape(session['mail']).capitalize()

        cur.execute("SELECT u.student_id, u.name, u.surname, u.department, u.class, u.class, u.image_id, p.post_id p.p_content, p.p_up_vote FROM user_profile u INNER JOIN post p ON u.student_id = p.student_id AND u.student_id = %s ORDER BY post_id DESC", [user_key])
        join_info = cur.fetchall()

        img_blob = join_info['image_id']
        image = b64encode(img_blob).decode("utf-8")

        cur.execute("SELECT student_id FROM user WHERE mail = %s", [mail_session])
        student_id = cur.fetchone()
        student_id = student_id["student_id"]

        return render_template(('profile.html'),student_id = student_id, session_mail=mail_session, info = join_info, image=image, obj=img_blob)
    
    return render_template("login.html")

def delete_profile(profile_key):
    mysql = current_app.config["mysql"]

    mail_session = escape(session['mail'])
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT student_id FROM user WHERE mail = %s", [mail_session])
    student_id = cursor.fetchone()
    student_id = student_id["student_id"]

    cursor.execute("DELETE FROM user_profile WHERE student_id = %s", [profile_key])

    mysql.connection.commit()

    cursor.close()
      
    return redirect(url_for('logout_page'))
