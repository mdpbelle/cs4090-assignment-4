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
        name="Weekly task",
        due_date=datetime.date.today(),
        priority="Medium",
        category="Personal",
        recurrence="weekly"
    )
    assert task["recurrence"] == "weekly"

    # test monthly task creation
    task = add_task(
        name="Monthly task",
        due_date=datetime.date.today(),
        priority="Low",
        category="Work",
        recurrence="monthly"
    )
    assert task["recurrence"] == "monthly"

    # TODO: make sure task attributes match the source
