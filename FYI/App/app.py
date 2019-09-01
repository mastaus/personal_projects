import os
from flask import Flask, url_for, render_template, jsonify, request, abort, redirect
# from fyi_api import insert_person, insert_event
#
app = Flask('FYI_app')
#
# @app.route('/insert_person', methods=['POST'])
# def insert():
#     if not request.json:
#         abort(400)
#     data = request.json
#
#     response = insert_person(data)
#
#     return jsonify(response)
#
# @app.route('/insert_event', methods=['POST'])
# def insert():
#     if not request.json:
#         abort(400)
#     data = request.json
#
#     response = insert_event(data)
#
#     return jsonify(response)
#
# @app.route('/update_person', methods=['POST'])
# def update():
#     if not request.json:
#         abort(400)
#     data = request.json
#
#     response = update_person(data)
#
#     return jsonify(response)
#
# @app.route('/update_event', methods=['POST'])
# def update():
#     if not request.json:
#         abort(400)
#     data = request.json
#
#     response = update_event(data)
#
#     return jsonify(response)
#
# @app.route('/delete_person', methods=['POST'])
# def delete():
#     if not request.json:
#         abort(400)
#     data = request.json
#
#     response = delete_person(data)
#
#     return jsonify(response)
#
# @app.route('/delete_event', methods=['POST'])
# def delete():
#     if not request.json:
#         abort(400)
#     data = request.json
#
#     response = delete_event(data)
#
#     return jsonify(response)

@app.route('/')
def index():
    return render_template('index.html')

app.run(debug=True)
