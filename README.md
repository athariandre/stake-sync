# Stake Sync - Weekly Business Update Automation

A service that helps business owners submit weekly updates and automatically produces tailored written messages for multiple audiences (investors, employees, partners).

## Features

- 📝 **Raw Input Collection**: Simple chatbot interface for collecting weekly updates
- 🎨 **Style Adaptation**: Analyzes writing samples to match your communication style
- 🤖 **AI Draft Generation**: Generates tailored drafts for investors, employees, and partners
- ✏️ **Review & Edit Workflow**: Simple review loop with natural language editing
- 📧 **Email Distribution**: Automated sending via SendGrid
- 📊 **Live Dashboard**: Public tracking board showing sent updates

## Tech Stack

- **Backend**: Python with FastAPI
- **Database**: SQLite (easy to upgrade to PostgreSQL)
- **AI**: Google Gemini API
- **Email**: SendGrid API
- **Frontend**: HTML/CSS/JavaScript (no complex frameworks)

## Setup Instructions

### Prerequisites

- Python 3.9+
- Google Gemini API key
- SendGrid API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/athariandre/stake-sync.git
cd stake-sync
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. Initialize the database:
```bash
python -m app.database.init_db
```

### Running the Application

Start the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access the application:
- Chatbot Interface: http://localhost:8000
- Dashboard: http://localhost:8000/dashboard/{user_id}
- API Docs: http://localhost:8000/docs

## Project Structure

```
stake-sync/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── database/
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── database.py         # Database connection
│   │   └── init_db.py          # Database initialization
│   ├── services/
│   │   ├── gemini_service.py   # Gemini API integration
│   │   ├── sendgrid_service.py # SendGrid integration
│   │   ├── style_analyzer.py   # Writing style analysis
│   │   ├── draft_generator.py  # Draft generation logic
│   │   └── memory_service.py   # Agent context/memory
│   ├── routes/
│   │   ├── auth.py             # Authentication routes
│   │   ├── updates.py          # Update collection routes
│   │   ├── style.py            # Style sample routes
│   │   ├── drafts.py           # Draft generation routes
│   │   ├── review.py           # Review workflow routes
│   │   ├── send.py             # Email sending routes
│   │   └── dashboard.py        # Dashboard routes
│   └── static/
│       ├── chatbot.html        # Chatbot interface
│       ├── dashboard.html      # Dashboard page
│       ├── css/
│       └── js/
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

## API Routes

### Authentication (Optional)
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user

### Update Collection
- `POST /update/submit` - Submit weekly update
- `GET /update/list` - List all updates
- `GET /update/{id}` - Get specific update

### Style Management
- `POST /style/upload` - Upload writing sample
- `GET /style/profile` - Get style profile

### Draft Generation
- `POST /generate-drafts/{update_id}` - Generate drafts for all audiences
- `GET /draft/{id}` - Get specific draft

### Review Workflow
- `POST /review/apply-edits/{draft_id}` - Apply edits to draft
- `POST /review/approve/{draft_id}` - Approve draft
- `POST /review/reject/{draft_id}` - Reject draft
- `POST /review/regenerate/{draft_id}` - Regenerate draft

### Sending
- `POST /send/{draft_id}` - Send approved draft

### Dashboard
- `GET /dashboard/{user_id}` - View user's dashboard (HTML)

## Usage Guide

1. **Setup Your Profile**: Upload 2-3 writing samples to establish your style
2. **Submit Weekly Update**: Use the chatbot to submit your raw weekly update
3. **Review Drafts**: Review AI-generated drafts for each audience
4. **Edit if Needed**: Request changes via natural language or edit manually
5. **Approve & Send**: Approve drafts to send emails automatically
6. **Track**: View sent updates on your public dashboard

## Development

Run tests:
```bash
pytest tests/
```

Format code:
```bash
black app/
```

Lint code:
```bash
flake8 app/
```

## License

MIT License
