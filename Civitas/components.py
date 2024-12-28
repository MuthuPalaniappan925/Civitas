## Import Packages
import streamlit as st
from datetime import datetime
from typing import Dict, Any, List
from analysis_service import IssueAnalyzer
from db_manager import CommunityIssueDB

class IssueUploader:
    @staticmethod
    def render(db:CommunityIssueDB):
        col1,col2 = st.columns(2)

        with col1:
            uploaded_file = st.file_uploader(
                "Upload Image",
                type=["jpg","jpeg","png"]
            )
            if uploaded_file:
                st.image(
                    uploaded_file,
                    caption="Uploaded Image",
                    use_column_width=True
                )
        
        with col2:
            description = st.text_area(
                "What is the Issue ?"
            )
        
            if st.button("Submit Issue"):
                if uploaded_file and description:
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    try:
                        analyzer = IssueAnalyzer()
                        analysis = analyzer.analyze_community_issue(temp_path, description)
                        formatted_result = analyzer.format_analysis_response(analysis)
                        formatted_result['image_path'] = temp_path

                        db.store_issue(formatted_result)
                        st.success("Issue analyzed and stored successfully!")
                        st.json(formatted_result)

                    except Exception as e:
                        st.error(
                            f"Method Failed: {str(e)}"
                        )

class IssueDashboard:
    @staticmethod
    def render(db:CommunityIssueDB):
        issues = db.get_all_issues()
        st.info("Getting Issues")
        if issues:
            st.success("Retrival Done")
        else:
            st.error("Retrival Failed")

        col1, col2, col3 = st.columns(3)
        with col1:
            departments = list(set(issue['primary_department'] for issue in issues))
            dept_filter = st.selectbox("Filter by Department", ["All"] + departments)
        
        with col2:
            severity_filter = st.selectbox("Filter by Severity", ["All", "HIGH", "MEDIUM", "LOW"])
        
        with col3:
            urgency_filter = st.selectbox("Filter by Urgency", ["All", "IMMEDIATE", "SOON", "ROUTINE"])
        
        filtered_issues = IssueDashboard._apply_filters(issues, dept_filter, severity_filter, urgency_filter)
        IssueDashboard._display_issues(filtered_issues)

    @staticmethod
    def _apply_filters(issues: List[Dict[str, Any]], dept_filter: str, severity_filter: str, urgency_filter: str) -> List[Dict[str, Any]]:
        filtered_issues = issues
        if dept_filter != "All":
            filtered_issues = [i for i in filtered_issues if i['primary_department'] == dept_filter]
        if severity_filter != "All":
            filtered_issues = [i for i in filtered_issues if i['severity'] == severity_filter]
        if urgency_filter != "All":
            filtered_issues = [i for i in filtered_issues if i['urgency'] == urgency_filter]
        return filtered_issues

    @staticmethod
    def _display_issues(issues: List[Dict[str, Any]]):
        for issue in issues:
            with st.expander(f"{issue['issue_type']}"):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    if issue['image_path']:
                        try:
                            st.image(issue['image_path'], use_column_width=True)
                        except:
                            st.warning("Image not available")
                
                with col2:
                    st.write(f"**Location:** {issue['location']}")
                    st.write(f"**Severity:** {issue['severity']}")
                    st.write(f"**Urgency:** {issue['urgency']}")
                    st.write("**Safety Concerns:**")
                    for concern in issue['safety_concerns']:
                        st.write(f"- {concern}")
                    st.write("**Recommended Actions:**")
                    for action in issue['recommended_actions']:
                        st.write(f"- {action['task']} ({action['priority']} priority)")