from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user 
from .models import Note, Exercise
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
#function to receive form inputs for note and store to database
def home():
    if request.method == 'POST':
        note = request.form.get('note')
       
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
#function to delete the note as required- this is where JS is referenced from the base.html and json is temporarily used to delete item
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId) 
    if note: 
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit() 
            
    return jsonify({})

@views.route('/workout', methods=['GET', 'POST'])
@login_required
#function to receive form inputs for workout info and store to db
def input_exercise():
    if request.method == 'POST':
        exercise1 = request.form.get('exercise')
        reps1 = request.form.get('reps')
        weight1 = request.form.get('weight')
        sets1 = request.form.get('sets')
       
        #need to buff up these checks to ensure the right type is being inputted?       
        if len(exercise1) < 1:
            flash('Entry is too short!', category='error')
        elif len(reps1) < 1:
            flash('Entry is too short!', category='error')
        elif len(weight1) < 1:
            flash('Entry is too short!', category='error')
        elif len(sets1) < 1:
            flash('Entry is too short!', category='error')
        else:
            i=0
            while i < int(sets1):
                new_exercise = Exercise(exercise=exercise1, reps=reps1, weight=weight1, user_id=current_user.id)
                db.session.add(new_exercise)
                db.session.commit()
                i+=1
            flash('Exercise added!', category='success')

    return render_template("workout.html", user=current_user)

@views.route('/delete-set', methods=['POST'])
#function to delete sets as required- this is where JS is referenced from the base.html and json is temporarily used to delete item
def delete_set():
    set = json.loads(request.data)
    setId = set['setId']
    set = Exercise.query.get(setId) 
    if set: 
        if set.user_id == current_user.id:
            db.session.delete(set)
            db.session.commit() 
            
    return jsonify({})