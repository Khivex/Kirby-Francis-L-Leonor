from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Student database (in-memory)
students = {
    1: {
        "id": 1,
        "name": "Kirby Francis L. Leonor",
        "grade": 12,
        "section": "Stallman",
        "subjects": ["Mathematics", "Science", "English", "Filipino", "Programming"],
        "email": "kirby.leonor@student.edu"
    }
}

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to Kirby's Flask Student API!",
        "version": "2.0",
        "endpoints": {
            "/": "API Home",
            "/student": "Get current student info",
            "/student/<id>": "Get student by ID",
            "/students": "Get all students",
            "/add-student": "Add new student (POST)",
            "/health": "API health check"
        }
    })

@app.route('/student')
def get_student():
    """Get the current student (you)"""
    return jsonify({
        "name": "Kirby Francis L. Leonor",
        "grade": 12,
        "section": "Stallman",
        "status": "Senior High School",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/student/<int:student_id>')
def get_student_by_id(student_id):
    """Get a specific student by ID"""
    student = students.get(student_id)
    if student:
        return jsonify(student)
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route('/students')
def get_all_students():
    """Get all students"""
    return jsonify({
        "count": len(students),
        "students": list(students.values())
    })

@app.route('/add-student', methods=['POST'])
def add_student():
    """Add a new student"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    
    new_id = max(students.keys()) + 1 if students else 1
    new_student = {
        "id": new_id,
        "name": data.get('name'),
        "grade": data.get('grade', 12),
        "section": data.get('section', 'Unknown'),
        "subjects": data.get('subjects', []),
        "email": data.get('email', '')
    }
    
    students[new_id] = new_student
    return jsonify({
        "message": "Student added successfully",
        "student": new_student
    }), 201

@app.route('/health')
def health_check():
    """Check if API is running"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_students": len(students)
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
