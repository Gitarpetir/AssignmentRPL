# Week 7 – Tasks

## Task 1: Add more endpoints and validations

Add additional API endpoints and implement proper input validation and error handling.
- **PR Link:** https://github.com/Gitarpetir/AssignmentRPL/pull/1
- **Description:** Added `DELETE /notes/{note_id}` endpoint and input validations for Note schemas.
- **Manual Review vs. Graphite AI Review:**
  - **Manual Review:** It was noted that while validations were added for the `Note` models, similar validations for the `ActionItem` models were completely missed. A redundant `return` statement in the DELETE endpoint was also found.
  - **Graphite AI Review:** Graphite ran successfully but left **0 comments**.
  - **Comparison:** In this specific task, the manual review was better. Graphite failed to notice the missing validations for the other models (missing the broader context of the application), whereas the manual review caught this inconsistency easily.

## Task 2: Extend extraction logic

### Task 2: Extend extraction logic
* **PR Link:** https://github.com/Gitarpetir/AssignmentRPL/pull/2
* **Description:** Enhanced the `extract_action_items` logic using a compiled Regex pattern to efficiently and case-insensitively extract tasks (TODO, ACTION, TASK, BUG).
* **Manual Review vs. Graphite AI Review:**
  * **Manual Review:** The manual review praised the performance optimization of compiling the Regex globally. However, it caught a significant logic flaw: to pass the "Ship it!" test, the AI simply added `if line.endswith("!"):`. This is too broad and would incorrectly extract any normal sentence ending with an exclamation mark as an action item.
  * **Graphite AI Review:** Graphite ran successfully but left **0 comments**.
  * **Comparison:** The AI review was worse than the manual review. Graphite completely missed the over-extraction bug caused by the overly broad `endswith("!")` condition. It verified that the code passed the tests but failed to think about real-world edge cases outside the test suite.

## Task 3: Try adding a new model and relationships

Create new database models with relationships and update the application to support them.

## Task 4: Improve tests for pagination and sorting

Enhance test coverage for pagination and sorting functionality across the application.
