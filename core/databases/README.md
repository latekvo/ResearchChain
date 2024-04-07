## What's this?
This directory contains all the getters and setters for all 5 global databases,
with more potentially coming in later.

## Now vs Future
Currently, these simple getters and setters utilize TinyDB, 
and effectively behave as singletons for all the detached, separate workers.

In the future, we'll want to these functions to optionally call
remote database providers, and act as a wrapper for these databases.