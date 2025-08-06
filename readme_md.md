# Jira Label Manager

A Streamlit web application for adding labels to multiple Jira issues using JQL queries.

## Features

- 🔍 Search Jira issues using JQL queries
- 🏷️ Add multiple labels to selected issues
- 📊 View search results in a clean table format
- ✅ Real-time progress tracking during updates
- 🔒 Secure credential handling

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- Jira API token (not your password)
- Access to a Jira instance

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd jira-label-manager
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser and navigate to `http://localhost:8501`

### Getting Your Jira API Token

1. Go to your Atlassian Account Settings: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a label (e.g., "Streamlit Jira App")
4. Copy the generated token

## Usage

1. **Configure Connection**: Enter your Jira instance URL, username, and API token in the sidebar
2. **Search Issues**: Enter a JQL query to find the issues you want to update
3. **Review Results**: Check the found issues in the results table
4. **Add Labels**: Enter the labels you want to add (comma-separated)
5. **Confirm**: Review and confirm the changes
6. **Monitor Progress**: Watch real-time updates as labels are added

## JQL Query Examples

```jql
# Find issues assigned to a specific user
assignee = "john.doe@company.com"

# Find issues in a specific project with a certain status
project = "MYPROJECT" AND status = "In Progress"

# Find recently created issues
created >= -7d

# Find issues with specific labels
labels = "bug" OR labels = "urgent"
```

## Security Notes

- API tokens are handled securely and not stored
- All connections use HTTPS
- Credentials are only kept in memory during the session

## Troubleshooting

### Common Issues

1. **Authentication Error**: Verify your username and API token
2. **JQL Syntax Error**: Check your JQL query syntax
3. **Permission Error**: Ensure you have edit permissions on the issues
4. **Network Error**: Check your internet connection and Jira instance URL

### Support

For issues or questions, please contact your system administrator or create an issue in the repository.

## License

This project is licensed under the MIT License.