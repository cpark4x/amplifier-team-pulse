# Team Pulse: Coherence for AI-First Teams

> *Your team builds at machine speed. Alignment, leverage, and focus are still at human speed.*

## The Problem

AI-first teams work in a fundamentally new way. Each person spends their day in a 1:1 collaboration with AI — building tools, shipping features, running experiments — individually, at machine speed. The output is real and the pace is extraordinary.

But the organization around them can't keep up. Individual work is opaque to teammates. Learnings and tools stay siloed with whoever built them. Attention drifts from agreed outcomes because everything feels productive. Connections between people's work go unseen. And when strategy shifts from the top, there's no mechanism to realign the team at the speed the work demands.

This is a two-way problem. Leaders need to drive clarity downward as priorities evolve. The team's work needs to flow visibility upward without manual reconstruction. Traditional standups and status docs can't do either — they weren't designed for this velocity or this level of individual autonomy.

Each person works in their own human-AI pair, producing work that is opaque to everyone else. Individual learnings, tools, techniques, and insights stay siloed — the team's collective capability is capped by what people happen to mention in conversation. AI makes everything feel productive, so attention drifts from agreed outcomes without anyone noticing — building a cool tool feels like progress even when it's disconnected from what matters. Connections between people's work go unseen — people may be driving the same outcome from different angles, duplicating effort, or creating tools others could leverage. Direction evolves faster than it can be communicated — strategy isn't static, and leaders need a way to push updated direction downward and see how the team adapts.

Team Pulse is the coherence layer for AI-first teams — because the velocity and novelty of the work demands AI-powered tools to keep everyone aligned.

## What Team Pulse Is

Team Pulse is a two-way alignment system for AI-first teams.

At the bottom, it passively watches. Activity flows in from Amplifier sessions and GitHub without anyone doing anything. The system sees what each person is building, what tools they've created, what capabilities are emerging across the team.

At the top, it carries intent. Leaders set outcomes — what the team is trying to achieve — and when those priorities shift, the change is visible immediately to everyone affected.

In the middle, it asks one question: *"Which outcomes does this drive?"* Not on a rigid schedule — whenever there's enough new work to warrant it. Maybe that's after a big push, maybe it's at the end of the week, maybe a manager triggers it before a 1:1. The system proposes, the human confirms. That lightweight confirmation is the bridge between raw activity and meaningful alignment.

From those three layers, everything else follows. ICs see where their work fits into the team's goals and what their teammates are building. Managers see which outcomes are progressing, where attention has drifted, and where people's work connects in ways nobody expected. Leaders see trajectory and can push course corrections that flow down immediately.

The underlying belief: in AI-first teams, productivity isn't the bottleneck — coherence is. Team Pulse doesn't make people more productive. It makes sure all that productivity points in the right direction.

## How It Works

Three layers, each building on the last.

**Outcomes** — top-down, set by leaders. Leaders define what the team is trying to achieve. These aren't static quarterly goals — they're living targets that evolve as strategy evolves. When priorities shift — a new opportunity, a deprioritized initiative, a course correction — the change flows through the system immediately. Everyone sees the current set of outcomes and can tell whether their work is connected to something that still matters.

**Activity** — bottom-up, captured passively. The system continuously captures what each person is building — from Amplifier sessions and GitHub repos. Tools they've created, capabilities they've shipped, code they've committed. Nobody logs anything. Nobody runs anything. The work is observed and recorded automatically, in the background.

**Alignment** — the bridge, lightweight human judgment. The system proposes connections between captured activity and current outcomes. Each person confirms or adjusts: *"Yes, this drives that outcome"* or *"No, this was experimentation"* or *"Actually, this connects to something new."* This is the one moment that requires a human — and it's the most valuable moment in the system, because it's where intent meets evidence.

From these three layers, the system generates everything else: outcome progress views for ICs, drift and connection detection for managers, trajectory narratives for leadership. All automatic, all from the same underlying data.

## What Team Pulse Is Not

Team Pulse is not a time tracker — it observes what was built, not how many hours were spent. It's not a performance ranking tool — it creates shared awareness, not stack rankings. And it's not a project management tool — it doesn't manage tasks or sprints. How people organize their individual work is their business.

## The Three Views

All three audiences see the same data differently.

**The IC View: "Where do I fit?"** An IC opens Team Pulse and sees the team's current outcomes. Under each outcome, they see who's contributing and what work has been captured — including their own. They can see what tools and capabilities their teammates have built. They can see when an outcome they're driving has stalled, or when a new outcome has been added from above. They don't see rankings or comparisons. They see a map of the team's work with themselves on it.

**The Manager View: "Where do I intervene?"** A manager sees outcomes grouped by status — on track, at risk, stalled. They see which outcomes have active contributors and which ones nobody is touching. They see when someone's captured activity is disconnected from any outcome — the drift signal. They see connections across people's work that might not be obvious. This view is designed for the question: *"Where does my team need me right now?"*

**The Leader View: "Where is this going?"** A leader sees trajectory. Outcomes across teams, with narrative context explaining what each team is working on and why it matters. When a leader updates priorities — adds an outcome, deprioritizes another — it flows down immediately. They don't need to ask for a status update. The system generates one from the alignment data, with enough narrative that a VP who doesn't know the details can understand the state in 30 seconds.

## How We Get There

Scoped to Sam's org first.

**Phase 1: Passive activity capture.** Activity capture is identity-based, not repo-based. Each person opts in by having a profile with their GitHub handles. Once opted in, the system captures activity across everything those handles touch — public repos, private repos that are explicitly shared, and all company repos. No repo list to curate or maintain. The system captures from two sources: Amplifier sessions (what the person worked on during their AI-assisted sessions) and GitHub activity (commits, PRs, and contributions across all repos tied to their handles). Only opted-in team members are tracked. Activity capture is transparent — every person can see exactly what the system has recorded about them.

**Phase 2: Alignment confirmation and views.** Replace the formal commitment-logging ceremony with the system proposing what each person worked on and asking for outcome connections. The system presents captured activity and asks: *"Which outcomes does this drive?"* The person confirms, adjusts, or marks it as intentional experimentation. The `drives:` field stays — it's the core innovation — but it comes from confirmation, not data entry. Simultaneously, build the IC, manager, and leader views over the alignment data — generated perspectives over the same underlying data.

**Phase 3 (future direction): Capability and learning surfacing.** As people build tools, bundles, recipes, and techniques, the system tracks and makes them discoverable to the team. Individual learnings become collective capability. This is the "leverage each other's work" piece — turning individual tools and insights into team-wide assets.
