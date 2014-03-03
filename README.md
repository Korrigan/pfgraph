PFGRAPH
-------

Abstract
========

PfGraph is a tool to integrate PF monitoring metrics into Graphite.


How it works
============

PFgraph retrieve metrics from an IOCTL on /dev/pf (the equivalent of
`pfctl -vv -s info`) and send them to the server, well formated with the
pickle protocol.

To run it once, just launch `pfgraph.py <server> [port]`.

You should consider creating a cron to run it every minutes.


LICENSE
=======

This code is under MIT license. See `LICENSE` file for further details.
