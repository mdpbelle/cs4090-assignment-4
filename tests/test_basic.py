import pytest
import sys
import os 
import json
import pytest
from datetime import datetime, timedelta

# set path to src folder so tests know where to look
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from tasks import load_tasks, create_task, generate_unique_id, save_tasks, filter_tasks_by_priority, filter_tasks_by_category, filter_tasks_by_completion, search_tasks, get_overdue_tasks

TEST_FILE = "test_basic.json"

@pytest.fixture
def sample_tasks():
    return [
            {"id": 1, "title": "special", "priority": "High", "category": "Work", "due_date": "2025-05-15", "completed": False},
        {"id": 2, "title": "completed", "priority": "Medium", "category": "Personal", "completed": True},
        {"id": 3, "title": "overdue", "priority": "Low", "category": "Personal", "due_date": "2025-04-15", "completed": False}
    ]

def test_create_task():
    task = create_task("New", "A task", "High", "Work", "2025-05-10", "16:45", 90, 3)
    assert task["title"] == "New"
    assert task["priority"] == "High"
    assert task["due_time"] == "16:45"

def test_save_and_load_tasks(sample_tasks):
    save_tasks(sample_tasks, TEST_FILE)
    loaded = load_tasks(TEST_FILE)
    assert len(loaded) == 3
    assert loaded[0]["title"] == "special"
    os.remove(TEST_FILE)

def test_load_tasks_nonexistent():
    assert load_tasks("nonexistent_file.json") == []

def test_create_task_no_title():
    with pytest.raises(ValueError, match="Title is required"):
        create_task("")

def test_generate_unique_id(sample_tasks):
    assert generate_unique_id(sample_tasks) == 4

def test_generate_unique_id_fail():
    assert generate_unique_id([]) == 1

def test_filter_by_category(sample_tasks):
    filtered = filter_tasks_by_category(sample_tasks, "Work")
    assert len(filtered) == 1
    assert filtered[0]["category"] == "Work"


def test_filter_by_priority(sample_tasks):
    filtered = filter_tasks_by_priority(sample_tasks, "Low")
    assert len(filtered) == 1
    assert filtered[0]["priority"] == "Low"

def test_filter_by_completion(sample_tasks):
    filtered = filter_tasks_by_completion(sample_tasks, True)
    assert len(filtered) == 1
    assert filtered[0]["completed"] == True

def test_search_tasks(sample_tasks):
    query = "special"
    filtered = search_tasks(sample_tasks, query)
    assert len(filtered) == 1
    assert filtered[0]["title"] == "special"

def test_get_overdue_tasks(sample_tasks):
    filtered = get_overdue_tasks(sample_tasks)
    assert len(filtered) == 1
    assert filtered[0]["completed"] == False
    assert filtered[0]["title"] == "overdue"

