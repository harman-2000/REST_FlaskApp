from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
api= Api(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sqlite.db'
db=SQLAlchemy(app)

class todomodel(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    student_id=db.Column(db.String(10))
    name=db.Column(db.String(200))
    branch=db.Column(db.String(200))
    college=db.Column(db.String(200))
    batch=db.Column(db.String(200))
    course=db.Column(db.String(200))
    first_language=db.Column(db.String(500))

#db.create_all()

task_post_args=reqparse.RequestParser()

task_post_args.add_argument("student_id",type=str,help="student_id is required",required=True)
task_post_args.add_argument("name",type=str,help="name is required",required=True)
task_post_args.add_argument("branch",type=str,help="branch is required",required=True)
task_post_args.add_argument("college",type=str,help="college is required",required=True)
task_post_args.add_argument("batch",type=str,help="batch is required",required=True)
task_post_args.add_argument("course",type=str,help="course is required",required=True)
task_post_args.add_argument("first_language",type=str,help="first_language is required",required=True)


resource_fields= { 'id': fields.Integer,'student_id': fields.String, 'name':fields.String, 'branch':fields.String, 'college':fields.String, 'batch':fields.String, 'course':fields.String, 'first_language':fields.String}

class allStudents(Resource):
    def get(self):
        tasks=todomodel.query.all()
        todos={}
        for task in tasks:
            todos[task.id]={"student_id":task.student_id, "name":task.name, "branch":task.branch,"college":task.college,"batch":task.batch,"course":task.course,"first_language":task.first_language}
        return todos

class students(Resource):
    @marshal_with(resource_fields)
    def get(self,todo_id):
        task=todomodel.query.filter_by(id=todo_id).first()
        if not task:
            abort(404, message="Could not find task with that id")	
        return task
    
    @marshal_with(resource_fields)
    def post(self,todo_id):
        args=task_post_args.parse_args()
        task=todomodel.query.filter_by(id=todo_id).first()
        if task:
            abort(409,message="id taken....")
        
        todo=todomodel(id=todo_id, student_id=args['student_id'],name=args['name'], branch=args['branch'], college=args['college'], batch=args['batch'], course=args['course'], first_language=args['first_language'])
        db.session.add(todo)
        db.session.commit()
        return todo, 201
    
    def delete(self,todo_id):
        task=todomodel.query.filter_by(id=todo_id).first()
        db.session.delete(task)
        return 'Student Deleted', 204

api.add_resource(allStudents, '/mcit/cst-students/all')
api.add_resource(students, '/mcit/cst-students/all/<int:todo_id>') 
 
if __name__ == '__main__':
    app.run(debug=True)
