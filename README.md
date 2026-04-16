# AI for FinOps Skills

> **A collection of Agent Skills for AI-powered FinOps (Cloud Financial Operations) guidance**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FinOps Framework](https://img.shields.io/badge/FinOps-Framework%202024-blue)](https://www.finops.org/framework/)
[![Agent Skills](https://img.shields.io/badge/Agent-Skills%20Spec-green)](https://agentskills.io/specification)

## Overview

This repository contains a collection of Agent Skills that enable AI agents to provide expert, framework-aligned guidance on FinOps and cloud financial operations topics.

Each skill lives in its own subdirectory and follows the [Agent Skills Specification](https://agentskills.io/specification).

## Available Skills

| Skill | Directory | Description |
|-------|-----------|-------------|
| **FinOps Framework Expert** | [`finops/`](finops/) | Comprehensive guidance on the FinOps framework — principles, phases, maturity model, domains, capabilities, and personas |

## Repository Structure

```
ai-for-finops-skills/
├── README.md                # This file
├── INSTALLATION.md          # Installation instructions for all skills
├── LICENSE.md               # MIT License
└── finops/                  # FinOps Framework Expert skill
    ├── SKILL.md             # Main skill file
    ├── README.md            # Skill documentation
    └── references/          # Detailed reference docs
        ├── principles.md
        ├── phases.md
        ├── maturity.md
        ├── domains-capabilities.md
        ├── personas.md
        └── terminology.md
```

## Quick Start

See [INSTALLATION.md](INSTALLATION.md) for full installation instructions.

```bash
# Install a specific skill by copying its directory to your skills path
cp -r finops /path/to/your/skills/directory/
```

## Adding New Skills

Each skill follows a standard structure:

```
<skill-name>/
├── SKILL.md        # Required — YAML frontmatter + skill prompt
├── README.md       # Skill documentation
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
