from flask import Blueprint, render_template, request, redirect, url_for, g
from flask_login import current_user
from datetime import datetime

from . import __init__
from . import db



bp = Blueprint("todolist", "todolist", url_prefix="/task")

@bp.before_request
def before_request():
    g.user_id = current_user.id if current_user.is_authenticated else None  

#user_id = g.user_id

def day(date_of_task):
  date = datetime.strptime(date_of_task,'%Y-%m-%d')
  date = date.strftime ('%d %m %Y')
  date = str(date)
  day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
  day = datetime.strptime(date, '%d %m %Y'). weekday()
  return day_name[day]

@bp.route("/add", methods=["GET", "POST",])
def add_tasks():
    conn = db.get_db()
    cursor = conn.cursor()
    
    g.user_id = current_user.id if current_user.is_authenticated else None
    user_id = g.user_id
    if request.method == "GET":
        cursor.execute("select id,urgency from urgency")
        statuses = cursor.fetchall()
        today_date = datetime.today().strftime ('%Y-%m-%d')
        return render_template("add_task.html", statuses=statuses, today_date=today_date)
    elif request.method == "POST":
        task = request.form.get("task")
        date_of_task = request.form.get("date_of_task")
        urgency = request.form.get("urgency")
        points = request.form.get("points")
        status = 2
        day_of_task = day(date_of_task)
        cursor.execute("insert into task (task, date_of_task, day, points, urgency_id, status_id, user_id) values (%s,%s,%s,%s,%s,%s,%s)", (task, date_of_task, day_of_task, points, urgency, status, user_id))
        conn.commit()
        return redirect(url_for("index"), 302)
    
@bp.route("/<id>/detail")
def taskdetail(id):
    g.user_id = current_user.id if current_user.is_authenticated else None
    user_id = g.user_id
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("select t.task, t.date_of_task, u.urgency, t.points, ts.status from task t, urgency u, task_status ts where t.id = %s and u.id = t.urgency_id and t.status_id=ts.id and t.user_id=%s", (id, user_id))
    task = cursor.fetchone()
    if not task:
         return render_template("taskdetails.html"), 404 
    task, date_of_task, urgency, points, status = task
    id = int(id)
    status_colour = {"Complete" : "success",
                "Not Complete" : "dark"}
    urgency_colour = {"Normal": "primary",
               "Expendable" : "secondary",
               "Important" : "warning",
               "Very Important" : "danger"}

    return render_template("taskdetails.html", 
                           id = id,
                           task = task,
                           points = points,  
                           urgency=urgency,  
                           u_cls=urgency_colour[urgency],
                           s_cls=status_colour[status], 
                           status=status
                           )



@bp.route("/<id>/edit", methods=["GET", "POST",])
def edit_task(id): 
    g.user_id = current_user.id if current_user.is_authenticated else None
    user_id = g.user_id
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("select t.task, t.date_of_task, t.urgency_id, t.status_id, t.points from task t, urgency u where t.id = %s and u.id = t.urgency_id and t.user_id = %s", (id, user_id))
    task = cursor.fetchone()
    if not task:
        return render_template("taskdetails.html"), 404    

    if request.method == "GET":
        task, date_of_task, urgency, status, points = task
        cursor.execute("select id,urgency from urgency")
        statuses = cursor.fetchall()
        return render_template("taskedit.html", 
                               id = id,
                               task=task,
                               date_of_task=date_of_task,
                               points=points,
                               urgency = urgency,
                               status=status,
                               statuses=statuses
                               )
    elif request.method == "POST":
        task = request.form.get("task")
        date_of_task = request.form.get("date_of_task")
        points = request.form.get("points")
        urgency = request.form.get("urgency")
        status = request.form.get("status")
        if not status:
          status = '2'
        day_of_task = day(date_of_task)  
        cursor.execute("update task set task = %s, date_of_task = %s, day=%s, status_id=%s, points=%s, urgency_id=%s where id=%s and user_id = %s", (task, date_of_task, day_of_task, status, points, urgency, id, user_id))
        conn.commit()
        return redirect(url_for("index"), 302)

@bp.route("/<id>/overdue")
def overdue(id):
    g.user_id = current_user.id if current_user.is_authenticated else None
    user_id = g.user_id
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("select o.task, o.points from overdue_tasks o where o.id = %s and o.user_id", (id, user_id))
    overdue = cursor.fetchone()
    if not overdue:
         return render_template("overdue.html"), 404 
    task, points = overdue
    id = int(id)

    return render_template("overdue.html", 
                           id = id,
                           task = task,
                           points = points,  
                           )


@bp.route('/task/<id>/delete', methods=['GET', 'POST'])
def delete_task(id):
    g.user_id = current_user.id if current_user.is_authenticated else None
    user_id = g.user_id
    conn = db.get_db()
    cursor = conn.cursor()

    # Ensure the 'id' is an integer
    try:
        task_id = int(id)
    except ValueError:
        return render_template("error.html", message="Invalid task ID"), 400

    # Delete the task with the specified ID
    cursor.execute("DELETE FROM task WHERE id = %s and user_id = %s", (task_id, user_id))
    conn.commit()

    # Redirect to the index page after deletion
    return redirect(url_for('index'))
