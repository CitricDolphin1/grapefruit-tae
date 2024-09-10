import json
import sys

'''
    This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 
'''

gf = sys.modules[__name__]

start_message = ["Welcome to grapefruit!", "Please read the documentation and replace this start message with your own."]
prompt = ">" #Displayed at the comamand line
inventory_commands = ["inventory", "view inventory", "check inventory"] #commands to view inventory. overrides normal actions
look_commands = ["look", "look around"] #commands to look around the room
inventory_message = "Your inventory:" #shown before displaying inventory contents
fail = "You can't do that." #Shown when no valid action is found or no failure message is specificed for a failed action
inventory = [] #List of items in inventory
flags = [] #List of active flags
rooms = {} #Internal use only - the dictionary of rooms
conversations = {} #Internal use only - the dictionary of conversations
current_room = None #Mostly for internal use, set this to the starting room before running. Simply holds the current room
look_by_default = False #If true, automatically display the room description when entering a new room.
dead_actions = [] #Internal use only, contains a list of command IDs that have already run and can not be repeated
generic_verbs = ["use", "interact", "utilize", "do"] #List of verbs where at least one must be present to activate a non-enforced action without its specific verbs.
dev_mode = False #If true, rebuild dictionaries on every launch, enable verbose logging for command parsing and execution, and ignore fatal errors
end_game = False #Internal use only - if True, the game loop terminates
actions_dict = {} #Internal use only - the dictionary of actions
actions = [] #Internal use only - a list of all possible actions (action objects, not IDs)
parser_mode = 0 #Determines whether to use the normal or aggressive parser, or both

class action:
    '''The core of the Grapefruit engine. Actions are basically event modules activated by the verbs and nouns associated with them, which can optionally have external functions attached.
    There are WAY too many attributes here, and even more that can be configured after init, so please refer to the documentation.
    
    At a minimum, requires a unique id (any string), a success string, and at least one verb or noun.'''
    def __init__(self, id, success, verbs=[], nouns=[], need_items=[], warp="", enforce=False, expend=False, need_flags=[], gives_items=[], repeat=True, repeat_message="", items_fail="", flags_fail="", allowed_rooms=[], set_flags=[], remove_flags=[], avoid_flags=[], callback=None, fail_callback=None, conversation="", need_nouns=[]):
        if id in inventory_commands:
            print(f"Grapefruit ERROR: Tried to define an action with id {id}, which is already an inventory command.")
            if dev_mode == True:
                print("DEV: Continuing because DEV MODE is enabled.")
                print("DEV: THIS ERROR IS FATAL IN PRODUCTION MODE!!")
            else:
                print("The program will now close.")
                exit()
        if id in look_commands:
            print(f"Grapefruit ERROR: Tried to define an action with id {id}, which is already a look command.")
            if dev_mode == True:
                print("DEV: Continuing because DEV MODE is enabled.")
                print("DEV: THIS ERROR IS FATAL IN PRODUCTION MODE!!")
            else:
                print("The program will now close.")
                exit()
        if id in ["look","inventory","warp","setflag","delflag","setitem","delitem","undo","flags","validate"]:
            print(f"Grapefruit ERROR: {id} is a reserved word and is not a valid action ID.")
            if dev_mode == True:
                print("DEV: Continuing because DEV MODE is enabled.")
                print("DEV: THIS ERROR IS FATAL IN PRODUCTION MODE!!")
            else:
                print("The program will now close.")
                exit()
        
        self.id = id
        self.verbs = verbs
        self.nouns = nouns
        self.enforce = enforce
        self.expend = expend
        self.need_items = need_items
        self.success = success
        self.need_flags = need_flags
        self.gives_items = gives_items
        self.repeat = repeat
        self.repeat_message = repeat_message
        self.allowed_rooms = allowed_rooms
        self.warp = warp
        self.set_flags = set_flags
        self.remove_flags = remove_flags
        self.callback = callback
        self.fail_callback = fail_callback
        self.avoid_flags = avoid_flags
        self.conversation = conversation
        self.need_nouns = need_nouns

        if items_fail != "":
            self.items_fail = items_fail
        else:
            self.items_fail = gf.fail
        if flags_fail != "":
            self.flags_fail = flags_fail
        else:
            self.flags_fail = gf.fail
        if repeat_message != "":
            self.repeat_message = repeat_message
        else:
            self.repeat_message = gf.fail

        gf.actions.append(self)


    id = "" #Unique ID for this action
    verbs = [] #List of verbs that can invoke the action
    nouns = [] #List of nouns associated with the action
    need_nouns = [] #List of nouns that MUST be present in the command for the action to succeed. Ignored by parser
    enforce = False #Whether to enforce the use of custom verbs instead of generic ones like "use"
    need_items = [] #List of items the player must have to invoke the action
    expend = False #Whether to delete the objects from the player's inventory
    need_flags = [] #List of flags that must be true in order to invoke the action.
    set_flags = [] #Flags to set when the action is invoked.
    remove_flags = [] #Flags to remove when the action is invoked.
    avoid_flags = [] #Flags that will prevent the action from being invoked.
    success = "" #Text to display when the action runs successfully.
    flags_fail = fail #Text to display when the action is invoked, but fails due to missing flags.
    items_fail = fail #Text to display when the action is invoked, but fails due to missing items.
    gives_items = [] #Items to add to the player's inventory when action is invoked
    callback = None #Optional function to run on success
    fail_callback = None #Optional function to run on failure
    allowed_rooms = [] #List of room IDs the action works in. Works in all rooms if empty.
    warp = "" #ID of a room to warp the player to when the action runs
    repeat = True #Whether to allow repeating the action
    repeat_message = "" #Message when attempting to repeat an action that can not be repeated
    conversation = "" #Conversation to run the when the action is triggered

