Feature: Add Task

  Scenario: Add a valid task
    Given I have an empty task list
    When I add a task with title "Study", priority "High", category "School", and due date "2025-05-15"
    Then the task list should contain a task titled "Study"

  Scenario: Add a task with missing title
    Given I have an empty task list
    When I try to add a task with no title
    Then I should see a ValueError

  Scenario: Add two tasks with different priorities
    Given I have an empty task list
    When I add a task titled "Email" with priority "High"
    And I add a task titled "Groceries" with priority "Low"
    Then the task list should contain 2 tasks

  Scenario: Add task with specific time and duration
    Given I have an empty task list
    When I add a task titled "Call Mom" with time "17:00" and duration 20
    Then the task should have a due time of "17:00" and duration of 20

  Scenario: Add duplicate titles
    Given I have an empty task list
    When I add a task titled "Repeat"
    And I add another task titled "Repeat"
    Then the task list should contain 2 tasks with the title "Repeat"


