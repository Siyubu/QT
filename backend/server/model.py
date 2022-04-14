from main import db
from flask_login import UserMixin 
from sqlalchemy.sql import func
from sqlalchemy import UniqueConstraint,Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password =db.Column(db.String(150))
    tasks = relationship('Task') 
    projects = relationship('Project')

class TaskProject(db.Model):
    __tablename__ = 'tasks-projects'
    __table_args__ = (
        UniqueConstraint('project_id', 'task_id'),
    )
    id = db.Column(db.Integer, primary_key = True)
    project_id= db.Column(db.ForeignKey('projects.id'), nullable=False)
    task_id = db.Column(db.ForeignKey('tasks.id'), nullable=False)

    project = relationship(u'Project', lazy="joined")
    task = relationship(u'Task', lazy="joined")

# TaskProject = Table('tasks-projects',Base.metadata,
#     db.Column("id",db.Integer,primary_key=True),
#     db.Column("project_id", db.Integer, db.ForeignKey("projects.id")),
#     db.Column("task_id", db.Integer, db.ForeignKey("tasks.id"))
# )

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    owner = db.Column(db.Integer, db.ForeignKey("users.id"))
    #tasks = relationship('Task', secondary='tasks-projects',backref='Project')

class Task(db.Model):
    __tablename__ ='tasks'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    start = db.Column(db.String(150))
    end = db.Column(db.String(150))
    description = db.Column(db.String(1000))
    priority = db.Column(db.String(150))
    project = db.Column(db.String(120))
    assignees = db.Column(db.String(200))
    file = db.Column(db.String(1000))
    owner = db.Column(db.Integer, db.ForeignKey("users.id"))
    #projects = relationship('Project', secondary=TaskProject, backref='Task')
    #assignees = relationship('Assignee', secondary='tasks-assignee')



class Assignee(db.Model):
    __tablename__ = 'assignees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    #tasks = relationship('Task', secondary='tasks-assignee', backref='Assignee')

    def __repr__(self):
        return self.name
    
class TasksAssignee(db.Model):
    __tablename__ = 'tasks-assignee'
    __table_args__ = (
        UniqueConstraint('assignee_id', 'task_id'),
    )

    id = db.Column(db.Integer, primary_key = True)
    assignee_id= db.Column(db.ForeignKey('assignees.id'), nullable=False)
    task_id = db.Column(db.ForeignKey('tasks.id'), nullable=False)

    assign = relationship('Assignee', lazy="joined")
    task = relationship(u'Task', lazy="joined")

