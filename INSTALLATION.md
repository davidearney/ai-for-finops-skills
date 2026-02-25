# FinOps Skill Installation Guide

This guide explains how to install and use the FinOps Framework Expert skill with Claude and agent-based systems.

## Directory Structure

The skill is properly structured according to the Agent Skills specification:

```
finops/
├── SKILL.md                              # Main skill file (REQUIRED)
├── README.md                             # Skill documentation
└── references/                           # Reference documentation
    ├── principles.md                     # The 6 FinOps Principles
    ├── phases.md                         # The 3 Phases (Inform/Optimize/Operate)
    ├── maturity.md                       # Crawl/Walk/Run maturity model
    ├── domains-capabilities.md           # 4 Domains & 22 Capabilities
    ├── personas.md                       # Core and Allied Personas
    └── terminology.md                    # FinOps glossary
```

## Installation Methods

### Method 1: Claude Code CLI (Recommended)

If you're using Claude Code (the CLI tool), place the skill in the skills directory:

1. **Locate your skills directory**:
   - Default location varies by installation
   - Check Claude Code settings for configured skills path

2. **Copy the skill**:
   ```bash
   cp -r finops /path/to/skills/directory/
   ```

3. **Verify installation**:
   - The skill should appear in available skills list
   - Skill name: `finops`

### Method 2: Direct Integration

For custom agent implementations:

1. **Include the skill directory** in your agent's skills path
2. **Configure skill loading** to discover `SKILL.md` files
3. **Enable reference file access** for the `references/` directory

### Method 3: Manual Reference

If not using an automated skill system:

1. **Read the SKILL.md file** for comprehensive instructions
2. **Reference individual files** in `references/` as needed
3. **Use as knowledge base** for FinOps guidance

## Verification

After installation, verify the skill is working:

### Test Query 1: Basic Framework
**Ask**: "What are the 6 FinOps Principles?"

**Expected**: Should list all 6 principles with explanations

### Test Query 2: Practical Guidance
**Ask**: "How do I build a tagging strategy?"

**Expected**: Should provide step-by-step guidance including:
- Defining allocation hierarchy
- Establishing mandatory vs. optional tags
- Creating naming conventions
- Implementing compliance monitoring
- Automation recommendations

### Test Query 3: Maturity Assessment
**Ask**: "What's the difference between Crawl and Walk maturity?"

**Expected**: Should explain maturity levels with KPI targets

## Usage Examples

### Example 1: Cost Optimization
```
User: We're spending too much on AWS. How do we reduce costs?

Agent (using finops skill):
- Assesses current maturity level
- Recommends starting with Inform phase (visibility)
- Identifies quick wins (waste elimination)
- Suggests progression to rate optimization
- Emphasizes value over cost reduction
```

### Example 2: Commitment Discounts
```
User: Should I buy Reserved Instances or Savings Plans?

Agent (using finops skill):
- Explains differences (resource-based vs. spend-based)
- Recommends analyzing usage patterns
- Suggests starting with Savings Plans for flexibility
- Provides target metrics (coverage, utilization)
- Warns about coordinating with workload optimization
```

### Example 3: Building a FinOps Practice
```
User: How do I start a FinOps practice in my organization?

Agent (using finops skill):
- Identifies relevant personas to engage
- Recommends Crawl-level activities
- Suggests quick wins for executive buy-in
- Provides meeting cadence recommendations
- Emphasizes cultural change alongside tooling
```

## Skill Activation

The skill automatically activates when users ask about:

- Cloud cost management
- FinOps practices, principles, or framework
- Cost allocation, tagging, showback, chargeback
- Reserved Instances, Savings Plans, Committed Use Discounts
- Rightsizing, optimization, forecasting, budgeting
- AWS, Azure, or GCP billing and cost management
- Unit economics, KPIs, or cloud financial metrics
- FinOps maturity, assessment, or roadmap planning
- Governance policies, automation, or anomaly detection
- Any cloud financial operations topics

## Configuration

