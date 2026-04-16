# AI for FinOps Skills

> **A collection of Agent Skills for AI-powered FinOps (Cloud Financial Operations) guidance**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FinOps Framework](https://img.shields.io/badge/FinOps-Framework%202024-blue)](https://www.finops.org/framework/)
[![Agent Skills](https://img.shields.io/badge/Agent-Skills%20Spec-green)](https://agentskills.io/specification)

## Overview

This repository contains a collection of Agent Skills that enable AI agents to provide expert, framework-aligned guidance on FinOps and cloud financial operations topics.

Each skill lives in its own subdirectory and follows the [Agent Skills Specification](https://agentskills.io/specification).

## Available Skills

### FOCUS Specification Workflow

Skills for working with the [FOCUS Specification](https://focus.finops.org/) and its GitHub repository.

| Skill | Directory | Description |
|-------|-----------|-------------|
| Analyze TF Meeting | [`analyze-tf-meeting/`](analyze-tf-meeting/) | Analyze FOCUS Task Force meeting transcripts to extract action items and issue summaries |
| Assess FR Impact | [`assess-fr-impact/`](assess-fr-impact/) | Assess adoption impact and supported features alignment for FOCUS feature requests |
| Classify FR | [`classify-fr/`](classify-fr/) | Classify FOCUS feature requests by impacted parties, ambiguity, and FinOps scope |
| Create TF Issues | [`create-tf-issues/`](create-tf-issues/) | Create GitHub issues from FOCUS Task Force meeting action items and post PR comments |
| Generate FOCUS Example | [`generate-focus-example/`](generate-focus-example/) | Generate FOCUS specification examples with CSV data and markdown narrative |
| Generate Success Criteria | [`generate-success-criteria/`](generate-success-criteria/) | Generate testable, practitioner-centric success criteria for FOCUS feature requests |
| Publish FR Updates | [`publish-fr-updates/`](publish-fr-updates/) | Post TF meeting summaries as comments on their respective Feature Request GitHub issues |
| Review PR | [`review-pr/`](review-pr/) | Review a FOCUS_Spec GitHub PR with structured comments and suggestions |
| Scope FR Implementation | [`scope-fr-implementation/`](scope-fr-implementation/) | Define MVP, North Star, and phasing strategy for FOCUS feature requests |
| Stress Test | [`stress-test/`](stress-test/) | Stress-test competing courses of action for FOCUS decisions using scenario analysis |
| Validate FOCUS CSV | [`validate-focus-csv/`](validate-focus-csv/) | Validate FOCUS CSV example files for arithmetic, nullability, and semantic correctness |
| Verify TF Analysis | [`verify-tf-analysis/`](verify-tf-analysis/) | Verify FOCUS Task Force meeting analysis output for completeness and accuracy |

### Data Generator Outreach

Skills for managing FOCUS data generator engagement.

| Skill | Directory | Description |
|-------|-----------|-------------|
| Outreach Draft | [`outreach-draft/`](outreach-draft/) | Draft personalized outreach messages for FOCUS data generators |
| Outreach Review | [`outreach-review/`](outreach-review/) | Review FOCUS data generator outreach status and flag overdue contacts |
| Update Org Support | [`update-org-support/`](update-org-support/) | Fetch org support counts from GitHub and update the Prioritization Framework sheet |

### Productivity & Utilities

General-purpose and session-management skills.

| Skill | Directory | Description |
|-------|-----------|-------------|
| Capture | [`capture/`](capture/) | End-of-session knowledge capture — review decisions, context updates, and action items |
| Check FOCUS GitHub | [`check-focus-github/`](check-focus-github/) | Monitor FOCUS_Spec GitHub for PRs awaiting review, new issues, and open action items |
| Check Meetings | [`check-meetings/`](check-meetings/) | Check Granola for recent meetings that haven't had action items extracted |
| Extract Meeting Tasks | [`extract-meeting-tasks/`](extract-meeting-tasks/) | Extract action items from meeting transcripts and create tracked GitHub issues |
| Markdown to Google Doc | [`md-to-gdoc/`](md-to-gdoc/) | Convert a markdown file to a Google Doc with proper table formatting and headings |
| Pre-Send Review | [`pre-send-review/`](pre-send-review/) | Review a document for accuracy, spec compliance, and audience readiness before sharing |
| Reflect | [`reflect/`](reflect/) | Review recent session patterns and propose CLAUDE.md or memory updates |
| Today | [`today/`](today/) | Assemble a daily briefing across GitHub, meetings, and vault; write to Obsidian |

### FinOps Framework Expert

| Skill | Directory | Description |
|-------|-----------|-------------|
| FinOps Framework Expert | [`finops/`](finops/) | Comprehensive guidance on the FinOps framework — principles, phases, maturity model, domains, capabilities, and personas |

## Repository Structure

```
ai-for-finops-skills/
├── README.md
├── INSTALLATION.md
├── LICENSE.md
├── analyze-tf-meeting/
│   └── SKILL.md
├── assess-fr-impact/
│   └── SKILL.md
├── capture/
│   └── SKILL.md
├── check-focus-github/
│   └── SKILL.md
├── check-meetings/
│   └── SKILL.md
├── classify-fr/
│   └── SKILL.md
├── create-tf-issues/
│   └── SKILL.md
├── extract-meeting-tasks/
│   ├── SKILL.md
│   └── references/
│       └── people.md
├── finops/
│   ├── SKILL.md
│   ├── README.md
│   └── references/
│       └── *.md
├── generate-focus-example/
│   └── SKILL.md
├── generate-success-criteria/
│   └── SKILL.md
├── md-to-gdoc/
│   ├── SKILL.md
│   └── convert_md_to_html.py
├── outreach-draft/
│   └── SKILL.md
├── outreach-review/
│   └── SKILL.md
├── pre-send-review/
│   └── SKILL.md
├── publish-fr-updates/
│   └── SKILL.md
├── reflect/
│   └── SKILL.md
├── review-pr/
│   └── SKILL.md
├── scope-fr-implementation/
│   └── SKILL.md
├── stress-test/
│   └── SKILL.md
├── today/
│   └── SKILL.md
├── update-org-support/
│   └── SKILL.md
├── validate-focus-csv/
│   ├── SKILL.md
│   └── validate_focus_csv.py
└── verify-tf-analysis/
    └── SKILL.md
```

## Quick Start

See [INSTALLATION.md](INSTALLATION.md) for full installation instructions.

```bash
# Clone the repo
git clone https://github.com/davidearney/ai-for-finops-skills.git

# Install a specific skill by copying its directory to your skills path
cp -r ai-for-finops-skills/review-pr /path/to/your/skills/directory/
```

## Adding New Skills

Each skill follows a standard structure:

```
<skill-name>/
├── SKILL.md        # Required — YAML frontmatter + skill prompt
└── references/     # Optional — supporting reference files
    └── *.md
```

**SKILL.md frontmatter** must include:

```yaml
---
name: <skill-name>
description: <description under 1024 characters with activation keywords>
license: MIT
metadata:
  author: <author>
  version: "1.0"
---
```

See any existing skill directory for a complete example.

## License

MIT License — see [LICENSE.md](LICENSE.md) for details.

Skills in this repository are independently maintained and are not affiliated with or endorsed by the FinOps Foundation.
