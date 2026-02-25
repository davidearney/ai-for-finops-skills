# FinOps Framework Expert Skill

A comprehensive Agent Skill providing expert guidance on FinOps (Cloud Financial Operations) based on the FinOps framework.

## What This Skill Provides

This skill enables AI agents to provide authoritative, framework-aligned guidance on:

- **Cloud cost optimization** across AWS, Azure, and GCP
- **Financial management** for cloud spending
- **Business value maximization** from cloud investments
- **FinOps maturity assessment** and roadmap planning
- **Cost allocation, tagging, and chargeback** strategies
- **Commitment discounts** (Reserved Instances, Savings Plans, Committed Use Discounts)
- **Workload optimization** (rightsizing, waste elimination, scheduling)
- **Forecasting and budgeting** best practices
- **Governance policies** and automation
- **Cross-functional collaboration** between Finance, Engineering, and Product teams

## Framework Coverage

This skill comprehensively covers the FinOps framework:

### ✅ 6 Core Principles
- Teams need to collaborate
- Business value drives technology decisions
- Everyone takes ownership for their technology usage
- FinOps data should be accessible, timely, and accurate
- FinOps should be enabled centrally
- Take advantage of the variable cost model of the cloud

### ✅ 3 Phases
- **Inform**: Visibility & Allocation
- **Optimize**: Rates & Usage
- **Operate**: Continuous Improvement & Operations

### ✅ Maturity Model
- **Crawl**: Basic processes, manual, reactive
- **Walk**: Documented processes, proactive, cross-functional
- **Run**: Automated, optimized, continuous improvement

### ✅ 4 Domains & 22 Capabilities
1. **Understand Usage & Cost** (4 capabilities)
2. **Quantify Business Value** (5 capabilities)
3. **Optimize Usage & Cost** (5 capabilities)
4. **Manage the FinOps Practice** (8 capabilities)

### ✅ Personas
- Core: FinOps Practitioner, Engineering, Finance, Product, Procurement, Leadership
- Allied: ITAM, ITFM, Sustainability, ITSM, Security

## Skill Structure

```
finops/
├── SKILL.md                              # Main skill file with comprehensive instructions
├── README.md                             # This file
└── references/                           # Detailed reference documentation
    ├── principles.md                     # Deep dive into the 6 FinOps Principles
    ├── phases.md                         # Comprehensive phase guidance
    ├── maturity.md                       # Maturity assessment framework
    ├── domains-capabilities.md           # All 22 capabilities with KPIs
    ├── personas.md                       # Detailed persona responsibilities
    └── terminology.md                    # FinOps glossary and terminology
```

## Usage

When activated, this skill provides:

1. **Framework-grounded recommendations** tied to FinOps principles and capabilities
2. **Maturity-appropriate guidance** tailored to Crawl, Walk, or Run stages
3. **Persona-specific insights** for cross-functional collaboration
4. **Practical implementation steps** for common FinOps tasks
5. **Reference to detailed documentation** when deep dives are needed

## Key Features

### Progressive Disclosure
- Core guidance in SKILL.md (~500 lines)
- Detailed reference material in separate files
- Efficient context usage through on-demand loading

### Comprehensive Coverage
- All FinOps framework components
- Cloud provider agnostic (AWS, Azure, GCP)
- Multi-cloud strategies and FOCUS specification
- Sustainability and intersecting disciplines

### Actionable Guidance
- Step-by-step implementation guides
- Sample KPIs and targets by maturity level
- Common scenarios and solutions
- Anti-patterns to avoid

## Common Use Cases

- "How do I build a tagging strategy?"
- "What Reserved Instances should I purchase?"
- "How do I implement chargeback?"
- "What's my FinOps maturity level?"
- "How do I forecast cloud costs?"
- "What governance policies should I establish?"
- "How do I optimize my commitment discount portfolio?"
- "How do I implement anomaly detection?"
- "What unit metrics should I track?"
- "How do I enable FinOps collaboration?"

## Framework Reference

This skill references the FinOps framework. For more information, see:
- https://www.finops.org/framework/

## License

MIT License - See skill metadata for details

## Version

- **Skill Version**: 1.0
- **Framework Version**: 2024
- **Last Updated**: January 2026

## Metadata

- **Author**: James Barney
- **Compatibility**: Requires access to cloud billing data and cost management tools when implementing recommendations
- **Skill Name**: `finops`
