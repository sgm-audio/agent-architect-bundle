---
name: show-working-directory
description: "Always announce the current working directory at the start of every response. User gets disoriented without spatial context — needs to know where files are relative to where operations happen."
version: 1.0.0
author: Scott Mills
license: MIT
---

# Always Show Current Directory

Every response must begin with `[cwd: /path]` showing the absolute current working directory.

This is required. The user works across many project directories and needs spatial grounding. Skipping this causes confusion on subsequent commands.

Example: `[cwd: /c/Users/scott/OneDrive/Desktop]`

When the working directory changes mid-conversation (e.g., after a `cd` command), announce the new path in the next response.
