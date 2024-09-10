import grapefruit as game
import random

actions = []

def quit_func():
    print("Are you sure you want to quit?")
    quit_confirm = input("[Y/N]:")
    if quit_confirm.lower() == "y" or quit_confirm.lower() == "yes":
        game.end()
    else:
        print("Okay, no worries.")
        print()
        return
    
def end_game():
    exit()

take = ["take","get","pick","grab","keep","add","obtain"]

help_lines=["People with glass houses shouldn't throw stones.",
            "Don't trust everything you read on the internet.",
            "If something seems too good to be true, it probably is.",
            "Reply hazy, try again",
            "If at first you don't succeed, try, try again.",
            "Almost everybody can benefit from therapy.",
            "It's okay to cry.",
            "Make sure to drink lots of water every day.",
            "If you're leaving the country, check the national travel advisories first.",
            "Studies show there is no strategy that can reliably beat the stock market. Instead, you should invest in low- or no- fee index funds while employing a buy-and-hold strategy.",
            "If you press the 'Q' key on your keyboard, the letter Q will appear on your screen!",
            "Cycling is more efficient than driving and is a great choice for short commutes.",
            "To win this game, try doing things that achieve the outcome you want.",
            "Don't start a career as a text adventure narrator. Trust me.",
            "College is great, but it's not the right choice for everyone. Consider whether it will help your career before enrolling.",
            "Never salt your soup before you taste it.",
            "There's a secret room behind the cactus.",
            "This game's code is human-readable. To win the game, just cheat by reading the code!",
            "Be cautious of media franchise reboots. They're usually just cash grabs.",
            "Reading books is a fun and cost-effective hobby.",
            "If you really like a piece of media, you should try to buy it directly instead of using a subscription-based service.",
            "You can safely wash darks and whites in the same load of laundry as long the water is cold and you don't add bleach.",
            "If you buy all your socks in the same style, you'll never have to worry about folding or losing socks again.",
            "wait i wasn't ready that time",
            "You'll have an easier time convincing people if you never tell them that they're wrong.",
            "It's often a good idea to take vitamin D supplements in the winter.",
            "Subscribe to CitricDolphin on YouTube.",
            "Be careful not to over-use antibiotics.",
            "Plastic recycling is a scam. Consider using paper or cardboard instead of disposable plastic.",
            "Nothing is a bargain if you don't need it.",
            "When buying groceries, pay attention to the price per volume, not just the total price.",
            "The choice of a lawyer is an important one and should not be based on advertising alone.",
            "No news is without bias. Make sure to seek a wide variety of sources.",
            "Wikipedia is actually very reliable these days.",
            "One good indicator of a charity's quality is its income:expenses ratio.",
            "Fans are cheaper to run than air conditioning, but can still be an effective tool to keep your house cool.",
            "You've got this, you can do it!",
            "Just because water is clear doesn't mean it's safe to drink. If you don't trust a water source, always boil it before drinking.",
            "When starting a new career, it's usually a good idea to live in or near a big city.",
            "Be careful if you buy solar panels -- there's a lot of terrible financing deal out there.",
            "If you don't have a credit score, you can still get a good home loan by requesting manual underwriting.",
            "Shoplifting isn't worth the risk.",
            "Don't drink saltwater in a survival situation -- it dehydrates you and can make you sick.",
            "It's easy to get sunburned when you go swimming. Make sure to put on high-SPF sunscreen!",
            "If you're trying to burn calories, it's less tiring to do lots of walking than a little bit of running.",
            "Self-deprecating humor can be funny, but be careful not to overuse it. Positive self talk is important for your mental health.",
            "Learning to touch type is easy and useful if you use the computer a lot.",
            "Comprehensible input is the most important part of learning a new language.",
            "Don't rush to buy mainstream products. There's often a cheaper alternative that works just as well.",
            "Working with lye is extremely dangerous. Make sure to use proper protection and have emergency washing stations available.",
            "Most inxepensive locks offer very little actual security.",
            "Use my code HOTELSEQUEL at checkout to get half off your firth month!",
            "The price of major appliances is often negotiable.",
            "People who invest in leisure time instead of products tend to report higher hapiness and satisfaction.",
            "Thrift shops are businesses, not charities. Consider donating your unwanted goods directly to charitable causes.",
            "Cutting calories affects your weight, but it doesn't necessarily make you healthier.",
            "Beware of survivorship bias. Successful people don't always give good advice.",
            "The only surefire way to beat the house is to quit while you're ahead and never come back.",
            "Paper is renewable, recylable, and decomposable. Don't be afraid to use paper!",
            "When working with digital documents, save early and save often.",
            "Blowing into game cartridges can actually make them corrode faster. If your game isn't working, simply remove it and re-insert it without blowing."
            ]

