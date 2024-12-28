##Importing Packages
import streamlit as st
from components import IssueUploader, IssueDashboard
from db_manager import CommunityIssueDB

st.set_page_config(page_title="Civitas", layout="wide")

def main():
    st.title("Civitas - A hub for resolving community challenges :)")

    if 'issues_db' not in st.session_state:
        st.session_state.issues_db = CommunityIssueDB()
    
    tab1, tab2 = st.tabs(["Report Issue", "View Issues"])
    
    with tab1:
        IssueUploader.render(st.session_state.issues_db)
    
    with tab2:
        st.info(
            "Dashboard Coming Soon"
        )

if __name__ == "__main__":
    main()