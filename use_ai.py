import joblib
import pandas as pd

# 1. Load the "Brains"
time_model = joblib.load('time_model.pkl')
risk_model = joblib.load('risk_model.pkl')

print("🏢 AI Project Consultant - Dual Mode")

# 2. Get User Inputs
pts = int(input("\nStory Points: "))
load = int(input("Team Load %: "))
deadline = float(input("Your Max Allowed Hours (Deadline): "))

levels = {1: "Junior", 2: "Mid", 3: "Senior"}
analysis_results = []

print("\n--- 🔍 Detailed Analysis ---")

for val, name in levels.items():
    # Use DataFrame to keep feature names consistent and avoid warnings
    feat = pd.DataFrame([[pts, val, load]], 
                        columns=['story_points', 'experience_level', 'team_load_percentage'])
    
    est_time = time_model.predict(feat)[0]
    risk_prob = risk_model.predict_proba(feat)[0][1] * 100
    
    # AI Standard: Low failure probability (e.g., under 30%)
    ai_status = "✅ RELIABLE" if risk_prob < 30 else "⚠️ UNRELIABLE"
    
    # User Standard: Under the input deadline
    user_status = "✅ ON-TIME" if est_time <= deadline else "❌ TOO SLOW"
    
    analysis_results.append({
        "level_val": val,
        "name": name,
        "time": est_time,
        "risk": risk_prob,
        "ai_status": ai_status,
        "user_status": user_status
    })
    
    print(f"{name:7} | Time: {est_time:4.1f}h | Risk: {risk_prob:4.1f}% | AI: {ai_status:12} | User: {user_status}")

print("\n" + "="*50)

# --- 🎯 RECOMMENDATION 1: AI STANDARDS ---
# Priority: Lowest Risk, then Highest Experience
ai_safe_list = [opt for opt in analysis_results if opt['ai_status'] == "✅ RELIABLE"]
print("🤖 [AI STANDARD RECOMMENDATION]")
if ai_safe_list:
    # Sort by risk (lowest first)
    best_ai = sorted(ai_safe_list, key=lambda x: x['risk'])[0]
    print(f"Winner: **{best_ai['name']}**")
    print(f"Reason: Historically, this level has the highest success rate for this task type.")
else:
    print("Winner: NONE")
    print("Reason: AI predicts all levels have a high historical failure rate for this task.")

print("-" * 30)

# --- 🎯 RECOMMENDATION 2: USER DEADLINE ---
# Priority: Most Efficient (Junior First) that meets the deadline
user_valid_list = [opt for opt in analysis_results if opt['user_status'] == "✅ ON-TIME"]
print("⏱️ [USER DEADLINE RECOMMENDATION]")
if user_valid_list:
    # Sort by level (Junior first) to save resources
    best_user = sorted(user_valid_list, key=lambda x: x['level_val'])[0]
    print(f"Winner: **{best_user['name']}**")
    print(f"Reason: They meet your {deadline}h deadline and save your senior resources.")
else:
    print("Winner: NONE")
    print("Reason: No developer is predicted to finish within your {deadline}h deadline.")

print("="*50)