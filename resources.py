from attr import field
from flask_restful import Resource, Api, reqparse, marshal_with, fields
from models import StudyResource, db
from flask_security import auth_required

parser = reqparse.RequestParser()  #if a client is sending data, it will convert into a dict
parser.add_argument('topic', type=str, help = "Topic should be string", required = True)
parser.add_argument('content', type=str, help = 'topic should be string')


api = Api(prefix='/api')

# marshal with is used to searalize the data coming from database

study_material_fields = {
    'id' : fields.Integer,
    'topic' : fields.String,
    'content' : fields.String,
    'creator_id' : fields.Integer
}

class StudyMaterial(Resource):
    
    
    # Get request will run this function (retrieve)
    @auth_required('token', 'session')
    @marshal_with(study_material_fields)
    def get(self):
        all_study_resources = StudyResource.query.all()
        return all_study_resources
    
    # post request will run this function (create)
    @auth_required('token', 'session')
    def post(self):
        data = parser.parse_args()
        new_study_resource = StudyResource(creator_id = 1, is_approved = False, **args)
        db.session.add(new_study_resource)
        db.session.commit()
        return {'message': 'Study resource added successfully'}, 201
    
api.add_resource(StudyMaterial, '/resources')