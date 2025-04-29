import pytest

# test add_recurring_task function
# basically makes sure there is a recurrence attribute that can be assigned daily, weekly, or monthly
def test_add_recurring_task():
    # test daily task creation
    task = add_task(
        name="Daily task",
        due_date=datetime.date.today(),
        priority="High",
        category="Work",
        recurrence="daily"
    )
    assert task["recurrence"] == "daily"

    # test weekly task creation
    task = add_task(
        title="Weekly task",
        due_date=datetime.date.today(),
        priority="Medium",
        category="Personal",
        recurrence="weekly"
    )
    assert task["recurrence"] == "weekly"

    # test monthly task creation
    task = add_task(
        title="Monthly task",
        due_date=datetime.date.today(),
        priority="Low",
        category="Work",
        recurrence="monthly"
    )
    assert task["recurrence"] == "monthly"

# tests adding a test with a set time of day
# basically makes sure there is a "task_time" attribute of tasks
def test_add_task_with_time():
    task_time = datetime.time(14, 30)
    task = add_task(
        title="Appointment/Meeting",
        due_date=datetime.date.today(),
        priority="Medium",
        category="Personal",
        task_time=task_time
    )
    assert task["task_time"] == task_time

# tests adding a test with an estimated completion time
# basically tests if there is a "completion_time" attribute of tasks
def test_add_task_completion_time():
    task = add_task(
        title="Timed task",
        due_date=datetime.date.today(),
        priority="High",
        category="Work",
        completion_time=90 # in minutes
    )
    assert task["completion_time"] == 90