def help_command():
    
    if not help_lines == []:
        random_choice = help_lines[random.randint(0, len(help_lines) - 1)]
        print(random_choice)
        help_lines.remove(random_choice)
    else:
        print("I'm out of advice.")

game.action(id="global_win",
                           success="Nice try. We fixed that exploit.",
                           verbs=["win"],
                           repeat_message="Not happening.")
game.action(id="global_drop", success="You can't do that.", verbs=["drop"], repeat_message="Seriously, you can't drop stuff. That's not a feature.")
game.action(id="global_save", success="There is no save feature.", verbs=["save"], repeat_message="No.")
game.action(id="global_quit", success="", verbs=["quit"], repeat=True, callback=quit_func)
game.action(id="global_help", success="", verbs=["help"], repeat=True, callback=help_command)
game.action(id="global_lose",success="Ah, you lost. What a shame!",callback=game.end)

start_bedroom = game.room("start_bedroom", ["A shabby hotel room.", "There's a window by the wall.","There's a nightstand by the bed and a safe in the corner.", "There's also a door to the hallway, and a door to the bathroom."])
game.current_room = start_bedroom

game.action(id="startroom_nightstand_top", success="It's a normal nightstand with a drawer.", verbs=["look", "examine", "check"], nouns=["nightstand", "dresser", "desk"], repeat=True, allowed_rooms=["start_bedroom"])
game.action(id="startroom_nightstand_drawer", success="You open the drawer on the nightstand. Your ID is inside.", verbs=["open", "check", "look", "examine"], nouns=["drawer","nightstand"], enforce=True, repeat=False, set_flags=["startroom_drawer_open"], repeat_message="The drawer is already open.", allowed_rooms=["start_bedroom"])
game.action(id="startroom_take_key", success="You take your ID.", verbs=take, enforce=True, nouns=["id"], gives_items=["ID"], repeat=False, repeat_message="The drawer is empty.", need_flags=["startroom_drawer_open"], allowed_rooms=["start_bedroom"])
game.action(id="startroom_open_safe", success="You open the safe.\nA black keycard is inside.\nYou take the keycard.", verbs=["open", "unlock", "access","look"], nouns=["safe", "key"], need_items=["Safe Key"], expend=True, gives_items=["Black Keycard"], repeat_message="The safe is empty.", items_fail="The safe is locked.", allowed_rooms=["start_bedroom"])
game.action(id="startroom_enter_bathroom", success="You enter the bathroom.", verbs=["go", "enter", "walk"], repeat=True, nouns=["bathroom", "restroom", "toilet"], enforce=True, warp="start_bathroom", allowed_rooms=["start_bedroom"])
game.action(id="startroom_enter_hallway", success="You enter the hallway.\nThe bedroom door closes behind you.", verbs=["go", "enter", "walk", "leave"], repeat=True, nouns=["hallway"], enforce=True, warp="hall1", allowed_rooms=["start_bedroom"])
game.action(id="startroom_window_look", success="You can see pavement down below, but it's otherwise pitch dark.", verbs=["look", "view", "inspect"], nouns=["window"], repeat=True, enforce=True, allowed_rooms=["start_bedroom"])
game.action(id="startroom_window_open", success="You open the window.\nA cool breeze fills the room.", verbs=["open"], nouns=["window"], set_flags=["startroom_window_open"], avoid_flags=["startroom_window_open"], repeat=True, flags_fail="The window is already open.", allowed_rooms=["start_bedroom"])
game.action(id="startroom_window_close", success="You close the window.\nNice and stuffy, just how you like it.", verbs=["close", "shut"], nouns=["window"], remove_flags=["startroom_window_open"], need_flags=["startroom_window_open"], repeat=True, flags_fail="The window is already closed.", allowed_rooms=["start_bedroom"])
game.action(id="startroom_window_exit", success="You step out of the window onto the ledge.\nLooks like you're about 6 floors up.", verbs=["exit","crawl","go","climb"], nouns=["window"], enforce=True, need_flags=["startroom_window_open"], flags_fail="The window is closed.", repeat=True, warp="start_ledge", allowed_rooms=["start_bedroom"])
game.action(id="startroom_window_run", success="You take a running leap out of the window.\nYou fall 6 floors to your death.\nNice!", verbs=["run","jump"], nouns=["window"], enforce=True, need_flags=["startroom_window_open"], flags_fail="You slam against the window.", allowed_rooms=["start_bedroom"], callback=game.end)
game.action(id="startroom_bed_sleep",
            success="You JUST woke up. You're not feeling tired enough for a nap.",
            verbs=["go","sleep","nap","snooze","check","investigate","look"],
            nouns=["bed","sleep"],
            allowed_rooms=["start_bedroom"],
            repeat=True
)

