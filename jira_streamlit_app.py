import streamlit as st
import base64
import requests
import pandas as pd
from typing import List, Tuple

# Page configuration
st.set_page_config(
    page_title="Jira Label Manager",
    page_icon="🏷️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #0052CC;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def find_issue_keys(jira_instance: str, username: str, api_token: str, jql_query: str) -> Tuple[List[str], str]:
    """
    Finds all issue keys that match a JQL query.
    Returns tuple of (issue_keys, error_message)
    """
    search_url = f"{jira_instance.rstrip('/')}/rest/api/2/search"
    credentials = f"{username}:{api_token}"
    base64_auth = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    
    headers = {
        "Authorization": f"Basic {base64_auth}",
        "Content-Type": "application/json"
    }
    
    issue_keys = []
    start_at = 0
    
    try:
        while True:
            payload = {
                "jql": jql_query,
                "fields": ["key", "summary"],
                "startAt": start_at,
                "maxResults": 100
            }
            
            response = requests.post(search_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            retrieved_issues = data.get('issues', [])
            if not retrieved_issues:
                break
            
            for issue in retrieved_issues:
                issue_keys.append({
                    'key': issue['key'],
                    'summary': issue['fields'].get('summary', 'No summary available')
                })
            
            start_at += len(retrieved_issues)
            
            # Safety check to prevent infinite loops
            if start_at > 10000:
                return [], "Too many results (>10000). Please refine your JQL query."
                
    except requests.exceptions.RequestException as e:
        return [], f"Error searching for issues: {str(e)}"
    except Exception as e:
        return [], f"Unexpected error: {str(e)}"
        
    return issue_keys, ""

def add_labels_to_issue(jira_instance: str, username: str, api_token: str, issue_key: str, labels_to_add: List[str]) -> Tuple[bool, str]:
    """
    Adds labels to a specific Jira issue.
    Returns tuple of (success, error_message)
    """
    update_url = f"{jira_instance.rstrip('/')}/rest/api/2/issue/{issue_key}"
    credentials = f"{username}:{api_token}"
    base64_auth = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    
    headers = {
        "Authorization": f"Basic {base64_auth}",
        "Content-Type": "application/json"
    }
    
    update_payload = {
        "update": {
            "labels": [{"add": label} for label in labels_to_add]
        }
    }
    
    try:
        response = requests.put(update_url, headers=headers, json=update_payload, timeout=30)
        if response.status_code == 204:
            return True, ""
        else:
            return False, f"Status: {response.status_code}, Response: {response.text}"
    except requests.exceptions.RequestException as e:
        return False, f"Request error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def main():
    # Header
    st.markdown('<h1 class="main-header">🏷️ Jira Label Manager</h1>', unsafe_allow_html=True)
    st.markdown("Add labels to multiple Jira issues using JQL queries")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Jira instance URL
        jira_instance = st.text_input(
            "Jira Instance URL",
            value="https://criteo.atlassian.net/",
            help="Your Jira instance URL (e.g., https://your-company.atlassian.net/)"
        )
        
        # Username
        username = st.text_input(
            "Username",
            help="Your Jira username or email"
        )
        
        # API Token
        api_token = st.text_input(
            "API Token",
            type="password",
            help="Your Jira API token (not your password)"
        )
        
        # Validation
        config_valid = all([jira_instance, username, api_token])
        
        if config_valid:
            st.success("✅ Configuration complete")
        else:
            st.warning("⚠️ Please fill in all configuration fields")
    
    # Main content area
    if not config_valid:
        st.info("👈 Please configure your Jira connection in the sidebar to get started.")
        return
    
    # JQL Query input
    st.header("1. Define Your Search Query")
    
    # Provide some example JQL queries
    with st.expander("📖 JQL Query Examples"):
        st.code('assignee = "john.doe@company.com" AND status = "In Progress"')
        st.code('project = "MYPROJECT" AND labels = "bug"')
        st.code('created >= -7d AND assignee in (currentUser())')
        st.code('labels = "co-marketing_forecast" AND assignee in (712020:85faf3c0-4db6-47b1-b5fa-9a619d79d63b)')
    
    jql_query = st.text_area(
        "JQL Query",
        height=100,
        placeholder="Enter your JQL query here...",
        help="Use JQL (Jira Query Language) to find the issues you want to update"
    )
    
    # Search button
    if st.button("🔍 Search Issues", type="primary", disabled=not jql_query.strip()):
        with st.spinner("Searching for issues..."):
            issues, error = find_issue_keys(jira_instance, username, api_token, jql_query)
            
            if error:
                st.markdown(f'<div class="error-box">❌ {error}</div>', unsafe_allow_html=True)
                st.session_state.issues = []
            else:
                st.session_state.issues = issues
                if issues:
                    st.markdown(f'<div class="success-box">✅ Found {len(issues)} issues</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="warning-box">⚠️ No issues found matching your query</div>', unsafe_allow_html=True)
    
    # Display found issues
    if hasattr(st.session_state, 'issues') and st.session_state.issues:
        st.header("2. Found Issues")
        
        # Create a DataFrame for better display
        df = pd.DataFrame(st.session_state.issues)
        st.dataframe(df, use_container_width=True)
        
        # Labels input
        st.header("3. Add Labels")
        labels_input = st.text_input(
            "Labels to Add",
            placeholder="label1, label2, label3",
            help="Enter labels separated by commas"
        )
        
        if labels_input:
            labels_to_add = [label.strip() for label in labels_input.split(',') if label.strip()]
            
            if labels_to_add:
                st.write(f"**Labels to be added:** {', '.join(labels_to_add)}")
                
                # Confirmation
                st.header("4. Confirmation")
                st.markdown(f'<div class="warning-box">⚠️ You are about to add the labels <strong>{", ".join(labels_to_add)}</strong> to <strong>{len(st.session_state.issues)} issues</strong>.</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    if st.button("✅ Confirm and Update", type="primary"):
                        st.session_state.confirm_update = True
                        st.session_state.labels_to_add = labels_to_add
                
                with col2:
                    if st.button("❌ Cancel"):
                        st.session_state.confirm_update = False
                        st.info("Operation cancelled.")
                
                # Execute updates
                if hasattr(st.session_state, 'confirm_update') and st.session_state.confirm_update:
                    st.header("5. Update Progress")
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    results_container = st.container()
                    
                    success_count = 0
                    failure_count = 0
                    
                    for i, issue in enumerate(st.session_state.issues):
                        issue_key = issue['key']
                        status_text.text(f"Updating {issue_key}...")
                        
                        success, error = add_labels_to_issue(
                            jira_instance, username, api_token, 
                            issue_key, st.session_state.labels_to_add
                        )
                        
                        if success:
                            success_count += 1
                            results_container.success(f"✅ {issue_key}: Updated successfully")
                        else:
                            failure_count += 1
                            results_container.error(f"❌ {issue_key}: {error}")
                        
                        progress_bar.progress((i + 1) / len(st.session_state.issues))
                    
                    status_text.text("Update complete!")
                    
                    # Final summary
                    st.header("6. Summary")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("✅ Successfully Updated", success_count)
                    
                    with col2:
                        st.metric("❌ Failed to Update", failure_count)
                    
                    # Reset confirmation state
                    st.session_state.confirm_update = False

if __name__ == "__main__":
    # Initialize session state
    if 'issues' not in st.session_state:
        st.session_state.issues = []
    
    main()