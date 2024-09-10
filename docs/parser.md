# Parser
The command parser is the backbone of the Grapefruit engine. It's the part that takes the user's input and intereprets it as an action. Most of the time, the parser can safely be thought of as a black box. However, when trying to debug stubborn actions that just won't trigger, it can be useful to understand its process in depth.

## Overview
Before any parsing is done, the command is checked against the list of look actions, inventory actions, and dev actions (in dev mode only). If any are detected, then the parser is bypassed, and the relevant special command is returned.

The parser works in three phases that are connected to each other.

The first phase is **candidate generation.** This phase reads the command and generates a set of all the commands which might be relevant. In a few cases, it can also bypass the other two phases entirely and directly return an action ID. If dev mode is enabled, the list of action candidates will be printed to the screen during this phase.

The second phase is **candidate selection.** A series of ordered steps are performed to try selecting a single action out of all candidates. The selected action is not necessarily the one most likely intended by the player by this point. If dev mode is enabled, then the attempted and successful strategies will be printed to the screen.

If an action is selected, it is sent to the third phase, **candidate verification.** The selected action is checked against a set of criteria to determine whether it was likely intended by the player. If the verification passes, then the selected action's ID is returned. If it fails, then control returns to the candidate selection phase, where the next strategy in sequence will be tried. If dev mode is enabled, each of the verification checks will be printed to the screen, as well as a note if any of the checks fail.

When the parser is successful, the ID of the intended action (not the action itself) is returned. When it fails, the generic failure message is printed, and the string "none" is returned.

Because the process is non-linear and somewhat cyclical, a flowchart is included that clearly illustrates the specifics of the parser's operation. However, it will also be described here for completeness. Note that this documentation is meant to provide a human-readable overview of the *intended process* and does not elaborate on implementation details (such as data structures).

## Candidate generation
1. Extract all verbs and nouns from the command and discard all other words.
2. Create a set of all actions associated with any of the verbs or nouns from the command. This is the initial set of candidates.
3. Eliminate all actions that are not allowed in the current room.
4. Eliminate all actions that have zero relevant verbs in the command (including generic verbs) and all candidates that have zero relevant nouns in the command (if nouns are specified for the action.)
5. If there is exactly one action candidate remaining, return it.
6. If there is exactly one action candidate remaining with both a verb AND a noun present, return it.
7. Continue to candidate selection.

## Candidate Selection
Candidate selection tries five strategies, twice each, to choose a single action. If any of the strategies fails, the next one in the sequence is tried. If a strategy succeeds, but verification fails, then the next one is sequence will be tried in that case too.

1. If there is exactly one action candidate with verb enforcement disabled, select it and send to verification.
2. If there is exactly one action candidate with all of its flag conditions met, select it and send to verification.
3. If there is exactly one action candidate with all of its item conditions met, select it and send to verification.
4. If there is exactly one action candidate with all of its flag AND item conditions met, select it and send to verification.
5. If there is exactly one action candidate with both a verb and a noun present, select it and send to verification.
6. Eliminate all action candidates that do not have at least one verb and one noun present in the command, then try all five strategies again with the reduced candidate set.
7. If all five strategies still fail with the reduced set, fail to parse.

## Candidate verification
In order to pass verification, the following four criteria must be met.

1. At least one verb associated with the selected action must be present in the command (including generic verbs is verb enforcement is disabled for the action).
2. If the selected action has any nouns specified, at least one of its nouns must be present in the command.
3. The command must not contain any nouns that are NOT relevant to the selected action, but ARE relevant to at least one other action in the candidate set.
4. The command must not contain any verbs that are NOT relevant to the selected action, but ARE relevant to at least one action in the candidate set in the candidate set that does NOT have an associated noun in the command. (For clarity, this is written as two steps in the flowchart.)

If all four criteria are met, verification passes and the selected action is returned. Otherwise, control returns to candidate selection.

---

# Aggressive Parser
In addition to the standard command parser, a completely different parser called the **agressive parser** may be used by changing the parser mode (see below). **The aggressive parser will be minimally maintained and may not support engine features added after the initial release.** As such, its use is not generally recommended. The aggressive parser was a rough first attempt at the normal parser, and is only retained because it has different properties which may be desirable in some situations:

+More likely to select an action
+Less picky about syntax
-Creates more false positives
-Can behave unexpectedly when multiple actions are referenced in a single command
~Unconditionally favors verbs, even when unrelated nouns are specified

The return behavior is the same for the aggressive parser as it is for the normal parser -- it returns the ID of the selected action (not the action itself) when successful, and "none" when it fails. Upon failure, it will print the generic failure message to the screen.

A flowchart is available for the aggressive parser, just like for the normal parser.

## Overview (Aggressive)
Like the normal parser, the aggressive parser operates in three phases.

The first two phases are still **candidate generation,** which is mostly the same as in the normal parser; and **candidate selection,** which has the same purpose as in the normal parser but operates differently.

The third phase is **candidate elimination,** which repeatedly manipulates and reduces the set of candidates in various ways until the selection phase is successful. The aggressive parser does not have a verification phase.

## Candidate Generation (Aggressive)
This phase works exactly the same as in the normal parser, *except* that control is handed to the selection phase immediately after step 4.

## Candidate Selection (Aggressive)
This phase tries six different strategies to select an action from the set of candidates. If any of the strategies is successful, then the action chosen by that strategy is immediately returned.

1. There is exactly one action candidate with both a verb AND a noun present in the command -- return that action.
2. The command does not contain any verbs relevant to any candidates, but DOES contain generic verbs; and a noun for exactly one action candidate with verb enforcement disabled is present in the command -- return the action associated with the noun.
3. There is exactly one action candidate with its flag conditions met -- return that action.
4. There is exactly one action candidate with its item conditions met -- return that action.
5. There is exactly one action candidate with its flag AND item conditions met -- return that action.
6. There is exactly one action candidate associated with a verb from the command (not including generic verbs), and more than one action candidate associated with a noun from the command -- return the action associated with the verb.
7. If this point is reached, go to candidate elimination.

## Candidate Elimination (Aggressive)
The elimination phase can be reached a maximum of five times, and its behavior differs depending on how many times it has already been reached. The first item in this list is what will run the first time this phase is reached.

1. Eliminate all candidates associated with any nouns from the command, then restart candidate selection.
2. Undo the previous elimination round and eliminate all candidates with verb enforcement enabled, then restart candidate selection.
3. Same as round 1 -- Eliminate all candidates associated with any nouns from the command, then restart candidate selection.
4. Eliminate all action candidates that do not have at least one verb and one noun present in the command, then restart candidate selection.
5. Fail to parse.

---

# Parser Modes
The parser has three modes that can be selected between by changing the value of Grapefruit.parser_mode to 0, 1, or 2. 0 is the default and is recommended in most cases.

0. Use the normal parser.
1. Use the aggressive parser.
2. Try using the normal parser first. If it fails, suppress the failure message and try the aggressive parser.