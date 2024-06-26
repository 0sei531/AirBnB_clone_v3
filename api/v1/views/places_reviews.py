#!/usr/bin/python3
"""places_review Module"""
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """Retrieves the list of all reviews associated with a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews_list = [review.to_dict() for review in place.reviews]
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """Retrieves a review by its ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review by its ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a new review associated with a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        abort(400, 'Not a JSON')
    required_fields = ['user_id', 'text']
    for field in required_fields:
        if field not in request_data:
            abort(400, 'Missing {}'.format(field))

    user_id = request_data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    review = Review(**request_data)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a review by its ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        abort(400, 'Not a JSON')
    ignored_fields = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in request_data.items():
        if key not in ignored_fields:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
