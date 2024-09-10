# Inventory and Flags
The inventory and flags are both lists of strings that can be used as conditions for actions and exchanges. They are functionally very similar, with slight differences.

-The absence of flags can be used as an action condition (see Actions), but not the absence of items. The absence of either can be used as a condition for exchanges within conversations (see Conversations).

-Multiple items can share the same name, but flags must be unique. Giving multiple items with the same name will create duplicates in the inventory, while setting multiple flags with the same name will result in only one flag with that name being set.

-The player can view their inventory, but can not view the list of flags.

Generally speaking, the inventory should be used to represent tangible objects in the player's posession, while flags should be used to keep track of intangible conditions (such as a door being open or closed) or to record information without the player being aware (such as setting up a trap for later on).

The inventory and flags can both be accessed directly as grapefruit.inventory and grapefruit.flags. It is easy to cause softlocks and crashes this way because it bypasses the normal protections and is not noticed by validation (see Dev Actions). As such, this technique should be done sparingly and with caution.
