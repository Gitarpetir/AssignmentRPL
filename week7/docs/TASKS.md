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

Enhance the action item extraction functionality with more sophisticated pattern recognition and analysis.

## Task 3: Try adding a new model and relationships

Create new database models with relationships and update the application to support them.

## Task 4: Improve tests for pagination and sorting

Enhance test coverage for pagination and sorting functionality across the application.
