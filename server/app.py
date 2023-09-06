from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# Route to get all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    # Retrieve all messages from the database ordered by created_at in ascending order
    messages = Message.query.order_by(Message.created_at.asc()).all()
    
    # Serialize the messages and return them as JSON
    serialized_messages = [message.to_dict() for message in messages]
    
    return jsonify(serialized_messages)

# Route to create a new message
@app.route('/messages', methods=['POST'])
def create_message():
    # Get the data from the request's JSON body
    data = request.get_json()
    
    # Extract the body and username from the data
    body = data.get('body')
    username = data.get('username')
    
    # Create a new message
    new_message = Message(body=body, username=username)
    
    # Add the message to the database
    db.session.add(new_message)
    db.session.commit()
    
    # Serialize the newly created message and return it as JSON
    serialized_message = new_message.to_dict()
    
    return jsonify(serialized_message), 201

# Route to update a message by ID
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    # Get the data from the request's JSON body
    data = request.get_json()
    
    # Find the message by ID
    message = Message.query.get(id)
    
    if not message:
        return jsonify({"error": "Message not found"}), 404
    
    # Update the message's body if provided in the request
    new_body = data.get('body')
    if new_body:
        message.body = new_body
    
    # Commit the changes to the database
    db.session.commit()
    
    # Serialize and return the updated message as JSON
    serialized_message = message.to_dict()
    
    return jsonify(serialized_message)

# Route to delete a message by ID
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    # Find the message by ID
    message = Message.query.get(id)
    
    if not message:
        return jsonify({"error": "Message not found"}), 404
    
    # Delete the message from the database
    db.session.delete(message)
    db.session.commit()
    
    return jsonify({"message": "Message deleted"}), 204

if __name__ == '__main__':
    app.run(port=5555)