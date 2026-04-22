# Project Workflow

## Guiding Principles

1. **The Plan is the Source of Truth:** All work must be tracked in `plan.md`
2. **The Tech Stack is Deliberate:** Changes to the tech stack must be documented in `tech-stack.md` *before* implementation
3. **Working Code First:** Functional pieces are integrated directly into the pipeline — no separate test layer required
4. **Per-Task Commits:** Commit after every completed task
5. **Summaries in Git Notes:** Task summaries stored as git notes
6. **Non-Interactive & CI-Aware:** Prefer non-interactive commands. Use `CI=true` for watch-mode tools (linters, formatters) to ensure single execution.

## Task Workflow

All tasks follow a strict lifecycle:

### Standard Task Workflow

1. **Select Task:** Choose the next available task from `plan.md` in sequential order

2. **Mark In Progress:** Before beginning work, edit `plan.md` and change the task from `[ ]` to `[~]`

3. **Implement:** Write the code to fulfill the task requirements. Working pieces are integrated directly into the pipeline.

4. **Verify with Formatter:** Run the project's custom `Formatter` (see `tech-stack.md`) to ensure code formatting compliance.

5. **Verify Linting:** Run `ruff check .` to ensure no linting errors.

6. **Verify Typing:** Run `mypy src/` to ensure type safety compliance.

7. **Document Deviations:** If implementation differs from tech stack:
   - **STOP** implementation
   - Update `tech-stack.md` with new design
   - Add dated note explaining the change
   - Resume implementation

8. **Commit Code Changes:**
   - Stage all code changes related to the task.
   - Propose a clear, concise commit message e.g, `feat(ui): Create basic HTML structure for calculator`.
   - Perform the commit.

9. **Attach Task Summary with Git Notes:**
   - **Step 9.1: Get Commit Hash:** Obtain the hash of the *just-completed commit* (`git log -1 --format="%H"`).
   - **Step 9.2: Draft Note Content:** Create a detailed summary for the completed task. This should include the task name, a summary of changes, a list of all created/modified files, and the core "why" for the change.
   - **Step 9.3: Attach Note:** Use the `git notes` command to attach the summary to the commit.
     ```bash
     git notes add -m "<note content>" <commit_hash>
     ```

10. **Get and Record Task Commit SHA:**
    - **Step 10.1: Update Plan:** Read `plan.md`, find the line for the completed task, update its status from `[~]` to `[x]`, and append the first 7 characters of the *just-completed commit's* commit hash.
    - **Step 10.2: Write Plan:** Write the updated content back to `plan.md`.

11. **Commit Plan Update:**
    - **Action:** Stage the modified `plan.md` file.
    - **Action:** Commit this change with a descriptive message (e.g., `conductor(plan): Mark task 'Create user model' as complete`).

### Phase Completion Verification and Checkpointing Protocol

**Trigger:** This protocol is executed immediately after a task is completed that also concludes a phase in `plan.md`.

1.  **Announce Protocol Start:** Inform the user that the phase is complete and the verification and checkpointing protocol has begun.

2.  **Verify Formatter Compliance:** Run the project's custom `Formatter` on all changed files.

3.  **Verify Linting & Typing:** Run `ruff check .` and `mypy src/` on changed files.

4.  **Propose a Detailed, Actionable Manual Verification Plan:**
    -   **CRITICAL:** Analyze `product.md`, `product-guidelines.md`, and `plan.md` to determine the user-facing goals of the completed phase.
    -   Generate a step-by-step plan with expected outcomes.

    **For a Backend/Science Change:**
    ```
    For manual verification, please follow these steps:

    **Manual Verification Steps:**
    1.  **Execute the following command in your terminal:** `python3 generate.py --source mnist`
    2.  **Confirm that you see:** New visualization files in `output/mnist/`
    ```

5.  **Await Explicit User Feedback:**
    -   After presenting the plan, ask: "**Does this meet your expectations? Please confirm with yes or provide feedback.**"
    -   **PAUSE** and await the user's response.

6.  **Create Checkpoint Commit:**
    -   Stage all changes. If no changes, proceed with an empty commit.
    -   Commit with a clear message (e.g., `conductor(checkpoint): Checkpoint end of Phase X`).

7.  **Attach Auditable Verification Report using Git Notes:**
    -   **Step 7.1: Draft Note Content:** Create a verification report with formatter/linting results, manual verification steps, and user confirmation.
    -   **Step 7.2: Attach Note:** `git notes add -m "<report>" <checkpoint_commit_hash>`

8.  **Get and Record Phase Checkpoint SHA:**
    -   **Step 8.1: Get Commit Hash:** `git log -1 --format="%H"`
    -   **Step 8.2: Update Plan:** Append `[checkpoint: <sha>]` to the phase heading in `plan.md`.
    -   **Step 8.3: Write Plan:** Write updated content back to `plan.md`.

9. **Commit Plan Update:**
    - **Action:** Stage the modified `plan.md` file.
    - **Action:** Commit with message `conductor(plan): Mark phase '<PHASE NAME>' as complete`.

10.  **Announce Completion:** Inform the user that the phase is complete and the checkpoint has been created.

### Quality Gates

Before marking any task complete, verify:

- [ ] Code passes Formatter checks
- [ ] No ruff linting errors
- [ ] mypy typing compliant
- [ ] Code follows project's code style guidelines (as defined in `code_styleguides/`)
- [ ] All public functions/methods are documented (docstrings)
- [ ] No security vulnerabilities introduced
- [ ] Documentation updated if needed

## Development Commands

### Setup
```bash
pip install -e ".[dev]"
```

### Daily Development
```bash
ruff check .          # Lint
ruff format .         # Format (or use Formatter)
mypy src/             # Type check
python3 generate.py   # Run pipeline
```

### Before Committing
```bash
ruff check . && mypy src/
```

## Code Review Process

### Self-Review Checklist
Before requesting review:

1. **Functionality**
   - Feature works as specified
   - Edge cases handled

2. **Code Quality**
   - Follows style guide
   - DRY principle applied
   - Clear variable/function names (per naming convention)
   - Appropriate comments

3. **Security**
   - No hardcoded secrets
   - Input validation present

4. **Performance**
   - Caching implemented where needed

## Commit Guidelines

### Message Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `chore`: Maintenance tasks

### Examples
```bash
git commit -m "feat(core): Implement delta field transformation"
git commit -m "fix(sweep): Correct occupancy calculation for edge cases"
git commit -m "docs(readme): Update installation instructions"
git commit -m "refactor(nucleus): Extract pattern extraction logic"
```

## Definition of Done

A task is complete when:

1. All code implemented to specification
2. Code passes Formatter checks
3. No ruff linting errors
4. mypy typing compliant
5. Documentation complete (if applicable)
6. Implementation notes added to `plan.md`
7. Changes committed with proper message
8. Git note with task summary attached to the commit
