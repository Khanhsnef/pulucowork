---
name: open-claude-view
description: Opens the local Claude View monitoring dashboard (http://localhost:47892) in the browser whenever the user asks to "mở claude view", "open claude view", "bật claude view", "xem claude view", "cv", or similar phrases.
---

# Open Claude View Skill

Triggers when the user asks to view or open the Claude View dashboard.

## Workflow

1. Ensure the `claude-view` server is active on port 47892. If inactive, start it in the background.
2. Run `open http://localhost:47892` to launch the browser UI.
3. Provide the user with a clickable link: [http://localhost:47892](http://localhost:47892).
