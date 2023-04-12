#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api

from models import db, Research, Author, ResearchAuthors

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/researches', methods=['GET'])
def research():

    if request.method == 'GET':
        researches = []
        for research in Research.query.all():
            research_dict = {
                'id': research.id,
                "topic": research.topic,
                "year": research.year,
                "page_count": research.page_count,
            }
            researches.append(research_dict)

        response = make_response(
            researches,
            200,
        )
    return response

@app.route('/researches/<int:id>', methods=['GET', 'DELETE'])
def research_by_id(id):
    research = Research.query.filter_by(id = id).first()

    if research == None:
        response_body = {
            "message": "Research paper not found"
        }
        response = make_response(jsonify(response_body), 404)

        return response

    else:
        if request.method == 'GET':
            research_dict = research.to_dict()

            response = make_response(
                research_dict,
                200
            )

            return response
### how do i add authors to the json? do i have to make a new get request like the one above and add authors after page_count?
        elif request.method == 'DELETE':
            # filter
            db.session.delete(research)
            db.session.commit()
            response_body = {
                "delete_successful": True,
                "message": ""    
            }
            response = make_response(
                response_body,
                200
            )
            return response
#     (a `ResearchAuthors` belongs
# to a `Research`, so you need to delete the `ResearchAuthors`s before the
# `Research` can be deleted).

@app.route('/authors', methods=['GET'])
def author():

    if request.method == 'GET':
        authors = []
        for author in Author.query.all():
            author_dict = {
                'id': author.id,
                "name": author.name,
                "field_of_study": author.field_of_study,
            }
            authors.append(author_dict)

        response = make_response(
            authors,
            200,
        )
    return response

@app.route('/research_authors', methods=['GET', 'POST'])
def research_author():

    if request.method == 'GET':
        research_authors = []
        for research_author in ResearchAuthors.query.all():
            research_author_dict = {
                'id': research_author.id,
                'author_id': research_author.author_id,
                'research_id': research_author.research_id,
            }
            research_authors.append(research_author_dict)

        response = make_response(
            research_authors,
            200,
        )

        return response

    elif request.method == 'POST':
        new_research_author = ResearchAuthors(
                author_id=request.form.get('author_id'),
                research_id=request.form.get('research_id'),
            )
        
        db.session.add(new_research_author)
        db.session.commit()

        research_dict = new_research_author.to_dict()

        response = make_response(
            research_dict,
            201
        )

        return response
    
    elif new_research_author == None:
        response_body = {
            "errors": ["validation errors"]
        }
        response = make_response(jsonify(response_body), 404)

        return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
