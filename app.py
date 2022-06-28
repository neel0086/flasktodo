import re
from turtle import title
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_BINDS'] = {
    'todocomment':  'sqlite:///todocomment.db',
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.id} - {self.title}"

class Todocomment(db.Model):
    __bind_key__ = 'todocomment'
    
    id = db.Column(db.Integer, primary_key = True)
    todo_id = db.Column(db.Integer, nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/" ,methods=['GET','POST'])
def main_page():
    return redirect('/todo')
    

@app.route("/todo" ,methods=['GET','POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    else:
        allTodo = Todo.query.all()
        return render_template('index.html', allTodo=allTodo)

@app.route("/todo/<int:id>" ,methods=['GET','POST'])
def view_todo(id):
    vtodo = Todo.query.filter_by(id=id).first()
    print(vtodo)
    return render_template('viewtodo.html', vtodo=vtodo)



@app.route('/todo/delete/<int:id>')
def delete(id):
    
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/todo')

@app.route('/todo/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(id=id).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/todo')
        
    todo = Todo.query.filter_by(id=id).first()
    return render_template('update.html', todo=todo)

@app.route('/todo/comment/<int:id>', methods=['GET', 'POST'])
def comment(id):
    if request.method=='POST':
        print(800)
        desc = request.form['desc']
        todo1 = Todocomment(desc=desc, todo_id = id)
        db.session.add(todo1)
        db.session.commit()
    else:
        comments = Todocomment.query.filter_by(todo_id=id).all()
        return render_template('comment.html', comments=comments,srno=id)

@app.route('/todo/comment/<int:id>/delete/<int:comment_id>', methods=['GET', 'POST'])
def comment_delete(id,comment_id):
    todo = Todocomment.query.filter_by(id = comment_id,todo_id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/todo/comment'+'/'+str(id))



if __name__ == '__main__':
    app.secret_key = "SecretCantBeSecret:;lol"
    app.run(debug=True,port=8000)