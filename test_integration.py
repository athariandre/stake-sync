#!/usr/bin/env python3
"""
Integration test example for StakeSync
Run this after setting up the application to test the complete workflow
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_complete_workflow():
    """Test the complete workflow from registration to sending."""
    
    print("🧪 Testing StakeSync Complete Workflow\n")
    
    # Step 1: Register a test user
    print("1️⃣  Registering test user...")
    user_data = {
        "name": "Test User",
        "email": f"test_{int(time.time())}@example.com"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    assert response.status_code == 200, f"Failed to register user: {response.text}"
    user = response.json()
    user_id = user["id"]
    print(f"   ✓ User registered with ID: {user_id}\n")
    
    # Step 2: Upload writing sample
    print("2️⃣  Uploading writing sample...")
    sample_data = {
        "user_id": user_id,
        "content": """
        Dear team,
        
        I'm excited to share our progress this week. We've made significant strides 
        in product development and achieved our quarterly goals. The team has been 
        working diligently, and I'm proud of what we've accomplished together.
        
        Looking forward to next week's milestones.
        
        Best regards,
        Test User
        """
    }
    response = requests.post(f"{BASE_URL}/style/upload", json=sample_data)
    assert response.status_code == 200, f"Failed to upload sample: {response.text}"
    style_info = response.json()
    print(f"   ✓ Style profile created")
    print(f"   Tone: {style_info['style_profile']['tone']}\n")
    
    # Step 3: Create audience groups
    print("3️⃣  Creating audience groups...")
    audiences = {
        "investors": ["investor1@example.com", "investor2@example.com"],
        "employees": ["employee1@example.com", "employee2@example.com"],
        "partners": ["partner1@example.com"]
    }
    
    for group_type, emails in audiences.items():
        audience_data = {
            "user_id": user_id,
            "group_type": group_type,
            "emails": emails
        }
        response = requests.post(f"{BASE_URL}/audience/create", json=audience_data)
        assert response.status_code == 200, f"Failed to create {group_type} group: {response.text}"
        print(f"   ✓ {group_type.capitalize()} group created ({len(emails)} recipients)")
    print()
    
    # Step 4: Submit weekly update
    print("4️⃣  Submitting weekly update...")
    update_data = {
        "user_id": user_id,
        "content": """
        This week was incredibly productive. We launched our new feature to beta users 
        and received overwhelmingly positive feedback. Key metrics:
        - 500 beta signups in 3 days
        - 85% user satisfaction score
        - 30% increase in daily active users
        
        Challenges: Server capacity needed scaling, addressed by DevOps team.
        
        Next week: Full product launch, marketing campaign kickoff, hiring 2 engineers.
        """
    }
    response = requests.post(f"{BASE_URL}/update/submit", json=update_data)
    assert response.status_code == 200, f"Failed to submit update: {response.text}"
    update = response.json()
    update_id = update["id"]
    print(f"   ✓ Update submitted with ID: {update_id}\n")
    
    # Step 5: Generate drafts (this may take a while with real Gemini API)
    print("5️⃣  Generating drafts for all audiences...")
    print("   (This step requires valid GEMINI_KEY in .env)")
    print("   Skipping draft generation in test mode")
    print("   To test with real API, uncomment the following lines:\n")
    
    # Uncomment these lines when you have valid API keys:
    """
    response = requests.post(f"{BASE_URL}/drafts/generate/{update_id}?user_id={user_id}")
    if response.status_code == 200:
        drafts = response.json()
        print(f"   ✓ Drafts generated:")
        for audience, draft in drafts.items():
            print(f"     - {audience.capitalize()}: {len(draft['content'])} characters")
            draft_id = draft['id']
            
            # Step 6: Approve draft
            print(f"\n6️⃣  Approving {audience} draft...")
            response = requests.post(f"{BASE_URL}/review/approve/{draft_id}?user_id={user_id}")
            assert response.status_code == 200
            print(f"   ✓ Draft approved")
            
            # Step 7: Send draft (requires valid SENDGRID_API_KEY)
            # Uncomment when ready to actually send emails:
            # response = requests.post(f"{BASE_URL}/send/{draft_id}?user_id={user_id}")
            # if response.status_code == 200:
            #     send_result = response.json()
            #     print(f"   ✓ Email sent to {send_result['recipients_count']} recipients")
    else:
        print(f"   ✗ Failed to generate drafts: {response.text}")
    """
    
    # Step 8: Check dashboard
    print("\n8️⃣  Dashboard URL:")
    print(f"   http://localhost:8000/dashboard/{user_id}\n")
    
    print("✅ Test workflow completed successfully!")
    print(f"\n📊 Summary:")
    print(f"   User ID: {user_id}")
    print(f"   Update ID: {update_id}")
    print(f"   Audience groups: 3 (investors, employees, partners)")
    print(f"\nNote: To complete the full test with draft generation and email sending,")
    print(f"add valid API keys to .env and uncomment the relevant sections in this script.")

if __name__ == "__main__":
    try:
        # First check if server is running
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ Server is not running. Start it with:")
            print("   uvicorn app.main:app --reload")
            exit(1)
        
        test_complete_workflow()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running:")
        print("   uvicorn app.main:app --reload")
        exit(1)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