game.room("start_ledge", ["You're balanced on a small balcony connected to that shabby hotel room.","Looks like you're about six floors up."])

game.action(id="startledge_jump", success="You jump off and hit the ground.\nYou don't exactly stick the landing, and you break your back.\nNice job, idiot!", verbs=["jump","fall"], allowed_rooms=["start_ledge"], callback=game.end)
game.action(id="startledge_enter_startroom", success="You climb back into the hotel room.", verbs=["enter","crawl","go","through","climb"], nouns=["window","bedroom"], repeat=True, allowed_rooms=["start_ledge"], warp="start_bedroom")
game.action(id="startledge_close_window", success="That doesn't seem like the best idea.", verbs=["close","shut"], nouns=["window"], repeat=True, allowed_rooms=["start_ledge"])

game.room("start_bathroom", ["A run-down yet clean bathroom.","Complete with a toilet, sink, and shower.","You vaguely recall leaving some loose change on the vanity earlier.","There's also a door to the bedroom."])

game.action(id="startbathroom_enter_startroom", success="That's enough bathroom time for now.\nYou enter the bedroom.", repeat=True, verbs=["go", "enter", "walk", "return"], nouns=["bedroom", "main", "back"], enforce=True, warp="start_bedroom", allowed_rooms=["start_bathroom"])
game.action(id="startbathroom_enter_startroom_leave_alt", success="That's enough bathroom time for now.\nYou enter the bedroom.", repeat=True, verbs=["exit","leave"], nouns=["bathroom"], enforce=True, warp="start_bedroom", allowed_rooms=["start_bathroom"])
game.action(id="startbathroom_toilet_flush", repeat=False, success="You flush the toilet.\nIt's pretty slow, and the handle leaks a bit.", verbs=["flush", "activate"], nouns=["toilet"], repeat_message="Once is enough. Conserve water.", allowed_rooms=["start_bathroom"])
game.action(id="startbathroom_run_sink", success="You turn the sink on, but nothing comes out.", verbs=["run", "turn", "enable"], nouns=["sink"], repeat_message="Doesn't work.", allowed_rooms=["start_bathroom"])

