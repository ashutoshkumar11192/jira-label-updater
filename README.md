# 🏷️ Jira Label Manager - Jupyter Notebook Version

A Jupyter notebook-based tool for adding labels to multiple Jira issues using JQL queries.

## Features

- **Interactive Configuration**: Easy setup with ipywidgets for Jira connection details
- **JQL Query Support**: Use powerful Jira Query Language to find specific issues
- **Batch Label Updates**: Add multiple labels to multiple issues at once
- **Real-time Progress**: Monitor updates with live progress indicators
- **Error Handling**: Comprehensive error reporting for failed operations

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. **Start Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```

2. **Open the notebook**: Navigate to and open `jira_label_manager.ipynb`

3. **Run the setup cells**: Execute the first few cells to install dependencies and import libraries

4. **Configure your Jira connection**:
   - Enter your Jira instance URL (e.g., `https://your-company.atlassian.net/`)
   - Enter your username/email
   - Enter your Jira API token

5. **Search for issues**:
   - Enter a JQL query to find the issues you want to update
   - Click "Search Issues" to retrieve matching issues

6. **Add labels**:
   - Enter comma-separated labels you want to add
   - Click "Add Labels to Issues" to perform the batch update

## Getting a Jira API Token

1. Go to your Jira profile settings
2. Navigate to "Security" > "API tokens"  
3. Click "Create API token"
4. Give it a descriptive name and copy the generated token
5. Use this token in the notebook's API Token field

## JQL Query Examples

```jql
# Find issues assigned to you that are in progress
assignee = currentUser() AND status = "In Progress"

# Find bugs in a specific project
project = "MYPROJECT" AND labels = "bug"

# Find recently created issues
created >= -7d AND assignee in (currentUser())

# Find issues with specific labels and assignees
labels = "co-marketing_forecast" AND assignee in (712020:85faf3c0-4db6-47b1-b5fa-9a619d79d63b)
```

## Differences from Streamlit Version

This Jupyter notebook version provides the same functionality as the original Streamlit app but with these advantages:

- **Local execution**: No need for a Streamlit server
- **Cell-by-cell execution**: Run code incrementally and inspect intermediate results
- **Better debugging**: Easier to troubleshoot issues with step-by-step execution
- **Offline capability**: Works completely offline once dependencies are installed
- **Customization**: Easy to modify and extend with additional functionality

## Troubleshooting

### Common Issues

1. **"ipywidgets not working"**: Make sure you have Jupyter widgets properly installed and enabled:
   ```bash
   pip install ipywidgets
   jupyter nbextension enable --py widgetsnbextension
   ```

2. **"Authentication failed"**: Double-check your API token and ensure it hasn't expired

3. **"JQL query errors"**: Verify your JQL syntax using Jira's built-in JQL editor first

4. **"Connection timeout"**: Check your internet connection and Jira instance URL

### Requirements

- Python 3.7+
- Jupyter Notebook or JupyterLab
- Active internet connection (for Jira API calls)
- Valid Jira account with API token

## Security Notes

- **Never commit API tokens**: Keep your API tokens secure and don't include them in version control
- **Use environment variables**: Consider storing sensitive credentials in environment variables
- **Token permissions**: Ensure your API token has appropriate permissions for the issues you want to modify

## License

This project is provided as-is for educational and productivity purposes.