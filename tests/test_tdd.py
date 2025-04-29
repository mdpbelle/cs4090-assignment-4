import pytest
from datetime import date, timedelta, time
import sys
import os

# set path to src folder so tests know where to look
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from tasks import create_task

# test add_recurring_task function
# basically makes sure there is a recurrence attribute that can be assigned daily, weekly, or monthly
def test_add_recurring_task():
    # test daily task creation
    task = create_task(
        title="Daily task",
        due_date=date.today(),
        priority="High",
        category="Work",
        recurrence="daily"
    )
    assert task["recurrence"] == "daily"

    # test weekly task creation
    task = create_task(
        title="Weekly task",
        due_date=date.today(),
        priority="Medium",
        category="Personal",
        recurrence="weekly"
    )
    assert task["recurrence"] == "weekly"

    # test monthly task creation
    task = create_task(
        title="Monthly task",
        due_date=date.today(),
        priority="Low",
        category="Work",
        recurrence="monthly"
    )
    assert task["recurrence"] == "monthly"

# tests adding a test with a set time of day
# basically makes sure there is a "task_time" attribute of tasks
def test_add_task_with_time():
    due_time = "14:30"
    task = create_task(
        title="Appointment/Meeting",
        due_date=date.today() + timedelta(days=1),
        priority="Medium",
        category="Personal",
        due_time=due_time
    )
    assert task["due_time"] == due_time

# tests adding a test with an estimated completion time
# basically tests if there is a "completion_time" attribute of tasks
def test_add_task_completion_time():
    task = create_task(
        title="Timed task",
        due_date=date.today(),
        priority="High",
        category="Work",
        completion_time=90 # in minutes
    )
    assert task["completion_time"] == 90