game.action(id="startbathroom_toilet_drink", success="Ew, gross, no.", verbs=["drink"], enforce=True, nouns=["toilet"], repeat=False, set_flags=["startroom_toilet_drink_1"], avoid_flags=["startroom_toilet_drink_1"], allowed_rooms=["start_bathroom"], need_flags=[])
game.action(id="startbathroom_toilet_drink_2", success="What the heck? No, don't do that.", verbs=["drink"], enforce=True, nouns=["toilet"], repeat=False, need_flags=["startroom_toilet_drink_1"], set_flags=["startroom_toilet_drink_2"], avoid_flags=["startroom_toilet_drink_2"], allowed_rooms=["start_bathroom"])
game.action(id="startbathroom_toilet_drink_3", success="Are you serious? You really wanna do this??", verbs=["drink"], enforce=True, nouns=["toilet"], repeat=False, need_flags=["startroom_toilet_drink_2"], set_flags=["startroom_toilet_drink_3"], avoid_flags=["startroom_toilet_drink_3"], allowed_rooms=["start_bathroom"])
game.action(id="startbathroom_toilet_drink_4", success="I'll give you one more chance to change your mind.", verbs=["drink"], enforce=True, nouns=["toilet"], repeat=False, need_flags=["startroom_toilet_drink_3"], set_flags=["startroom_toilet_drink_4"], avoid_flags=["startroom_toilet_drink_4"], allowed_rooms=["start_bathroom"])
game.action(id="startbathroom_toilet_drink_5", success="Fine, you asked for it.\n\nYou plunge your face into the bowl and take a nice big swig of toilet water.\nIt tastes really bad, but for some reason, you swallow it anyway.\nYou probably have some kind of disease now.\n\nHappy? Jeez...", verbs=["drink"], enforce=True, nouns=["toilet"], repeat=False, need_flags=["startroom_toilet_drink_4"], set_flags=["toilet_disease"],repeat_message="No, you're not doing that again.", allowed_rooms=["start_bathroom"])
game.action(id="startbathroom_vanity_look",
            success="There's some change on the vanity.",
            verbs=["look","check"],
            nouns=["vanity"],
            avoid_flags=["player_has_change"],
            flags_fail="Nothing to see here.",
            allowed_rooms=["start_bathroom"]
            )
game.action(id="startbathroom_change_take",
            success="You take the loose change.\nIt adds up to 99 cents.",
            verbs=take,
            enforce=True,
            nouns=["change","coins","vanity"],
            repeat=False,
            repeat_message="You already took the loose change.",
            gives_items=["99 Cents"],
            allowed_rooms=["start_bathroom"],
            set_flags=["player_has_change"]
            )

def startbathroom_pee_ending():
    print("Oh, let me give you some privacy.")
    print()
    for _ in range(3):
        input(game.prompt)
        print()
    print("The narrator is gone...")
    game.end()
    return

game.action(id="startbathroom_toilet_pee", success="", verbs=["pee", "urinate", "poo", "poop", "defecate", "go"], repeat=True, enforce=True, nouns=["toilet"], allowed_rooms=["start_bathroom"], callback=startbathroom_pee_ending)
game.action(id="startbathroom_shower_use", success="I think you have more important things to be doing.", verbs=["take"], nouns=["shower", "bath"], repeat_message="Nope.", allowed_rooms=["start_bathroom"])

game.room("hall1", ["A hallway full of doors.", "Looks like you're on the sixth floor.", "There's an elevator at the end of the hall.","Your bedroom is on this floor."])

game.action(id="hall1_enter_bedroom", success="You go back into your bedroom.", verbs=["go", "enter", "walk", "return"], nouns=["bedroom","room"], enforce=True, repeat=True, allowed_rooms=["hall1"], warp="start_bedroom", need_items=["Bedroom Keycard"], items_fail="You don't have a key to get back in.")
game.action(id="hall1_check_doors",
                           success="Room 69 has a nicer door than the others.\nThey're all locked, though.",
                           verbs=["check","examine","try","look"],
                           enforce=True,
                           nouns=["door","doors"],
                           repeat=False,
                           repeat_message="All locked.",
                           allowed_rooms=["hall1"]
                           )
game.action(id="hall1_knock_doors",
            success="You knock on every door in the hall.\nNobody answers any of them.",
            verbs=["knock"],
            enforce=True,
            nouns=["door","doors"],
            repeat=True,
            allowed_rooms=["hall1"])

game.room("elevator",["Just a normal elevator.","Looks like there's six floors, plus a basement.","There's also a keycard reader."])

game.action(id="elevator_enter",
                           success="You enter the elevator.",
                           verbs=["go","enter","walk","get"],
                           nouns=["elevator","lift"],
                           repeat=True,
                           warp="elevator",
                           allowed_rooms=["hall1","floor1_lobby","floor2_lobby","floor3_lobby","floor4_lobby","floor5_lobby","basement_lobby"]
                           )
game.action(id="elevator_keycard",
                           success="You scan the black keycard.\nThe basement button lights up.",
                           verbs=["scan","put","insert"],
                           nouns=["card","key","keycard"],
                           repeat=True,
                           need_items=["Black Keycard"],
                           items_fail="You don't have a keycard that will work.",
                           set_flags=["elevator_basement_active"],
                           allowed_rooms=["elevator"]
                           )
