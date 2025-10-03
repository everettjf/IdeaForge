# IdeaForge


<!-- Author: everettjf -->
```bash
export OPENAI_API_KEY=sk-...
git clone git@github.com:everettjf/IdeaForge.git
cd IdeaForge
uv sync --extra dev
uv run ideaforge plan "an todo list app with swiftui on ios"
```


<p align="center">
  <img src="https://img.shields.io/badge/IdeaForge-LangGraph%20Planner-5531FF?style=for-the-badge" alt="IdeaForge badge" />
</p>

<h1 align="center">IdeaForge</h1>

<p align="center">
  Turn a one-line product idea into a launch-ready, multi-level roadmap powered by LangGraph, ReAct reasoning, and a vibrant CLI experience.
</p>

<p align="center">
  <a href="https://github.com/everettjf/IdeaForge/stargazers"><img src="https://img.shields.io/github/stars/everettjf/IdeaForge?color=F7B500&style=for-the-badge" alt="GitHub stars"></a>
  <a href="https://github.com/everettjf/IdeaForge/issues"><img src="https://img.shields.io/github/issues/everettjf/IdeaForge?color=FF5C93&style=for-the-badge" alt="GitHub issues"></a>
  <a href="#-star-history"><img src="https://img.shields.io/badge/Star%20History-Chart-00BBDC?style=for-the-badge" alt="Star history"></a>
  <a href="https://www.python.org/downloads/release/python-3110/"><img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python version"></a>
</p>

---

## ✨ Why IdeaForge?

<table>
  <tr>
    <td><strong>Plan & Execute Pipeline</strong></td>
    <td>LangGraph orchestrates a planner pass and a ReAct executor loop to flesh out each objective.</td>
  </tr>
  <tr>
    <td><strong>Launch-Oriented Tree</strong></td>
    <td>Always ends with a publish/deploy track so your roadmap spans research through release.</td>
  </tr>
  <tr>
    <td><strong>Working Status Stream</strong></td>
    <td>Rich-powered spinner mirrors a “Working…” console, echoing every milestone while models run.</td>
  </tr>
  <tr>
    <td><strong>Reasoning Visibility</strong></td>
    <td>Optional ReAct analysis panel makes the AI’s decision trail easy to audit or iterate on.</td>
  </tr>
</table>

---

## 🚀 Quick Start

```bash
# 1. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone and enter the project
git clone https://github.com/everettjf/IdeaForge.git
cd IdeaForge

# 3. Provide your OpenAI key
export OPENAI_API_KEY=sk-...

# 4. Install dependencies (creates .venv)
uv sync --extra dev
```

---

## 🧠 Usage

```bash
uv run ideaforge plan "AI-powered personal finance web app"
# or, equivalently
uv run ideaforge "AI-powered personal finance web app"
```

**Key options**
- `--plan-model`: planner stage model (default `gpt-4o-mini`).
- `--react-model`: optional executor override.
- `--temperature` / `--react-temperature`: sampling control for each stage.
- `--no-show-analysis`: hide the ReAct reasoning trace.

> Tip: If `OPENAI_API_KEY` is not set, the CLI will securely prompt for it before planning.

---

## 📟 CLI Showcase

