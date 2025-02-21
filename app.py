from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from langchain.llms import DeepSeek
from langchain.chains import SQLDatabaseChain
from langchain.sql_database import SQLDatabase

app = Flask(__name__)
CORS(app)

# Setup SQLite database
db_path = "example.db"
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

# Initialize DeepSeek LLM
llm = DeepSeek()

# Setup SQL Generation Chain
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