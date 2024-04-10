## What's this?
This directory contains all the getters and setters for all 5 global databases,
with more potentially coming in later.

## Now vs Future
Currently, these simple getters and setters utilize TinyDB, 
and effectively behave as singletons for all the detached, separate workers.

In the future, we'll want to these functions to optionally call
remote database providers, and act as a wrapper for these databases.

## Important notes
All db calls return lists of entire objects, unless it's specified otherwise.
This is the default since we're prioritizing speed and minimal latency over 
security or cleanliness, and these systems are not intended to be run publicly,
but as a closed network.