game.conversation(id="elevator_buttons",exchanges=[
    game.exchange(id="elevator_choose_floor",lines=["Please choose a floor."],options=["First Floor","Second Floor","Third Floor","Fourth Floor","Fifth Floor","Sixth Floor","Basement","Basement"],branches=["elevator1","elevator2","elevator3","elevator4","elevator5","elevator6","elevatorb","elevatorb_fail"]),
    game.exchange(id="elevator1",lines=["The elavator takes you to the first floor.","You leave the elevator."],options=[],end=True,warp="floor1_lobby"),
    game.exchange(id="elevator2",lines=["The elavator takes you to the second floor.","You leave the elevator."],options=[],end=True,warp="floor2_lobby"),
    game.exchange(id="elevator3",lines=["The elavator takes you to the third floor.","You leave the elevator."],options=[],end=True,warp="floor3_lobby"),
    game.exchange(id="elevator4",lines=["The elavator takes you to the fourth floor.","You leave the elevator."],options=[],end=True,warp="floor4_lobby"),
    game.exchange(id="elevator5",lines=["The elavator takes you to the fifth floor.","You leave the elevator."],options=[],end=True,warp="floor5_lobby"),
    game.exchange(id="elevator6",lines=["The elavator takes you to the sixth floor.","You leave the elevator."],options=[],end=True,warp="hall1"),
    game.exchange(id="elevatorb",lines=["The elavator takes you to the basement.","You leave the elevator."],options=[],end=True,warp="basement_lobby",need_flags=["elevator_basement_active"]),
    game.exchange(id="elevatorb_fail",lines=["You push the button, but nothing happens."],options=["Oh."],branches=["elevator_choose_floor"],avoid_flags=["elevator_basement_active"])
])
game.action(id="elevator_buttons",
            success="",
            verbs=["go","push","press","leave","exit","get"],
            enforce=True,
            nouns=["floor","button","story","basement"],
            repeat=True,
            conversation="elevator_buttons",
            allowed_rooms=["elevator"]
            )

