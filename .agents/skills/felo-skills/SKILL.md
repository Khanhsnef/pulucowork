---
name: felo-skills
description: Complete Felo AI Skill Suite — Generate presentation slides (PPTX), real-time web search, mindmaps, web page content fetch, YouTube subtitles, X/Twitter search & writing, landing pages, LiveDocs, and Apple buy advisory from the terminal or AI agent workflows.
---

# Felo AI Complete Skill Suite

The Felo AI Skill Suite integrates Felo AI's multimodal generation, real-time web search, and presentation engine into AI agent workflows.

## Skill Modules Summary

| Module | Description | Guide |
|---|---|---|
| `felo-slides` | Generate PPTX presentation slides & Live Doc edit links from prompts, local images, or PDFs | `./felo-slides/SKILL.md` |
| `felo-content-to-slides` | Turn webpage articles or YouTube videos directly into PPTX slide decks | `./felo-content-to-slides/SKILL.md` |
| `felo-mindmap` | Generate mindmaps, fishbone diagrams, and timelines | `./felo-mindmap/SKILL.md` |
| `felo-search` | Real-time web search for current events, weather, prices, news | `./felo-search/SKILL.md` |
| `felo-landingpage` | Generate self-contained HTML landing pages | `./felo-landingpage/SKILL.md` |
| `felo-livedoc` | Manage LiveDocs knowledge bases and resources | `./felo-livedoc/SKILL.md` |
| `felo-web-fetch` | Fetch webpage content into Markdown or plain text | `./felo-web-fetch/SKILL.md` |
| `felo-youtube-subtitling` | Extract subtitles/captions from YouTube videos | `./felo-youtube-subtitling/SKILL.md` |
| `felo-x-search` | Search X (Twitter) tweets, users, and replies | `./felo-x-search/SKILL.md` |
| `felo-twitter-writer` | Craft X/Twitter posts and long-form threads | `./felo-twitter-writer/SKILL.md` |
| `felo-superAgent` | AI conversation with real-time SSE streaming | `./felo-superAgent/SKILL.md` |
| `apple-buy-advisor` | Research and compare Apple hardware products | `./apple-buy-advisor/SKILL.md` |
| `claw-deck` | Generate presentation decks for OpenClaw/Claw | `./claw-deck/SKILL.md` |
| `doc-snapshot-agent` | Automatic document illustration and snapshots | `./doc-snapshot-agent/SKILL.md` |

## Setup & API Key

Ensure `felo-ai` CLI is installed and configured:

```bash
npm install -g felo-ai
felo config set FELO_API_KEY "your-api-key-here"
```

Or set the environment variable:

```bash
export FELO_API_KEY="your-api-key-here"
```
