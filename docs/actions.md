# Actions
Actions make up most of the gameplay in the Grapefruit engine. An action is essentially a single unit of gameplay -- when a player enters a command, a single action will be performed. Everything that happens in your game happens because an action told it to happen.

In addition to their basic function of providing feedback and narration, actions can do all of the following:

-Add items to inventory.

-Remove items from inventory.

-Set flags.

-Remove flags.

-Warp the player to a different room.

-Trigger custom code (see Callbacks).

-Trigger conversations (see Conversations).

They can also be conditioned upon certain varibles:

-The presence of items in the inventory.

-A flag being set.

-A flag *not* being set.

## All paramaters

**Actions have no methods, but lots of paramaters. Here all of them. Most of them can be left alone most of the time.**

**id (required):** A unique sting representing the action.

**success (required)**: A string to display when the action is successul. If empty (""), nothing will be displayed. Feedback is good for your player, so always try to set a success string unless you have a very good reason not to!

**verbs:** a list of verbs to associate with the action, where each verb is a single string with no spaces.

**nouns:** a list of nouns to associate with the action, where each noun is a single string with no spaces.

You can choose to only set verbs or only set nouns, but if both are empty, then your action will be impossible to trigger!

**enforce:** Boolean (False by default). If True, require one of the specificed verbs to trigger the action. If False, allow the action to be triggered by its nouns using generic verbs. Throughout this docs, this is referred to as "verb enforcement."

If enforce is True and you have not specified any verbs, then your action will be impossible to trigger!

**need_nouns:** A list of nouns that MUST ALL be in the command for the action to succeed. This is checked only when the action actually runs and is ignored by the parser. If left empty, this will not be checked.

**need_items:** A list of items (strings) that the player must have in their inventory to trigger the action.

**items_fail:** The message to display if the action fails due to missing items.

**gives_items:** A list of items (strings) that will be added to the player's inventory when the action is run.

**expend:** Boolean (False by default). If True, remove the required items from the player's inventory when the action is run. If False, allow the player to keep their items after performing the action.

**need_flags:** A list of flags (strings) that must be set in order for the action to be triggered.

**set_flags:** A list of flags that will be set when the action is triggered.

**remove_flags:** A list of flags that will be removed (if set) when the action is triggered.

**avoid_flags:** A list of flags that must NOT be set in order for the action to be triggered.

**flags_fail:** The message to be displayed if the action fails due to missing flags. 

**callback:** A function to execute when the action is run (see Callbacks).

**fail_callback:** A function (or dialogue) to execute when the action is invoked, but fails for any reason.

**allowed_rooms:** A list of room IDs (strings) that the action is allowed to be performed in. If left blank, the action can be performed in any room.

**warp**: A room ID (string) to set as the current room when the action runs. If left blank, no warp will occur.

**repeat:** Boolean (True by default). If True, the action may be performed more than once. If False, the action can only be performed once.

**repeat_message:** A string to display if the player attemps to repeat an action where repeat == False. (Will not trigger the fail callback; see Callbacks)

## Bulk Definition

Sometimes, you may want to quickly create a lot of trivial, unimportant actions simply to anticipate the player's choices and provide feedback. For this, you can use the "bulk" method.

To do this, simply use the grapefruit.bulk method with the following POSITIONAL parameters:

**noun:** A string representing the noun you want the actions to be associated with. If you don't want the actions to have any associated nouns, then use an empty string ("").

**rooms:** A list of the room IDs that the actions should be allowed in. If you want to allow the actions in every room, use an empty list ([]).

**args:** An indefinite number of lists formatted as follows:

[["list","of","verbs","goes","here"], "Success message goes here."]

For every argument given, one action will be created with the id of "BULK_{noun}_{first_verb}." It will be repeatable, have no flag or item conditions, and not set any flags or items.

For example, this code using bulk definition:

```python
grapefruit.bulk("apple", ["example_room"],
  [["bite","chomp"],"You take a bite out of the apple."],
  [["smell","sniff"],"The apple smells sweet."]
)
```

...is equivalent to this code using manual definitions:

```python
grapefruit.action(id="BULK_apple_bite",
  verbs=["bite","chomp"],
  nouns=["apple"],
  repeat=True,
  allowed_rooms=["example_room"],
  success="You take a bite out of the apple."
)

grapefruit.action(id="BULK_apple_smell",
  verbs=["smell","sniff"],
  nouns=["apple"],
  repeat=True,
  allowed_rooms=["example_room"],
  success="The apple smells sweet."
)
```

As you can see, bulk action definition is much more efficient when creating lots of simple actions at once.
