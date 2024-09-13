# Grapefruit: Simple, Semantic, Expandable Text Adventure Engine
---
## Simple.
Grapefruit is contained inside a single py file that can be imported as a Python 3.7+ module.
The only external dependencies are sys and json, which both come included with most Python installations.
Grapefruit handles command parsing automatically -- no long lists of variations.
Write your entire game in pure Python code -- no proprietary markdown or scripting.

## Semantic.
Keywords and functions are exactly what you would expect.
Actions are called "actions."
Dialogue sequences are called "conversations."
Locations are called "rooms."
All paramaters are clearly named and documented.

## Expandable.
Write your own Python functions and associate them with game actions.
Write your own plugins and integrate them seamlessly into the core game loop.
No need to modify the engine itself.

---

## Dependencies
**Python 3.7 or higher.** Parts of this program rely on dictionaries to maintain insertion order, which is specified in 3.7+ but only considered an implementation detail in older verions. *Some* implementations of 3.6 and earlier may work (including the official binary), but it is not guaranteed.

**sys**

**json**

---

This is mostly a personal project to fulfill my long-standing goal of creating a fairly robust text adventure engine. It's not super pretty, but it's very easy to work with. A one-room demo with five possible actions can be created in less than ten lines.

The command parser for this engine is deliberately minimal and completely insensitive to grammar. Much of the parsing is pre-computed and then performed at runtime using dictionary lookups. A vast majority of natural language *and* terse commands are interpreted correctly while most non sequiturs are rejected. Although there are some downsides to this approach, it has the benefits of being small, efficient, predictable, and natural-language-agnostic.

See the documentation to get started. There's also a quick-and-dirty demo included as a reference.

---

## Why "Grapefruit?"
I like citrus :)
