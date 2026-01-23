import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestRegressor
import urllib.parse

# 1. CONNECT TO YOUR WAREHOUSE
user = "root"
raw_password = "Siddhesh@24"
password = urllib.parse.quote_plus(raw_password)
engine = create_engine(f"mysql+pymysql://{user}:{password}@localhost/smart_planner")

# 2. THE BIG JOIN (Fetching data into one view)
query = """
SELECT 
    t.story_points, 
    t.actual_hours, 
    d.experience_level, 
    s.team_load_percentage 
FROM historical_tasks t
JOIN developers d ON t.dev_id = d.dev_id
JOIN sprint_context s ON t.sprint_id = s.sprint_id;
"""
df = pd.read_sql(query, con=engine)
print("✅ Data fetched and joined successfully!")

# 3. ENCODING (Convert words to numbers)
# Mapping: Junior=1, Mid=2, Senior=3
level_map = {'Junior': 1, 'Mid': 2, 'Senior': 3}
df['experience_level'] = df['experience_level'].map(level_map)

# 4. SPLIT DATA INTO INPUTS (X) AND OUTPUT (y)
X = df[['story_points', 'experience_level', 'team_load_percentage']] # Inputs
y = df['actual_hours'] # The answer we want to predict

# 5. INITIALIZE THE BRAIN (Decision Tree)
model = RandomForestRegressor(n_estimators=100, random_state=42)

# 6. TRAIN THE BRAIN (This is the learning part)
model.fit(X, y)
print("🧠 The AI Brain is now trained!")

# 7. TEST THE BRAIN
# Let's pretend a new task comes in: 
# 8 Story Points, Junior Dev (1), Team Load 110%
print(f"Junior (1): {model.predict([[5, 1, 100]])[0]:.2f}")
print(f"Mid    (2): {model.predict([[5, 2, 100]])[0]:.2f}")
print(f"Senior (3): {model.predict([[5, 3, 100]])[0]:.2f}")