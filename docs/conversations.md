# Conversations
Conversations allow a player to navigate a fixed network of choices. Conversations are mostly intended to be used for interactions with characters, but can technically be used for any scenario where you want to force the player to choose from a pre-determined list of choices, such as choosing a floor button in an elevator.

## Functionality
When a conversation is triggered, a list of options is displayed to the player, and they can choose between them by typing the respective number. The player will not be able to proceed until they select one of the displayed options. Below is a brief example of what part of a conversation might look like to the player.

```
>talk to clerk

Hi, how can I help you?
1. I want to buy
2. I want to sell
3. It's nothing, nevermind

>4

Please choose a valid option.

1. I want to buy
2. I want to sell
3. It's nothing, nevermind.

>1

Sure, what would you like to buy?
1. Milk
2. Eggs
3. I changed my mind
```

## Parameters
Conversations, like actions and rooms, can be named but don't have to be. Conversations only directly accept two parameters.
**id:** A unique string representing the conversation.
**exchanges:** A list of exchanges, explained below. The first exchange in this list will be triggered as soon as the conversation starts.

Conversations handle the user interaction, but the actual content of the conversation is stored in *exchanges.* An exchange is similar to an action in most ways. They have several parameters and no methods.

**id:** A unique string representing the exchange. Unlike other IDs, which must be globally uinque, exchange IDs only have to unique within the scope of the conversation containing the exchange.
**lines:** A list of strings to display when the exchange is triggered.
**options:** A list of options presented to the player (one string each).
**branches:** A list of exchange IDs to be triggered by the respective options.

The first option in the options list will trigger the first exchange in the branches lest, and so on. Both lists must be the same length.

**need_flags:** A list of flags (strings) that must be set in order for the exchange to be triggered.
**set_flags:** A list of flags that will be set when the exchange is triggered.
**remove_flags:** A list of flags that will be removed (if set) when the exchange is triggered.
**avoid_flags:** A list of flags that must NOT be set in order for the exchange to be triggered.

**need_items:** A list of items (strings) that the player must have in their inventory to trigger the exchange.
**gives_items:** A list of items (strings) that will be added to the player's inventory when the exchange is run.
**avoid_items:** A list of items (strings) that must NOT be in the player's inventory to trigger the exchange.
**expend:** Boolean (False by default). If True, remove the required items from the player's inventory when the action is run. If False, allow the player to keep their items after performing the action.

If all of the conditions for an exchange (items and flags) are not met, then the exchange will not display as an option in the conversation.

**callback:** A function to execute when the exchange is run (see Callbacks).
**warp**: A room ID (string) to set as the current room when the exchange is triggered. If left blank, no warp will occur.
**end:** Boolean (False by default). If True, the conversation will end when this exchange is triggered, after its lines are displayed. If False, continue to present the player with options as normal.

## Ending conversations
There are two ways to end a conversation:

1. Use "end" as the exchange ID of one of the options (in the branches list). Use this if you want the conversation to end as soon as an option is chosen, with no feedback.
2. Trigger an exchange where "end" is True. Use this if you want to display a final message and/or trigger a callback (see Callbacks) when the conversation ends.

## Syntax
Creating a conversation is as simple as instantiating a conversation and supplying it with the required paramaters. It's easiest to instantiate the exchanges in-line with the conversation.

Below is an excerpt of the code that makes up the conversation above. The indentation is not necessary to the syntax, but it makes the code much more readable.

```python
import grapefruit as gf

gf.conversation(id="shopkeeper_talk",
                exhanges=[
                    gf.exchange(id="start",
                        lines=["Hi, how can I help you?"],
                        options=["I want to buy", "I want to sell", "It's nothing, nevermind."],
                        branches=["buy","sell","end"]
                    ),
                    gf.exchange(id="buy",
                        lines=["Sure, what would you like to buy?"],
                        options=["Milk","Eggs","I changed my mind","I can't afford anything."],
                        branches=["milk","buy_eggs","start","broke"]
                    ),
                    gf.exchange=(id="broke",
                        lines=["Oh, okay, please come back later then! Bye!"],
                        options=[],
                        branches=[],
                        avoid_items=["One Dollar"],
                        end=True
                    ),
                    gf.exchange(id="milk",
                        lines=["Here you go, thank you!"],
                        options=["Thanks."],
                        branches=["start"],
                        need_items=["One Dollar"],
                        expend=True,
                        gives_items=["Milk"]
                    ),
                    ...
                ]
)
```

## Triggering Conversations
Once you have defined a conversation, you can trigger it directly in one of two ways.

1. Assign the conversation to a variable, and use the run_conversation method in your own plugins or callbacks (see Callbacks):

```python
shopkeeper_talk = gf.conversation(id="shopkeeper_talk",
...
)

def my_plugin():
    shopkeeper_talk.run_conversation()
    return
```

2. Specify the conversation ID as the "conversation" paramater of an action.

```python
gf.conversation(id="shopkeeper_talk",
...
)

gf.action(id="try_talking",
        conversation="shopkeeper_talk",
        ...
)
```