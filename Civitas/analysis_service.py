## Importing Packages
from jsonschema import ValidationError
import ollama # type: ignore
import base64
import json
from typing import List,Dict,Optional
from schemas import CommunityIssueAnalysis

class IssueAnalyzer:
    @staticmethod
    def analyze_community_issue(image_path: str, user_description: Optional[str] = None) -> CommunityIssueAnalysis:
        """
        Analyzes a community issue using vision AI and returns structured, validated results.
        """
        # Convert image to base64
        with open(image_path, "rb") as image_file:
            img_str = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Create the analysis prompt with updated JSON structure matching Pydantic model
        base_prompt = """Analyze this community issue image and provide a detailed assessment.
        Focus on identifying the problem, its severity, and necessary actions.
        Only JSON format should be the output.
        
        Required analysis points:
        1. Issue Type: What kind of problem is shown
        2. Severity: Rate as HIGH/MEDIUM/LOW
        3. Urgency: IMMEDIATE/SOON/ROUTINE
        4. Location: Describe where this issue is
        5. Safety: List any safety risks
        6. Impact: How this affects the community
        7. Actions: What needs to be done, including responsible departments
        8. Primary Department: Main department responsible
        
        Provide your analysis in this exact JSON format:
        {
            "issue_type": "string",
            "severity": "HIGH|MEDIUM|LOW",
            "urgency": "IMMEDIATE|SOON|ROUTINE",
            "location_context": "string",
            "safety_concerns": ["string"],
            "community_impact": ["string"],
            "recommended_actions": [
                {
                    "action": "string",
                    "priority": "HIGH|MEDIUM|LOW",
                    "timeframe": "string",
                    "departments": ["DEPARTMENT_NAME"]
                }
            ],
            "primary_department": "DEPARTMENT_NAME",
            "additional_notes": "string"
        }

        Valid department names are: PUBLIC_WORKS, SANITATION, PARKS_REC, TRANSPORTATION, 
        PUBLIC_SAFETY, CODE_ENFORCEMENT, UTILITIES, ENVIRONMENTAL, HEALTH, ANIMAL_CONTROL

        Apart from this no extra text should be provided in the response."""

        if user_description:
            base_prompt += f"\n\nResident's description: {user_description}\nVerify and incorporate this information in your analysis."

        try:
            print("hi")
            # Get analysis from vision model
            response = ollama.chat(
                model='llama3.2-vision',
                messages=[
                    {
                        'role': 'user',
                        'content': base_prompt,
                        'images': [img_str]
                    }
                ]
            )
            
            # Extract JSON from response
            content = response['message']['content']
            
            # Handle potential JSON formatting in markdown
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].strip()
                
            # Parse and validate with Pydantic
            analysis_dict = json.loads(content)
            
            # Ensure departments field exists in recommended_actions
            for action in analysis_dict.get('recommended_actions', []):
                if 'departments' not in action:
                    action['departments'] = [analysis_dict['primary_department']]
                    
            validated_analysis = CommunityIssueAnalysis(**analysis_dict)
            return validated_analysis
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse AI response as JSON: {str(e)}")
        except ValidationError as e:
            raise ValueError(f"Validation error: {str(e)}")
        except Exception as e:
            raise Exception(f"Analysis failed: {str(e)}")
    
    @staticmethod
    def format_analysis_response(analysis: CommunityIssueAnalysis) -> Dict:
        """Formats the analysis results into a clean structure."""
        return {
            "issue_summary": {
                "type": analysis.issue_type,
                "severity": analysis.severity,
                "urgency": analysis.urgency,
                "location": analysis.location_context
            },
            "safety_assessment": {
                "concerns": analysis.safety_concerns,
                "community_impact": analysis.community_impact
            },
            "department": {
                "primary": analysis.primary_department
            },
            "action_plan": {
                "actions": [
                    {
                        "task": action.action,
                        "priority": action.priority,
                        "when": action.timeframe,
                        "departments": action.departments
                    }
                    for action in analysis.recommended_actions
                ]
            },
            "notes": analysis.additional_notes
        }