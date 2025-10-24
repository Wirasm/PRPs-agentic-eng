---
description: Run all prp core commands in squence from feature request to pr
---

---
description: Run all prp core commands in sequence from feature request to pr
---

Feature: $ARGUMENTS

Execute in sequence:
1. Create a task for a subagent, make the subagent read /prp-core-new-branch and instruct the subagent what to name the branch based ont he users feature request
2. Create a detailed prompt based on the users request and send the request to a subagent with the task tool the subagent must follow the isntructions in /prp-core-create
3. When the agent is done with the task. Find the file created by the create command in PRPs/fetures
3. Launch a new subagent wioth a detailed task to follow the instructions in `/prp-core-execute and the prp file is the argument input for this request
4. Run `/prp-core-commit` when the agent is done
5. Run `/prp-core-pr` (generate title from feature)


When done let the user know, give a summary of what was done