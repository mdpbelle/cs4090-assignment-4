import pytest
import sys
import os
import json
from datetime import datetime, timedelta
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from tasks import save_tasks, load_tasks, create_task, get_overdue_tasks, generate_unique_id, filter_tasks_by_priority, filter_tasks_by_category, filter_tasks_by_completion, search_tasks

TEST_FILE = "tests/test_advance.json"

@pytest.fixture
def sample_tasks():
    return [
        {"id": 1, "title": "Urgent", "priority": "High", "category": "Work", "due_date": "2025-05-15", "completed": False},
        {"id": 2, "title": "Done", "priority": "Medium", "category": "Personal", "completed": True},
        {"id": 3, "title": "Late", "priority": "Low", "category": "Errands", "due_date": "2025-04-15", "completed": False}
    ]

@pytest.mark.parametrize("priority,expected_count", [
    ("High", 1),
    ("Medium", 1),
    ("Low", 1),
    ("None", 0)
])
def test_filter_priority_param(sample_tasks, priority, expected_count):
    filtered = filter_tasks_by_priority(sample_tasks, priority)
    assert len(filtered) == expected_count

def test_overdue_mocked(sample_tasks):
    with patch("tasks.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2025, 4, 20)
        mock_dt.strptime = datetime.strptime
        overdue = get_overdue_tasks(sample_tasks)
        assert len(overdue) ==1
        assert overdue[0]["title"] == "Late"

def test_save_and_load_tmp(sample_tasks, tmp_path):
    test_file = tmp_path / "tasks.json"
    save_tasks(sample_tasks, TEST_FILE)
    loaded = load_tasks(TEST_FILE)
    assert len(loaded) == 3

@pytest.mark.parametrize("title", ["", None])
def test_create_task_no_title_param(title):
    with pytest.raises(ValueError):
        create_task(title)
