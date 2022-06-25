# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.


### Backend

The [backend](./backend/README.md) directory contains a completed Flask and SQLAlchemy server. 

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend that consume the data from the Flask server. 
> View the [Frontend README](./frontend/README.md) for more details.

## API Documentation

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": false, 
    "error": 400,
    "message": "bad request"
}
```

The API will return any of these error types when a request fail:

400: Bad Request
404: Resource Not Found
422: Not Processable
500: Internal Server Error
405: Method Not Allowed

### Endpoints

**GET /categories**

General:
- Returns a list of categories, success value
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

Sample: ```curl http://127.0.0.1:5000/categories```

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

**GET '/questions?page=${integer}'**

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

Sample: ```curl http://127.0.0.1:5000/questions?page=1```

```json
{
  "success": true,
  "questions": [
     {
      "answer": "Maya Angelou", 
      "category": "4", 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": "4", 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": "1", 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
  ],
  "total_questions": 19,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "None"
}
```

**GET /categories/{id}/questions**

- Fetches questions for a cateogry specified by id request argument
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string paginated in groups of 10.

Sample: ```curl http://127.0.0.1:5000/categories/3/questions```

```
{
  "success": true,
  "current_category": "Geography", 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": "3", 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": "3", 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": "3", 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "total_questions": 3
}
```

**DELETE /questions/{id}**

- Deletes the question of the given ID if it exists.
- Request Arguments: id - integer
- Returns: Does not return anything besides the appropriate HTTP status code. 

Sample ```curl -X DELETE http://127.0.0.1:5000/questions/16?page=2 ```


**POST /questions/{id}**

- Sends a post request in order to add a new question
- Request Body:
```
{
    "question": "The Taj Mahal is located in which Indian city?"
    "answer": "Agra", 
    "category": "3", 
    "difficulty": 2, 
}
```
Returns: Does not return any new data besides the appropriate HTTP status code. 

Sample: ```curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"The Taj Mahal is located in which Indian city?", "answer": "Agra","category" :"3", "difficulty":"2"}'```

**POST /questions/search**

General:
- Sends a post request in order to search for a specific question by search term
- Request Body:

```
{
  "searchTerm": "who"
}
```

Sample ```curl http://127.0.0.1:5000/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"who"}'```

Returns: array of questions, a number of total questions that met the search term and the current category string

```
{
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": "4", 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": "4", 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": "1", 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
  ], 
  "success": true, 
  "total_questions": 3,
  "current_category": "none"
}
```

**POST /quizzes**

General:
- Sends a post request in order to get the next question
- Request Body:

```
{
    "previous_questions": [10, 6, 17]
    'quiz_category': {
        'id': 0,
        'type': 'All'
    }
}
```

Sample``` curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"All","id":0}, "previous_questions":[10, 6, 17]}'``` 

- Returns: a single new question object

```
{
  "question": {
    "answer": "Agra", 
    "category": "3", 
    "difficulty": 2, 
    "id": 15, 
    "question": "The Taj Mahal is located in which Indian city?"
  }, 
  "success": true
}
```
