# Team 2 Project - "PawLink"

## Team Members
- Daniel Trimble (dstrimble)
- Billy Spann (billyspann)
- Brandon Wilson (brandowun)
- Elizabeth Lee (elizlee1)
- Mia Diaz Cruz (miadc0117)
- Daniel Cronin (dcronin05)
- Stefany Roman (stefanyromann)

## Tech Stack
- Python
- Flask
- SQLite
- HTML/JS/CSS

## Project Idea
Pet matching app where pet owners build profiles to coordinate park meetups.

## Mission Statement
Our mission is to link pups and people in the real world by simplifying socialization. Matching dogs based on location, size, energy, and temperament, we make community park meetups safer, more predictable, and way more fun. Better matches, better playdates, more tail wags. Welcome to Pawlink.

## Defined roles
PawLink has 2 user roles
Unregistered Users
Registered Users

### Unregistered User
A visitor who has yet to create an account  They can learn what PawLink is, but unable to create matches or meetups until they register
What they can do:
View the front pages to see what Pawlink is about and the idea behind it. 
Ccreate accounts which would be sigining up for Pawlink


What they can't do:
Create or edit a profile
Browse or  match with other pet owners
Create, join, or view park metups

### Registered User
A pet owner who has created an account and is logged in. They have full access to PawLinks core features.

What they can do:
Log in and out
Create and edit their profile and dog's profile (location, size, energy, temperament).
Browse and match with other pet owners based on compatibility 
Coordinate park meetups with their matches.

What they can't do:
Remove users
Edit code via frontend nore backend

## The Problem
Dog owners sometimes find it challenging to find safe, compatible, and predictable playdate partners for their pets.
Traditional dog socialization methods rely almost entirely on random chance. Taking a dog to a public neighborhood park blind relies on the random chance there will be a) another compatible dog and/or b) a safe environment. This creates an environment with three core issues:

Unpredictable Temperaments - Gentle or anxious dogs are routinely exposed to highly aggressive or overly dominant dogs, leading to  fights or psychological trauma.

Pet Size Differences - A hyperactive large breed playing too roughly with a fragile small or medium breed can cause accidental  injuries.

Mismatched Energy Levels - A low-energy dog simply trying to rest can become overwhelmed and defensive when pursued by a high-energy dog.

This unpredictability can lead to injuries and behavioral regression in dogs which ultimately causes owner anxiety and social isolation from the local pet community.

## The Solution
PawLink takes the guesswork out of dog meetups by letting you pre-screen playmates based on personality and size, so you can set up safe, predictable playdates in the real world. Instead of walking into a public park blind, owners use PawLink to build detailed behavioral profiles and schedule perfect playdates before their dogs ever meet:

Compatibility Filtering - Matches potential partners by explicit criteria: location, size, energy levels, and temperament.

Safe Pre-Meeting Communication - Matched owners use messaging to chat, share behavioral nuances, and finalize boundaries safely before committing to an in-person, 1-on-1 meeting.
## Team Workflow

### Definition of Done

Every pull request is reviewed and approved by a team member who did not write the changes. Each pull request describes what changed and why. A pull request that implements a backlog item links to that Issue, and all acceptance criteria on the Issue are met.

This Definition of Done grows as the pipeline develops: automated tests in Module 6, CI enforcement in Module 7, and static analysis later in the course.

### Communication

Slack (class workspace, Team 2 channel) for async updates and blockers. Google Meet for team meetings. GitHub is the source of truth for work state. Work is tracked through Issue and pull request interaction in comments, reviews and commits.

### Branching Strategy

All work happens on a `feature/`, `bug/` or `docs/` branch. `main` is protected
and accepts changes only through a pull request approved by another teammate.
Branch names start with the prefix and a short description, e.g.
`bug/fix-login-logic-typo`.

| Prefix | Use | Example |
| :--- | :--- | :--- |
| `feature/` | New capability | `feature/user-login` |
| `bug/` | Defect fix | `bug/remove-extra-description` |
| `docs/` | Documentation only | `docs/add-roles-file` |
