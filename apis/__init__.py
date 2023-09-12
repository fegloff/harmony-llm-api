from flask_restx import Api
from .vertex_resource import api as vertex_namespace

api = Api(
    title='LLM Api',
    version='1.0',
    description='LLM API',
)

api.add_namespace(vertex_namespace)