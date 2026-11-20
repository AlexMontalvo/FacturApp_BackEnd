from flask import Blueprint, jsonify, request
from src.models.products import Products
from src.utils.auth import token_required

products_bp = Blueprint('products_v1', __name__, url_prefix='/api/v1')

@products_bp.route('/products', methods=['GET'])
def get_products():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)

    products, total_products = Products.get_paginated(page=page, per_page=per_page)
    total_pages = (total_products + per_page - 1) // per_page
    return jsonify({
        'data': 
        [{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock,
        'category_id': product.category_id,
        'active': product.active
        } for product in products],
        'meta': {
            'page': page,
            'per_page': per_page,
            'total_products': total_products,
            'has_next': page < total_pages,
            'has_prev': page > 1    
            }
    }), 200


@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = Products.get_by_id(product_id)
    if product:
        return jsonify({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock,
            'category_id': product.category_id,
            'active': product.active
        })
    else:
        return jsonify({'error': 'Product not found'}), 404
    
@products_bp.route('/products', methods=['POST'])
@token_required
def post_product():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    stock = data.get('stock', 0)
    category_id = data.get('category_id')
      
    errors = {}
    if not name:
      errors['name'] = 'Name is required.'

    if not price:
      errors['price'] = 'Price is required.'
    else:
      try:
          price = float(price)
          if price < 0:
              errors['price'] = 'Price must be a non-negative number.'
      except ValueError:
          errors['price'] = 'Price must be a valid number.'

    if not category_id:
      errors['category_id'] = 'Category ID is required.'

    if errors:
        return jsonify({'success': False,
                        'message': 'Errors in data validation',
                        'validation errors': errors
                        }),400

    
    new_product = Products(name=name, description=description, price=price, stock=stock, category_id=category_id)
   
    Products.save(new_product)

    return jsonify({
        'id': new_product.id,
        'name': new_product.name,
        'description': new_product.description,
        'price': new_product.price, 
        'stock': new_product.stock,
        'category_id': new_product.category_id, 
        'active': new_product.active
        }),201

@products_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Products.get_by_id(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    data = request.get_json() or {}
    name = data.get('name', product.name)
    description = data.get('description', product.description)
    price = data.get('price', product.price)
    stock = data.get('stock', product.stock)
    category_id = data.get('category_id', product.category_id)
    active = data.get('active', product.active)

    errors = {}

    # 1. Validar Name
    if not name or not str(name).strip():
        errors['name'] = 'Name is required.'
    elif product.name != name:
        existing_product = Products.get_by_name(name)
        if existing_product:
            errors['name'] = 'Name must be unique.'

    # 2. Validar Price
    if price is None or price == '':
        errors['price'] = 'Price is required.'
    else:
        try:
            price = float(price)
            if price < 0:
                errors['price'] = 'Price must be a non-negative number.'
        except (ValueError, TypeError):
            errors['price'] = 'Price must be a valid number.'

    # 3. Validar Stock
    if stock is not None:
        try:
            stock = int(stock)
            if stock < 0:
                errors['stock'] = 'Stock must be a non-negative number.'
        except (ValueError, TypeError):
            errors['stock'] = 'Stock must be a valid number.'

    # 4. Validar Category ID
    if not category_id:
        errors['category_id'] = 'Category ID is required.'

    # Si hay errores, retornar 400 antes de tocar el objeto product
    if errors:
        return jsonify({
            'success': False,
            'message': 'Errors in data validation',
            'validation errors': errors
        }), 400

    # 5. Actualizar datos y guardar
    product.name = name.strip()
    product.description = description
    product.price = price
    product.stock = stock
    product.category_id = category_id
    product.active = active

    Products.update(product)

    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock,
        'category_id': product.category_id,
        'active': product.active
    }), 200
