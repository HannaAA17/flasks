from datetime import datetime

from flask import render_template, redirect, url_for, flash

from app import app, db
from models import Task
from forms import AddTaskForm, DeleteTaskForm


@app.route('/')
@app.route('/index')
def index():
    ctx = {'tasks':Task.query.all()}
    return render_template('index.html', **ctx)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddTaskForm()
    if form.validate_on_submit():
        t = Task(title=form.title.data, date=datetime.utcnow())
        db.session.add(t)
        db.session.commit()
        flash('Added to Database')
        return redirect(url_for('index'))
    else:
        return render_template('add.html', form=form)


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    t = Task.query.get_or_404(task_id)
    form = AddTaskForm()
    
    if form.validate_on_submit():
        t.title = form.title.data
        t.date = datetime.utcnow()
        db.session.commit()
        flash('Edited Successfully')
        return redirect(url_for('index'))
    
    else:
        form.title.data = t.title
        ctx = {'form':form, 'task_id':task_id}
        return render_template('edit.html', **ctx)

@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete(task_id):
    t = Task.query.get_or_404(task_id)
    form = DeleteTaskForm()
    
    if form.validate_on_submit():
        db.session.delete(t)
        db.session.commit()
        flash('Deleted Successfully')
        return redirect(url_for('index'))
    
    else:
        ctx = {'form':form, 'task_id':task_id}
        return render_template('delete.html', **ctx)