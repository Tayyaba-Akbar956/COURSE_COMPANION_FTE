# Documentation Folder

This folder contains **all project documentation** organized in a structured manner.

## Structure

```
docs/
├── specs/                    # Specification documents
│   ├── functional/          # User-facing feature specs (what it does)
│   ├── technical/           # Implementation specs (how it works)
│   ├── api/                 # API contract specs (request/response)
│   └── TEMPLATE-SPEC.md     # Spec template
│
├── decisions/               # Architecture Decision Records (ADRs)
│   ├── approved/            # Approved decisions
│   ├── rejected/            # Rejected decisions
│   └── TEMPLATE-ADR.md      # ADR template
│
├── logs/                    # Conversation logs
│   └── TEMPLATE-LOG.md      # Log template
│
├── approvals/               # Approval tracking
│   ├── pending/             # Awaiting approval
│   ├── approved/            # Approved items
│   ├── rejected/            # Rejected items
│   └── TEMPLATE-APPROVAL.md # Approval template
│
└── skills/                  # Agent skills (AI tutor behaviors)
    ├── concept-explainer.md
    ├── quiz-master.md
    ├── socratic-tutor.md
    └── progress-motivator.md
```

## Quick Links

- [Spec Template](./specs/TEMPLATE-SPEC.md)
- [ADR Template](./decisions/TEMPLATE-ADR.md)
- [Log Template](./logs/TEMPLATE-LOG.md)
- [Approval Template](./approvals/TEMPLATE-APPROVAL.md)

## Usage

### Creating a New Spec

1. Copy `specs/TEMPLATE-SPEC.md`
2. Fill in the template
3. Save as `specs/{type}/SPEC-{TYPE}-{NUMBER}-{feature}-v1.0.md`
4. Request approval in chat
5. After approval, move to `approved/` folder

### Recording a Decision

1. Copy `decisions/TEMPLATE-ADR.md`
2. Fill in context, options, and decision
3. Save as `decisions/ADR-{NUMBER}-{title}.md`
4. Link to approval in `approvals/approved/`

### Logging a Conversation

1. Copy `logs/TEMPLATE-LOG.md`
2. Fill in conversation summary
3. Save as `logs/{YYYY-MM-DD}-session.md`

### Requesting Approval

1. Copy `approvals/TEMPLATE-APPROVAL.md`
2. Fill in approval details
3. Save as `approvals/{pending,approved,rejected}/APPROVAL-{NUMBER}-{ref}.md`

## Naming Conventions

| Document Type | Pattern | Example |
|---------------|---------|---------|
| Functional Spec | `SPEC-F-{NUM}-{feature}-v{version}.md` | `SPEC-F-001-content-delivery-v1.0.md` |
| Technical Spec | `SPEC-T-{NUM}-{feature}-v{version}.md` | `SPEC-T-001-database-schema-v1.0.md` |
| API Spec | `SPEC-A-{NUM}-{feature}-v{version}.md` | `SPEC-A-001-content-apis-v1.0.md` |
| ADR | `ADR-{NUM}-{title}.md` | `ADR-001-technology-stack.md` |
| Log | `{YYYY-MM-DD}-session.md` | `2026-03-29-session.md` |
| Approval | `APPROVAL-{NUM}-{ref}.md` | `APPROVAL-001-spec-f-001.md` |

## Related Documents

- [QWEN.md](../QWEN.md) - Project operating manual
- [README.md](../README.md) - Project overview

---

*Last Updated: March 29, 2026*
