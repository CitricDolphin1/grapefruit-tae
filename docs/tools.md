# Tools
There are a handful of miscellaneous tools that can be used to aid in development.

## Saving/Loading
Saving and loading allows you to import and export session information, including:

-Inventory

-Flags

-Current room

-State of non-repetable actions

You can create a save by instantiating the grapefruit.save class. Unlike most classes, saves are NOT tracked internally by the engine and must be assigned to be useful.
You can load a save using the grapefruit.load(save) function and passing it a save object as the parameter.

The built in saving and loading tools are NOT persistent across sessions. If you need to save to and load from files, use a serialization tool (such as pickle) to write save objects to files.

## Miscellaneous Functions
There's a handful of functions that can be useful when creating plugins or callbacks.

fatal_error(error): If dev mode is disabled, display the string {error} and then close the game. If dev mode is enabled, display the string {error}, but continue execution.

warp(room): Set the current room to the one specified by the id {room}. Note that this accepts a ROOM ID AS A STRING, not an actual room object.

setflag(flag): Set a flag {flag}.

devprint(string): Print {string} only if dev mode is enabled.

build_dictionary(): Rebuild the dictionary files.

reset(): Reset the engine parameters, but keep all rooms, actions, and conversations.

end(): Terminate the game loop

## Internal Engine Variables
It's usually a bad idea to access these variables directly. Some of them are validated during runtime, and this validation is bypassed when accessing them directly. Others are never validated because they are not intended to hold arbitrary data. Both cases mean that manipulating these variables directly can create instability or crashes.

They are documented here anyway for completeness. If you access them, be aware that you may run into issues that can only be understood by debugging the engine itself.

inventory: List of strings representing the inventory.

flags: List of strings representing set flags.

rooms: A dictionary with room IDs as keys, and the respective room objects as values.

conversations: A dictionary with conversation IDs as keys, and the respective conversation objects as values.

current_room: The current room (room object, not just the ID). It's almost always better to define a room and then warp to it.

dead_actions: A list of IDs of actions that can not be repeated and have already run.

end_game: Boolean. If True, the game loop will terminate and this value will be reset to False. There is no reason to access this directly 
instead of using the end() function.

actions_dict: A dictionary with action IDs as keys, and the respective action objects as values.

actions: A list of all possible actions. Functionally the same as actions_dict.values()