class room:
    '''A room for the grapefruit engine. Does nothing on its own, but can have actions associated with it.
    The basis for the illusion of space.
    
    id: (str) A unique id for the room.
    description: (list) a list of strings to display line by line when the player looks around the room.
    '''
    def __init__(self, id, description):
        self.id = id
        self.description = description
        gf.rooms[id] = self
    id = "" #Unique ID for the room
    description = [] #List of lines of text to display when the player looks around

class exchange:
    '''One set of dialogue and dialogue options for use in a conversation.
    See documentation for all parameters and proper usage.
    At a minimum, requires a unique id and list of lines of dialogue.'''
    def __init__(self, id, lines, options=[], branches=[], need_flags=[], avoid_flags=[], set_flags=[], remove_flags=[], need_items=[], gives_items=[], expend=False, callback=None, warp="", end=False, avoid_items=[]):
        if id == "end":
            fatal_error(f"Grapefruit ERROR: {id} is a reserved keyword and is not a valid exchange id.")
        
        self.id = id
        self.lines = lines
        self.options = options
        self.branches = branches
        self.need_flags = need_flags
        self.avoid_flags = avoid_flags
        self.set_flags = set_flags
        self.remove_flags = remove_flags
        self.need_items = need_items
        self.gives_items = gives_items
        self.expend = expend
        self.callback = callback
        self.warp = warp
        self.end = end
        self.avoid_items = avoid_items

        if options == []:
            self.end = True

    id = ""
    lines = []
    options = []
    branches = []
    need_flags = []
    avoid_flags = []
    set_flags = []
    remove_flags = []
    need_items = []
    gives_items = []
    expend = False
    callback = None
    warp = ""
    end = False
        


class conversation:
    '''A set of exchanges to be explored in a dialogue interaction.
    Requires a unique id and a list of exchanges. See documentation for full usage.'''
    def __init__(self, id, exchanges):
        self.id = id
        self.exchanges_dict = {}
        for exchange in exchanges:
            if exchange.id in self.exchanges_dict.keys():
                fatal_error(f"GRAPEFRUIT ERROR: Tried to define duplicate exchange id {exchange.id} in {self.id}")
            self.exchanges_dict[exchange.id] = exchange
        gf.conversations[id] = self
        
    id = ""
    exchanges_dict = {}

    def __run_exchange(self, exchange, exchanges_dict):
        for flag in exchange.set_flags:
            setflag(flag)

        for flag in exchange.remove_flags:
            if flag in flags:
                delflag(flag)

        for item in exchange.gives_items:
            inventory.append(item)

        if exchange.expend == True:
            for item in exchange.need_items:
                if item in inventory:
                    inventory.remove(item)
                else:
                    devprint(f"DEV WARNING: tried to remove invalid item {item} from inventory")


        for line in exchange.lines:
            print(line)
        print()

        if exchange.warp != "":
            warp(exchange.warp)

        if exchange.callback != None:
            try:
                proceed = exchange.callback()
                if proceed == False:
                    return "end"
            except TypeError:
                pass

        if exchange.end == True:
            return "end"

        branches = []
        options = []
        for i in range(len(exchange.branches)):
            branch_id = exchange.branches[i]
            if branch_id == "end":
                branches.append(exchange.branches[i])
                options.append(exchange.options[i])
                continue
            if branch_id not in self.exchanges_dict.keys():
                devprint(f"DEV: Bypassing invalid exchange {branch_id} in conversation {self.id}")
                continue
            branch = exchanges_dict[branch_id]
            if sorted(_get_overlap(branch.need_flags, flags)) == sorted(branch.need_flags):
                if _get_overlap(branch.avoid_flags, flags) == []:
                    if _get_overlap(branch.avoid_items, inventory) == []:
                        if sorted(_get_overlap(inventory, branch.need_items)) == sorted(branch.need_items):
                            branches.append(exchange.branches[i])
                            options.append(exchange.options[i])


        while True:
            for i in range(len(options)):
                print(f"{i+1}: {options[i]}")

            print()
            user_choice = input(prompt)
            try:
                user_choice = int(user_choice) - 1  
            except:
                print("Please choose a valid option.")
                print()
                continue
            
            if user_choice not in range(len(options)):
                print("Please choose a valid option.")
                print()
                continue

            return branches[user_choice]
    
    def run_conversation(self):
        current_branch = list(self.exchanges_dict)[0]
        while current_branch != "end":
            if current_branch in self.exchanges_dict.keys():
                next_branch = self.__run_exchange(self.exchanges_dict[current_branch], self.exchanges_dict)
                current_branch = next_branch
            else:
                fatal_error(f"GRAPEFRUIT ERROR: Triggered invalid exchange {current_branch}")
                devprint("DEV: Ending conversation due to error.")
                return
        return
    
