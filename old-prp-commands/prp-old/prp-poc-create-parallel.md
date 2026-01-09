# Create Parallel React POCs

## Request: $ARGUMENTS

Usage: `/prp-poc-create-parallel [number_of_demos] "[problem_statement]"`
Example: `/prp-poc-create-parallel 5 "create a dashboard for tracking team productivity with real-time metrics"`

## Parallel POC Creation Mission

Create multiple React POC variations simultaneously to **maximize concept validation** through diverse implementation approaches. This command generates PRPs for parallel execution using specialized UI/UX and User Journey agents.

**Critical Understanding**: Each POC targets different aspects of the same problem:
- Different UI/UX approaches (minimal, polished, experimental)
- Different user journey focuses (power user, casual user, admin)
- Different technical approaches (component-heavy, page-based, single-file)
- Different fidelity levels (wireframe, demo, MVP)

## Parallel Creation Strategy

### Agent Specialization Pattern

For **N demos** requested, create **N pairs** of specialized agents:
- **N UI-UX Agents**: Each focusing on different design approaches
- **N User Journey Agents**: Each targeting different user personas/flows

**Agent Assignment Matrix:**
```yaml
Demo 1: @ui-ux-agent (Minimal/Clean) + @user-journey-agent (Power User)
Demo 2: @ui-ux-agent (Polished/Professional) + @user-journey-agent (Casual User) 
Demo 3: @ui-ux-agent (Experimental/Modern) + @user-journey-agent (Admin User)
Demo 4: @ui-ux-agent (Dashboard-Heavy) + @user-journey-agent (Mobile-First)
Demo 5: @ui-ux-agent (Component-Library) + @user-journey-agent (Accessibility-First)
```

### POC Variation Strategy

Each POC should explore different aspects:

**Design Variations:**
- **Minimal**: Clean, simple, content-focused
- **Polished**: Professional, brand-aligned, stakeholder-ready
- **Experimental**: Modern patterns, micro-interactions, innovative UI
- **Dashboard-Heavy**: Data visualization focused, charts/graphs
- **Component-Library**: Showcases reusable design system components

**User Journey Variations:**
- **Power User**: Feature-rich, keyboard shortcuts, advanced workflows
- **Casual User**: Simplified navigation, guided experiences, fewer options
- **Admin User**: Management interfaces, bulk actions, system controls
- **Mobile-First**: Touch-optimized, responsive, gesture-based
- **Accessibility-First**: Screen reader optimized, keyboard navigation, high contrast

## Implementation Process

### Step 1: Problem Analysis & POC Strategy

Analyze the problem statement and create a **parallel execution plan**:

1. **Parse Request Arguments**
   - Extract number of demos requested (default: 5)
   - Analyze problem statement for key concepts and requirements
   - Identify core user personas and interaction patterns

2. **Design POC Matrix**
   - Create unique combination of UI approach + User journey for each demo
   - Ensure each POC validates different aspects of the problem
   - Plan directory structure: `poc-{problem-slug}-{variant-number}`

### Step 2: Parallel Agent Research

**Execute all research agents in PARALLEL using Task tool:**

```yaml
# Spawn N pairs of agents simultaneously
Task 1 - @ui-ux-agent for Demo 1:
"Analyze the problem: '{problem_statement}' and design a MINIMAL/CLEAN UI approach.
Focus on: Clean typography, generous whitespace, content-first design.
Research component patterns and create UI specifications for a React POC.
Target: Stakeholder presentations requiring clear concept demonstration.
Return: UI component architecture, styling approach, and design specifications."

Task 2 - @user-journey-agent for Demo 1:
"Analyze the problem: '{problem_statement}' and design a POWER USER journey.
Focus on: Advanced features, keyboard shortcuts, efficient workflows.
Research user patterns and create journey specifications for React POC.
Target: Users who need maximum functionality and control.
Return: User flow architecture, interaction patterns, and journey specifications."

Task 3 - @ui-ux-agent for Demo 2:
"Analyze the problem: '{problem_statement}' and design a POLISHED/PROFESSIONAL UI approach.
Focus on: Brand alignment, professional aesthetics, stakeholder-ready presentation.
Research premium component patterns and create UI specifications for React POC.
Target: Executive demos and client presentations.
Return: UI component architecture, styling approach, and design specifications."

Task 4 - @user-journey-agent for Demo 2:
"Analyze the problem: '{problem_statement}' and design a CASUAL USER journey.
Focus on: Simplified navigation, guided experiences, progressive disclosure.
Research beginner-friendly patterns and create journey specifications for React POC.
Target: Users new to the system who need guidance and simplicity.
Return: User flow architecture, interaction patterns, and journey specifications."

# Continue pattern for remaining demos...
```

### Step 3: PRP Generation from Research

After all research agents complete, **synthesize results into POC PRPs**:

1. **Use prp_poc_react.md template** for each POC
2. **Incorporate agent research** into context sections
3. **Customize each PRP** based on UI/UX + User Journey specifications
4. **Create unique identifiers** for parallel development

### Step 4: POC Specification Matrix

Generate **N PRPs** with these variations:

**POC 1: Minimal Power User**
```yaml
poc_name: "poc-{problem-slug}-minimal-power"
ui_approach: "Clean, typography-focused, content-first design"
user_journey: "Advanced features, keyboard shortcuts, efficient workflows"
fidelity: "Demo"
unique_aspects: "Focuses on functionality over aesthetics, rapid interaction patterns"
```

