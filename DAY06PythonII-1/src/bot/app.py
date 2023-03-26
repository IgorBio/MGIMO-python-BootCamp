from flask import Flask, request, Response, jsonify
from database.dbapi import DatabaseConnector

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
db = DatabaseConnector()

@app.route("/list_books", methods=["GET"])
async def get_list_books():
    data = await db.list_books()
    return data


@app.route("/add", methods=["POST", "GET"])
async def add_book():
    if request.method == "POST":
        post_data = request.get_json()
        res = await db.add(post_data["title"], post_data["author"], post_data["published"])
        return res
    else:
        print(request)
        return {"POST": "ONLY"}


if __name__ == "__main__":
    app.run(debug=True)
