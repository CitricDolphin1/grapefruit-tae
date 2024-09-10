# Usage
To use Grapefruit, place the grapefruit.py file in the same directory as your game, and import it as a named module.

# Basics
There are two basic elements required for a Grapefruit game: a room, and a list of actions. Let's start with rooms.

## Rooms
A room is exactly what it sounds like -- a location in the game. Rooms only have two attributes and no methods, but they form the basis for the illusion of physical space.

**id:** A unique ID for the room. Can be any string.

**description:** A list of strings describing the room. This is what the player will see when looking around.

To create a room, simply instantiate a Grapefruit.room object. Rooms can be named, but don't have to be -- the engine internally keeps track of every room created.

```python
import grapefruit as gf
gf.room(id="start_room", description=["A small, mostly empty room.", "There's a table in the corner."])
```

## A note about IDs
While IDs must be unique, they only have to be unique to their type. For example, two rooms can not have the same ID, but a room and an action can both have the same ID without conflicting.

## Basic Actions
Actions are the backbone of Grapefruit. Actions can be performed by the player through their typed commands. Actions have lots of paramaters, but at a minimum, they need the following:

**id:** A unique id for the action. Can be any string except the following: "look","inventory","warp","setflag","delflag","setitem","delitem","undo","flags","validate"

**success:** A string to display when the player performs the action.

**verbs:** A list of strings, where each string is a verb associated with the action (no spaces). Examples include "jump," "open," "hit," etc.

Like rooms, actions may be named but don't have to be.

```python
import grapefruit as gf
gf.action(id="win",
                success="Congratulations! You win!",
                verbs=["win","succeed"])
```

## Configuring basic settings
Now that you have a default room and an action, your game is almost ready to run. The only thing left to do is configure some basic settings.
All of these can be accessed as attributes of the module itself (e.g. gf.startmessage = ...). All of these can be left at their defaults, but you should probably change the start message at a minimum.

**start_message:** A list of strings to display line-by-line when the game first starts up.

**prompt:** The prompt to display at the command line. Set to ">" by default.

**inventory_commands:** List of special commands to view the inventory (see tools).

**look_commands:** List of special commands to that display the current room's description.

**inventory_message:** When the player checks their inventory, display this string before the inventory contents are listed.

**fail:** The message shown when a player tries to perform an invalid action or fails at an action.

**look_by_default:** Boolean, whether to display the room description every time the player enters a new room. False by default.

**generic_verbs:** A list of verbs (strings) that can be used to interact with certain actions (see Actions).

**dev_mode:** Boolean, False by default. If True, the game will rebuild dictionaries on every launch, enable debug logging and tools, and ignore fatal errors. (See Dev Mode)

**parser mode:** Integer. Determined how commands will be parsed. This should usually be left alone -- see Parser.

## Running your game.
Time to put it all together. To start your game, simply execute grapefruit.run(room), where room is a grapefruit room. In this case, the room is assigned to **start_room,** but it could also be defined directly in the argument itself if you prefer.
```python
import grapefruit as gf

start_room = gf.room(id="start_room", description=["A small, mostly empty room.", "There's a table in the corner."])

gf.action(id="win",
                success="Congratulations! You win!",
                verbs=["win","succeed"])

gf.run(start_room)
```

That's it! Your game will now be running and accepting commands.

---

If you're not sure where to go from here, I'd recommend reading the following docs in this order:
-actions
-inventory and flags
-conversations
-dev mode
-callbacks and plugins
-tools
-parser (most users can safely skip this one)
