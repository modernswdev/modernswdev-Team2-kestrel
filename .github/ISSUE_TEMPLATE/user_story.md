## User Story
**As a** matched dog owner, 
**I want to** message my play partner before meeting, 
**So that** we can establish location, compatibility, and boundaries in advance.
---
## Acceptance Criteria
* [ ] Comments added are viewable by both matches.
* [ ] The chat screen displays a timestamp or sending history so users can see when messages were sent.
* [ ] The interface prevents users from sending completely blank messages (e.g., the "Send" button turns grey/disabled if the text box is empty).

### Scenario 1: Sending a message
* **Given** I am on the chat screen with a matched dog owner,
* **When** I type a text message and click the "Send" button,
* **Then** the message should immediately appear in the chat log.

### Scenario 2: Receiving a message
* **Given** I have a new unread message from a match,
* **When** I open the messaging tab,
* **Then** I should see an unread badge indicating which match sent the message.

## Notes
* Can users send **images/photos**, or is it **strictly text-only** for this version? `[Specify here]`
* Can a user **unmatch/block** someone directly from the chat screen if they cross boundaries? `[Yes/No]`