class save:
    '''Stores session information in a single object. This includes inventory, flags, current room, and unrepeatable actions.
    Does NOT handle saving to files directly.
    If you need multi-session persistence, implement your own system to serialize this object using e.g. pickle.'''

    def __init__(self):
        self.saved_inventory = gf.inventory
        self.saved_flags = gf.flags
        self.saved_room = gf.current_room
        self.saved_dead_actions = gf.dead_actions

    saved_inventory = []
    saved_flags = []
    saved_room = None
    saved_dead_actions = []

def load(save):
    '''Restores session information from a save object.
    Does NOT handle loading from files directly.
    If you need multi-session persistence, serialize and deserialize the save object using e.g. pickle, and instantiate it before using this function.'''
    gf.inventory = save.saved_inventory
    gf.flags = save.saved_flags
    gf.current_room = gf.saved_room
    gf.dead_actions = save.saved_dead_actions
    return

def fatal_error(error):
    '''Terminate the game with the given error message.
    In dev mode, display the error but continue execution.'''
    print(error)
    if dev_mode == True:
        print("Continuing because DEV MODE is enabled.")
        print("THIS ERROR IS FATAL IN PRODUCTION MODE!!")
    else:
        print("The game will now close.")
        exit()

def warp(room_id):
    '''Set the current room to the room with the given id.'''
    if room_id in rooms.keys():
        devprint(f"DEV: Warping to {room_id}")
        gf.current_room = rooms[room_id]
        for line in rooms[room_id].description:
            print(line)
    else:
        fatal_error(f"GRAPEFRUIT ERROR: Tried to warp to invalid room {room_id}")

def setflag(flag):
    if flag in flags:
        devprint(f"DEV WARNING: Tried to set duplicate flag {flag}")
    else:
        flags.append(flag)
        devprint(f"DEV: Set flag {flag}")
    return

def delflag(flag):
    if flag not in flags:
        devprint(f"DEV WARNING: Tried to remove non-existent flag {flag}")
    else:
        flags.remove(flag)
        devprint(f"DEV: Removed flag {flag}")
    return

def devprint(string):
    '''Print a string only if the game is in dev mode.'''
    if gf.dev_mode == True:
        print(string)
    return

def validate(actions_list):
    '''Check for unused/redundant content and invalid references.'''
    if dev_mode == False:
        print("Validation is only available when dev mode is enabled.")
        return
    
    print("Note: validation does not check callback functions or plugins.")
    print()

    print("Checking for global actions...")
    for action in actions_list:
        if action.allowed_rooms == []:
            print(f"GLOBAL ACTION: {action.id} is allowed in all rooms.")
    print()
    
    print("Checking and logging warps...")
    warps = []
    for action in actions_list:
        if action.warp != "":
            warps.append(action.warp)
        if action.warp not in rooms.keys() and action.warp != "":
            print(f"INVALID WARP!! action id: {action.id} warp: {action.warp}")
    for conversation in conversations.values():
        for exchange in conversation.exchanges_dict.values():
            if exchange.warp != "":
                warps.append(exchange.warp)
            if exchange.warp not in rooms.keys() and exchange.warp != "":
                print(f"INVALID WARP!! exchange id: {exchange.id} warp: {exchange.warp}")

    print()

    print("Checking rooms...")
    print("If the default room shows up here, you can usually ignore it.")
    for room_id in rooms.keys():
        if room_id not in warps:
            print(f"UNREACHABLE ROOM!! {room_id} has no warps!")
    print()

    print("Checking items...")
    given_items = []
    needed_items = {}
    for action in actions_list:
        for item in action.need_items:
            if item not in needed_items.keys():
                needed_items[item] = []
            needed_items[item].append(action.id)

        for item in action.gives_items:
            if item not in given_items:
                given_items.append(item)

    for conversation in gf.conversations.values():
        for exchange in conversation.exchanges_dict.values():
            for item in exchange.need_items:
                if item not in needed_items.keys():
                    needed_items[item] = []
                needed_items[item].append("exchange " + exchange.id)

            for item in exchange.gives_items:
                if item not in given_items:
                    given_items.append(item)

    for item in needed_items.keys():
        if item not in given_items:
            print(f"IMPOSSIBLE ITEM!! {item} is needed by {needed_items[item]} but never given!")
    print()

    print("Checking flags...")
    set_flags = {}
    checked_flags = {}
    avoided_flags = {}
    for action in actions_list:
        for flag in action.need_flags:
            if flag not in checked_flags.keys():
                checked_flags[flag] = []
            checked_flags[flag].append(action.id)

        for flag in action.set_flags:
            if flag not in set_flags.keys():
                set_flags[flag] = []
            set_flags[flag].append(action.id)

        for flag in action.avoid_flags:
            if flag not in avoided_flags.keys():
                avoided_flags[flag] = []
            avoided_flags[flag].append(action.id)

    for conversation in gf.conversations.values():
        for exchange in conversation.exchanges_dict.values():
            for flag in exchange.need_flags:
                if flag not in checked_flags.keys():
                    checked_flags[flag] = []
                checked_flags[flag].append("exchange " + exchange.id)

            for flag in exchange.set_flags:
                if flag not in set_flags.keys():
                    set_flags[flag] = []
                set_flags[flag].append("exchange " + exchange.id)

            for flag in exchange.avoid_flags:
                if flag not in avoided_flags.keys():
                    avoided_flags[flag] = []
                avoided_flags[flag].append("exchange " + exchange.id)

    for flag in checked_flags.keys():
        if flag not in set_flags.keys():
            print(f"IMPOSSIBLE FLAG! {flag} is needed by {checked_flags[flag]} but never set!")
    print()

    for flag in set_flags.keys():
        if flag not in checked_flags.keys() and flag not in avoided_flags.keys():
            print(f"UNUSED FLAG! {flag} is set by {set_flags[flag]} but never checked!")
    print()

    for flag in avoided_flags.keys():
        if flag not in set_flags.keys():
            print(f"UNUSED FLAG! {flag} is avoided by {avoided_flags[flag]} but never set!")
    print()

    print("Checking conversations...")
    for conversation in conversations.values():
        defined_branches = []
        referenced_branches = []
        for exchange in conversation.exchanges_dict.values():
            if exchange.id != list(conversation.exchanges_dict)[0]:
                defined_branches.append(exchange.id)
            for branch in exchange.branches:
                if branch != "end":
                    referenced_branches.append(branch)
        for branch in defined_branches:
            if branch not in referenced_branches:
                print(f"UNREACHABLE BRANCH! {branch} is defined in {conversation.id} but never referenced!")
        for branch in referenced_branches:
            if branch not in defined_branches and branch != list(conversation.exchanges_dict)[0]:
                print(f"INVALID BRANCH! {branch} is referenced in {conversation.id} but never defined!")
    print()

    print("Validation complete.")
    print()


