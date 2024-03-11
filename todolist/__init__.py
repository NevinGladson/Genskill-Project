from flask import Flask, render_template, request, g
from flask_login import current_user, LoginManager
import datetime
import os
from .db import User

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

  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint)

  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  login_manager = LoginManager()
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(user_id):
      # Implement a function to load the user from your database
      # Example: return User.query.get(int(user_id))
      conn = db.get_db()
      cursor = conn.cursor()
      cursor.execute(f"select * from user where id = %s", (user_id, ))
      user = cursor.fetchone()
      return user


  @app.before_request
  def before_request():
    g.user_id = current_user.id if current_user.is_authenticated else None
  
  @login_manager.user_loader
  def load_user(user_id):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM app_user WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        user = User(*user_data)
        return user
    return None


  #user_id = g.user_id

  
  @app.route("/index")
  def index():
    g.user_id = current_user.id if current_user.is_authenticated else None
    user_id = g.user_id
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute(f"insert into overdue_tasks (task, points) select t.task, t.points from task t where t.date_of_task < %s and t.status_id=%s and t.user_id = %s", (today_date, 2, user_id))
    cursor.execute(f"delete from task t where t.date_of_task < %s and t.user_id = %s", (today_date, user_id))
    conn.commit()
    oby = request.args.get("order_by", "date_of_task")  
    order = request.args.get("order", "asc")
    if oby == "date_of_task":
      if order == "asc":
           cursor.execute(f"select t.id, t.task, t.date_of_task, t.day, u.urgency, ts.status from task t, urgency u, task_status ts where t.urgency_id=u.id and t.status_id=ts.id and t.status_id = 2 and t.user_id = %s order by t.date_of_task", (user_id,))
      else:
           cursor.execute(f"select t.id, t.task, t.date_of_task, t.day, u.urgency, ts.status from task t, urgency u, task_status ts where t.urgency_id=u.id and t.status_id=ts.id and t.status_id = 2 and t.user_id = %s order by t.date_of_task desc", (user_id,))
    if oby == "urgency":
      if order == "asc":
           cursor.execute(f"select t.id, t.task, t.date_of_task, t.day, u.urgency, ts.status from task t, urgency u, task_status ts where t.urgency_id=u.id and t.status_id=ts.id and t.status_id = 2 and t.user_id = %s order by t.urgency_id", (user_id,))
      else:
           cursor.execute(f"select t.id, t.task, t.date_of_task, t.day, u.urgency, ts.status from task t, urgency u, task_status ts where t.urgency_id=u.id and t.status_id=ts.id and t.status_id = 2 and t.user_id = %s order by t.urgency_id desc", (user_id,))
    if oby == "status":
      if order == "asc":
           cursor.execute(f"select t.id, t.task, t.date_of_task, t.day, u.urgency, ts.status from task t, urgency u, task_status ts where t.urgency_id=u.id and t.status_id=ts.id and t.status_id = 2 and t.user_id = %s order by t.date_of_task", (user_id,))
      else:
           cursor.execute(f"select t.id, t.task, t.date_of_task, t.day, u.urgency, ts.status from task t, urgency u, task_status ts where t.urgency_id=u.id and t.status_id=ts.id and t.status_id = 1 and t.user_id = %s order by t.date_of_task", (user_id,))
    tasks = cursor.fetchall()
    cursor.execute(f"select o.id, o.task from overdue_tasks o where o.user_id =%s", (user_id,))
    overdue = cursor.fetchall()
    
    return render_template('index.html', tasks=tasks, overdue=overdue, order="desc" if order=="asc" else "asc")
      
  
  @app.route("/weekly")
  def weekly_sched(): 
    endweek_date = (datetime.datetime.today() + datetime.timedelta(days=7)).strftime ('%Y-%m-%d')
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("select t.id, t.task, t.date_of_task, t.day, u.urgency, ts.status from task t, urgency u, task_status ts where t.urgency_id=u.id and t.status_id=ts.id and t.date_of_task between (%s) and (%s) order by t.date_of_task", (today_date, endweek_date))
    tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)
    
 

  return app
  