**POC 2: Polished Casual User**
```yaml
poc_name: "poc-{problem-slug}-polished-casual"
ui_approach: "Professional aesthetics, brand-aligned, premium components"
user_journey: "Guided experience, progressive disclosure, help tooltips"
fidelity: "MVP"
unique_aspects: "Executive-ready presentation with beginner-friendly flows"
```

**POC 3: Experimental Admin**
```yaml
poc_name: "poc-{problem-slug}-experimental-admin"
ui_approach: "Modern patterns, micro-interactions, innovative UI elements"
user_journey: "Management interfaces, bulk actions, system administration"
fidelity: "Demo"
unique_aspects: "Cutting-edge design patterns with administrative power features"
```

**POC 4: Dashboard Mobile-First**
```yaml
poc_name: "poc-{problem-slug}-dashboard-mobile"
ui_approach: "Data visualization heavy, charts and metrics focused"
user_journey: "Touch-optimized interactions, responsive design, gesture-based"
fidelity: "Demo"
unique_aspects: "Analytics dashboard optimized for mobile devices"
```

**POC 5: Component-Library Accessible**
```yaml
poc_name: "poc-{problem-slug}-components-a11y"
ui_approach: "Design system showcase, reusable component patterns"
user_journey: "Screen reader optimized, keyboard navigation, inclusive design"
fidelity: "MVP"
unique_aspects: "Accessibility-first design with component library demonstration"
```

## PRP Output Structure

For each POC, generate a complete PRP file:

**File:** `PRPs/poc-{problem-slug}-{variant}.md`

**Content Structure:**
1. **Goal Section**: Specific to UI approach + User journey combination
2. **POC Scope**: Tailored to the variation's unique focus
3. **Context**: Incorporates both UI-UX and User Journey agent research
4. **Implementation Blueprint**: Customized task sequence for the variant
5. **Validation Loop**: POC-appropriate validation for the specific approach

## Parallel Execution Preparation

### Project Structure Setup

```
react-poc-project/
├── public/
├── src/
│   ├── poc-{problem-slug}-minimal-power/
│   ├── poc-{problem-slug}-polished-casual/
│   ├── poc-{problem-slug}-experimental-admin/
│   ├── poc-{problem-slug}-dashboard-mobile/
│   ├── poc-{problem-slug}-components-a11y/
│   └── App.tsx  # Main navigation between POCs
├── package.json
└── README.md
```

### Main App Navigation

Each POC should be accessible from a main navigation page:

```tsx
// App.tsx structure
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<POCNavigationHub />} />
        <Route path="/minimal-power" element={<POCMinimalPower />} />
        <Route path="/polished-casual" element={<POCPolishedCasual />} />
        <Route path="/experimental-admin" element={<POCExperimentalAdmin />} />
        <Route path="/dashboard-mobile" element={<POCDashboardMobile />} />
        <Route path="/components-a11y" element={<POCComponentsA11y />} />
      </Routes>
    </Router>
  )
}
```

## Success Criteria

### Research Quality
- [ ] **All agent pairs completed**: N UI-UX + N User Journey agents finished successfully
- [ ] **Diverse approaches identified**: Each POC targets different aspects of problem
- [ ] **Research synthesis complete**: Agent findings incorporated into PRP context
- [ ] **Unique value propositions**: Each POC validates different assumptions

### PRP Quality
- [ ] **N complete PRPs generated**: One for each POC variation
- [ ] **Context completeness**: Each PRP enables one-pass implementation
- [ ] **Validation approaches**: POC-appropriate testing for each variant
- [ ] **Implementation clarity**: Clear task sequences for parallel development

### Parallel Readiness
- [ ] **Unique naming**: All POCs have distinct identifiers and directories
- [ ] **Isolated development**: POCs can be developed simultaneously without conflicts
- [ ] **Shared infrastructure**: Common mock data and routing setup defined
- [ ] **Execution ready**: All PRPs ready for parallel execution command

## Anti-Patterns

### Research Anti-Patterns
- ❌ **Don't create identical approaches**: Ensure each POC explores different aspects
- ❌ **Don't skip agent specialization**: Each agent should have distinct focus
- ❌ **Don't generalize findings**: Customize context for each POC's unique approach
- ❌ **Don't rush parallel research**: Let all agents complete before synthesis

### PRP Generation Anti-Patterns
- ❌ **Don't copy-paste PRPs**: Each should be tailored to its unique approach
- ❌ **Don't ignore agent research**: Incorporate all findings into appropriate PRPs
- ❌ **Don't create conflicting requirements**: Ensure POCs can coexist in same project
- ❌ **Don't skip validation customization**: Each POC needs appropriate testing approach

### DO Focus On
- ✅ **Maximum concept coverage**: Each POC validates different aspects of the problem
- ✅ **Specialized agent research**: Leverage UI-UX and User Journey expertise fully
- ✅ **Parallel development readiness**: Structure for simultaneous implementation
- ✅ **Stakeholder value**: Each POC provides unique insights for decision making

---

**Remember**: The goal is **comprehensive concept validation** through **diverse parallel approaches**. Each POC should explore the problem from a different angle, maximizing the insights available to stakeholders for informed decision-making.