game.room(id="floor1_lobby",description=["A pretty standard looking hotel lobby.","There's a clerk at a desk by the front door."])
game.conversation(id="floor1_clerk",
                  exchanges=[
                        game.exchange(id="floor1_clerk_greeting", #Start
                                    lines=["Hello sir!","Or madam.","Or whatever you are. I can't see anything, it's all just text.","How can I help you?"],
                                    options=["Where am I?","Where am I?","Who are you?","Why is the door locked?","How did I get here?","I need a keycard.","Bye."],
                                    branches=["floor1_clerk_where","floor1_clerk_where_corrupted","floor1_clerk_who","floor1_clerk_locked","floor1_clerk_how","floor1_clerk_keycard","end"]
                                    ),
                        game.exchange(id="floor1_clerk_loop", #Start repeat
                                    lines=["Anything else I can do for you?"],
                                    options=["Where am I?","Where am I?","Who are you?","Why is the door locked?","How did I get here?","I need a keycard.","Bye."],
                                    branches=["floor1_clerk_where","floor1_clerk_where_corrupted","floor1_clerk_who","floor1_clerk_locked","floor1_clerk_how","floor1_clerk_keycard","end"]
                                    ),
                        game.exchange(id="floor1_clerk_where", #Where am I?
                                      lines=["Why, you're at the famously adequate Grapefruit Inn, of course!"],
                                      options=["Of course...","Wait, what?"],
                                      branches=["floor1_clerk_loop","floor1_clerk_where_corrupted"],
                                      set_flags=["floor1_clerk_where_seen"],
                                      avoid_flags=["floor1_clerk_where_seen"],
                                      ),
                        game.exchange(id="floor1_clerk_where_corrupted",
                                      lines=["I've said too much already."],
                                      options=["..."],
                                      branches=["floor1_clerk_loop"],
                                      need_flags=["floor1_clerk_where_seen"]
                                      ),
                        game.exchange(id="floor1_clerk_who", #Who are you?
                                      lines=["My name is Leonydas, and I'm here to help your stay be as comfortable as possible."],
                                      options=["Uh, ok."],
                                      branches=["floor1_clerk_loop"]
                                      ),
                        game.exchange(id="floor1_clerk_locked", #Why is the door locked?
                                      lines=["Oh, there's something wrong with those doors. They only open from the outside.","You're welcome to use the back exit on the fourth floor."],
                                      options=["Ok."],
                                      branches=["floor1_clerk_loop"],
                                      need_flags=["floor1_frontdoor_checked"]
                                      ),
                        game.exchange(id="floor1_clerk_how", #How did I get here?
                                      lines=["Well, my records say that you checked in...three days ago.","Looks like you arrived by taxi."],
                                      options=["Ok.","I don't remember that..."],
                                      branches=["floor1_clerk_loop","floor1_clerk_how_remember"]
                                      ),
                        game.exchange(id="floor1_clerk_how_remember",
                                      lines=["Ahh, one of those nights, eh?","Happens to the best of us.","(He gives you a wink.)"],
                                      options=["Right..."],
                                      branches=["floor1_clerk_loop"]
                                      ),
                        game.exchange(id="floor1_clerk_keycard", #I need a keycard.
                                      lines=["Oh, no problem at all.","I'll just need to see the ID you checked in with."],
                                      options=["I don't have an ID...","Okay, here you go.","I changed my mind."],
                                      branches=["floor1_clerk_keycard_fail","floor1_clerk_keycard_get","floor1_clerk_loop"],
                                      avoid_flags=["clerk_gave_keycard"]
                                      ),
                        game.exchange(id="floor1_clerk_keycard_get",
                                      lines=["Let's see...","Okay, this looks right to me!","Here's your new keycard."],
                                      options=["Thanks."],
                                      branches=["floor1_clerk_loop"],
                                      set_flags=["clerk_gave_keycard"],
                                      gives_items=["Bedroom Keycard"],
                                      need_items=["ID"]
                                      ),
                        game.exchange(id="floor1_clerk_keycard_fail",
                                      lines=["Well, I can't give you a new keycard unless I see your ID."],
                                      options=["Darn."],
                                      branches=["floor1_clerk_loop"],
                                      avoid_items=["ID"]
                                      )
                  ])
game.action(id="floor1_clerk_talk",
            success="",
            verbs=["talk","converse","check","ask","tell","say","greet"],
            nouns=["clerk","desk"],
            repeat=True,
            conversation="floor1_clerk",
            allowed_rooms=["floor1_lobby"]
            )
game.action(id="floor1_clerk_look",
            success="He smiles at you but doesn't say a word.",
            verbs=["look"],
            enforce=True,
            nouns=["clerk"],
            allowed_rooms=["floor1_lobby"],
            repeat=True
            )
game.action(id="floor1_frontdoor_check",
            success="The door is locked.",
            verbs=["go","check","walk","exit","leave", "open"],
            nouns=["door"],
            repeat=True,
            allowed_rooms=["floor1_lobby"],
            set_flags=["floor1_frontdoor_checked"]
            )

game.room(id="floor2_lobby",description=["Just another hotel hallway.","This one also has a vending machine in it."])
game.action(id="floor2_lobby_vending_check",
            success="The vending machine sells Pebble Cola.\nCosts one dollar per can.",
            nouns=["vending","machine"],
            verbs=["check","look","investigate"],
            enforce=True,
            repeat=True,
            allowed_rooms=["floor2_lobby"]
            )
game.action(id="floor2_lobby_vending_buy",
            success="You get an ice cold can of Pebble Cola.",
            verbs=["buy","purchase"],
            nouns=["vending","machine","cola","pebble"],
            need_items=["99 Cents", "Penny"],
            expend=True,
            items_fail="You can't afford it.",
            repeat=True,
            gives_items=["Pebble Cola"],
            allowed_rooms=["floor2_lobby"]
            )
game.action(id="global_cola_drink",
            success="You drink the Pebble Cola. It tastes like tin foil.\nYou keep the can.",
            verbs=["drink","consume"],
            nouns=["soda","cola","pebble"],
            need_items=["Pebble Cola"],
            expend=True,
            gives_items=["Empty Cola Can"],
            repeat=True
            )
