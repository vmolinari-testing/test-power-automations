# Test Power Automations

Small FastAPI server used to test integrations with Microsoft Power Automate and Teams.

## Requirements

- Python 3.13+
- `uv`

## Installation

```bash
uv sync
```

## Run

```bash
uv run uvicorn main:app --reload
```

The server will be available at:

```
http://127.0.0.1:8000
```

## Available endpoints

| Method | Endpoint        | Description                           |
| ------ | --------------- | ------------------------------------- |
| GET    | `/`             | Health check                          |
| GET    | `/automations`  | Returns mock automation data          |
| POST   | `/api/messages` | Receives Microsoft Teams bot messages |

## Purpose

This project is intended to:

- test HTTP requests from Power Automate;
- experiment with Adaptive Cards in Microsoft Teams;
- prototype integrations before connecting to real services such as GitLab or Jira.
