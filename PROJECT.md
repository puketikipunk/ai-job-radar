# CareerPilot

## Product summary

CareerPilot is a configurable job-discovery and job-search support tool. Its first user is an Engineering Project Manager in Ireland with a technical, regulated-software background. It should turn a fragmented daily search into a concise, trustworthy digest of relevant roles.

The repository is named `ai-job-radar`; the product and Python application are named CareerPilot.

## First-release outcome

On a schedule, CareerPilot collects job listings from approved company career pages and other permitted public sources; normalises and deduplicates them; applies transparent rule-based relevance scoring; stores the results; and emails a digest of new high-value opportunities.

The initial profile prioritises Engineering Project Manager, Technical Program Manager, Delivery Manager, software/engineering programme, PMO, and engineering operations roles in Cork, hybrid Cork, and remote-in-Ireland settings. It should down-rank or exclude unrelated construction, marketing, clinical, finance, and ERP/SAP roles.

## Product boundaries

CareerPilot does not scrape websites that prohibit automation, circumvent authentication or bot protections, submit applications, or make eligibility claims about employers. It surfaces evidence and links; the user remains responsible for reviewing a role and applying.

AI-assisted matching, CV tailoring, cover letters, application tracking, analytics, and a dashboard are planned follow-on capabilities. They must not delay the reliable daily-digest workflow.

## Success measures

- A scheduled run completes reliably and produces an understandable result.
- New jobs appear once, with direct source links and an explanation of their score.
- The user can change target roles, locations, exclusions, sources, and delivery settings without editing application code.
- Failures in one source do not prevent processing the rest.

See [the vision](docs/vision.md), [architecture](docs/architecture.md), and [roadmap](ROADMAP.md) for detail.