game.action(id="global_cola_dump",
            success="You pour out the Pebble Cola on the ground.\nWhat a waste...\nYou keep the can.",
            verbs=["dump","pour","empty","spill"],
            enforce=True,
            nouns=["soda","cola","pebble"],
            need_items=["Pebble Cola"],
            expend=True,
            gives_items=["Empty Cola Can"],
            repeat=True
            )

game.room(id="floor3_lobby",description=["Wow! Yet another hotel hallway.","This one has some kind of recyling machine in the corner."])
game.action(id="floor3_recycler_check",
            success="There's a sign above the machine.\n'Recycle aluminum or plastic here, get $1!'",
            verbs=["check","look","go"],
            enforce=True,
            nouns=["machine","recycling"],
            allowed_rooms=["floor3_lobby"],
            repeat=True
            )
game.action(id="floor3_reycler_can_success",
            success="You put the soda can into the machine.\nIt whirrs for a moment, and then dispenses a $1 bill.\nYou take the money.",
            verbs=["put","recycle","throw"],
            nouns=["can","machine"],
            need_nouns=["can"],
            need_items=["Empty Cola Can"],
            expend=True,
            gives_items=["$1 Bill"],
            repeat=False,
            repeat_message="You already recycled your soda can.",
            allowed_rooms=["floor3_lobby"]
            )
game.action(id="floor3_recycler_can_full",
            success="Your soda can is still full.",
            verbs=["put","recycle","throw"],
            nouns=["can","machine"],
            need_nouns=["can"],
            need_items=["Pebble Cola"],
            repeat=True,
            allowed_rooms=["floor3_lobby"]
            )

game.room(id="floor4_lobby",description=["Looks like a normal hotel hallway.","One of the doors has a neon \"EXIT\" sign above it and a window to the outside."])
game.action(id="floor4_lobby_exit",
            success="You open the door and walk through it.\nYou immediately fall four floors onto hard pavement. It hurts your legs a bit.\nYou should have seen this coming, you are on the fourth floor after all.",
            verbs=["go","walk","exit","leave","open"],
            enforce=True,
            nouns=["door","exit"],
            warp="outside",
            allowed_rooms=["floor4_lobby"],
            repeat=True
            )

game.room(id="floor5_lobby",description=["Shockingly, it looks like a normal hotel hallway.","There's a man in the hall confusedly holding a key.","He shoots you a glance."])
game.conversation(id="floor5_lobby_man",
                  exchanges=[
                      game.exchange(
                          id="floor5_man_start",
                          lines=["Uh, hi...can I help you?"],
                          options=["Can I have that key?","No, nevermind."],
                          branches=["floor5_man_key_ask","end"]
                      ),
                      game.exchange(
                          id="floor5_man_key_ask", #Can I have that key?
                          lines=["I don't know, CAN you?"],
                          options=["Fine, MAY I have that key?"],
                          branches=["floor5_man_key_ask_1"],
                          avoid_items=["Safe Key"]
                      ),
                      game.exchange(
                          id="floor5_man_key_ask_1", #Fine, MAY I have that key?
                          lines=["Well, I'm not sure what it is. I just found it on the floor.","I guess I could part with it for a dollar."],
                          options=["Deal.","Deal.","I can't afford that."],
                          branches=["floor5_man_key_coins","floor5_man_key_success","floor5_man_key_broke"]
                      ),
                      game.exchange(
                          id="floor5_man_key_coins",
                          lines=["Okay, here you--","Wait, you're paying entirely in coins??","No, no. I'm not dealing with all that.\nCome back when you have paper money."],
                          options=["Ok."],
                          branches=["end"],
                          need_items=["Penny","99 Cents"],
                          avoid_items=["$1 Bill"]
                      ),
                      game.exchange(
                          id="floor5_man_key_success",
                          lines=["Right then, here you are."],
                          options=["Thanks."],
                          branches=["end"],
                          need_items=["$1 Bill"],
                          expend=True,
                          gives_items=["Safe Key"]
                      ),
                      game.exchange(
                          id="floor5_man_key_broke",
                          lines=["Can't even spare a dollar? Well then, it must not be worth much to you."],
                          options=["Whatever."],
                          branches=["end"]
                      )
                  ]
                  )
