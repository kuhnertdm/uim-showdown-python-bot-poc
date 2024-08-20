# UIM Showdown - Python Discord Bot POC

A POC for a Python version of the UIM Showdown Discord bot

## Code flows

### Submitting a request:

* User calls an application command (slash command)
* Discord.py library runs the code in the method annotated with @bot.tree.command in showdown-bot-poc.py
* Command method handles input validation (e.g. KCs must not be negative, pick-list values must be in the pick-list, etc), and if this validation fails, it raises a BingoUserError
* Command method creates an ApprovalRequest object from the context (which is an Interaction object) and passes it to BingoUtils.requestApproval(), then sends back a confirmation message
* BingoUtils.requestApproval() sends a message to the approvals channel with the request details, and constructs custom button subclasses to include with it, which include callback methods and the request info

### Approving a request:

* Staff member clicks the approve button on the message in the approvals channel
* The callback method in the ApproveButton class (in Buttons.py) is called
* The callback method calls the approve() method on the ApprovalRequest object (which was stored on the button)
* ApprovalRequest.approve() calls requestApproved() on its approval handler
* The approval handler's requestApproved() method handles things like talking to the spreadsheet
* Back in the button's callback method, it removes the buttons, sends a sucess message to the approvals channel, and then sends the "approved" message back to the submissions channel

### Denying a request:

* Staff member clicks the deny button on the message in the approvals channel
* The callback method in the DenyButton class (in Buttons.py) is called
* The callback method calls the deny() method on the ApprovalRequest object (which was stored on the button), which currently does nothing (this may be removed)
* The callback method remove the buttons, sends a sucess message to the approvals channel, and then sends the "denied" message back to the submissions channel