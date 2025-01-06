from flask import Flask ,send_from_directory ,jsonify, render_template , url_for , redirect ,flash , abort , session, request , flash
from flask_login import UserMixin ,LoginManager , login_manager ,login_required , login_user , current_user, logout_user
from werkzeug.security import generate_password_hash , check_password_hash
import os
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.orm import backref
from datetime import datetime




app = Flask(__name__)
app.config["SECRET_KEY"] =  "AAAAAAAAAAAAAAAAA"
login_manager =LoginManager(app)   





# --------------------------database----------------------------

file_dir =os.path.dirname(__file__)
goal_route= os.path.join(file_dir,'app.db')
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///' + goal_route
db=SQLAlchemy(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    id=db.Column(db.Integer, primary_key= True )
    username=db.Column(db.String(20),nullable=False ,unique = True)
    password =db.Column(db.String(25) , nullable =False , unique = True)
    email =db.Column(db.String(30) , nullable =False ,unique = True,)



class Note(db.Model):
    id=db.Column(db.Integer, primary_key= True )
    title = db.Column(db.String(100), nullable=False)  
    text=db.Column(db.String(2500) , nullable=False)
    date=db.Column(db.Date, nullable=False, default=datetime.utcnow)  
    time=db.Column(db.Time, nullable=False, default=datetime.utcnow().time)
    uid=db.Column(db.Integer(), db.ForeignKey('user.id'), nullable =False)
    user=db.relationship('User' , backref='owner' , lazy=True)


with app.app_context():
    db.create_all()
# ------------------------route--------------------------------


@app.route('/signUp' , methods = ['GET' , 'POST'])
def signUp():
    if request.method=='POST':
        data = request.get_json()
        username1 = data.get("username")
        password1 = data.get("password")
        email1 = data.get("email")
        hashed_pass=generate_password_hash(password1)
        existing_user=User.query.filter((User.username==username1)| (User.email == email1)).first()
        if not existing_user:
            new_user=User(username = username1 , password=hashed_pass , email=email1)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'massage' : 'user created successfully'}) , 201
        return jsonify({"error": "user already exists"}) , 400
    return send_from_directory('templates', 'signUp.html')

# ----------------------------login------------------------

@app.route('/login' , methods=['POST' , 'GET'])
def login():
    if request.method=='POST':
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        user: User = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password , password):
            login_user(user)
            return jsonify({"message": "Login successful"}), 200
        return jsonify({"error": "Invalid credentials"}), 401
    return send_from_directory('templates', 'login.html')



# -----------------------   protected -------------------------

@app.route('/protected' , methods=['POST' ,'GET'])
@login_required
def protected():
    if request.method=='POST':
        return jsonify({"message": f"Welcome, {current_user.username}"}), 200
    return send_from_directory('templates', 'protected.html' )

# ------------------------   noting  --------------------------


@app.route('/noting' , methods=['POST' , 'GET'])
@login_required
def noting():
    data = request.get_json()
    text = data.get('text')
    new_note=Note(text=text , uid=current_user.id)
    db.session.add(new_note)
    db.session.commit()
    return jsonify({"message": "Note added successfully"}), 201

    # user_notes = Note.query.filter_by(uid=current_user.id).all()        return render_template('protected.html' , notes=user_notes)

        # try:
        #     note = Note(text =text)
        #     db.session.add(note)
        #     db.session.commit()
        #     return 'successfully...'
        # except Exception as er:
        #     return ' error is ==> ' + str(er)


# --------------------------------  show  ------------------------

@app.route('/show')
@login_required
def show():

    notes = Note.query.filter_by(uid=current_user.id).all()
    return jsonify([{"id": note.id, "text": note.text} for note in notes]), 200


    # notes = Note.query.filter_by(uid=current_user.id).all()
    # notes_html='<h3> your notes : </h3><ul>'
    # for note in notes:
    #     notes_html+=f'<li>{note.text}</li>'
    # notes_html+="</ul>"

    # return notes_html , 200, {'content-type':'text/'}

# ----------------------------  delete  ----------------------

# @app.route('/delete' ,methods=['POST' , 'GET'])
# def delete():
#     data = request.get_json()
#     note_id=data.get('id')
#     note=Note.query.filter_by(id=int(note_id), uid=current_user.id).first()
#     if note:
#         db.session.delete(note)
#         db.session.commit()
#         return jsonify({"message": "Note deleted successfully"}), 200
#     return jsonify({"error": "Note not found"}), 404


@app.route('/delete', methods=['POST'])
@login_required
def delete():
    data = request.get_json()
    note_id = data.get('id')
    note = Note.query.filter_by(id=int(note_id), uid=current_user.id).first()
    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify({"message": "Note deleted successfully"}), 200
    return jsonify({"error": "Note not found"}), 404


# ---------------------------   logout  ----------------

@app.route('/logout' , methods=['POST' , 'GET'])
def logout():
        logout_user()
        return jsonify({"message": "Logged out successfully"}), 200
    






app.run(debug=True)