game.action(id="floor5_man_talk",
            success="",
            verbs=["talk","converse","ask","greet"],
            nouns=["man","guy","key","person","him"],
            repeat=True,
            conversation="floor5_lobby_man",
            allowed_rooms=["floor5_lobby"]
            )
game.action(id="floor5_man_attack",
            success="You lunge at the man.\nBefore you can land a single blow, he pulls out a pistol and shoots you.",
            verbs=["attack","punch","fight","brawl","assault","hit"],
            enforce=True,
            nouns=["man","guy","key","person","him"],
            callback=game.end,
            allowed_rooms=["floor5_lobby"]
            )
game.action(id="floor5_man_steal",
            success="He's literally looking at you. How do you expect to pickpocket him, genius?",
            verbs=["steal","pickpocket","pick","pocket"],
            nouns=["man","guy","key","person","him"],
            enforce=True,
            repeat=False,
            repeat_message="It's not gonna happen.",
            allowed_rooms=["floor5_lobby"]
            )
game.action(id="floor5_man_look",
            success="The man glances up briefly to return your gaze, but he seems preoccupied by the key.",
            verbs=["look"],
            nouns=["man","guy","person","him"],
            enforce=True,
            allowed_rooms=["floor5_lobby"]
            )

game.room(id="outside",description=["It's pitch dark all around you.","You can't see anything in any direction except the pavement beneath you, and the hotel behind you.","There's also a penny on the ground."])
game.action(id="outside_penny_get",
            success="You take the penny.\nIt's good luck, after all.",
            verbs=take,
            nouns=["penny"],
            repeat=False,
            repeat_message="You already took the penny.",
            gives_items=["Penny"],
            allowed_rooms=["outside"]
            )
game.action(id="outside_leave",
            success="You pick a random direction and start walking.\nStill, nothing appears in your path.\nWill you find anything out there? Who knows...",
            verbs=["leave","escape","run","walk","explore"],
            enforce=True,
            nouns=["away"],
            callback=game.end,
            allowed_rooms=["outside"]
            )
game.action(id="outside_hotel_enter",
            success="You walk back into the hotel through the front door.",
            verbs=["enter","go","walk"],
            nouns=["door","hotel"],
            repeat=True,
            warp="floor1_lobby",
            allowed_rooms=["outside"]
            )

game.room(id="basement_lobby",description=["You enter the basement.","It's dark, but it looks like some kind of subway station.","There's a single train car with its door open."])
game.action(id="basement_train_enter_disease",
            verbs=["board","enter","walk","go","get","ride"],
            nouns=["train","car","subway"],
            success="You board the train car.\nThe doors close behind you and the train car starts to move.\nYou're relieved to be getting out of here, but who knows where you're going...\n\nOh, you also throw up.\nI guess you shouldn't have drunk that toilet water earlier.",
            need_flags=["toilet_disease"],
            callback=game.end,
            allowed_rooms=["basement_lobby"]
            )
game.action(id="basement_train_enter",
            verbs=["board","enter","walk","go","get","ride"],
            nouns=["train","car","subway"],
            success="You board the train car.\nThe doors close behind you and the train car starts to move.\nYou're relieved to be getting out of here, but who knows where you're going...",
            avoid_flags=["toilet_disease"],
            callback=game.end,
            allowed_rooms=["basement_lobby"]
            )

while True:
    print("GRAPEFRUIT HOTEL DEMO")
    print("Licensed under GNU GPL v3")
    print("NOTE: Some commands that you would expect to work do nothing in this game.")
    print("This is not a limitation of the engine, but rather a limitation of the scope of this specific demo.")
    print()
    game.fail = "I'm not sure what you mean."
    game.start_message = ["You wake up in a shabby hotel room.", "You're not sure where you are.", "Maybe you should LOOK around.", "You can also check your INVENTORY at any time.", "Type 'help' at any time to get advice."]
    game.look_by_default = True

    game.start("start_bedroom")

    print("GAME OVER")
    play_again = input("Would you like to play again? [Y/N]:")
    if play_again.lower() == "y" or play_again.lower() == "yes":
        game.reset()
        continue
    else:
        print("Thanks for playing!")
        exit()