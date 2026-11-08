from flask import Blueprint, jsonify, request
from src.models.products import Products
products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():


    products = Products.get()
    return jsonify([{
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock,
            'category_id': product.category_id,
            'active': product.active
        } for product in products])

