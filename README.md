# Stake Sync - Weekly Business Update Automation

A service that helps business owners submit weekly updates and automatically produces tailored written messages for multiple audiences (investors, employees, partners).

## 🎯 Overview

StakeSync eliminates the time-consuming process of writing separate weekly updates for different audiences. Submit one raw update, and the system automatically:

1. **Analyzes your writing style** from uploaded samples
2. **Generates three tailored drafts** for investors, employees, and partners
3. **Allows natural language editing** ("make it more concise", "add metrics")
4. **Sends emails** to your audience lists via SendGrid
5. **Publishes updates** to a live dashboard
6. **Maintains contextual memory** of past updates for consistency

**Time savings:** 15-20 minutes vs. 1-2 hours writing manually

## ✨ Features

- 📝 **Raw Input Collection**: Simple chatbot interface for collecting weekly updates
- 🎨 **Style Adaptation**: Analyzes writing samples to match your communication style
- 🤖 **AI Draft Generation**: Generates tailored drafts for investors, employees, and partners using Google Gemini
- ✏️ **Review & Edit Workflow**: Simple review loop with natural language editing
- 📧 **Email Distribution**: Automated sending via SendGrid
- 📊 **Live Dashboard**: Public tracking board showing sent updates
- 🧠 **Agent Memory**: Maintains 4-6 weeks of contextual history for consistent messaging

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Google Gemini API key ([Get one here](https://ai.google.dev/))
- SendGrid API key ([Get one here](https://sendgrid.com/))

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/athariandre/stake-sync.git
cd stake-sync
```

2. **Run the setup script:**
```bash
./setup.sh
```

3. **Configure your API keys:**
```bash
# Edit .env file
nano .env

# Add your keys:
GEMINI_KEY=your_gemini_api_key_here
SENDGRID_API_KEY=your_sendgrid_api_key_here
SENDGRID_FROM_EMAIL=noreply@yourdomain.com
```

4. **Start the server:**
```bash
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. **Open the chatbot:**
```
http://localhost:8000/static/chatbot.html
```

## 📖 Documentation

- **[User Guide](USER_GUIDE.md)** - Complete guide for business owners
- **[API Documentation](API_DOCS.md)** - REST API reference
- **[Deployment Guide](DEPLOYMENT.md)** - Production deployment instructions

## 🏗️ Architecture

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

## 🔐 Security

- ✅ **CodeQL Scan**: No vulnerabilities detected
- ✅ **Input Validation**: Pydantic models validate all inputs
- ✅ **SQL Injection Protection**: SQLAlchemy ORM
- ✅ **Environment Variables**: Secrets not in code
- ⚠️ **Authentication**: Basic implementation (enhance for production)

**Security Summary**: The MVP has been scanned with CodeQL and shows no security vulnerabilities. For production use, implement JWT-based authentication, rate limiting, HTTPS/TLS, input sanitization, and CORS policy restrictions.

## 🧪 Testing

### Run Syntax Validation
```bash
python test_syntax.py
```

### Run Integration Test
```bash
# Start the server first
uvicorn app.main:app --reload

# In another terminal
python test_integration.py
```

## 🤝 Contributing

Contributions are welcome! Please fork the repository, create a feature branch, make your changes, add tests, and submit a pull request.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/athariandre/stake-sync/issues)
- **Documentation**: See docs in this repository

## 🗺️ Roadmap

### MVP (Current)
- ✅ Core functionality
- ✅ Simple chatbot UI
- ✅ Three audience support
- ✅ Basic style analysis

### Future Enhancements
- [ ] Voice input support
- [ ] Advanced style fine-tuning
- [ ] Scheduled sending
- [ ] Email reminders
- [ ] Analytics dashboard
- [ ] Multi-language support
- [ ] Slack/Teams integration
- [ ] Mobile app

---

Built with ❤️ for business owners who want to spend less time writing and more time building.
