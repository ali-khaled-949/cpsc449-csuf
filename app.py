from flask import Flask, render_template, request, redirect, url_for
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MongoDB connection string from environment variable
uri = os.getenv("MONGODB_URI")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.note_app  # Access the note_app database
notes_collection = db.notes  # Access the notes collection within note_app

# Test the connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Define your routes here (as previously discussed)
@app.route('/')
def home():
    notes = notes_collection.find()
    return render_template('home.html', notes=notes)

@app.route('/add', methods=['POST'])
def add_note():
    cwid = request.form.get('cwid')
    full_name = request.form.get('full_name')
    note_data = {'cwid': cwid, 'full_name': full_name}
    notes_collection.insert_one(note_data)
    return redirect(url_for('home'))

@app.route('/delete/<note_id>')
def delete_note(note_id):
    notes_collection.delete_one({'_id': ObjectId(note_id)})
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5002)
