---
name: SQL to HTML Report
description: An end-to-end workflow skill that takes a SQL query, executes it against the local database, and generates a beautiful HTML report with charts.
---

# SQL to HTML Report Generator

## Goal
Automate the tedious pipeline of running SQL queries and manually formatting the results into presentation-ready HTML reports.

## Prerequisites
- The SQLite MCP server must be running and connected to `data/state_store.db` (or any target database).
- The user must provide a valid SQL query or the name of a `.sql` file in the workspace.

## Workflow

1. **Read & Validate SQL:**
   - If the user provides a `.sql` file, read its contents.
   - If the user provides raw SQL, validate that it is a safe `SELECT` statement. Do not execute destructive commands (DROP, DELETE, UPDATE).

2. **Execute Query:**
   - Use the SQLite MCP to execute the SQL query against the local database.
   - Retrieve the resulting dataset (JSON/CSV format).

3. **Analyze Data:**
   - Briefly inspect the data to determine the best visualization type (e.g., Line chart for time-series, Bar chart for categorical comparisons, Table for raw data dumps).

4. **Generate HTML Report:**
   - Create a standalone HTML file.
   - Embed CSS for modern, clean, and responsive styling (Ahamove brand colors preferred: Orange/Blue).
   - Use a lightweight charting library like Chart.js or Recharts via CDN to render the data.
   - Include a data table below the chart.
   - Include the original SQL query in a collapsible `<details>` tag at the bottom for reference.

5. **Save & Notify:**
   - Save the HTML file in the current directory or `Output/` folder with a descriptive name (e.g., `report_YYYYMMDD_topic.html`).
   - Notify the user with the file path so they can open it in their browser.
