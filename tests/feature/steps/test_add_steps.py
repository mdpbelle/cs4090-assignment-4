import pytest
from behave import given, when, then
from tasks import create_task
from datetime import datetime
import sys
import os

# make sure it knows where to run tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))
from tasks import create_task

@given("I have an empty task list")
def step_impl(context):
    context.tasks = []

@when('I add a task with title "{title}", priority "{priority}", category "{category}", and due date "{due_date}"')
def step_impl(context, title, priority, category, due_date):
    task = create_task(title, "", priority, category, due_date)
    context.tasks.append(task)

@when('I try to add a task with no title')
def step_impl(context):
    try:
        create_task("")
    except ValueError as e:
        context.error = e

@when('I add a task titled "{title}" with priority "{priority}"')
def step_impl(context, title, priority):
    task = create_task(title, "", priority, "General")
    context.tasks.append(task)

@when('I add a task titled "{title}" with time "{due_time}" and duration {duration:d}')
def step_impl(context, title, due_time, duration):
    task = create_task(title, "", "Medium", "Calls", "2025-05-15", due_time, duration)
    context.tasks.append(task)

@when('I add a task titled "{title}"')
def step_impl(context, title):
    task = create_task(title)
    context.tasks.append(task)

@when('I add another task titled "{title}"')
def step_impl(context, title):
    task = create_task(title)
    context.tasks.append(task)

@then('the task list should contain a task titled "{title}"')
def step_impl(context, title):
    assert any(t["title"] == title for t in context.tasks)

@then("I should see a ValueError")
def step_impl(context):
    assert isinstance(context.error, ValueError)

@then("the task list should contain 2 tasks")
def step_impl(context):
    assert len(context.tasks) == 2

@then('the task should have a due time of "{due_time}" and duration of {duration:d}')
def step_impl(context, due_time, duration):
    task = context.tasks[-1]
    assert task["due_time"] == due_time
    assert task["completion_time"] == duration

@then('the task list should contain 2 tasks with the title "{title}"')
def step_impl(context, title):
    matches = [t for t in context.tasks if t["title"] == title]
    assert len(matches) == 2