def _get_overlap(list1, list2):
    '''Intended for internal use by Grapefruit. Returns the cardinal intersection of two lists.'''
    return list(set(list1) & set(list2))

def _inverse(dict):
    '''For internal use only.
    Return the inverse of a dictionary where the values are lists.'''
    final_dict = {}

    for i in range(len(dict)):
        key = list(dict.keys())[i]
        value = list(dict.values())[i]
        for item in value:
            if item not in final_dict.keys():
                final_dict[item] = []
            if key not in final_dict[item]:
                final_dict[item].append(key)

    return final_dict
            
def build_dictionary():
    '''Rebuilds the nouns.json and verbs.json files from scratch, which are required for the game to run.
    The engine does this automatically on first launch, and on every launch if dev_mode is True, so it's usually best to leave this alone.
    
    Inputs:
        actions: a list of actions.
    Outputs:
        None.'''
    dictionary = {}
    for action in actions:
        for verb in action.verbs:
            if not verb in dictionary.keys():
                dictionary[verb] = [action.id]
            else:
                dictionary[verb].append(action.id)
    
    with open ("verbs.json", "w") as dict_file:
        json.dump(dictionary, dict_file, indent=4)

    nouns_dictionary = {}
    for action in actions:
        for noun in action.nouns:
            if not noun in nouns_dictionary.keys():
                nouns_dictionary[noun] = [action.id]
            else:
                nouns_dictionary[noun].append(action.id)
        for item in action.need_items:
            if not item in nouns_dictionary.keys():
                nouns_dictionary[item] = [action.id]
            else:
                nouns_dictionary[item].append(action.id)

    with open ("nouns.json", "w") as nouns_file:
        json.dump(nouns_dictionary, nouns_file, indent=4)

def _build_actions_dict():
    '''For internal use only.
    Build and return the dictionary of actions, given a list of actions.'''
    dict = {}
    for action in actions:
        dict[action.id] = action
    return dict

def _load_verb_dictionary():
    '''For internal use only.
    Load and return the dictionary of verbs.'''
    dicts = []
    with open ("verbs.json", "r") as dict_file:
        return json.load(dict_file)
        
def _load_noun_dictionary():
    '''For internal use only.
    Load and return the dictionary of verbs.'''
    dicts = []
    with open ("nouns.json", "r") as dict_file:
        return json.load(dict_file)
    
