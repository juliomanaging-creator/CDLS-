# Sprint Manager Agent - Quick Start Guide

## What Is This?

The Sprint Manager Agent is your **AI project manager** that will help you execute the 6-week CDLS implementation. Think of it as having a senior PM working alongside you, tracking every task, identifying blockers, and keeping you on schedule.

## What It Does

✅ **Daily Task Lists** - Tells you exactly what to work on today  
✅ **Progress Tracking** - Monitors completion across all 5 tracks  
✅ **Blocker Detection** - Identifies issues before they become problems  
✅ **Timeline Adjustments** - Dynamically adjusts schedule based on reality  
✅ **Status Reports** - Generates daily, weekly, and overall reports  
✅ **Integration Coordination** - Coordinates Friday integration checkpoints  

## Quick Setup (5 minutes)

### Step 1: Install Dependencies

```bash
pip install anthropic --break-system-packages
```

### Step 2: Set Your API Key

```bash
export CLAUDE_API_KEY="your-anthropic-api-key-here"
```

### Step 3: Start the Agent

```python
python sprint-manager-agent.py
```

## Interactive Menu

When you run the agent, you'll see:

```
🚀 CDLS SPRINT MANAGER - AI Project Manager
=======================================================================

SPRINT MANAGER MENU
=======================================================================
1. Get today's task list
2. Update task status
3. Generate status report (daily/weekly/overall)
4. Check for blockers
5. Adjust timeline
6. Get next action suggestions
7. Friday integration check
8. Save state
9. Exit
```

## Typical Daily Workflow

### Morning (9:00 AM)
1. Start the agent
2. Select Option 1: "Get today's task list"
3. Review recommended tasks and priorities
4. Start working on highest priority items

### During the Day
- As you complete tasks, use Option 2 to update status
- The agent tracks your progress and unblocks dependent tasks
- Get suggestions for next tasks with Option 6

### End of Day (5:00 PM)
1. Update all completed tasks
2. Generate daily report (Option 3)
3. Save state (Option 8)
4. Review tomorrow's focus

### Friday Afternoon
- Run Option 7 for integration check
- Coordinate with any team members
- Generate weekly report (Option 3 → "weekly")

## Example Session

```
Select option (1-9): 1

📋 Generating today's task list...

📅 2026-01-13T09:00:00
Week 1, Day 1

Total estimated: 16h
Team capacity: 8h

Recommendations:
🎯 Focus on critical path items today! Start with environment setup 
across all tracks to unblock tomorrow's development work.

Tasks:
  • [W1D1-T1-ENV] Set up Hardhat environment (2h)
  • [W1D1-T2-ENV] Set up Python environment (2h)
  • [W1D1-T3-ENV] Initialize Next.js project (2h)
  • [W1D1-T4-ENV] Install Temporal SDK (1h)
  • [W1D1-T5-DB] Set up PostgreSQL database (3h)

---

[Complete W1D1-T1-ENV]

Select option (1-9): 2

Task ID: W1D1-T1-ENV
Status: 1=Not Started, 2=In Progress, 3=Completed, 4=Blocked
New status (1-4): 3
Hours spent (optional): 2.5
Notes (optional): Hardhat configured with Sepolia testnet

⏳ Updating task...

✅ Task updated!
Analysis: Great progress! Environment setup completed ahead of schedule. 
This unblocks tomorrow's contract development. Consider starting the 
testnet configuration next since you have time remaining today.

---
```

## Pro Tips

### 1. Update Tasks Frequently
The more you update, the better the agent can:
- Track actual vs. estimated time
- Adjust timeline predictions
- Identify patterns
- Suggest optimizations

### 2. Add Notes
When updating tasks, add notes about:
- What worked well
- What was challenging
- Discoveries made
- Time-saving shortcuts

The agent learns from these and gives better suggestions.

### 3. Check Blockers Daily
Run Option 4 every morning to catch issues early.

### 4. Use Reports for Communication
Generate weekly reports to share with:
- Investors
- Partners
- Team members
- Advisors

### 5. Save State Regularly
Option 8 saves your progress. Do this:
- End of each day
- After major milestones
- Before making big changes

## Advanced Usage (Python API)

If you want to integrate the agent into your own scripts:

