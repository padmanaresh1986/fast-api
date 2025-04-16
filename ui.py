import streamlit as st
import requests

# Base URL of the FastAPI backend
BASE_URL = "http://127.0.0.1:8000"

# Title of the app
st.title("Task Management App")

# Sidebar for navigation
st.sidebar.header("Navigation")
option = st.sidebar.selectbox(
    "Choose an action",
    ["Create Task", "View All Tasks", "View Specific Task", "Update Task", "Delete Task"]
)

# Function to handle API requests
def api_request(method, endpoint, data=None, params=None):
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"Error: {e.response.text}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Create Task
if option == "Create Task":
    st.header("Create a New Task")
    title = st.text_input("Title")
    description = st.text_area("Description")
    status = st.selectbox("Status", ["pending", "in_progress", "completed"])
    if st.button("Create Task"):
        if title and description:
            task_data = {"title": title, "description": description, "status": status}
            result = api_request("POST", "/tasks", data=task_data)
            if result:
                st.success("Task created successfully!")
                st.json(result)
        else:
            st.error("Please fill in all fields.")

# View All Tasks
elif option == "View All Tasks":
    st.header("All Tasks")
    tasks = api_request("GET", "/tasks")
    if tasks:
        st.table(tasks)

# View Specific Task
elif option == "View Specific Task":
    st.header("View a Specific Task")
    task_id = st.text_input("Enter Task ID")
    if st.button("Get Task"):
        if task_id:
            task = api_request("GET", f"/tasks/{task_id}")
            if task:
                st.json(task)
        else:
            st.error("Please enter a Task ID.")

# Update Task
elif option == "Update Task":
    st.header("Update a Task")
    task_id = st.text_input("Enter Task ID")
    title = st.text_input("New Title")
    description = st.text_area("New Description")
    status = st.selectbox("New Status", ["pending", "in_progress", "completed"])
    if st.button("Update Task"):
        if task_id and title and description:
            updated_data = {"title": title, "description": description, "status": status}
            result = api_request("PUT", f"/tasks/{task_id}", data=updated_data)
            if result:
                st.success("Task updated successfully!")
                st.json(result)
        else:
            st.error("Please fill in all fields.")

# Delete Task
elif option == "Delete Task":
    st.header("Delete a Task")
    task_id = st.text_input("Enter Task ID")
    if st.button("Delete Task"):
        if task_id:
            result = api_request("DELETE", f"/tasks/{task_id}")
            if result:
                st.success("Task deleted successfully!")
                st.json(result)
        else:
            st.error("Please enter a Task ID.")