### Compatibility Requirements
The skill metadata specifies:
```yaml
compatibility: Requires access to cloud billing data and cost management tools when implementing recommendations
```

This means:
- The skill provides **guidance** and **recommendations**
- **Implementation** requires access to cloud billing systems
- Some recommendations may need specific cloud provider access

### Tool Permissions
The skill may recommend using:
- Cloud provider CLIs (AWS CLI, Azure CLI, gcloud)
- Cost management tools (native or third-party)
- Data analysis tools (for billing data)
- Automation frameworks

Ensure your environment has appropriate permissions if implementing recommendations.

## Reference Files

The skill uses progressive disclosure for efficient context usage:

### Primary Content (SKILL.md)
Loaded when skill activates. Contains:
- Core framework overview
- 6 Principles, 3 Phases, Maturity Model
- Quick reference for all domains and capabilities
- Common tasks and scenarios
- Response guidelines

### Reference Files (references/*.md)
Loaded on-demand for deep dives:
- **principles.md**: Detailed principle explanations, anti-patterns, tensions
- **phases.md**: Comprehensive phase guidance, iteration cadence
- **maturity.md**: Maturity assessment framework, progression criteria
- **domains-capabilities.md**: All 22 capabilities with detailed activities and KPIs
- **personas.md**: Persona responsibilities, RACI matrices, communication guidance
- **terminology.md**: Complete FinOps glossary and acronyms

## Troubleshooting

### Issue: Skill not found
**Solution**: Verify the directory is named `finops` (lowercase) and contains `SKILL.md`

### Issue: Reference files not loading
**Solution**: Ensure `references/` subdirectory is present with all 6 files

### Issue: Responses lack framework alignment
**Solution**: Check that SKILL.md frontmatter is properly formatted YAML

### Issue: Getting generic cost advice instead of FinOps-specific
**Solution**: Explicitly mention "FinOps" in your query to ensure skill activation

## Updating the Skill

To update the skill with new FinOps framework content:

1. **Review official framework** at https://www.finops.org/framework/
2. **Update relevant files**:
   - Core changes → SKILL.md
   - Principle changes → references/principles.md
   - New capabilities → references/domains-capabilities.md
   - Terminology updates → references/terminology.md
3. **Update metadata** in SKILL.md frontmatter (version, framework-version)
4. **Test** with sample queries to ensure accuracy

## Support and Feedback

- **Framework Documentation**: https://www.finops.org/framework/
- **Issues**: Report skill-specific issues to the skill maintainer

## License

This skill is released under the MIT License. See SKILL.md metadata for details.

This skill is independently maintained and is not affiliated with or endorsed by the FinOps Foundation.

## Version Information

- **Current Skill Version**: 1.0
- **Framework Version**: 2024
- **Last Updated**: January 2026
- **Skill Name**: `finops`
- **Skill Description**: Expert FinOps guidance for cloud cost optimization and financial management

## Next Steps

After installation:

1. ✅ **Test the skill** with the verification queries above
2. ✅ **Review SKILL.md** to understand full capabilities
3. ✅ **Explore reference files** for deep dives on specific topics
4. ✅ **Ask FinOps questions** and see the framework-aligned responses
5. ✅ **Provide feedback** on skill effectiveness and accuracy

## Advanced Usage

### For FinOps Practitioners
Use this skill to:
- Validate your approaches against the framework
- Get quick answers to framework questions
- Generate content for stakeholder communication
- Plan maturity progression roadmaps
- Research best practices for specific capabilities

### For Developers
Use this skill to:
- Understand cost implications of architecture decisions
- Learn tagging and allocation best practices
- Get guidance on cost-effective cloud design
- Understand FinOps collaboration expectations

### For Leadership
Use this skill to:
- Understand FinOps value proposition
- Learn about maturity progression
- Get guidance on team structure and governance
- Understand cross-functional collaboration needs

### For Finance Teams
Use this skill to:
- Learn cloud financial management concepts
- Understand forecasting and budgeting best practices
- Get guidance on chargeback implementation
- Learn about cloud-specific financial metrics
