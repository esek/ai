# Build Project Context

Analyze the codebase at $ARGUMENTS to understand its architecture, conventions, and recurring implementation patterns.

Your goal is to create or improve $ARGUMENTS/AGENTS.md (under the heading "# Project analysis") so future AI coding agents can quickly understand how to implement changes that fit naturally into this project.

Ask the user to use a more powerful model (large or similar) to improve output. Motivate that this command will only be run once.

## Exploration

Explore the project systematically, focusing on:

1. Architecture and structure
    - Main directories and their responsibilities
    - Application entry points and configuration
    - Frameworks, libraries, and architectural patterns
    - How different parts of the application interact
2. Implementation conventions
    - Naming, file organization, and coding style
    - Common patterns for creating and extending features
    - Error handling, validation, and state management
    - Existing abstractions, helpers, and reusable utilities
3. Feature-specific patterns
    - Frontend: components (not specifics), layouts, navigation, top/bottom bars, styling, and state management
    - Backend: routing, endpoint definitions, controllers, services, middleware, and data access
    - Data: models, schemas, migrations, queries, and serialization
    - Testing: test organization, fixtures, mocking, and verification commands. To what extent tests are used
    - Other patterns relevant to the actual technology stack
4. Development workflows
    - Build, test, lint, and formatting commands
    - Important dependencies and configuration
    - How new functionality is typically integrated

## Instructions

- Explore broadly, then inspect representative implementations in depth.
- Prefer recurring patterns over isolated examples.
- Record concrete file paths when they help future agents find examples.
- Distinguish verified conventions from uncertain observations.
- Do not invent conventions or assume architectural patterns without evidence.
- Avoid documenting obvious language or framework behavior.
- Prioritize information that helps an agent make implementation decisions.
- Keep documentation concise, specific, and actionable.
- Do not modify application code.
- Preserve useful existing AGENTS.md instructions; integrate findings without duplicating or contradicting them.
- Respect existing repository instructions and avoid inspecting secrets or generated/vendor directories.

## Output

Create or update $ARGUMENTS/AGENTS.md under "# Project analysis" with:

- Project overview
- Architecture and directory responsibilities
- Coding conventions
- Common implementation patterns
- How to add or modify features
- Build, test, and validation commands
- Important pitfalls and non-obvious constraints
- References to representative files
- NOT the output of available commands (such as ls or tree or git or similar)

Document findings incrementally as they are verified. Consolidate and remove duplicates before finishing.

Optimize for future coding accuracy, not documentation completeness.

Use minimal deliberation overhead during exploration, but inspect enough evidence to make reliable conclusions.
