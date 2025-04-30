import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from tasks import load_tasks, save_tasks, filter_tasks_by_priority, filter_tasks_by_category
import subprocess

def main():
    st.title("To-Do Application")
    
    # Load existing tasks
    tasks = load_tasks()

    # Patch old tasks
    for task in tasks:
        task.setdefault("due_time", "00:00")
        task.setdefault("completion_time", 0)
        task.setdefault("recurrence", "none")
    
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
        
        if submit_button and task_title:
            new_task = {
                "id": len(tasks) + 1,
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
        col1, col2 = st.columns([4, 1])
        with col1:
            if task["completed"]:
                st.markdown(f"~~**{task['title']}**~~")
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
    with st.expander("Run Unit Tests (dev only)"):
        if st.button("Run Tests"):
            with st.spinner("Running pytest..."):
                result = subprocess.run(["pytest", "tests"], capture_output=True, text=True)
                st.text(result.stdout)
                if result.stderr:
                    st.error(result.stderr)

if __name__ == "__main__":
    main()
