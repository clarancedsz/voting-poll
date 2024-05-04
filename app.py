from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure the database connection parameters
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'admin'

try:
    # Connect to the database
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    logger.info("Connected to the database")
except psycopg2.Error as e:
    logger.error("Unable to connect to the database: %s", e)

# Initialize cursor
cur = conn.cursor()

@app.route('/api/submit-vote', methods=['POST'])
def submit_vote():
    vote_data = request.get_json()
    name = vote_data['name']
    choice = vote_data['choice']
    time = vote_data['time']
    cur.execute("INSERT INTO vote (name, choice, time) VALUES (%s, %s, %s)", (name, choice, time))
    conn.commit()
    return jsonify({'message': 'Vote submitted successfully'})

@app.route('/api/get-votes', methods=['GET'])
def get_votes():
    cur.execute("SELECT id, name, choice, time FROM vote")
    votes = cur.fetchall()
    vote_list = [{'id': vote[0], 'name': vote[1], 'choice': vote[2], 'time': vote[3]} for vote in votes]
    return jsonify(vote_list)

@app.route('/api/results', methods=['GET'])
def get_results():
    cur.execute("SELECT choice, COUNT(*) FROM vote GROUP BY choice")
    results = cur.fetchall()
    result_list = [{'choice': result[0], 'count': result[1]} for result in results]
    return jsonify(result_list)

if __name__ == '__main__':
    app.run(debug=True)
