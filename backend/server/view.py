
from flask import Blueprint, request
from flask_login import current_user
from flask_cors import cross_origin
from .model import Assignee,Task
from main import db
from .auth import formatUser
import json

view = Blueprint("view",__name__)

@view.route('/assignees', methods=['GET','POST'])
@cross_origin()
def home():
    if request.method == 'GET':
        
        assignees = Assignee.query.all() 
        if assignees:
            return formatAssignee(assignees)
        else:
            return {"status":404, "assignee":"No assignee in db yet"}

def formatAssignee(assignees):
    assigns = []
    for a in assignees:
        print(a.__dict__)
        assigns.append({a.id:a.name})
    return {"assigns": assigns}

@view.route('/create-task', methods=['GET','POST'])
@cross_origin()
def create_task():
    if request.method == 'POST':
        name = request.json['name']
        startDate = request.json['startDate']
        endDate = request.json["endDate"]
        assignees = formatAssignees(request.json["assignees"])
        projectName = request.json["projectName"]
        description = request.json["description"]
        priority = request.json["priority"]
        selectedFile = json.dumps(request.json["selectedFile"])
        task = Task.query.filter_by(name = name).first()
        if task:
            return {"status":422, "message": f"task with {name} name already exist"}
        else:
            new_task = Task(name = name,start = startDate,end = endDate,assignees = assignees,project = projectName,description = description,priority = priority,file = selectedFile)
            db.session.add(new_task)
            db.session.commit()
            return {"status":200, "task":formatTask(new_task)}


@view.route('/get-tasks', methods=['GET','POST'])
@cross_origin()
def get_tasks():
    if request.method == 'GET':
        tasks = Task.query.all()
        if tasks:
            tasks_res = []
            for t in tasks:
                tasks_res.append(formatTask(t))
            return {"status":200,"tasks": tasks_res}
    
        else:
            return {"status":404, "assignee":"No assignee in db yet"}


def formatTask(task):
    return{
       "name":task.name,
       "start":task.start,
       "end": task.end,
       "assignees":task.assignees,
       "project":task.project,
       "description":task.description,
       "priority":task.priority,
       "file":task.file
    }

def formatAssignees( assigns):
    assign = []
    for a in assigns:
        if a is not None:
            assign.append(a)
    return ','.join(assign)

    



