from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user 
from .models import Note, Exercise, User
from . import db
import json
from sqlalchemy import func
from datetime import datetime, timedelta, date

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

    #this section declares a list for each type of exercise for reference in creating table data dictionaries
    #to-do: make charts that can be selected with various time domains
    #to-do: picture a specific exercise over time via drop down menu
    #to-do: multi-colored charts and side by side
    #select time domain for table and filter it
    
    #list to track all types of exercises in the DB
    exercise_log = []

    #loop thru all types of exercises in the DB and append to ongoing list only if it's a new exercise
    for row in db.session.query(Exercise):
        flag = 1
        while flag == 1:
            for i in range(len(exercise_log)):
                if exercise_log[i] != row.exercise:
                    flag = 1
                else:
                    flag = 0
                    break
            if flag == 1:
                exercise_log.append(row.exercise)

    #list to track all dates in the DB
    date_log = []

    #loop thru all dates in the DB and append to ongoing list only if it's a new exercise
    for row in db.session.query(Exercise):
        flag = 1
        while flag == 1:
            for i in range(len(date_log)):
                if date_log[i] != row.date:
                    flag = 1
                else:
                    flag = 0
                    break
            if flag == 1:
                date_log.append(row.date)

    #a dictionary to hold cumulative sets for each date (index) and cumulative sets (value)
    #to-do: user match account
    # all_sets_dict = {}
   
    # for i in range(len(date_log)):
    #     Sets = db.session.query(Exercise).filter(Exercise.date == date_log[i]).count()
    #     all_sets_dict.update({date_log[i]: Sets})  
    
    # print(date_log)
    # print(all_sets_dict)


    #NOT IN CURRENT USE: a dictionary to hold exercises and cumulative sets over time- individual exercises
    #to-do: user match account
    exercise_sets_dict = {}
   
    for i in range(len(exercise_log)):
        Sets = db.session.query(Exercise).filter(Exercise.exercise == exercise_log[i]).count()
        exercise_sets_dict.update({exercise_log[i]: Sets})  

    #make a dictionary with types of exercises for keys, and cumulative sum of reps for values
    #to-do: match to user account
    reps_dict = {}

    for i in range(len(exercise_log)):
        Reps = db.session.query(func.sum(Exercise.reps)).filter(Exercise.exercise == exercise_log[i]).scalar()
        reps_dict.update({exercise_log[i]: Reps})

    #this section goes thru each type of exercise in the database table and calculates power output, list is summed
    #todo: make sure the user is matched to current user
    power_dict = {}
    power_list = []
    
    for i in range(len(exercise_log)):
        power_list.clear()
        for instance in db.session.query(Exercise).filter(Exercise.exercise == exercise_log[i]):
            Power = instance.reps * instance.weight
            if Power > 0:
                power_list.append(Power)
                power_dict.update({exercise_log[i]: sum(power_list)})
            
    #this section will search DB for a the maximum weight for each exercise and return that value for chart
    #todo: make sure the user is matched to current user    
    max_dict = {}

    for i in range(len(exercise_log)):
        max_weight = db.session.query(func.max(Exercise.weight)).filter(Exercise.exercise == exercise_log[i]).scalar()
        if max_weight > 0:
            max_dict.update({exercise_log[i]: max_weight})

    #tie all dictionaries for various chart to json objects to pass to the template
    return render_template("workout.html", 
        set_data = json.dumps(exercise_sets_dict),
        reps_data = json.dumps(reps_dict),
        power_data = json.dumps(power_dict),
        max_data = json.dumps(max_dict), 
        user=current_user
    )

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