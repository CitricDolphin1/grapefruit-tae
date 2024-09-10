# Dev Mode
Dev mode helps you test and debug your game. When dev mode is enabled, Grapefruit's behavior changes in the following ways.

## Fatal errors are bypassed
Some actions normally cause the engine to terminate, such as creating an action with a reserved word as an ID.
While dev mode is enabled, these actions will be allowed, but a warning will be displayed.

## Warnings are enabled for potentially unintended behaviors
Some invalid behaviors like attempting to create a duplicate flag, or removing a flag or inventory item that doesn't exist, will normally be ignored completely.
While dev mode is enabled, warnings will be displayed when these actions are attempted.
These warnings do not necessarily mean that anything is wrong, but are a useful indicator that you may have logic bugs if they show up unexpectedly.

## The dictionaries are rebuilt on every launch
Normally, the nouns.json and verbs.json files are only built when they fail to load (due to being corrupt, invalid, or missing).
To help quickly test new actions, these files will be rebuilt from scratch on every launch while dev mode is enabled.

## Debugging commands are enabled
While dev mode is enabled, a handful of special commands may be used to help quickly test certain parts of your game.
-warp "room_id": Immediately warp to the room with the id "room_id"
-setflag "flag": Set a flag with the name "flag"
-delflag "flag": Delete the flag with the name "flag" if it exists
-setitem "item": Add an item with the name "item" to the inventory
-delitem "item": Remove one item with the name "item" from the inventory, if it exists.
-undo "actionid": If an non-repeatable action with the id "actionid" has already been performed, this command will allow it to be performed again.
-flags: Display all flags that have been set.
-validate: Detect and list global actions, invalid or unused rooms, unobtainable items, unused or unobtainable flags, and unreachable conversation branches. **It's a good idea to validate at least once before releasing your game.**

## Parsing is logged verbosely
When the player types a command, it immediately goes to the parser.
The parser goes through several steps to determine what action the player intended.
While dev mode is enabled, each of these steps will be noted in the output. This information is useful to determine what's going wrong when a command does not trigger the action you expect it to.

For details on understanding the parser output, see Parser.