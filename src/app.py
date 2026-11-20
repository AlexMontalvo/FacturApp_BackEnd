from flask import Flask
from src.models import Base, engine
from src.models.categories import Categories
from src.models.products import Products

from src.routes import register_routes

app = Flask(__name__)

register_routes(app)

app.config['JWT_SECRET_KEY'] = 'your_secret_key'
Base.metadata.create_all(engine)

@app.route('/')
def health():
    return {
        'sucess': True, 
        'message':'Api is runing'
    }
    

if __name__ == '__main__':
    app.run(debug=True)