def parse_normal(command, verbs_dict, nouns_dict, actions_dict, room):
    '''Intreprets a command and returns the ID of the action most likely to be intended by the player.
    
    Inputs:
        command: a string representing the user's typed command
        verbs_dict: the verbs dictionary
        nouns_dict: the nouns dictionary
        actions_dict: the actions dictionary
        room: the currently active room
    '''

    #Word association and candidate generation
    command = command.lower()
    words = command.split()
    noun_actions = {} # Noun:Action ID
    verb_actions = {} # Verb:Action ID

    if command in look_commands:
        return "look"
    if command in inventory_commands:
        return "inventory"
    
    if dev_mode == True:
        if len(words) > 0:
            if words[0] in ["warp","setflag","delflag","setitem","delitem","undo","flags"]:
                return words[0]

    for word in words:
        if word in verbs_dict.keys():
            if word not in verb_actions.keys():
                verb_actions[word] = verbs_dict[word]
            else:
                for action_id in verbs_dict[word]:
                    verb_actions[word].append(action_id)
        if word in nouns_dict.keys():
            if word not in noun_actions.keys():
                noun_actions[word] = nouns_dict[word]
            else:
                for action_id in nouns_dict[word]:
                    noun_actions[word].append(action_id)

    inverse_noun_actions = _inverse(noun_actions) #Action ID:Verb
    inverse_verb_actions = _inverse(verb_actions) #Action ID:Noun

    room_candidates = []
    for action_id in list(inverse_verb_actions.keys()) + list(inverse_noun_actions.keys()):
        action = actions_dict[action_id]
        if (action.allowed_rooms == [] or room.id in action.allowed_rooms) and action_id not in room_candidates:
            room_candidates.append(action_id)

    #Filter by relevance (verb + [], non-enforced noun + [], verb + noun)
    verb_noun_overlap = _get_overlap(inverse_noun_actions.keys(), inverse_verb_actions.keys())
    candidates = []
    for action_id in room_candidates:
        action = actions_dict[action_id]
        if (_get_overlap(action.verbs, words) != [] and action.nouns == []) or (_get_overlap(action.nouns, words) != [] and action.enforce == False) or (action_id in verb_noun_overlap):
            candidates.append(action_id)
    devprint("DEV: Action candidates:")
    devprint(candidates)

    #No candidates
    if candidates == []:
        devprint("DEV: No valid candidates")
        if gf.parser_mode == 0:
            print(fail)
        return "none"
    
    #One candidate
    if len(candidates) == 1:
        devprint("DEV: Parsed by only valid candidate")
        return candidates[0]

    #Try single verb/noun overlap
    if len(verb_noun_overlap) == 1:
        devprint("DEV: Parsed by single verb/noun overlap")
        return verb_noun_overlap[0]
    
    #Break ties
    final_candidate = "none"
    error = False
    devprint("DEV: Trying to break tie by specificity and conditions...")
    i = 0
    filtered = False
    all_candidates = candidates.copy()
    while i < 6:

        if error == True:
            final_candidate = "none"
            error = False
            continue

        # This block runs OUT OF SEQUENCE from how you'd expect, mind the conditionals (can not possibly run on first iteration)
        if final_candidate != "none": 
            devprint("Attempting to verify selected action...")
            try:
                final_candidate_verbs = inverse_verb_actions[final_candidate]
            except KeyError:
                final_candidate_verbs = []
            try:
                final_candidate_nouns = inverse_noun_actions[final_candidate]
            except KeyError:
                final_candidate_nouns = []

            action = actions_dict[final_candidate]
            # if no specific verbs, and no generic verbs (when those are allowed)
            if final_candidate_verbs == [] and (_get_overlap(words, gf.generic_verbs) == [] or action.enforce == True):
                devprint("DEV: Rejecting selected action due to missing verbs")
                error = True
                continue

            # if action has associated nouns but none are used in command
            if final_candidate_nouns != [] and _get_overlap(words, action.nouns) == []:
                devprint("DEV: Rejecting selected action due to missing nouns")
                error = True
                continue

            extra_nouns = [noun for noun in noun_actions.keys() if noun not in final_candidate_nouns]
            for action_id in all_candidates:
                action = actions_dict[action_id]
                #   extra nouns are present                           nouns were used
                if _get_overlap(extra_nouns, action.nouns) != [] and final_candidate_nouns != []:
                    error = True
                    final_candidate = "none"
                    devprint("DEV: Rejecting selected action due to noun conflict")
                    break
            if error == True:
                continue

            extra_verbs = [verb for verb in verb_actions.keys() if verb not in final_candidate_verbs]
            for action_id in all_candidates:
                action = actions_dict[action_id]
                #   extra verbs are present                             potential conflict does not use relevant nouns
                if _get_overlap(extra_verbs, action.verbs) != [] and _get_overlap(final_candidate_nouns, action.nouns) == []:
                    error = True
                    final_candidate = "none"
                    devprint("DEV: Rejecting selected action due to verb conflict")
                    break
            if error == True:
                continue

            devprint("DEV: Selected action passed verification")
            return final_candidate

        if i == 0:
            devprint("DEV: Trying to break tie by verb enforcement...")
            non_enforced_actions = [] #Try by verb enforcement
            for action_id in candidates:
                action = actions_dict[action_id]
                if action.enforce == False:
                    non_enforced_actions.append(action_id)
            if len(non_enforced_actions) == 1:
                final_candidate = non_enforced_actions[0]
                devprint(f"DEV: Selected action {final_candidate} by verb enforcement filtering")
                i += 1
                continue

        if i == 1:
            devprint("DEV: Trying to break tie by flag conditions...")
            flag_actions = []
            for action_id in candidates:
                action = actions_dict[action_id]
                #   needed flags are set                                                            no avoided flags are set
                if sorted(_get_overlap(flags, action.need_flags)) == sorted(action.need_flags) and _get_overlap(flags, action.avoid_flags) == []:
                    flag_actions.append(action_id)
            if len(flag_actions) == 1:
                final_candidate = flag_actions[0]
                devprint(f"DEV: Selected action {final_candidate} by flag conditions")
                i += 1
                continue

        if i == 2:
            devprint("DEV: Trying to break tie by item conditions...")
            item_actions = []
            for action_id in candidates:
                action = actions_dict[action_id]
                #   needed items are in inventory
                if sorted(_get_overlap(inventory, action.need_items)) == sorted(action.need_items):
                    item_actions.append(action_id)
            if len(item_actions) == 1:
                final_candidate = item_actions[0]
                devprint(f"DEV: Selected action {final_candidate} by item conditions")
                i += 1
                continue

        if i == 3:
            devprint("DEV: Trying to break tie by flag + item overlap...")
            if len(_get_overlap(item_actions, flag_actions)) == 1:
                final_candidate = _get_overlap(item_actions, flag_actions)[0]
                devprint(f"DEV: Selected action {final_candidate} by flag + item overlap")
                i += 1
                continue

        if i == 4:
            devprint("DEV: Trying to break tie by verb/noun overlap...")
            if len(verb_noun_overlap) == 1:
                if verb_noun_overlap[0] in candidates:
                    final_candidate = verb_noun_overlap[0]
                    devprint(f"DEV: Selected action {final_candidate} by verb/noun overlap")
                    i += 1
                    continue

        if i == 5 and filtered == False:
            filtered = True
            devprint("DEV: Filtering by verb/noun overlap and restarting...")
            candidates_temp = candidates.copy()
            candidates = []
            for action_id in candidates_temp:
                if action_id in verb_noun_overlap:
                    candidates.append(action_id)
            i = 0
            continue
        elif i == 5 and filtered == True:
            i = 6
            continue

        i += 1
        continue

    # Failure state
    if gf.parser_mode == 0:
        devprint("DEV: Failed to choose an action, checking for a special failure state...")
        devprint("")
    else:
        devprint("DEV: Failed to choose an action, skipping failure message due to parser mode")
        return "none"

    print(fail)
    return "none"


