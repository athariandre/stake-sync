# User Guide - StakeSync

## Getting Started

Welcome to StakeSync! This guide will walk you through using the system to automate your weekly business updates.

## First-Time Setup

### 1. Create Your Account

1. Open the chatbot interface at `http://localhost:8000/static/chatbot.html`
2. Enter your name and email
3. Click "Continue"
4. **Save your User ID** - you'll need this to log in again

### 2. Upload Writing Samples

To help StakeSync match your writing style:

1. Navigate to the **Style Samples** tab
2. Paste 2-3 samples of your writing (emails, updates, blog posts, etc.)
3. Click "Upload Sample" for each
4. The system will analyze your tone, sentence length, and common phrases

**Tip:** Use diverse samples that represent how you communicate with different audiences.

### 3. Set Up Your Audiences

1. Go to the **Manage Audiences** tab
2. Enter email addresses for each audience type:
   - **Investors**: Your investors and board members
   - **Employees**: Your team members and staff
   - **Partners**: Business partners and collaborators
3. Click "Save" for each audience group

Format: One email per line or comma-separated

## Weekly Workflow

### Step 1: Submit Your Update

1. Navigate to the **Submit Update** tab
2. Write your raw weekly update - be as detailed as you like
3. Include:
   - Key achievements this week
   - Challenges faced
   - Important metrics
   - Upcoming plans
4. Click "Submit Update"

The system will automatically generate three tailored drafts (one for each audience).

### Step 2: Review Drafts

1. Go to the **Review Drafts** tab
2. Click on an update to view its drafts
3. Each draft is customized for its audience:
   - **Investors**: Upbeat, confident, metrics-focused
   - **Employees**: Supportive, motivating, team-focused
   - **Partners**: Honest, collaborative, strategic

### Step 3: Refine (if needed)

For each draft, you can:

- **Approve**: Accept the draft as-is
- **Request Edit**: Ask for changes in natural language
  - Example: "Make it more concise" or "Add more detail about the product launch"
- **Regenerate**: Create a completely new version
- **Manual Edit**: (coming soon) Edit the text directly

### Step 4: Send Updates

1. Once you approve a draft, you'll be prompted to send it
2. Confirm to send emails to that audience
3. The update will automatically appear on your public dashboard

### Step 5: Track on Dashboard

View your sent updates at: `http://localhost:8000/dashboard/{your_user_id}`

This page shows:
- All sent updates
- Which audiences received each update
- 2-3 sentence summaries
- Timestamps

Share this URL with anyone who should have access to your updates.

## Tips for Best Results

### Writing Your Raw Update

✅ **Do:**
- Be detailed and comprehensive
- Include specific numbers and metrics
- Mention both wins and challenges
- Write in your natural voice

❌ **Don't:**
- Try to write for a specific audience
- Polish or edit too much
- Worry about formatting
- Leave out important context

### Style Samples

- Upload emails you've actually sent
- Use recent writing (within last 6 months)
- Include variety: formal reports, casual emails, presentations
- Aim for at least 200 words per sample

### Editing Drafts

When requesting edits, be specific:
- ✅ "Add more detail about our Q3 revenue growth"
- ✅ "Make the tone more casual"
- ✅ "Shorten to 3 paragraphs"
- ❌ "Make it better"
- ❌ "Fix it"

## Troubleshooting

### "Draft generation failed"
- Check that you've uploaded at least one writing sample
- Verify your GEMINI_KEY is set correctly in `.env`
- Try regenerating the draft

### "Failed to send email"
- Verify your SENDGRID_API_KEY is correct
- Check that you've added recipients for that audience
- Ensure email addresses are valid

### "User not found"
- Double-check your user ID
- If you lost your ID, create a new account

## Advanced Features

### Memory System

StakeSync remembers your last 4-6 weeks of updates to maintain context and consistency across communications.

### Audience Modifiers

Each audience has built-in tone modifiers:
- **Investors**: Confident, metric-driven
- **Employees**: Supportive, team-oriented
- **Partners**: Collaborative, strategic

You can customize these by uploading different style samples for different contexts.

## API Access

For developers or automation, all features are available via REST API:

- API documentation: `http://localhost:8000/docs`
- Interactive testing: `http://localhost:8000/redoc`

## Support

For issues or questions:
1. Check the README.md for technical setup
2. Review error messages in the browser console (F12)
3. Open an issue on GitHub

## Privacy & Security

- Your data is stored locally in SQLite
- Writing samples are never shared externally
- Only you can access your drafts before sending
- Dashboard is unlisted (not indexed by search engines)
- No tracking or analytics

## Best Practices

1. **Submit weekly**: Consistency helps the AI understand your patterns
2. **Review carefully**: Always read drafts before approving
3. **Update style samples**: Upload new samples every 3-6 months
4. **Maintain audience lists**: Keep email lists current
5. **Archive important updates**: Download or screenshot sent updates

## Example Workflow

**Monday morning:**
1. Spend 10 minutes writing raw update
2. Submit through chatbot
3. Review three generated drafts (5 minutes)
4. Request edits if needed
5. Approve and send

**Total time:** 15-20 minutes vs. 1-2 hours writing separate updates manually

## Next Steps

Ready to send your first update? Start with the "Submit Update" tab!

Need help? Check the troubleshooting section or review the README.md for technical details.
