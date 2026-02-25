# FinOps Framework Expert Skill

> **A comprehensive Agent Skill providing authoritative, framework-aligned guidance on Cloud Financial Operations (FinOps)**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FinOps Framework](https://img.shields.io/badge/FinOps-Framework%202024-blue)](https://www.finops.org/framework/)
[![Agent Skills](https://img.shields.io/badge/Agent-Skills%20Spec-green)](https://agentskills.io/specification)

## Overview

This skill enables AI agents to provide expert guidance on FinOps (Cloud Financial Operations) based on the [FinOps framework](https://www.finops.org/framework/). It covers the complete framework including principles, phases, maturity model, domains, capabilities, and personas.

**Use this skill when working on**: Cloud cost optimization, AWS/Azure/GCP billing, cost allocation, Reserved Instances, Savings Plans, forecasting, budgeting, tagging strategies, chargeback, governance, or any cloud financial management topic.

## 🎯 What This Skill Provides

- ✅ **Complete FinOps Framework coverage** - All 6 principles, 3 phases, 22 capabilities
- ✅ **Maturity-based guidance** - Tailored advice for Crawl, Walk, and Run stages
- ✅ **Practical implementation** - Step-by-step guides for common FinOps tasks
- ✅ **Multi-cloud support** - AWS, Azure, GCP, and hybrid environments
- ✅ **Cross-functional collaboration** - Guidance for all personas (Engineering, Finance, Product, etc.)
- ✅ **Business value focus** - Not just cost reduction, but value maximization

## 📋 Framework Coverage

### The 6 FinOps Principles
1. Teams need to collaborate
2. Business value drives technology decisions
3. Everyone takes ownership for their technology usage
4. FinOps data should be accessible, timely, and accurate
5. FinOps should be enabled centrally
6. Take advantage of the variable cost model of the cloud

### The 3 Phases (Iterative Cycle)
- **Inform**: Establish visibility and allocation
- **Optimize**: Improve rates and usage efficiency
- **Operate**: Operationalize through governance and automation

### Maturity Model
- **Crawl**: Basic processes, manual, reactive (50% allocation, 60% RI coverage)
- **Walk**: Documented, proactive, cross-functional (80% allocation, 70% RI coverage)
- **Run**: Automated, continuous improvement (90%+ allocation, 80%+ RI coverage)

### 4 Domains & 22 Capabilities
1. **Understand Usage & Cost** (4 capabilities)
2. **Quantify Business Value** (5 capabilities)
3. **Optimize Usage & Cost** (5 capabilities)
4. **Manage the FinOps Practice** (8 capabilities)

### Personas
- **Core**: FinOps Practitioner, Engineering, Finance, Product, Procurement, Leadership
- **Allied**: ITAM, ITFM, Sustainability, ITSM, Security

## 🚀 Quick Start

### Installation

```bash
# Copy the finops directory to your skills location
cp -r finops /path/to/your/skills/directory/

# Verify structure
ls -R finops/
# Should show: SKILL.md, README.md, references/*.md
```

See [INSTALLATION.md](INSTALLATION.md) for detailed instructions.

### Test It

Try these queries after installation:

1. **Framework basics**: "What are the 6 FinOps Principles?"
2. **Practical guidance**: "How do I build a tagging strategy?"
3. **Maturity assessment**: "What's the difference between Crawl and Walk maturity?"

## 📁 Directory Structure

```
finops/
├── SKILL.md                              # Main skill file (REQUIRED)
├── README.md                             # Skill documentation
└── references/                           # Detailed reference docs
    ├── principles.md                     # Deep dive into principles
    ├── phases.md                         # Comprehensive phase guidance
    ├── maturity.md                       # Maturity assessment framework
    ├── domains-capabilities.md           # All 22 capabilities
    ├── personas.md                       # Persona responsibilities
    └── terminology.md                    # FinOps glossary
```

## 💡 Common Use Cases

### For FinOps Practitioners
- "How do I assess our FinOps maturity?"
- "What's the best tagging strategy for cost allocation?"
- "How do I implement chargeback vs. showback?"
- "What KPIs should I track at Walk maturity?"

### For Engineers
- "Should I buy Reserved Instances or Savings Plans?"
- "How do I rightsize my EC2 instances?"
- "What's the best way to handle shared costs?"
- "How do I architect for cloud cost efficiency?"

### For Finance Teams
- "How do I forecast cloud costs accurately?"
- "What's the difference between amortized and unblended costs?"
- "How do I set up cloud budgets?"
- "When should we use chargeback vs. showback?"

### For Leadership
- "What's the ROI of implementing FinOps?"
- "How do I structure a FinOps team?"
- "What governance policies should we establish?"
- "How do we balance cost optimization with innovation?"

## 🎓 Key Features

### Progressive Disclosure
- **SKILL.md** (~500 lines): Core framework overview, quick reference, common tasks
- **Reference files** (~2000 lines total): Deep dives into specific topics
- **On-demand loading**: Agent loads detailed docs only when needed

### Framework Alignment
Every response is grounded in:
- ✅ The 6 FinOps Principles
- ✅ Current maturity level (Crawl/Walk/Run)
- ✅ Relevant capabilities and domains
- ✅ Cross-functional persona involvement
- ✅ Business value focus

### Practical Guidance
Includes step-by-step instructions for:
- Building tagging strategies
- Optimizing commitment discounts
- Creating forecasts
- Conducting maturity assessments
- Implementing anomaly management
- Establishing governance policies

## 📊 Skill Metadata

```yaml
name: finops
description: Expert FinOps guidance for cloud cost optimization and financial management
license: MIT
compatibility: Requires access to cloud billing data when implementing recommendations
version: "1.0"
framework-version: "2024"
```

## 🔧 Technical Details

### Skill Specification Compliance
This skill follows the [Agent Skills Specification](https://agentskills.io/specification):
- ✅ Valid skill name (`finops`)
- ✅ Properly formatted YAML frontmatter
- ✅ Description under 1024 characters with keywords
- ✅ Progressive disclosure pattern
- ✅ Organized reference documentation

### Activation Keywords
The skill activates for queries about:
- Cloud cost management, optimization, reduction
- FinOps, finops, cloud financial operations
- AWS/Azure/GCP billing, costs, spending
- Reserved Instances, Savings Plans, Committed Use Discounts
- Cost allocation, tagging, showback, chargeback
- Forecasting, budgeting, unit economics
- Rightsizing, waste elimination, optimization
- Cloud governance, policies, automation

## 📚 Reference Documentation

Each reference file provides deep expertise:

| File | Focus | Key Content |
|------|-------|-------------|
| **principles.md** | The 6 Principles | Anti-patterns, tensions, applications |
| **phases.md** | Inform/Optimize/Operate | Phase activities, iteration cadence, KPIs |
| **maturity.md** | Crawl/Walk/Run | Assessment framework, progression guidance |
| **domains-capabilities.md** | 22 Capabilities | Detailed activities, metrics, dependencies |
| **personas.md** | Stakeholder roles | Responsibilities, RACI, communication |
| **terminology.md** | FinOps glossary | 80+ terms, acronyms, definitions |

## 🌟 Example Interactions

### Example 1: Commitment Discount Strategy
```
User: We have $50K/month in steady EC2 usage. Should we buy RIs or Savings Plans?

Agent (using finops skill):
Based on the FinOps Framework, here's my recommendation:

1. ANALYZE USAGE PATTERNS (Inform Phase)
   - Review 90+ days of historical usage
   - Identify truly steady-state workloads
   - Consider future growth plans

2. START WITH SAVINGS PLANS (Recommended)
   - More flexibility than Standard RIs
   - Can apply across instance families
   - 20-66% discount range
   - Target 70% coverage initially

3. KEY METRICS TO TRACK
   - Coverage: Target 70% (Walk maturity)
   - Utilization: Target 80%+
   - Break-even: <9 months

4. COORDINATE WITH WORKLOAD OPTIMIZATION
   - Don't commit to waste (Principle #2)
   - Rightsize first, then commit

This aligns with Principle #6 (variable cost model) by committing
to baseline while keeping growth variable.

Would you like help calculating the specific commitment amount?
```

### Example 2: Building a FinOps Practice
```
User: We're new to cloud and costs are growing. How do we start FinOps?

Agent (using finops skill):
Great question! Let's start at Crawl maturity with quick wins:

PHASE 1: INFORM (First 30 days)
1. Set up data ingestion (AWS CUR/Azure Cost Export/GCP BigQuery)
2. Implement basic allocation (by account/subscription/project)
3. Create executive dashboard (top cost drivers)
4. Set up anomaly alerts (>20% daily changes)

PHASE 2: OPTIMIZE (Days 31-60)
5. Identify obvious waste (unattached volumes, unused IPs)
6. Implement dev/test scheduling
7. Start basic rightsizing

PHASE 3: OPERATE (Days 61-90)
8. Establish weekly cost review meetings
9. Define mandatory tags (CostCenter, Owner, Environment)
10. Create basic governance policies

PERSONAS TO ENGAGE:
- FinOps Practitioner: Lead the initiative (you?)
- Engineering: Implement optimizations
- Finance: Budget alignment
- Leadership: Executive sponsorship (CRITICAL)

QUICK WINS TO DEMONSTRATE VALUE:
- Delete unused resources: 100% savings on waste
- Schedule non-prod: 60-70% savings on dev/test
- Basic rightsizing: 20-50% on over-provisioned

Start small, show value, then expand!
```

## 🤝 Contributing

This skill references the FinOps framework. To suggest improvements:

1. **Review the source**: https://www.finops.org/framework/
2. **Identify gaps**: Compare skill content to current framework
3. **Update relevant files**: SKILL.md for core changes, references/*.md for details
4. **Test thoroughly**: Verify responses remain framework-aligned
5. **Update metadata**: Version numbers and dates

## 📖 Additional Resources

- **FinOps Framework**: https://www.finops.org/framework/
- **FOCUS Specification**: https://focus.finops.org/
- **Training & Certification**: FinOps Certified Practitioner

## 📄 License

MIT License

This skill is independently maintained and is not affiliated with or endorsed by the FinOps Foundation.

## 📋 Version History

- **v1.0** (January 2026)
  - Initial comprehensive release
  - Complete framework coverage (2024 version)
  - All 6 principles, 3 phases, 22 capabilities
  - Progressive disclosure structure
  - Agent Skills specification compliant

## 🙏 Acknowledgments

This skill draws on publicly available FinOps framework concepts and the broader community of FinOps practitioners.

---

**Ready to maximize your cloud business value?** Install the skill and start asking FinOps questions!

For installation help, see [INSTALLATION.md](INSTALLATION.md)