def parse_aggressive(command, verbs_dict, nouns_dict, actions_dict, room):
    '''
    An older and different version of the command parser that is more likely to choose an action, but struggles with conflicts and sometimes returns unexpected actions.
    parse_normal should be preferred over this in most cases!
    
    Inputs:
        command: a string representing the user's typed command
        verbs_dict: the verbs dictionary
        nouns_dict: the nouns dictionary
        actions_dict: the actions dictionary
        room: the currently active room
    '''

    devprint("DEV: Using aggressive parser!")

    command = command.lower()
    if command in look_commands:
        return "look"
    if command in inventory_commands:
        return "inventory"
    
    words = command.split()
    if dev_mode == True:
        if len(words) > 0:
            if words[0] in ["warp","setflag","delflag","setitem","delitem","undo","flags"]:
                return words[0]
    
    verbs = []
    nouns = []
    verb_actions = []
    noun_actions = []
    for word in words:
        if word in verbs_dict.keys():
            verbs.append(word)
            for action_id in verbs_dict[word]:
                if action_id not in verb_actions:
                    verb_actions.append(action_id)

        if word in nouns_dict.keys():
            nouns.append(word)
            for action_id in nouns_dict[word]:
                if action_id not in noun_actions:
                    noun_actions.append(action_id)

    candidates = []
    for action_id in verb_actions + noun_actions:
        action = actions_dict[action_id]
        if (action.allowed_rooms == [] or room.id in action.allowed_rooms) and action_id not in candidates:
            candidates.append(action_id)

    for i in range(0,4):
        verb_actions = _get_overlap(candidates, verb_actions.copy())
        noun_actions = _get_overlap(candidates, noun_actions.copy())
        if i == 0:
            devprint("DEV: action candidates:")
            devprint(candidates)

        #By now, we only have actions associated with the command words and allowed in this room

        #Zero-th check: No candidates
        if len(candidates) == 0 and i == 0:
            return "none"

        #Only one valid candidate
        if len(candidates) == 1:
            devprint("DEV: parsed by only valid candidate")
            return candidates[0]
        
        #Single verb/noun overlap
        verb_noun_overlap = _get_overlap(verb_actions, noun_actions)
        if len(verb_noun_overlap) == 1:
            devprint("DEV: parsed by single verb/noun overlap")
            return verb_noun_overlap[0]
        
        #Single generic verb + noun
        if verbs == [] and _get_overlap(words, generic_verbs) != []:
            generic_noun_actions = []
            for action_id in noun_actions:
                if actions_dict[action_id].enforce == False:
                    generic_noun_actions.append(action_id)
            if len(generic_noun_actions) == 1:
                devprint("DEV: Parsed by single generic verb + noun")
                return generic_noun_actions[0]
        
        #Flag exclusive
        flag_actions = []
        for action_id in candidates:
            action = actions_dict[action_id]
            if sorted(_get_overlap(action.need_flags, flags)) == sorted(action.need_flags) and _get_overlap(action.avoid_flags, flags) == []:
                flag_actions.append(action_id)
        if len(flag_actions) == 1:
            devprint("DEV: parsed by flag conditions")
            return flag_actions[0]

        #Item exclusive
        item_actions = []
        for action_id in candidates:
            action = actions_dict[action_id]
            if sorted(_get_overlap(action.need_items, inventory)) == sorted(action.need_items):
                item_actions.append(action_id)
        if len(item_actions) == 1:
            devprint("DEV: parsed by item conditions")
            return item_actions[0]
        
        #Flag and item exclusive
        if len(_get_overlap(flag_actions, item_actions)) == 1:
            devprint("DEV: parsed by single item/flag overlap")
            return _get_overlap(flag_actions, item_actions)[0]

        #Filter by verb action in verb/noun conflict
        if len(verb_actions) == 1 and noun_actions != [] and _get_overlap(verb_actions, noun_actions) == []:
            devprint("DEV: parsed by preferring only verb action")
            return verb_actions[0]
            
        if i == 0 or i == 2:
            devprint("DEV: filtering for non-noun verb actions...")
            pre_noun_filter_candidates = candidates.copy()
            candidates = list(set(verb_actions) - set(noun_actions))
            
        #Filter out verb enforced actions, then repeat
        if i == 1:
            candidates = pre_noun_filter_candidates.copy()
            devprint("DEV: restoring noun actions and filtering verb enforced actions...")
            candidates_temp = candidates.copy()
            candidates = []
            for action_id in candidates_temp:
                action = actions_dict[action_id]
                if action.enforce == False:
                    candidates.append(action_id)
            continue

        #Only keep verb/noun overlaps
        if i == 3:
            devprint("DEV: filtering by verb/noun overlaps...")
            candidates_temp = candidates.copy()
            for action_id in candidates_temp:
                if action_id not in verb_noun_overlap:
                    candidates.remove(action_id)

    #Failed to parse
    return "none"

