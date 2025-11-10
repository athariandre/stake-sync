# Getting Started with StakeSync

Welcome! This guide will get you up and running with StakeSync in 15 minutes.

## What You'll Build

A complete weekly business update automation system that:
- Takes your raw weekly update (one submission)
- Generates three tailored messages (investors, employees, partners)
- Allows you to review and edit with natural language
- Sends emails automatically to your audiences
- Publishes updates to a live dashboard

## Prerequisites

Before starting, ensure you have:

1. **Python 3.9 or higher**
   ```bash
   python3 --version  # Should show 3.9 or higher
   ```

2. **Google Gemini API Key**
   - Get one free at: https://ai.google.dev/
   - Click "Get API Key" → "Create API key in new project"
   - Copy your key

3. **SendGrid API Key**
   - Sign up free at: https://sendgrid.com/
   - Navigate to Settings → API Keys → Create API Key
   - Copy your key

## Quick Setup (15 minutes)

### Step 1: Clone and Setup (2 minutes)

```bash
# Clone the repository
git clone https://github.com/athariandre/stake-sync.git
cd stake-sync

# Run automated setup
chmod +x setup.sh
./setup.sh
```

This will:
- Create a Python virtual environment
- Install all dependencies
- Create a .env file template
- Initialize the database

### Step 2: Configure API Keys (2 minutes)

```bash
# Edit the .env file
nano .env  # or use your preferred editor
```

Update these three lines:
```env
GEMINI_KEY=your_actual_gemini_api_key_here
SENDGRID_API_KEY=your_actual_sendgrid_api_key_here
SENDGRID_FROM_EMAIL=noreply@yourdomain.com
```

Save and exit (Ctrl+X, then Y, then Enter in nano).

### Step 3: Start the Server (1 minute)

```bash
# Activate virtual environment
source venv/bin/activate

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Step 4: Open the Chatbot (instant)

Open your browser and go to:
```
http://localhost:8000/static/chatbot.html
```

## First-Time User Setup (10 minutes)

### 1. Create Your Account (1 minute)

On the chatbot page:
1. Leave "User ID" blank
2. Enter your name
3. Enter your email
4. Click "Continue"

**Important:** Save your User ID! You'll need it to log in again.

### 2. Upload Writing Samples (3 minutes)

Click the "Style Samples" tab:
1. Paste a sample of your writing (email, update, blog post)
2. Click "Upload Sample"
3. Repeat 2-3 times with different samples

The system will analyze your:
- Writing tone (formal, casual, enthusiastic, etc.)
- Sentence length preferences
- Common phrases you use

### 3. Set Up Audiences (3 minutes)

Click the "Manage Audiences" tab:

**Investors:**
```
investor1@example.com
investor2@example.com
```

**Employees:**
```
employee1@example.com
employee2@example.com
```

**Partners:**
```
partner1@example.com
```

Click "Save" for each group.

### 4. Submit Your First Update (3 minutes)

Click the "Submit Update" tab:

Paste your raw weekly update:
```
This week we launched our beta feature to 100 users.
Key metrics: 85% satisfaction, 30% increase in engagement.
Challenge: Server scaling issues, resolved by DevOps.
Next week: Full launch, marketing campaign, hiring 2 engineers.
```

Click "Submit Update"

The system will automatically:
- Generate three drafts (takes 15-30 seconds)
- Show them in the "Review Drafts" tab

### 5. Review and Send (3 minutes)

Click "Review Drafts" tab:

For each draft:
1. **Read** the generated message
2. **Choose**:
   - ✅ **Approve** if it looks good
   - 🔄 **Regenerate** for a new version
   - ✏️ **Request Edit** (e.g., "Make it shorter")
3. **Send** when approved

## Verify Everything Works

### Check Your Dashboard

Go to: `http://localhost:8000/dashboard/{your_user_id}`

You should see:
- Your sent updates
- Audience badges (Investors, Employees, Partners)
- Auto-generated summaries
- Timestamps

### Check Your Email

If you used real email addresses, check that the emails were received.

## Troubleshooting

### "Failed to generate drafts"

**Cause:** Invalid or missing GEMINI_KEY

**Fix:**
1. Check .env file has your actual API key
2. Verify the key works at: https://aistudio.google.com/
3. Restart the server

### "Failed to send email"

**Cause:** Invalid SENDGRID_API_KEY or no recipients

**Fix:**
1. Verify SendGrid API key in .env
2. Check that you saved audience groups
3. Test SendGrid key at: https://app.sendgrid.com/settings/api_keys

### "User not found"

**Cause:** Wrong user ID or database reset

**Fix:**
1. Double-check your user ID
2. Create a new account if needed
3. Save the new user ID

### Server won't start

**Cause:** Port 8000 already in use

**Fix:**
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001
# Then access: http://localhost:8001/static/chatbot.html
```

### Dependencies won't install

**Cause:** Network issues or Python version

**Fix:**
```bash
# Try with explicit timeout
pip install --timeout=300 -r requirements.txt

# Or install in batches
pip install fastapi uvicorn sqlalchemy pydantic
pip install google-genai sendgrid python-dotenv
```

## Daily Workflow

Once set up, here's your weekly routine:

**Monday morning (15 minutes):**

1. Open chatbot
2. Write raw update (5 min)
3. Submit
4. Review 3 drafts (5 min)
5. Request edits if needed
6. Approve and send (5 min)

**Total:** 15 minutes vs. 60-120 minutes writing manually

## Next Steps

- **Learn More:** Read [USER_GUIDE.md](USER_GUIDE.md) for advanced features
- **API Access:** Check [API_DOCS.md](API_DOCS.md) for automation
- **Deploy:** See [DEPLOYMENT.md](DEPLOYMENT.md) for production setup

## Tips for Best Results

### Writing Your Raw Update

✅ **Do:**
- Include specific metrics
- Mention both wins and challenges
- Write in your natural voice
- Be detailed

❌ **Don't:**
- Write for a specific audience
- Polish too much
- Worry about formatting

### Better Drafts

- Upload quality writing samples
- Use 3+ diverse samples
- Update samples every 3-6 months
- Be specific with edit requests

### Natural Language Edits

Good examples:
- "Make it 30% shorter"
- "Add more metrics"
- "Use a more casual tone"
- "Focus on the product launch"

## Support

**Problems?**
1. Check this guide
2. Review [README.md](README.md)
3. Check console for errors (F12 in browser)
4. Open an issue on GitHub

## Success! 🎉

You're now ready to automate your weekly updates!

**Your time savings:**
- Setup: 15 minutes (one-time)
- Weekly: 15 minutes vs. 1-2 hours manual
- **Saved per week: 45-105 minutes**

---

Questions? Check the [USER_GUIDE.md](USER_GUIDE.md) or open an issue.