```python
import os
import asyncio
from datetime import datetime
from sprint_manager_agent import SprintManagerAgent, TaskStatus

async def main():
    # Initialize
    manager = SprintManagerAgent(
        claude_api_key=os.getenv("CLAUDE_API_KEY"),
        project_start_date=datetime(2026, 1, 13),
        team_size=1  # Just you
    )
    
    # Get today's work
    tasks = await manager.get_daily_task_list()
    print("Today's focus:", tasks['recommendations']['motivational_message'])
    
    # Complete a task
    result = await manager.update_task_status(
        task_id="W1D1-T1-ENV",
        status=TaskStatus.COMPLETED,
        actual_hours=2.5,
        notes="Environment ready to go!"
    )
    print("Next:", result['analysis'])
    
    # Generate report
    report = await manager.generate_status_report("daily")
    print(report)
    
    # Save progress
    manager.save_state()

asyncio.run(main())
```

## Understanding the Output

### Task Status
- **not_started**: Haven't begun yet
- **in_progress**: Currently working on it
- **completed**: ✅ Done!
- **blocked**: Can't proceed (needs dependencies or help)

### Priority Levels
- **critical**: Must do today, blocks other work
- **high**: Important, do soon
- **medium**: Normal priority
- **low**: Nice to have, do if time permits

### Health Status (Reports)
- **🟢 Green**: On schedule, no major issues
- **🟡 Yellow**: Minor concerns, watch closely
- **🔴 Red**: Behind schedule or blocked, needs attention

## Customization

### Change Team Size
If you add developers, update in code:

```python
manager = SprintManagerAgent(
    claude_api_key=api_key,
    project_start_date=start_date,
    team_size=3  # Now a 3-person team
)
```

The agent will adjust task allocation accordingly.

### Change Work Hours
If you work part-time:

```python
manager = SprintManagerAgent(
    claude_api_key=api_key,
    project_start_date=start_date,
    work_hours_per_day=4.0  # 4 hours instead of 8
)
```

## Troubleshooting

### "API key not found"
```bash
# Make sure you set it:
export CLAUDE_API_KEY="sk-ant-..."

# Verify it's set:
echo $CLAUDE_API_KEY
```

### "Task not found"
- Check the task ID spelling
- Use Option 1 to see valid task IDs

### "No tasks for today"
- You might be ahead of schedule! 🎉
- Use Option 6 to get suggestions for next work

### State File Corrupted
If sprint_state.json gets corrupted:
```bash
# Backup the old one
mv sprint_state.json sprint_state.json.backup

# Start fresh (you'll lose progress tracking)
python sprint-manager-agent.py
```

## What Makes This Special

Unlike traditional project management tools, this agent:

1. **Understands Context**: Uses Claude to intelligently prioritize based on project stage, dependencies, and risks

2. **Learns & Adapts**: Analyzes your velocity and adjusts timeline predictions

3. **Proactive Guidance**: Doesn't just track - actively suggests what to do next

4. **Integration Aware**: Knows when different tracks need to sync up

5. **Natural Language**: Talk to it like a colleague, not a database

## Real Example: Week 1, Day 1

**8:45 AM**: Start agent, get task list  
**9:00 AM**: Begin Hardhat environment setup  
**11:00 AM**: Complete, update agent (2h actual vs 2h estimated)  
**11:15 AM**: Agent suggests Python environment next  
**12:00 PM**: Lunch break  
**1:00 PM**: Complete Python environment  
**3:00 PM**: Start Next.js project  
**5:00 PM**: Update status, generate daily report  
**5:15 PM**: Save state and review tomorrow's plan

**Agent automatically**:
- Tracked 3 completed tasks
- Calculated you're on schedule
- Unblocked 3 dependent tasks for tomorrow
- Suggested starting database setup if you have energy
- Generated professional status report

## Next Steps

1. **Today**: Set up environment, run the agent
2. **This Week**: Use it daily, build the habit
3. **Next Week**: Start seeing velocity metrics
4. **Week 3**: Agent helping predict completion accurately
5. **Week 6**: Complete project with full tracking history

## Support

Questions? Issues? Want to enhance the agent?

The agent's code is fully documented and customizable. You can:
- Add more tasks to any sprint
- Change priorities
- Add custom workflows
- Integrate with other tools

---

**Ready to start building?** 🚀

```bash
export CLAUDE_API_KEY="your-key"
python sprint-manager-agent.py
```

Your AI project manager is waiting to help you succeed!
