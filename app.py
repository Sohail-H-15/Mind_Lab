from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
import secrets
import re
import json
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Gemini AI
GEMINI_AVAILABLE = False
genai = None

try:
    import google.generativeai as genai
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    if GEMINI_API_KEY and GEMINI_API_KEY.strip() and GEMINI_API_KEY != 'your_api_key_here':
        genai.configure(api_key=GEMINI_API_KEY.strip())
        GEMINI_AVAILABLE = True
        print("✓ Gemini API configured successfully!")
    else:
        GEMINI_AVAILABLE = False
        print("⚠ Warning: GEMINI_API_KEY not found in environment. Using fallback responses.")
        if os.path.exists('.env'):
            print("   Note: .env file exists but key not loaded. Check file format.")
        else:
            print("   Note: .env file not found. Create it with: GEMINI_API_KEY=your_key")
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠ Warning: google-generativeai not installed. Install with: pip install google-generativeai python-dotenv")
except Exception as e:
    GEMINI_AVAILABLE = False
    print(f"⚠ Warning: Gemini API initialization failed: {e}. Using fallback responses.")

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Database initialization
def init_db():
    conn = sqlite3.connect('mindlab.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  email_verified INTEGER DEFAULT 0,
                  verification_token TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Concepts table
    c.execute('''CREATE TABLE IF NOT EXISTS concepts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  topic TEXT NOT NULL,
                  content TEXT,
                  difficulty_level TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # Activities table
    c.execute('''CREATE TABLE IF NOT EXISTS activities
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  concept_id INTEGER,
                  activity_type TEXT NOT NULL,
                  activity_data TEXT,
                  score INTEGER,
                  completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (concept_id) REFERENCES concepts (id))''')
    
    # Chat history table
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  message TEXT NOT NULL,
                  response TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    conn.commit()
    conn.close()

# Database helper functions
def get_db():
    conn = sqlite3.connect('mindlab.db')
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False, insert=False):
    conn = get_db()
    cur = conn.execute(query, args)
    if insert:
        conn.commit()
        last_id = cur.lastrowid
        conn.close()
        return last_id
    rv = cur.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Email validation
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        # Password validation: 8 characters, one uppercase, one special character
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return render_template('register.html')
        
        if not re.search(r'[A-Z]', password):
            flash('Password must contain at least one uppercase letter.', 'error')
            return render_template('register.html')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            flash('Password must contain at least one special character (!@#$%^&*(),.?":{}|<>)', 'error')
            return render_template('register.html')
        
        if not is_valid_email(email):
            flash('Invalid email address.', 'error')
            return render_template('register.html')
        
        # Check if user exists
        existing_user = query_db('SELECT * FROM users WHERE username = ? OR email = ?', 
                                (username, email), one=True)
        if existing_user:
            flash('Username or email already exists.', 'error')
            return render_template('register.html')
        
        # Create user
        verification_token = secrets.token_urlsafe(32)
        password_hash = generate_password_hash(password)
        
        query_db('INSERT INTO users (username, email, password, verification_token) VALUES (?, ?, ?, ?)',
                (username, email, password_hash, verification_token), insert=True)
        
        # In production, send email with verification link
        # For now, we'll auto-verify or provide a simple verification page
        flash(f'Registration successful! Verification token: {verification_token} (In production, this would be sent via email)', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/verify/<token>')
def verify_email(token):
    user = query_db('SELECT * FROM users WHERE verification_token = ?', (token,), one=True)
    if user:
        query_db('UPDATE users SET email_verified = 1 WHERE id = ?', (user['id'],))
        flash('Email verified successfully!', 'success')
        return redirect(url_for('login'))
    flash('Invalid verification token.', 'error')
    return redirect(url_for('register'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('login.html')
        
        user = query_db('SELECT * FROM users WHERE username = ?', (username,), one=True)
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    concepts = query_db('SELECT * FROM concepts WHERE user_id = ? ORDER BY created_at DESC LIMIT 10', (user_id,))
    return render_template('dashboard.html', concepts=concepts)

@app.route('/clear-concepts', methods=['POST'])
@login_required
def clear_concepts():
    user_id = session['user_id']
    query_db('DELETE FROM concepts WHERE user_id = ?', (user_id,))
    query_db('DELETE FROM activities WHERE concept_id IN (SELECT id FROM concepts WHERE user_id = ?)', (user_id,))
    flash('All concepts cleared successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/concept-playground', methods=['GET', 'POST'])
@login_required
def concept_playground():
    if request.method == 'POST':
        topic = request.form.get('topic')
        if topic:
            user_id = session['user_id']
            # Save concept
            concept_id = query_db('INSERT INTO concepts (user_id, topic) VALUES (?, ?)',
                                 (user_id, topic), insert=True)
            return redirect(url_for('playground_activity', topic=topic))
    
    return render_template('concept_playground.html')

@app.route('/playground/<topic>')
@login_required
def playground_activity(topic):
    return render_template('playground_activity.html', topic=topic)

@app.route('/api/generate-activities/<topic>')
@login_required
def generate_activities(topic):
    """Generate different types of activities for a topic"""
    activities = {
        'drag_drop': generate_drag_drop(topic),
        'fill_blanks': generate_fill_blanks(topic),
        'flashcards': generate_flashcards(topic),
        'quiz': generate_quiz(topic),
        'concept_flow': generate_concept_flow(topic)
    }
    return jsonify(activities)

def call_gemini(prompt, temperature=0.7):
    """Call Gemini API with a prompt"""
    if not GEMINI_AVAILABLE or genai is None:
        return None
    
    try:
        # Use gemini-2.0-flash (fast and stable) or fallback to gemini-2.5-flash
        model_names = ['gemini-2.0-flash', 'gemini-2.5-flash', 'gemini-1.5-flash']
        
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(temperature=temperature))
                return response.text
            except Exception as e1:
                if model_name != model_names[-1]:  # Not the last one
                    continue
                else:
                    raise e1
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None

def generate_drag_drop(topic):
    """Generate drag and drop puzzle using Gemini API"""
    if GEMINI_AVAILABLE:
        prompt = f"""Create a drag-and-drop learning activity for the topic "{topic}".

Return ONLY a JSON object with this exact structure:
{{
    "title": "Activity title",
    "items": ["item1", "item2", "item3", "item4", "item5", "item6"],
    "targets": ["Category 1", "Category 2", "Category 3"],
    "correct_mapping": {{
        "item1": "Category 1",
        "item2": "Category 1",
        "item3": "Category 2",
        "item4": "Category 2",
        "item5": "Category 3",
        "item6": "Category 3"
    }}
}}

The items should be key terms/concepts related to {topic}, and targets should be logical categories that these items can be sorted into. Include 5-8 items and 3-4 target categories. The correct_mapping shows which items belong to which category. Return ONLY the JSON, no other text."""
        
        response = call_gemini(prompt)
        if response:
            try:
                # Clean response to extract JSON
                json_str = response.strip()
                if '```json' in json_str:
                    json_str = json_str.split('```json')[1].split('```')[0].strip()
                elif '```' in json_str:
                    json_str = json_str.split('```')[1].split('```')[0].strip()
                return json.loads(json_str)
            except:
                pass
    
    # Fallback to templates
    templates = {
        'photosynthesis': {
            'title': 'Photosynthesis Process',
            'items': ['Sunlight', 'Water', 'Carbon Dioxide', 'Chlorophyll', 'Oxygen', 'Glucose'],
            'targets': ['Energy Source', 'Reactants', 'Catalyst', 'Products'],
            'correct_mapping': {
                'Sunlight': 'Energy Source',
                'Chlorophyll': 'Catalyst',
                'Water': 'Reactants',
                'Carbon Dioxide': 'Reactants',
                'Oxygen': 'Products',
                'Glucose': 'Products'
            }
        },
        'default': {
            'title': f'{topic} - Key Components',
            'items': [f'{topic} Component 1', f'{topic} Component 2', f'{topic} Component 3'],
            'targets': ['Category A', 'Category B', 'Category C'],
            'correct_mapping': {
                f'{topic} Component 1': 'Category A',
                f'{topic} Component 2': 'Category B',
                f'{topic} Component 3': 'Category C'
            }
        }
    }
    return templates.get(topic.lower(), templates['default'])

def generate_reorder(topic):
    """Generate reorder steps activity using Gemini API"""
    if GEMINI_AVAILABLE:
        prompt = f"""Create a step-by-step reordering activity for the topic "{topic}".

Return ONLY a JSON object with this exact structure:
{{
    "title": "Activity title",
    "steps": ["Step 1 description", "Step 2 description", "Step 3 description", "Step 4 description", "Step 5 description"]
}}

The steps should describe a process or sequence related to {topic}. Include 5-7 steps in logical order. Return ONLY the JSON, no other text."""
        
        response = call_gemini(prompt)
        if response:
            try:
                json_str = response.strip()
                if '```json' in json_str:
                    json_str = json_str.split('```json')[1].split('```')[0].strip()
                elif '```' in json_str:
                    json_str = json_str.split('```')[1].split('```')[0].strip()
                return json.loads(json_str)
            except:
                pass
    
    # Fallback to templates
    templates = {
        'photosynthesis': {
            'title': 'Order the Photosynthesis Steps',
            'steps': [
                'Light energy is absorbed by chlorophyll',
                'Water molecules are split',
                'Carbon dioxide enters the leaf',
                'Glucose is produced',
                'Oxygen is released'
            ]
        },
        'default': {
            'title': f'{topic} - Process Steps',
            'steps': [
                f'Step 1: Introduction to {topic}',
                f'Step 2: Understanding {topic} concepts',
                f'Step 3: Applying {topic}',
                f'Step 4: Advanced {topic} topics'
            ]
        }
    }
    return templates.get(topic.lower(), templates['default'])

def generate_fill_blanks(topic):
    """Generate fill-in-the-blanks activity using Gemini API"""
    if GEMINI_AVAILABLE:
        prompt = f"""Create a fill-in-the-blanks activity for the topic "{topic}".

Return ONLY a JSON object with this exact structure:
{{
    "title": "Activity title",
    "text": "A paragraph about {topic} with __1__, __2__, __3__ marking blanks. Use __1__, __2__, __3__, etc. for each blank.",
    "blanks": ["answer1", "answer2", "answer3"]
}}

Create 3-5 blanks in a coherent paragraph explaining {topic}. The answers should be key terms. Return ONLY the JSON, no other text."""
        
        response = call_gemini(prompt)
        if response:
            try:
                json_str = response.strip()
                if '```json' in json_str:
                    json_str = json_str.split('```json')[1].split('```')[0].strip()
                elif '```' in json_str:
                    json_str = json_str.split('```')[1].split('```')[0].strip()
                return json.loads(json_str)
            except:
                pass
    
    # Fallback to templates
    templates = {
        'photosynthesis': {
            'title': 'Complete the Photosynthesis Description',
            'text': 'Photosynthesis is the process by which plants convert __1__ and __2__ into __3__ using __4__ from sunlight.',
            'blanks': ['carbon dioxide', 'water', 'glucose', 'energy']
        },
        'default': {
            'title': f'Complete the {topic} Description',
            'text': f'{topic} is an important concept that involves __1__ and __2__ to achieve __3__.',
            'blanks': ['component1', 'component2', 'goal']
        }
    }
    return templates.get(topic.lower(), templates['default'])

def generate_flashcards(topic):
    """Generate flashcards using Gemini API"""
    if GEMINI_AVAILABLE:
        prompt = f"""Create educational flashcards for the topic "{topic}".

Return ONLY a JSON array with this exact structure:
[
    {{"front": "Question 1", "back": "Answer 1"}},
    {{"front": "Question 2", "back": "Answer 2"}},
    {{"front": "Question 3", "back": "Answer 3"}},
    {{"front": "Question 4", "back": "Answer 4"}}
]

Create 4-6 flashcards with questions on the front and clear, concise answers on the back. Return ONLY the JSON array, no other text."""
        
        response = call_gemini(prompt)
        if response:
            try:
                json_str = response.strip()
                if '```json' in json_str:
                    json_str = json_str.split('```json')[1].split('```')[0].strip()
                elif '```' in json_str:
                    json_str = json_str.split('```')[1].split('```')[0].strip()
                return json.loads(json_str)
            except:
                pass
    
    # Fallback to templates
    templates = {
        'photosynthesis': [
            {'front': 'What is photosynthesis?', 'back': 'The process by which plants convert light energy into chemical energy.'},
            {'front': 'What are the reactants?', 'back': 'Carbon dioxide and water.'},
            {'front': 'What are the products?', 'back': 'Glucose and oxygen.'},
            {'front': 'Where does photosynthesis occur?', 'back': 'In the chloroplasts of plant cells.'}
        ],
        'default': [
            {'front': f'What is {topic}?', 'back': f'{topic} is a fundamental concept in this field.'},
            {'front': f'Why is {topic} important?', 'back': f'{topic} helps us understand key principles.'},
            {'front': f'How does {topic} work?', 'back': f'{topic} operates through specific mechanisms.'}
        ]
    }
    return templates.get(topic.lower(), templates['default'])

def generate_quiz(topic):
    """Generate mini quiz using Gemini API"""
    if GEMINI_AVAILABLE:
        prompt = f"""Create a multiple-choice quiz for the topic "{topic}".

Return ONLY a JSON object with this exact structure:
{{
    "title": "Quiz title",
    "questions": [
        {{
            "question": "Question text",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0
        }}
    ]
}}

Create 3-5 questions with 4 options each. The "correct" field should be the index (0-3) of the correct answer. Return ONLY the JSON, no other text."""
        
        response = call_gemini(prompt)
        if response:
            try:
                json_str = response.strip()
                if '```json' in json_str:
                    json_str = json_str.split('```json')[1].split('```')[0].strip()
                elif '```' in json_str:
                    json_str = json_str.split('```')[1].split('```')[0].strip()
                return json.loads(json_str)
            except:
                pass
    
    # Fallback to templates
    templates = {
        'photosynthesis': {
            'title': f'{topic} Quiz',
            'questions': [
                {
                    'question': 'What is the primary source of energy for photosynthesis?',
                    'options': ['Water', 'Sunlight', 'Carbon Dioxide', 'Oxygen'],
                    'correct': 1
                },
                {
                    'question': 'Which gas is released during photosynthesis?',
                    'options': ['Carbon Dioxide', 'Nitrogen', 'Oxygen', 'Hydrogen'],
                    'correct': 2
                },
                {
                    'question': 'Where does photosynthesis primarily occur?',
                    'options': ['Roots', 'Stem', 'Leaves', 'Flowers'],
                    'correct': 2
                }
            ]
        },
        'default': {
            'title': f'{topic} Quiz',
            'questions': [
                {
                    'question': f'What is a key aspect of {topic}?',
                    'options': ['Option A', 'Option B', 'Option C', 'Option D'],
                    'correct': 0
                },
                {
                    'question': f'Which statement about {topic} is true?',
                    'options': ['Statement 1', 'Statement 2', 'Statement 3', 'Statement 4'],
                    'correct': 1
                }
            ]
        }
    }
    return templates.get(topic.lower(), templates['default'])

def generate_concept_flow(topic):
    """Generate concept flow builder activity using Gemini API"""
    if GEMINI_AVAILABLE:
        prompt = f"""Create a concept flow activity for the topic "{topic}".

Return ONLY a JSON object with this exact structure:
{{
    "title": "Activity title",
    "steps": [
        {{"id": 1, "text": "Step 1 description"}},
        {{"id": 2, "text": "Step 2 description"}},
        {{"id": 3, "text": "Step 3 description"}},
        {{"id": 4, "text": "Step 4 description"}},
        {{"id": 5, "text": "Step 5 description"}}
    ],
    "correct_flow": [1, 2, 3, 4, 5]
}}

Create 4-6 steps that represent a logical sequence or process related to {topic}. The "correct_flow" array should contain the step IDs in the correct order. Return ONLY the JSON, no other text."""
        
        response = call_gemini(prompt)
        if response:
            try:
                json_str = response.strip()
                if '```json' in json_str:
                    json_str = json_str.split('```json')[1].split('```')[0].strip()
                elif '```' in json_str:
                    json_str = json_str.split('```')[1].split('```')[0].strip()
                return json.loads(json_str)
            except:
                pass
    
    # Fallback to templates
    templates = {
        'photosynthesis': {
            'title': 'Photosynthesis Process Flow',
            'steps': [
                {'id': 1, 'text': 'Light energy absorbed'},
                {'id': 2, 'text': 'Water molecules split'},
                {'id': 3, 'text': 'Carbon dioxide enters'},
                {'id': 4, 'text': 'Glucose produced'},
                {'id': 5, 'text': 'Oxygen released'}
            ],
            'correct_flow': [1, 2, 3, 4, 5]
        },
        'default': {
            'title': f'{topic} Concept Flow',
            'steps': [
                {'id': 1, 'text': f'Introduction to {topic}'},
                {'id': 2, 'text': f'Understanding {topic} basics'},
                {'id': 3, 'text': f'Applying {topic} concepts'},
                {'id': 4, 'text': f'Advanced {topic} topics'},
                {'id': 5, 'text': f'Mastering {topic}'}
            ],
            'correct_flow': [1, 2, 3, 4, 5]
        }
    }
    return templates.get(topic.lower(), templates['default'])

@app.route('/api/save-activity', methods=['POST'])
@login_required
def save_activity():
    data = request.json
    user_id = session['user_id']
    concept = query_db('SELECT id FROM concepts WHERE user_id = ? AND topic = ?', 
                      (user_id, data['topic']), one=True)
    
    if concept:
        import json
        query_db('INSERT INTO activities (concept_id, activity_type, activity_data, score) VALUES (?, ?, ?, ?)',
                (concept['id'], data['type'], json.dumps(data['data']), data.get('score', 0)), insert=True)
        return jsonify({'success': True})
    return jsonify({'success': False}), 400

@app.route('/pattern-insight', methods=['GET', 'POST'])
@login_required
def pattern_insight():
    if request.method == 'POST':
        topic = request.form.get('topic')
        if topic:
            insights = generate_insights(topic)
            return render_template('pattern_insight.html', topic=topic, insights=insights)
    
    return render_template('pattern_insight.html')

def generate_insights(topic):
    """Generate AI pattern insights for a topic using Gemini API"""
    if GEMINI_AVAILABLE:
        prompt = f"""Analyze the topic "{topic}" and provide educational insights.

Return ONLY a JSON object with this exact structure:
{{
    "summary": "A concise 1-2 sentence summary of the topic",
    "patterns": ["Pattern 1", "Pattern 2", "Pattern 3", "Pattern 4"],
    "difficulty": "basic" or "intermediate" or "expert",
    "explanation": "A detailed 2-3 sentence explanation of the concept",
    "related_topics": ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"]
}}

Provide insightful analysis. Patterns should be key themes or concepts. Difficulty should reflect learning complexity. Related topics should be genuinely connected. Return ONLY the JSON, no other text."""
        
        response = call_gemini(prompt)
        if response:
            try:
                json_str = response.strip()
                if '```json' in json_str:
                    json_str = json_str.split('```json')[1].split('```')[0].strip()
                elif '```' in json_str:
                    json_str = json_str.split('```')[1].split('```')[0].strip()
                result = json.loads(json_str)
                # Ensure difficulty is valid
                if result.get('difficulty') not in ['basic', 'intermediate', 'expert']:
                    result['difficulty'] = 'intermediate'
                return result
            except Exception as e:
                print(f"Error parsing Gemini insights: {e}")
    
    # Fallback to rule-based pattern mapping
    topic_lower = topic.lower()
    
    # Summarization
    summaries = {
        'photosynthesis': 'Photosynthesis is the biological process by which plants, algae, and some bacteria convert light energy into chemical energy stored in glucose molecules.',
        'default': f'{topic} is a fundamental concept that involves understanding key principles and their applications.'
    }
    summary = summaries.get(topic_lower, summaries['default'])
    
    # Pattern recognition
    patterns = {
        'photosynthesis': ['Energy conversion', 'Chemical reactions', 'Biological processes', 'Plant biology'],
        'default': ['Core concepts', 'Key principles', 'Fundamental mechanisms', 'Practical applications']
    }
    recognized_patterns = patterns.get(topic_lower, patterns['default'])
    
    # Difficulty level prediction
    difficulty_keywords = {
        'basic': ['introduction', 'basics', 'fundamentals', 'simple'],
        'intermediate': ['advanced', 'complex', 'detailed', 'analysis'],
        'expert': ['research', 'theoretical', 'quantum', 'molecular']
    }
    difficulty = 'intermediate'
    for level, keywords in difficulty_keywords.items():
        if any(kw in topic_lower for kw in keywords):
            difficulty = level
            break
    
    # Concept explanation
    explanations = {
        'photosynthesis': 'Photosynthesis occurs in two main stages: light-dependent reactions (capturing light energy) and light-independent reactions (Calvin cycle, producing glucose).',
        'default': f'{topic} can be understood through systematic study of its components, relationships, and real-world applications.'
    }
    explanation = explanations.get(topic_lower, explanations['default'])
    
    # Related topics
    related = {
        'photosynthesis': ['Cellular respiration', 'Chloroplasts', 'Plant biology', 'Energy flow', 'Ecosystems'],
        'default': [f'{topic} applications', f'{topic} theory', f'Advanced {topic}', f'{topic} examples']
    }
    related_topics = related.get(topic_lower, related['default'])
    
    return {
        'summary': summary,
        'patterns': recognized_patterns,
        'difficulty': difficulty,
        'explanation': explanation,
        'related_topics': related_topics
    }

@app.route('/chatbot', methods=['GET', 'POST'])
@login_required
def chatbot():
    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            response = generate_chatbot_response(message)
            user_id = session['user_id']
            
            # Save to chat history
            query_db('INSERT INTO chat_history (user_id, message, response) VALUES (?, ?, ?)',
                    (user_id, message, response), insert=True)
            
            return jsonify({'response': response})
    
    # Get chat history
    user_id = session['user_id']
    history = query_db('SELECT * FROM chat_history WHERE user_id = ? ORDER BY created_at DESC LIMIT 20', 
                      (user_id,))
    
    return render_template('chatbot.html', history=history)

@app.route('/clear-chat', methods=['POST'])
@login_required
def clear_chat():
    user_id = session['user_id']
    query_db('DELETE FROM chat_history WHERE user_id = ?', (user_id,))
    flash('Chat history cleared successfully!', 'success')
    return redirect(url_for('chatbot'))

def generate_chatbot_response(message):
    """Generate chatbot response using Gemini API"""
    # Use Gemini API if available
    if GEMINI_AVAILABLE:
        prompt = f"""You are a friendly educational chatbot for MindLab learning platform. Help students learn by answering their questions clearly and encouraging them to use interactive features.

Student question: {message}

Provide a helpful, educational response. If relevant, mention that they can explore the topic in the Concept Playground or use Pattern Insights. Keep responses conversational and encouraging. Limit to 2-3 sentences."""
        
        response = call_gemini(prompt, temperature=0.9)
        if response:
            return response.strip()
    
    # Fallback to keyword-based responses
    message_lower = message.lower()
    
    # Keyword-based responses
    responses = {
        'hello': 'Hello! How can I help you learn today?',
        'hi': 'Hi there! What would you like to know?',
        'help': 'I can help you understand concepts, answer questions, and guide your learning. What topic interests you?',
        'photosynthesis': 'Photosynthesis is the process by which plants convert light energy into chemical energy. Would you like to learn more about it in the Concept Playground?',
        'what is': 'I can explain concepts to you! Try asking about a specific topic, or use the Concept Playground for interactive learning.',
        'how': 'Great question! I can help explain processes and concepts. For interactive learning, check out the Concept Playground.',
        'why': 'That\'s an important question! Understanding the "why" helps deepen your knowledge. Would you like to explore this in the Concept Playground?',
        'thank': 'You\'re welcome! Keep learning and exploring!',
        'thanks': 'You\'re welcome! Feel free to ask more questions anytime.',
    }
    
    # Check for keywords
    for keyword, response in responses.items():
        if keyword in message_lower:
            return response
    
    # Default response
    default_responses = [
        "That's an interesting question! I'd recommend exploring this topic in the Concept Playground for interactive learning.",
        "I can help you understand this better. Try using the Pattern Insight Engine to get detailed analysis, or the Concept Playground for hands-on practice.",
        "Great question! For the best learning experience, I suggest checking out the interactive activities in the Concept Playground.",
        "I'm here to help! You can learn more about this topic through our interactive activities or pattern insights."
    ]
    
    import random
    return random.choice(default_responses)

if __name__ == '__main__':
    init_db()
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)

