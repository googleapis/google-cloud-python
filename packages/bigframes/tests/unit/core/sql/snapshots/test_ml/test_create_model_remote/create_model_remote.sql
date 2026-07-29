CREATE MODEL `my_remote_model`
INPUT (prompt STRING)
OUTPUT (content STRING)
REMOTE WITH CONNECTION `my_project.us.my_connection`
OPTIONS(endpoint = 'gemini-pro')
