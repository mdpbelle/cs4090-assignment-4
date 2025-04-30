import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from tasks import load_tasks, save_tasks, get_overdue_tasks, generate_unique_id, filter_tasks_by_priority, filter_tasks_by_category
import subprocess
import sys
import os
import webbrowser

# set sys path to src directory so it knows where to look
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

def main():
    st.title("To-Do Application")
    
    # Load existing tasks
    tasks = load_tasks()

    # Patch old tasks
    for task in tasks:
        task.setdefault("due_time", "00:00")
        task.setdefault("completion_time", 0)
        task.setdefault("recurrence", "none")

    # get overdue tasks from file
    overdue_tasks = get_overdue_tasks(tasks)
    overdue_ids = {task["id"] for task in overdue_tasks}
    
    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")
    
    # Task creation form
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"])
        task_due_date = st.date_input("Due Date")
        task_due_time = st.time_input("Time of Day (optional)")
        task_completion_time = st.number_input("Estimated Time (minutes)", min_value=0, step=5)
        task_recurrence = st.selectbox("Recurrence", ["none", "daily", "weekly", "monthly"])
        submit_button = st.form_submit_button("Add Task")
        
        now_date = datetime.now().date()
        now_time = datetime.now().time()

        if submit_button:
            if not task_title:
                st.sidebar.error("Task title is required.")
            elif task_due_date < now_date:
                st.sidebar.warning("Due date has already passed.")
            elif task_due_date == now_date and task_due_time < now_time:
                st.sidebar.warning("Due time is in the past.")
            else:
                new_task = {
                    "id": generate_unique_id(tasks),
                    "title": task_title,
                    "description": task_description,
                    "priority": task_priority,
                    "category": task_category,
                    "due_date": task_due_date.strftime("%Y-%m-%d"),
                    "completed": False,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "due_time": task_due_time.strftime("%H:%M"),
                    "completion_time": task_completion_time,
                    "recurrence": task_recurrence
                }
                tasks.append(new_task)
                save_tasks(tasks)
                st.sidebar.success("Task added successfully!")
    
    # Main area to display tasks
    st.header("Your Tasks")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(set([task["category"] for task in tasks])))
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    
    show_completed = st.checkbox("Show Completed Tasks")
    
    # Apply filters
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]
    
    # Display tasks
    for task in filtered_tasks:
        # check for new overdue tasks
        task_datetime = datetime.strptime(task["due_date"] + " " + task["due_time"], "%Y-%m-%d %H:%M")
        is_overdue = not task["completed"] and task_datetime < datetime.now()
        col1, col2 = st.columns([4, 1])
        with col1:
            if task["completed"]:
                st.markdown(f"~~**{task['title']}**~~")
            elif task["id"] in overdue_ids or is_overdue:
                st.markdown(f"**{task['title']} (Overdue)**")
            else:
                st.markdown(f"**{task['title']}**")
            st.write(task["description"])
            st.caption(f"Due: {task['due_date']} at {task['due_time']} | Priority: {task['priority']} | Category: {task['category']} | Recurrence: {task['recurrence']}")
        with col2:
            if st.button("Complete" if not task["completed"] else "Undo", key=f"complete_{task['id']}"):
                for t in tasks:
                    if t["id"] == task["id"]:
                        if  not t["completed"]:
                            t["completed"] = True
                            # Handle recurrence
                            if t["recurrence"] == "daily":
                                new_due = datetime.strptime(t["due_date"], "%Y-%m-%d") + timedelta(days=1)
                                t["due_date"] = new_due.strftime("%Y-%m-%d")
                                t["completed"] = False
                            elif t["recurrence"] == "weekly":
                                new_due = datetime.strptime(t["due_date"], "%Y-%m-%d") + timedelta(weeks=1)

                                t["due_date"] = new_due.strftime("%Y-%m-%d")
                                t["completed"] = False
                            elif t["recurrence"] == "monthly":
                                new_due = datetime.strptime(t["due_date"], "%Y-%m-%d") + relativedelta(months=1) 
                                t["due_date"] = new_due.strftime("%Y-%m-%d")
                                t["completed"] = False
                        else:
                            t["completed"] = False
                        save_tasks(tasks)
                        st.rerun()
            if st.button("Delete", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()
    st.title("Pytest Advanced Feature Runner")
    if st.button("Run Parameterized Tests"):
        st.code(subprocess.getoutput("pytest tests/test_advanced.py -k 'param'"))
    if st.button("Run Mocked Tests"):
        st.code(subprocess.getoutput("pytest tests/test_advanced.py -k 'mock'"))
    if st.button("Run tmp_path tests"):
        st.code(subprocess.getoutput("pytest tests/test_advanced.py -k 'tmp'"))
    if st.button("Run BDD Tests"):
        env = os.environ.copy() # copy current environment
        env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")) # modify pythonpath
        result = subprocess.run(["behave", "../tests/feature"],
                                cwd="src",
                                capture_output=True,
                                text=True)
        st.text_area("BDD Output", result.stdout + "\n" + result.stderr, height=300)
        #st.code(subprocess.getoutput("behave tests/feature"))
    if st.button("Run Unit Tests"):
        with st.spinner("Running pytest..."):
            result = subprocess.run(["pytest", "tests"], capture_output=True, text=True)
            st.text(result.stdout)
            if result.stderr:
                st.error(result.stderr)            
    if st.button("Run with Coverage and generate HTML report"):
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        with st.spinner("Running coverage..."):
            try:
                result = subprocess.run(["coverage", "run", "-m", "pytest", "tests/"], cwd=root, capture_output=True, text=True)
                st.text(result.stdout)
                st.text(result.stderr)
                subprocess.run(["coverage", "html"], check=True)
                st.text("View report in /htmlcov/index.html")
            except subprocess.CalledProcessError as e:
                st.error(f"Error running coverage: {e}")

if __name__ == "__main__":
    main()
