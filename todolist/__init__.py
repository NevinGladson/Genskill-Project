from flask import Flask, render_template, request,g
import datetime
import os

today_date = datetime.datetime.today().strftime ('%Y-%m-%d')

def create_app(test_config=None):
  app = Flask("todolist", instance_relative_config=True)
  
#  app.config.from_mapping()
  
  app.config.from_mapping(DATABASE="todolist",
  SECRET_KEY='dev',
  #DATABASE=os.path.join(app.instance_path, 'todolist'),
    )

  if test_config is None:
      # load the instance config, if it exists, when not testing
      app.config.from_pyfile('config.py', silent=True)
  else:
      # load the test config if passed in
      app.config.from_mapping(test_config)

  # ensure the instance folder exists
  try:
      os.makedirs(app.instance_path)
  except OSError:
      pass
  
  from . import tasks 
  app.register_blueprint(tasks.bp)
  
  from . import db 
  db.init_app(app)
  
  @app.route("/")
  def index():
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute(f"insert into overdue_tasks (task, points) select t.task, t.points from task t where t.date_of_task < %s and t.status=%s", (today_date, 2))
    cursor.execute(f"delete from task t where t.date_of_task < %s", (today_date, ))
    conn.commit()
    oby = request.args.get("order_by", "date_of_task")  
    order = request.args.get("order", "asc")
    if oby == "date_of_task":
      if order == "asc":
           cursor.execute(f"select t.id, t.task, t.date_of_task, t.day, u.urgency, ts.status from task t, urgency u, task_status ts where t.urgency=u.id and t.status=ts.id and t.status = 2 order by t.date_of_task")
      else:
           cursor.execute(f"select t.id, t.task, t.date_of_task, t.day, u.urgency, ts.status from task t, urgency u, task_status ts where t.urgency=u.id and t.status=ts.id and t.status = 2 order by t.date_of_task desc")
    if oby == "urgency":
      if order == "asc":
           cursor.execute(f"select t.id, t.task, t.date_of_task, t.day, u.urgency, ts.status from task t, urgency u, task_status ts where t.urgency=u.id and t.status=ts.id and t.status = 2 order by t.urgency")
      else:
           cursor.execute(f"select t.id, t.task, t.date_of_task, t.day, u.urgency, ts.status from task t, urgency u, task_status ts where t.urgency=u.id and t.status=ts.id and t.status = 2 order by t.urgency desc")
    if oby == "status":
      if order == "asc":
           cursor.execute(f"select t.id, t.task, t.date_of_task, t.day, u.urgency, ts.status from task t, urgency u, task_status ts where t.urgency=u.id and t.status=ts.id and t.status = 2 order by t.date_of_task")
      else:
           cursor.execute(f"select t.id, t.task, t.date_of_task, t.day, u.urgency, ts.status from task t, urgency u, task_status ts where t.urgency=u.id and t.status=ts.id and t.status = 1 order by t.date_of_task")
    tasks = cursor.fetchall()
    cursor.execute(f"select o.id, o.task from overdue_tasks o")
    overdue = cursor.fetchall()
    
    return render_template('index.html', tasks=tasks, overdue=overdue, order="desc" if order=="asc" else "asc")
      
  
  @app.route("/weekly")
  def weekly_sched(): 
    endweek_date = (datetime.datetime.today() + datetime.timedelta(days=7)).strftime ('%Y-%m-%d')
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("select t.id, t.task, t.date_of_task, t.day, u.urgency, ts.status from task t, urgency u, task_status ts where t.urgency=u.id and t.status=ts.id and t.date_of_task between (%s) and (%s) order by t.date_of_task", (today_date, endweek_date))
    tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)
    
  #@app.route('/task/<int:id>/delete', methods=['GET', 'POST'])
  #def delete_task(id):
  #  cursor.execute("delete from task where id = %d", (id))
  #  return redirect(url_for('index'))

  return app
  


