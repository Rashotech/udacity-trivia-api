from crypt import methods
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
from sqlalchemy.sql.functions import func


QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def fetch_categories():
        try:
            # fetch all categories
            all_categories = Category.query.order_by(Category.id).all()

            if len(all_categories) == 0:
                abort(404)

            categoriesDict = {}
            for category in all_categories:
                categoriesDict[category.id] = category.type

            return jsonify({ 
                "success": True,
                "categories": categoriesDict 
            })
        except Exception as e:
            print(e)
            abort(400)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions')
    def fetch_questions():
        #fetch all questions
        selection = Question.query.order_by(Question.id).all()

        #fetch current questions in a page
        current_questions = paginate_questions(request, selection)

        if (len(current_questions) == 0):
            abort(404)

        #fetch all categories
        all_categories = Category.query.all()
        categoriesDict = {}
        for category in all_categories:
            categoriesDict[category.id] = category.type
        
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': categoriesDict,
            "current_category": None
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        question = Question.query.filter(Question.id == id).one_or_none()

        if (question is None):
            abort(404)
        else:
            question.delete()
        return jsonify(), 204


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route("/questions", methods=["POST"])
    def create_question():
        #get Request body
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)

        #Validate Request Body
        if(new_question is None or new_answer is None or
            new_difficulty is None or new_category is None):
            abort(422)

        question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
        question.insert()
        return jsonify(), 201

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    #Search Route Created. Modified in the frontend
    @app.route('/questions/search', methods=['POST']) 
    def search_questions():
        try:
            body = request.get_json()

            search_term = body.get('searchTerm', None)

            #Validate request body
            if (search_term is None):
                abort(422)


            selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search_term))
            )
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection.all()),
                'current_category': None
            })
        except Exception as e:
            print(e)
            abort(400)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def fetch_question_by_category(id):
        try:
            category = Category.query.filter(Category.id == id).one_or_none()
            if category is None:
                abort(404)

            selection = Question.query.filter(Question.category == id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': category.type
            })
        except Exception as e:
            print(e)
            abort(400)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        body = request.get_json()
       
        previous_questions = body.get('previous_questions', None)
        category = body.get('quiz_category', None)

        category_id = category.get('id')

        if (previous_questions is None or category is None):
            abort(400)
        
        try:
            # Order randomly
            order_by = func.random()

            #Check if category is All or other categories
            if category_id == 0 :
                #Fetch questions randomly and not in previous questions
                question = Question.query.order_by(order_by).filter(Question.id.notin_(previous_questions)).first()
            else:
                question = Question.query.filter(Question.category == category_id).order_by(order_by).filter(Question.id.notin_(previous_questions)).first()

            #When the question is exhausted
            if question is None:
                return jsonify({
                    'success': True
            })

            return jsonify({
                'success': True,
                'question': question.format()
            })
        except Exception as e:
            print(e)
            abort(400)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            'error': 500,
            "message": "Internal server error"
        }), 500


    return app

