# Installation Guide

This guide explains how to install skills from this repository for use with Claude and other agent-based systems.

## Repository Structure

Each skill lives in its own subdirectory:

```
ai-for-finops-skills/
├── finops/          # FinOps Framework Expert
│   ├── SKILL.md
│   ├── README.md
│   └── references/
└── ...              # Additional skills added here
```

## Installing a Skill

### Method 1: Claude Code CLI (Recommended)

1. **Locate your skills directory** — check Claude Code settings for the configured skills path.

2. **Copy the skill directory**:
   ```bash
   # Install the finops skill
   cp -r finops /path/to/your/skills/directory/

   # Or clone the repo and copy from it
   git clone https://github.com/davidearney/ai-for-finops-skills.git
   cp -r ai-for-finops-skills/finops /path/to/your/skills/directory/
   ```

3. **Verify** — the skill should appear in the available skills list.

### Method 2: Direct Integration

For custom agent implementations, add the skill directory to your agent's configured skills path and ensure `SKILL.md` discovery is enabled.

### Method 3: Manual Reference

Read `SKILL.md` directly and use it as a knowledge base or system prompt.

## Available Skills

| Skill | Directory | Activation Keywords |
|-------|-----------|---------------------|
| FinOps Framework Expert | `finops/` | cloud cost, FinOps, AWS/Azure/GCP billing, Reserved Instances, Savings Plans, forecasting, chargeback, tagging |

## Verification

After installing a skill, test it with a query that matches its activation keywords. For example, after installing `finops`:

- "What are the 6 FinOps Principles?"
- "How do I build a tagging strategy?"
- "What's the difference between Crawl and Walk maturity?"

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Skill not found | Verify the directory name matches the `name:` field in `SKILL.md` frontmatter |
| Reference files not loading | Ensure the `references/` subdirectory is present |
| Generic responses | Explicitly mention the skill topic (e.g., "FinOps") in your query |

## License

All skills are released under the MIT License. See [LICENSE.md](LICENSE.md).
