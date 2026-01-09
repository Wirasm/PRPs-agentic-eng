name: "React POC Template v1 - Rapid Prototype Development"
description: |
Optimized for creating React-based POCs and prototypes from scratch.
Focuses on concept validation over production quality.
Designed for parallel POC creation (10+ concurrent).
Frontend-only with mocked data.
"Working over excellent" approach for rapid iteration.

---

## Goal

**POC Goal**: [Specific concept to validate - e.g., "Interactive dashboard for data visualization"]

**Deliverable**: [Concrete React artifact - component, page, user flow, integration demo]

**Success Definition**: [How you'll know the concept is validated - e.g., "Stakeholders can navigate core workflow with realistic data"]

## POC Scope & Constraints

**Fidelity Level**: [Demo/MVP]

- **Demo**: Polished UI for stakeholder presentations
- **MVP**: Near-production quality for user testing

**Must Have**: [Core functionality that proves the concept]

- [ ] [Primary user interaction works]
- [ ] [Key data displays correctly with mock data]
- [ ] [Critical user flow is navigable]

**Nice to Have**: [Features that enhance but aren't critical]

- [ ] [Secondary interactions]
- [ ] [Enhanced visual polish]
- [ ] [Additional user personas/flows]

**Won't Have**: [Explicitly excluded to maintain focus]

- [ ] [Real API integration]
- [ ] [Complex error handling]
- [ ] [Performance optimization]
- [ ] [Comprehensive testing]

## Why

**Concept Validation Need**: [What hypothesis are you testing?]

**User Experience Question**: [What UX assumption needs validation?]

**Technical Feasibility**: [What technical approach needs proving?]

**Business Value**: [How does this POC drive decision making?]

## What

**Primary User Journey**: [Step-by-step core flow to demonstrate]

1. [User action/page load]
2. [User interaction with data/UI]
3. [System response/navigation]
4. [Outcome/completion state]

**Key Interactions**: [Critical user interactions that validate concept]

- [Interaction type]: [Expected behavior with mock data]
- [UI element]: [User feedback/system response]

**Visual Requirements**: [UI/UX needs for effective concept validation]

- [Layout/component requirements]
- [Data visualization needs]
- [Interactive element specifications]

### Success Criteria

- [ ] **Core Flow Complete**: Primary user journey works end-to-end with mock data
- [ ] **Key Interactions Functional**: Critical interactions demonstrate concept clearly
- [ ] **Stakeholder Ready**: POC can be demonstrated to decision makers
- [ ] **Concept Validation**: Hypothesis can be tested with realistic user interactions
- [ ] **Documentation Complete**: Assumptions, limitations, and next steps documented

## All Needed Context (POC-Optimized)

### Context Completeness Check

_For POC development: "Does this context enable building a working prototype that validates the core concept?"_

### React Technology Stack

```yaml
# Current Tech Stack Requirements
framework: [React 19/Next.js 15/Vite]
styling: [Tailwind CSS/CSS Modules/styled-components]
components: [shadcn/ui/Material-UI/custom components]
typescript: [Strict mode/Basic types/Zod validation]
testing: [React Testing Library/Vitest/Jest]

# POC-Specific Choices
mock_data: [MSW/Static JSON/faker.js]
data_pattern: [REST API simulation/GraphQL mocks/Static objects]
state_management: [useState/useReducer/Zustand (if complex)]
routing: [React Router/Next.js router/hash routing]
```

### Mock Data Strategy

```yaml
# Primary Mock Approach
strategy: [MSW with faker.js/Static JSON files/Hardcoded objects]
complexity: [Simple objects/Relational data/Complex nested structures]
volume:
  [Small dataset for demos/Medium for realistic testing/Large for performance]

# Data Requirements
entities: [List key data models - User, Product, Order, etc.]
relationships: [How entities connect - one-to-many, many-to-many]
realistic_data:
  [Use faker.js/Real-looking placeholder content/Domain-specific examples]
```

### Similar Examples & Patterns (If Available)

```yaml
# MUST READ - Include these in your context window
- file: [path/to/similar/component.tsx]
  why: [Component structure pattern to follow]
  adapt: [What to modify for POC scope]
  critical: [Key patterns that prevent common React errors]

- url: [React documentation URL with specific section]
  why: [Specific hooks/patterns needed for implementation]
  critical: [Best practices for rapid prototyping]

- example: [Link to similar POC or demo]
  why: [UI/UX pattern inspiration]
  adapt: [How to customize for your concept]
```

### Project Context & Constraints

```yaml
# Development Environment
package_manager: [npm]
build_tool: [Vite]
dev_server: [3212]


# File Structure Convention
poc_directory: [/poc-{name}/src/poc-{name}//demos/{name}]
component_pattern: [PascalCase/kebab-case/existing project convention]
```

## Implementation Blueprint

### POC Architecture

```
/poc-{name}/
├── components/           # Core UI components
│   ├── ui/              # Reusable UI elements
│   ├── features/        # Feature-specific components
│   └── layout/          # Layout components
├── hooks/               # Custom hooks for data/state
│   ├── useMockData.ts   # Mock data fetching
│   └── usePocState.ts   # POC-specific state
├── data/                # Mock data and handlers
│   ├── mocks/           # Static mock data
│   ├── handlers/        # MSW request handlers
│   └── schemas/         # TypeScript types
├── pages/               # Main POC pages/routes
│   ├── index.tsx        # Entry point
│   └── demo/            # Core demo pages
├── styles/              # POC-specific styling
├── tests/               # Basic smoke tests
└── README.md            # POC documentation
```

### Implementation Tasks

**Task 1: CREATE poc-{name} foundation**

- SETUP: React project structure in designated directory
- CONFIGURE: TypeScript config, linting rules, basic dependencies
- INSTALL: Required packages (MSW, faker.js, UI library, etc.)
- MOCK: Initial data structure and MSW setup
- PLACEMENT: Follow project directory conventions
- DOCUMENT: POC scope and setup instructions

**Task 2: CREATE mock data system**

- IMPLEMENT: Mock data generation with faker.js or static data
- FOLLOW: Project data modeling patterns (if existing)
- CREATE: MSW handlers for API simulation
- TYPES: TypeScript interfaces for all data models
- VALIDATE: Mock data covers all POC user scenarios

**Task 3: CREATE core UI components**

- IMPLEMENT: Main POC UI components with TypeScript
- FOLLOW: Existing component patterns and naming conventions
- STYLE: Component styling following project standards
- PROPS: Proper TypeScript interfaces for all props
- RESPONSIVE: Basic mobile-responsive design (if required)

**Task 4: CREATE user flow pages**

- IMPLEMENT: Key pages for primary user journey
- CONNECT: Components with mock data hooks
- NAVIGATE: Routing between POC screens
- STATE: User interaction state management
- DEMO: Complete happy path user experience

**Task 5: CREATE basic interactions**

- IMPLEMENT: Core user interactions (clicks, forms, navigation)
- HANDLE: Form submissions with mock responses
- FEEDBACK: User feedback for interactions (loading states, confirmations)
- ERROR: Basic error boundaries for crash prevention
- ACCESSIBILITY: Basic ARIA labels and keyboard navigation

**Task 6: CREATE validation & documentation**

- IMPLEMENT: Basic smoke tests for core functionality
- VALIDATE: Manual testing of complete user flow
- DOCUMENT: POC assumptions, limitations, and findings
- DEMO: Preparation notes for stakeholder presentations
- NEXT: Recommendations for production implementation

## Validation Loop (POC-Optimized)

### Level 1: Syntax & Build (Immediate Feedback)

```bash
# TypeScript and linting validation
npm run lint                     # ESLint with React/TS rules
npx tsc --noEmit                # Type checking without build
npm run format                   # Prettier formatting

# Build validation
npm run build                    # Production build succeeds
npm run analyze                  # Bundle size analysis (if available)

# Expected: Zero TypeScript errors, successful build, reasonable bundle size
```

### Level 2: Demo Validation (User Experience)

```bash
# Development server
npm run dev                      # Dev server starts successfully
# Manual validation checklist:
# ✓ POC loads without errors
# ✓ Primary user flow navigable
# ✓ Key interactions work with mock data
# ✓ UI renders correctly on desktop/mobile
# ✓ Mock data displays realistically

# Basic automated testing
npm test                         # Smoke tests pass
npm test -- --coverage           # Basic coverage report

# Screenshot/recording for stakeholders
# Document any issues or limitations discovered
```

### Level 3: Concept Validation (Stakeholder & Business)

```bash
# Stakeholder demo preparation
# ✓ Demo script prepared with key talking points
# ✓ Mock data scenarios cover realistic use cases
# ✓ Known limitations documented and communicated
# ✓ Next steps and production requirements identified

# Feedback gathering
# ✓ Stakeholder feedback session conducted
# ✓ User reaction/understanding assessed
# ✓ Concept validation questions answered
# ✓ Decision-making criteria evaluated

# Documentation and next steps
# ✓ POC findings documented
# ✓ Production implementation requirements identified
# ✓ Follow-up actions defined
```

## Final Validation Checklist

### Technical Completeness

- [ ] **TypeScript Strict Mode**: All components and data properly typed
- [ ] **Mock Data Realistic**: Data scenarios represent real-world usage
- [ ] **Component Structure**: Following React best practices and project conventions
- [ ] **Build Process**: POC builds and runs without errors
- [ ] **Basic Testing**: Core functionality has smoke tests

### Feature Completeness

- [ ] **Primary User Flow**: Complete end-to-end journey works
- [ ] **Key Interactions**: Critical user interactions demonstrate concept
- [ ] **Visual Clarity**: UI clearly communicates the concept being validated
- [ ] **Data Integration**: Mock data integration shows realistic usage
- [ ] **Error Handling**: Basic error boundaries prevent crashes

### Business Validation

- [ ] **Concept Demonstrated**: Core hypothesis can be evaluated
- [ ] **Stakeholder Ready**: POC ready for decision-maker review
- [ ] **Limitations Clear**: Known constraints clearly documented
- [ ] **Next Steps Defined**: Production requirements identified
- [ ] **Success Criteria Met**: All original POC goals achieved

## POC Anti-Patterns

### Implementation Anti-Patterns

- ❌ **Don't over-engineer**: Skip complex architecture patterns for POC
- ❌ **Don't implement full error handling**: Focus on happy path demonstration
- ❌ **Don't create comprehensive test suites**: Basic smoke tests only
- ❌ **Don't optimize for performance**: Functionality over optimization
- ❌ **Don't integrate real APIs**: Mock data exclusively
- ❌ **Don't build production features**: Prototype-level implementation only

### Process Anti-Patterns

- ❌ **Don't expand scope during development**: Stick to defined "Must Have" items
- ❌ **Don't perfect the UI**: Good enough for concept validation
- ❌ **Don't implement edge cases**: Focus on primary user journey
- ❌ **Don't build for scalability**: Single-user, demo-focused

### Communication Anti-Patterns

- ❌ **Don't present as production-ready**: Clear POC expectations
- ❌ **Don't hide limitations**: Transparent about what's mocked/limited
- ❌ **Don't promise specific timelines**: POC findings inform estimates
- ❌ **Don't skip documentation**: Future developers need context

### DO Focus On

- ✅ **Concept validation**: Can stakeholders evaluate the core idea?
- ✅ **User journey demonstration**: Primary flow works end-to-end
- ✅ **Visual concept clarity**: UI effectively communicates the concept
- ✅ **Realistic data scenarios**: Mock data represents actual usage
- ✅ **Fast iteration**: Prioritize speed of development and feedback cycles
- ✅ **Clear limitations**: Document assumptions and constraints
- ✅ **Next step clarity**: Production requirements and recommendations

## Parallel POC Considerations

### Unique Identification

- **Naming Convention**: `poc-{feature}-{variant}` (e.g., poc-dashboard-minimal, poc-dashboard-advanced)
- **Directory Structure**: Isolated directory per POC to prevent conflicts
- **Git Strategy**: Separate branches or worktrees for parallel development

### Shared Resources

- **Mock Data Patterns**: Common mock data generation strategies

---

**Remember**: This template optimizes for **rapid concept validation** over **production quality**. The goal is to prove concepts quickly and inform production development decisions, not to build production-ready code.