def parse(command, verbs_dict, nouns_dict, actions_dict, room):
    '''Parse a command using one or both parsers, depending on the parser mode currently set.
    See documentation for details on parsers.'''
    if gf.parser_mode > 2:
        fatal_error(f"GRAPEFRUIT ERROR: Invalid parser mode ({gf.parser_mode})")
        print("DEV: Defaulting to parser mode 0 due to error")
        gf.parser_mode = 0

    chosen_action = "none"
    if gf.parser_mode == 0 or gf.parser_mode == 2:
        chosen_action = parse_normal(command, verbs_dict, nouns_dict, actions_dict, room)
    if gf.parser_mode == 1 or (gf.parser_mode == 2 and chosen_action == "none"):
        chosen_action = parse_aggressive(command, verbs_dict, nouns_dict, actions_dict, room)

    return chosen_action

def _dev_actions(command):
    '''For internal use only.
    Handles special dev_mode-only commands.'''
    words = command.split()
    if len(words) < 2:
        arg = "[none]"
    else:
        arg = command.split(" ", 1)[1]
    command = words[0]

    if command == "warp":
        print(f"DEV: Warping to room with id {arg}")
        warp(arg)
        print()
        return True
    
    if command == "setflag":
        setflag(arg)
        return True
    
    if command == "delflag":
        delflag(arg)
        return True
    
    if command == "setitem":
        inventory.append(arg)
        print(f"DEV: added {arg} to inventory")
        return True
    
    if command == "delitem":
        if arg not in inventory:
            print(f"DEV: item {arg} not in inventory")
        else:
            inventory.remove(arg)
            print(f"DEV: item {arg} removed from inventory.")
        return True

    if command == "undo":
        if arg not in dead_actions:
            print(f"DEV: {arg} has not in dead actions list")
        else:
            dead_actions.remove(arg)
            print(f"DEV: {arg} can now be repeated")
        return True
    
    if command == "flags":
        print("DEV: Listing flags:")
        print(flags)
        return True
    
    return False



