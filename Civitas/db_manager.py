## Importing Packages
import sqlite3
import json
from typing import List, Dict, Any

class CommunityIssueDB:
    def __init__(self,db_name="community_issues.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS community_issues (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    image_path TEXT,
                    issue_type TEXT,
                    severity TEXT,
                    urgency TEXT,
                    location TEXT,
                    safety_concerns TEXT,
                    community_impact TEXT,
                    recommended_actions TEXT,
                    primary_department TEXT,
                    additional_notes TEXT
                )
            ''')
        conn.commit()
        #conn.close()
    
    def store_issue(self,data:Dict[str,Any]) -> None:
        """Stores Issues in the DB"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            safety_concerns = json.dumps(data.get('safety_concerns', []))
            community_impact = json.dumps(data.get('community_impact', []))
            recommended_actions = json.dumps(data.get('recommended_actions', []))

            cursor.execute('''
                INSERT INTO community_issues (
                    image_path, issue_type, severity, urgency, location,
                    safety_concerns, community_impact, recommended_actions,
                    primary_department, additional_notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('image_path'),
                data.get('issue_type'),
                data.get('severity'),
                data.get('urgency'),
                data.get('location_context'),
                safety_concerns,
                community_impact,
                recommended_actions,
                data.get('primary_department'),
                data.get('additional_notes')
            ))

            conn.commit()
            #conn.close()
    
    def get_all_issues(self) -> List[Dict[str,Any]]:
        """Retrieve all issues from the db"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM community_issues')
            columns = [description[0] for description in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                issue_dict = dict(zip(columns, row))
                issue_dict['safety_concerns'] = json.loads(issue_dict['safety_concerns'])
                issue_dict['community_impact'] = json.loads(issue_dict['community_impact'])
                issue_dict['recommended_actions'] = json.loads(issue_dict['recommended_actions'])
                results.append(issue_dict)
            #conn.close()
            return results