from flask import Flask
from src.models import Base, engine
from src.models.categories import Categories
from src.models.products import Products
from src.routes.v1.products_routes import products_bp
from src.routes import register_routes
app = Flask(__name__)

##app.register_blueprint(products_bp)

register_routes(app)

app.config['JWT_SECRET_KEY'] = 'facturapp-adso-25t4-dev-secret-key-change-me'
Base.metadata.create_all(engine)

@app.route('/')
def health():
    return {
        'success': True,
        'message': 'API is running'
    }

if __name__ == '__main__':
    app.run(debug=True)