def run_action(command, action_id, actions_dict, room, flags, inventory):
    '''
    Attempts to run a specific action after verifying that it can be run.
    Also handles failure states.
    
    Inputs:
        command: a string representing the user's typed command
        action_id: the id of the action to be run
        actions_dict: the actions dictionary
        room: the currently active room
        flags: the flag list
        inventory: the inventory list

    Returns: None
    '''
    devprint(f"DEV: running action with id: {action_id}")
    if dev_mode == True:
        if _dev_actions(command) == True:
            return

    command = command.lower()
    if action_id == "look":
        for line in room.description:
            print(line)
        return
    if action_id == "inventory":
        print(inventory_message)
        for item in inventory:
            print(item)
        return

    if action_id == "none":
        return
    action = actions_dict[action_id]

    words = command.split()
    command_nouns = _get_overlap(words, action.nouns)
    command_verbs = _get_overlap(words, action.verbs)

    #Sanity check, this should never happen
    if room.id not in action.allowed_rooms and action.allowed_rooms != []:
        print(fail)
        return

    if action.enforce == True and command_verbs == []:
        print(fail)
        return
    
    if not (action.enforce == True and command_verbs == []):
        if action.repeat == False:
            if action.id in dead_actions:
                print(action.repeat_message)
                return
    
    error = "working"
    while error == "working":
        if action.enforce == False and command_verbs == []:
            if _get_overlap(words, gf.generic_verbs) == []:
                error = "no generic"
                devprint("DEV: action failed (no verbs)")
                continue
        if action.enforce == True and command_verbs == []:
            devprint("DEV: action failed (verb enforcement)")
            error = "enforce"
            continue
        if sorted(_get_overlap(inventory, action.need_items)) != sorted(action.need_items) and action.need_items != []:
            devprint("DEV: action failed (missing items)")
            devprint(f"DEV: Needs: {action.need_items}")
            error = "need items"
            continue
        if sorted(_get_overlap(flags, action.need_flags)) != sorted(action.need_flags) and action.need_flags != []:
            devprint("DEV: action failed (missing flags)")
            devprint(f"DEV: Needs: {action.need_flags}")
            error = "flags"
            continue
        if _get_overlap(flags, action.avoid_flags) != []:
            devprint("DEV: action failed (avoiding flags)")
            devprint(f"DEV: Avoids: {action.avoid_flags}")
            error = "flags"
            continue
        if sorted(_get_overlap(words, action.need_nouns)) != sorted(action.need_nouns):
            devprint("DEV: Action failed (requires nouns)")
            devprint(f"DEV: Requires: {action.need_nouns}")
            error = "nouns"
            continue

        #success state
        if action.success != "":
            print(action.success)
        for item in action.gives_items:
            inventory.append(item)
        for flag in action.set_flags:
            setflag(flag)
        for flag in action.remove_flags:
            delflag(flag)
        if action.expend == True:
            for item in action.need_items:
                inventory.remove(item)
        if action.warp != "":
            warp(action.warp)
        if action.repeat == False:
            dead_actions.append(action.id)
        if action.callback != None:
            action.callback()
        if action.conversation != "":
            conversations[action.conversation].run_conversation()
        return
        
    #Final failure state
    if error == "need items":
        print(action.items_fail)
        if action.fail_callback != None:
            action.fail_callback()
        return
    elif error == "flags":
        print(action.flags_fail)
        if action.fail_callback != None:
            action.fail_callback()
        return
    else:
        print(fail)
        return
    
def reset():
    '''Reset the engine, erasing all session progress and configured parameters, but maintaining defined actions, rooms, and conversations.'''
    gf.start_message = ["Welcome to grapefruit!", "Please read the documentation and replace this start message with your own."]
    gf.prompt = ">"
    gf.inventory_commands = ["inventory", "view inventory", "check inventory"]
    gf.look_commands = ["look", "look around"]
    gf.inventory_message = "Your inventory:"
    gf.fail = "You can't do that."
    gf.inventory = []
    gf.flags = []
    gf.current_room = None
    gf.look_by_default = False
    gf.dead_actions = []
    gf.generic_verbs = ["use", "interact", "utilize", "do"]
    gf.dev_mode = False
    gf.end_game = False #Internal use only
    gf.parser_type = 0

def end():
    '''Terminate the game loop.
    The only ways to use this are as a callback or by incorporating it into your own callback or plugin function.'''
    gf.end_game = True
    return
    
def start(default_room, plugin=None):
    '''Begin the core game loop. This will run until the Grapefruit.end() function is called.

    Inputs:
        -default_room: The ID of the room the game should start from.
        -plugin (optional): A function to run on every iteration of the game loop.
    Outputs: None
    '''

    nouns_dict = []
    verbs_dict = []
    actions_dict = []

    if dev_mode == True:
        print("DEV: DEV MODE IS ENABLED!! Rebuilding dictionary now.")
        print("DEV: Verbose processing is enabled, and most fatal errors will be bypassed.")
        print("DEV: Please disable this before release!!")
        print()
        build_dictionary()
        print()

    try:
        nouns_dict = _load_noun_dictionary()
        verbs_dict = _load_verb_dictionary()
    except:
        print("Failed to load dictionary files.")
        print("Rebulding dictionaries, please wait...")
        build_dictionary()
        nouns_dict = _load_noun_dictionary()
        verbs_dict = _load_verb_dictionary()
    finally:
        actions_dict = _build_actions_dict()

    for line in start_message:
        print(line)
    print()

    warp(default_room)
    print()

    while gf.end_game == False:
        if plugin != None:
            plugin()
        command = input(prompt)
        if command.lower() == "validate" and dev_mode == True:
            validate(actions)
        else:
            action_id = parse(command, verbs_dict, nouns_dict, actions_dict, current_room)
            run_action(command, action_id, actions_dict, current_room, flags, inventory)
        print()

    gf.end_game = False
    return