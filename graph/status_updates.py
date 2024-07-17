import requests

def send_data_to_server(data):
    print("Sending data to server:", data)
    response = requests.post('http://127.0.0.1:5000/api/processed', json=data)
    if response.status_code == 200:
        print("Processed data sent successfully:", response.json())
    else:
        print("Error sending processed data:", response.status_code, response.text)

def update_server_with_status(phase, message):
    data = {
        "phase": phase,
        "status": message
    }
    send_data_to_server(data)

def update_server_during_planner():
    update_server_with_status("planner", "Planner agent is working.")

def update_server_during_research():
    update_server_with_status("research", "Task passed to Researcher agent.")

def update_server_during_grader():
    update_server_with_status("grader", "Grader agent is evaluating the results.")

def update_server_during_generator():
    update_server_with_status("generator", "Generator agent is generating content.")

def update_server_during_reviewer():
    update_server_with_status("reviewer", "Reviewer agent is reviewing the content.")
