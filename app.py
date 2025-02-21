from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os
from langchain.llms import DeepSeek
from langchain.chains import SQLDatabaseChain
from langchain.sql_database import SQLDatabase

app = Flask(__name__)
CORS(app)

# MySQL Database Config (Use InfinityFree Credentials)
DB_HOST = "sqlXXX.infinityfree.com"  # Change this
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_NAME = "your_database_name"

# Connect to MySQL
def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# Setup LangChain & DeepSeek for AI SQL conversion
db = SQLDatabase.from_uri(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
llm = DeepSeek()
chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

@app.route("/query", methods=["POST"])
def query_db():
    data = request.json
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    try:
        sql_response = chain.run(user_query)
        return jsonify({"response": sql_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)