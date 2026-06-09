# Session Recovery

When a user returns to a new session saying they closed a previous session and want to know where they left off, use this pattern to reconstruct context.

## Workflow

1. **Browse recent sessions:**
   ```
   session_search()
   ```
   Returns the 2 most recent sessions with titles, previews, timestamps.

2. **Identify the right session** — pick the one with the closest timestamp and matching title.

3. **Scroll to the tail:**
   The browse result doesn't show the last messages directly. Get the session's full context:
   ```
   session_search(session_id="<id>")
   ```
   This dumps the session (first 20 + last 10 messages when large).

4. **If truncated, scroll to the very end:**
   From the read output, take the last message's `id` and scroll around it:
   ```
   session_search(session_id="<id>", around_message_id=<last_id>, window=10)
   ```
   Then increment the around_message_id and scroll forward until `messages_after < window` signals the end.

5. **Report concisely:**
   - What was completed
   - What was left open
   - Any cron jobs, files, or state that was described but not yet created
   - The exact last user question/request (so they can decide where to resume)

## Pitfalls

- **Described-but-not-executed actions:** The previous session may have described cron jobs, file writes, or other setup in a "tomorrow's plan" section without actually creating them. Check for this explicitly. If found, create them now.
- **Large sessions:** Sessions over ~200 messages are truncated in `read` mode. Always check the `truncated` flag in the response.
- **Cron jobs survive session closure:** Use `cronjob(action='list')` to check what's actually scheduled. Don't trust what was "described" — verify what exists.