```
╭─ IdeaForge ─╮
│ Idea: idea  │
╰─────────────╯
a todo list app on ios with swiftui
╭─────────────────────────────────────────────── Launch TODO Tree ────────────────────────────────────────────────╮
│ ├── Market Research → Market Research Report                                                                    │
│ │   summary: Conduct thorough market research to understand user needs and competitive landscape.               │
│ │   ├── Define Research Objectives → Document outlining research objectives.                                    │
│ │   │   summary: Establish clear objectives for what the market research aims to achieve.                       │
│ │   ├── Identify User Demographics and Competitors → List of user demographics and competitors.                 │
│ │   │   summary: Research and list key user demographics and competitors in the market.                         │
│ │   ├── Develop Survey and Interview Guide → Survey and interview guide document.                               │
│ │   │   summary: Create a comprehensive guide for surveys and interviews to gather user insights.               │
│ │   ├── Plan Participant Outreach → Outreach plan document.                                                     │
│ │   │   summary: Design a strategy to reach out to potential survey and interview participants.                 │
│ │   │   ├── Identify Target Participants → Target participant list.                                             │
│ │   │   │   summary: Create a list of potential participants based on user demographics.                        │
│ │   │   └── Develop Outreach Materials → Outreach materials.                                                    │
│ │   │       summary: Create emails and promotional materials for participant recruitment.                       │
│ │   ├── Data Collection → Raw data collected from surveys and interviews.                                       │
│ │   │   summary: Execute the surveys and interviews to collect data from participants.                          │
│ │   ├── Data Analysis → Data analysis report.                                                                   │
│ │   │   summary: Analyze the collected data to extract meaningful insights and trends.                          │
│ │   ├── Draft Market Research Report → Draft of the market research report.                                     │
│ │   │   summary: Compile findings and insights into a structured market research report.                        │
│ │   ├── Review and Finalize Report → Final market research report.                                              │
│ │   │   summary: Review the draft report for accuracy and completeness, then finalize it.                       │
│ │   └── Prepare for Distribution → Distribution plan.                                                           │
│ │       summary: Plan how to distribute the report and present findings to stakeholders.                        │
│ ├── Define Product Requirements → Product Requirements Document (PRD)                                           │
│ │   summary: Outline the key features and functionalities based on market research findings.                    │
│ │   ├── Conduct Market Research → Market Research Report                                                        │
│ │   │   summary: Analyze current market trends and competitor products.                                         │
│ │   │   ├── Identify Competitors → Competitor Analysis Document                                                 │
│ │   │   │   summary: List key competitors and their product offerings.                                          │
│ │   │   └── Analyze Market Trends → Market Trends Report                                                        │
│ │   │       summary: Research emerging trends in the industry.                                                  │
│ │   ├── Stakeholder Interviews → Interview Summary Report                                                       │
│ │   │   summary: Gather insights from potential users and stakeholders.                                         │
│ │   │   ├── Prepare Interview Questions → Interview Question Set                                                │
│ │   │   │   summary: Draft a set of questions to guide the interviews.                                          │
│ │   │   └── Conduct Interviews → Interview Transcripts                                                          │
│ │   │       summary: Interview selected stakeholders and users.                                                 │
│ │   ├── Feature Prioritization → Feature Prioritization Matrix                                                  │
│ │   │   summary: Prioritize features based on the gathered insights.                                            │
│ │   ├── Draft Product Requirements Document → Initial PRD Draft                                                 │
│ │   │   summary: Create an initial draft of the PRD based on research and interviews.                           │
│ │   ├── Review and Collect Feedback → Feedback Summary Document                                                 │
│ │   │   summary: Circulate the PRD draft for feedback from stakeholders.                                        │
│ │   ├── Refine PRD → Refined PRD                                                                                │
│ │   │   summary: Incorporate feedback and refine the PRD.                                                       │
│ │   ├── Validate Requirements → Validation Report                                                               │
│ │   │   summary: Validate the PRD with potential users through surveys or focus groups.                         │
│ │   ├── Final Review of PRD → Final Review Notes                                                                │
│ │   │   summary: Conduct a final review of the PRD with stakeholders.                                           │
│ │   ├── Obtain Approval → Approved PRD                                                                          │
│ │   │   summary: Get formal approval of the PRD from key stakeholders.                                          │
│ │   └── Prepare for Launch → Launch Readiness Checklist                                                         │
│ │       summary: Ensure all teams are aligned with the product requirements.                                    │
│ ├── Design Prototyping → Interactive Prototype                                                                  │
│ │   summary: Create wireframes and prototypes to visualize the product's user interface and experience.         │
│ │   ├── User Research → User Personas                                                                           │
│ │   │   summary: Conduct research to understand the target audience and their needs.                            │
│ │   │   ├── Conduct Surveys → Survey Results                                                                    │
│ │   │   │   summary: Create and distribute surveys to gather user insights.                                     │
│ │   │   └── Interviews → Interview Transcripts                                                                  │
│ │   │       summary: Conduct interviews with potential users to gather qualitative data.                        │
│ │   ├── Wireframing → Wireframe Designs                                                                         │
│ │   │   summary: Create wireframes to visualize the product's structure and layout.                             │
│ │   │   ├── Sketch Initial Wireframes → Initial Sketches                                                        │
│ │   │   │   summary: Draw rough sketches of the user interface.                                                 │
│ │   │   ├── Digital Wireframe Creation → Digital Wireframes                                                     │
│ │   │   │   summary: Use design tools to create digital wireframes.                                             │
│ │   │   └── Stakeholder Review → Feedback Document                                                              │
│ │   │       summary: Present wireframes to stakeholders for feedback.                                           │
│ │   ├── Prototyping → Interactive Prototype                                                                     │
│ │   │   summary: Develop an interactive prototype based on the wireframes.                                      │
│ │   │   ├── Create Low-Fidelity Prototype → Low-Fidelity Prototype                                              │
│ │   │   │   summary: Build a low-fidelity interactive prototype.                                                │
│ │   │   ├── Usability Testing (Low-Fidelity) → Usability Test Results                                           │
│ │   │   │   summary: Conduct usability testing on the low-fidelity prototype.                                   │
│ │   │   ├── High-Fidelity Prototype Development → High-Fidelity Prototype                                       │
│ │   │   │   summary: Develop a high-fidelity prototype incorporating design elements.                           │
│ │   │   ├── Usability Testing (High-Fidelity) → Final Usability Test Results                                    │
│ │   │   │   summary: Conduct usability testing on the high-fidelity prototype.                                  │
│ │   │   └── Prototype Refinement → Final Prototype                                                              │
│ │   │       summary: Refine the prototype based on usability test feedback.                                     │
│ │   ├── Documentation and Handoff → Prototype Documentation                                                     │
│ │   │   summary: Prepare documentation for the prototype and handoff to development.                            │
│ │   │   ├── Create Design Specifications → Design Specification Document                                        │
│ │   │   │   summary: Document design specifications for developers.                                             │
│ │   │   └── Handoff Meeting → Handoff Meeting Notes                                                             │
│ │   │       summary: Conduct a meeting with the development team to hand off the prototype.                     │
│ │   └── Launch Readiness → Launch Plan                                                                          │
│ │       summary: Prepare for the launch of the product.                                                         │
│ │       ├── Marketing Strategy Development → Marketing Plan                                                     │
│ │       │   summary: Create a marketing strategy for the product launch.                                        │
│ │       ├── User Onboarding Plan → Onboarding Plan                                                              │
│ │       │   summary: Develop a user onboarding plan to facilitate user adoption.                                │
│ │       └── Final Review → Final Review Document                                                                │
│ │           summary: Conduct a final review of all materials before launch.                                     │
│ ├── Development Phase → Shippable Product                                                                       │
│ │   summary: Build the application or web product based on the defined requirements and designs.                │
│ │   ├── Requirements Gathering → Documented requirements and designs.                                           │
│ │   │   summary: Collect and confirm all requirements and designs.                                              │
│ │   │   ├── Review existing documentation → Initial review notes.                                               │
│ │   │   │   summary: Analyze any existing requirements and designs.                                             │
│ │   │   └── Conduct stakeholder interviews → Stakeholder interview notes.                                       │
│ │   │       summary: Engage with stakeholders to gather additional requirements.                                │
│ │   ├── Development Setup → Configured development environment.                                                 │
│ │   │   summary: Prepare the development environment and tools.                                                 │
│ │   │   ├── Select development tools → List of selected tools.                                                  │
│ │   │   │   summary: Choose appropriate tools and technologies for development.                                 │
│ │   │   └── Set up version control → Version control repository.                                                │
│ │   │       summary: Implement a version control system for code management.                                    │
│ │   ├── Core Development → Developed application.                                                               │
│ │   │   summary: Build the application based on the gathered requirements.                                      │
│ │   │   ├── Implement front-end components → Front-end codebase.                                                │
│ │   │   │   summary: Develop user interface components.                                                         │
│ │   │   └── Implement back-end services → Back-end codebase.                                                    │
│ │   │       summary: Develop server-side logic and APIs.                                                        │
│ │   ├── Testing Phase → Tested application.                                                                     │
│ │   │   summary: Ensure the application is functioning as intended.                                             │
│ │   │   ├── Conduct unit testing → Unit test results.                                                           │
│ │   │   │   summary: Test individual components for correctness.                                                │
│ │   │   ├── Perform integration testing → Integration test results.                                             │
│ │   │   │   summary: Test the integration of components.                                                        │
│ │   │   └── User Acceptance Testing (UAT) → UAT feedback report.                                                │
│ │   │       summary: Validate the application with end-users.                                                   │
│ │   ├── Launch Preparation → Launch-ready product.                                                              │
│ │   │   summary: Prepare for the product launch.                                                                │
│ │   │   ├── Create deployment documentation → Deployment documentation.                                         │
│ │   │   │   summary: Document the deployment process and user guides.                                           │
│ │   │   └── Finalize launch strategy → Launch strategy document.                                                │
│ │   │       summary: Plan marketing and communication for the launch.                                           │
│ │   └── Product Launch → Launched application.                                                                  │
│ │       summary: Execute the launch of the application.                                                         │
│ │       ├── Deploy application to production → Deployed application.                                            │
│ │       │   summary: Move the application to the live environment.                                              │
│ │       └── Monitor post-launch performance → Post-launch report.                                               │
│ │           summary: Track application performance and user feedback.                                           │
│ └── Testing and QA → Test Report and Final Product                                                              │
│     summary: Conduct thorough testing to ensure the product is functional, user-friendly, and bug-free.         │
│     ├── Define Testing Scope → Testing Scope Document                                                           │
│     │   summary: Identify the areas of the product that require testing.                                        │
│     ├── Develop Test Plan → Test Plan Document                                                                  │
│     │   summary: Create a detailed plan outlining testing methodologies and timelines.                          │
│     ├── Prepare Testing Environment → Testing Environment Setup                                                 │
│     │   summary: Set up the necessary hardware and software for testing.                                        │
│     ├── Create Test Cases → Test Cases Document                                                                 │
│     │   summary: Develop test cases for all functionalities and user scenarios.                                 │
│     ├── Execute Tests → Test Execution Results                                                                  │
│     │   summary: Perform tests according to the test plan and document results.                                 │
│     ├── Log Bugs and Issues → Bug Log                                                                           │
│     │   summary: Record defects and issues found during testing.                                                │
│     ├── Prioritize Bugs → Prioritized Bug List                                                                  │
│     │   summary: Classify and prioritize bugs based on severity and impact.                                     │
│     ├── Fix Bugs → Bug Fixes                                                                                    │
│     │   summary: Collaborate with the development team to resolve identified issues.                            │
│     ├── Re-test → Re-test Results                                                                               │
│     │   summary: Conduct re-testing to ensure all bugs have been fixed.                                         │
│     ├── User Acceptance Testing (UAT) → UAT Feedback                                                            │
│     │   summary: Involve end-users to validate that the product meets their needs.                              │
│     ├── Finalize Test Report → Final Test Report                                                                │
│     │   summary: Compile a report detailing test results, issues found, and resolutions.                        │
│     ├── Launch Readiness Review → Launch Readiness Assessment                                                   │
│     │   summary: Assess the product's readiness for launch based on testing outcomes.                           │
│     ├── Deploy Final Product → Live Product                                                                     │
│     │   summary: Launch the product to the production environment.                                              │
│     └── Post-launch Monitoring → Post-launch Monitoring Report                                                  │
│         summary: Monitor the product after launch for any unforeseen issues.                                    │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭──────────────────────────────────────────────── ReAct Analysis ─────────────────────────────────────────────────╮
│ - Market Research: Define objectives and scope of market research. | Identify key user demographics and         │
│ competitive landscape. | Develop survey and interview guide. | Plan outreach for participants. | Collect data   │
│ through surveys and interviews. | Analyze collected data for insights. | Draft the market research report. |    │
│ Review and finalize the report. | Prepare for distribution and presentation.                                    │
│ - Define Product Requirements: Market Research | Stakeholder Interviews | Feature Prioritization | Drafting PRD │
│ | Review and Feedback | Refinement | Validation | Final Review | Approval | Launch Readiness                    │
│ - Design Prototyping: Identify the target audience and their needs. | Research best practices in UI/UX design.  │
│ | Define the core features and functionalities of the product. | Sketch initial wireframes based on user needs  │
│ and features. | Select appropriate tools for prototyping (e.g., Figma, Adobe XD). | Create low-fidelity         │
│ wireframes to visualize layout and flow. | Gather feedback on low-fidelity wireframes from stakeholders. |      │
│ Iterate on wireframes based on feedback. | Develop high-fidelity prototypes incorporating visual design         │
│ elements. | Conduct usability testing with high-fidelity prototypes. | Analyze usability testing results and    │
│ refine the prototype. | Prepare documentation for the prototype for handoff to development. | Plan for launch   │
│ readiness including marketing and user onboarding.                                                              │
│ - Development Phase: Identify and gather all defined requirements and designs. | Break down requirements into   │
│ actionable tasks. | Establish a development environment and necessary tools. | Assign roles and                 │
│ responsibilities to team members. | Implement the core functionalities based on requirements. | Conduct unit    │
│ testing for individual components. | Integrate components and perform integration testing. | Validate the       │
│ application against requirements and designs. | Prepare deployment documentation and user guides. | Conduct     │
│ user acceptance testing (UAT). | Finalize the product for launch. | Plan and execute the launch strategy.       │
│ - Testing and QA: Define Testing Scope | Develop Test Plan | Prepare Testing Environment | Create Test Cases |  │
│ Execute Tests | Log Bugs and Issues | Prioritize Bugs | Fix Bugs | Re-test | User Acceptance Testing (UAT) |    │
│ Finalize Test Report | Launch Readiness Review | Deploy Final Product | Post-launch Monitoring                  │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

## 🧪 Development

```bash
uv run pytest
```

> Tip: If you do not configure LangSmith credentials, warnings about missing API keys are expected.

### Project Layout

```
src/ideaforge/       # planner + CLI
tests/               # unit tests with stubbed LangGraph models
pyproject.toml       # uv + setuptools configuration
```

---

## 🗺 Roadmap

- [ ] Web dashboard for browsing generated trees
- [ ] Export to Notion / Linear / Jira
- [ ] Optional post-plan summarization report
- [x] Live CLI working status stream

Feel free to open an issue to suggest new features!

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=everettjf/IdeaForge&type=Date)](https://star-history.com/#everettjf/IdeaForge)

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing`).
3. Make your changes and add tests where relevant.
4. Run `uv run pytest`.
5. Open a pull request with a concise summary.

---

## 📄 License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.