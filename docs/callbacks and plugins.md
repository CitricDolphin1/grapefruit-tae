# Callbacks and Plugins

Callbacks and plugins are ways to expand the game functionality. Syntactically, both are just functions treated as objects.

Callbacks and plugins can not accept any parameters. If you need to pass data into a function, use global variables, or access engine variables directly (see Tools).

## Callbacks
A callback can be executed in the following conditions:
-When an action is triggered and runs successfully
-When an action is triggered, but fails (for any reason EXCEPT trying to repeat an unrepeatable action)
-When an exchange is triggered

The callback will run exactly once and then return control to the core game loop (see Plugins below). To create a callback, simply define the function with no parameters, and then pass it as an object as the "callback" parameter of an action or exchange, or the "fail_callback" parameter of an action.

```python
import grapefruit as gf

def my_callback():
    print("Write your custom code here!")

gf.action(id="special_action",
            callback=my_callback,
            ...
)
```

If used in an exchange, the callback runs AFTER the items, flags, and warps of the exchange are processed, but BEFORE options are displayed or the conversation ends.

If used in an action, the callback runs AFTER the items, flags, and warps of the exchange are processed, but BEFORE the action's conversation is triggered (if applicable).

## Plugins
A plugin is executed on every iteration of the game loop. Plugins are the first thing executed in the loop, meaning they execute BEFORE the player types a command, the command is processed, and an action is run. Note that this means the plugin will run BEFORE control is ever handed to the player.

To create a plugin, simply define the function with no parameters, and then pass it as an object as the optional "plugin" parameter of the grapefruit.run function.

```python
import grapefruit as gf

def my_plugin():
    print("Write your custom code here!")

startroom = gf.room(id="start_room",
...
)
...
gf.run(startroom, my_plugin)
```