# ZDNS Fast, Asynchronous DNS Resolution

ZDNS is a command line utility that allows fast, asynchronous DNS resolution of
a medium size (low order millions) list of domains. Right now this is down by
spawning a large number of processes. We should move this to use Python adns or
switch wholesale to golang for this processing.

Possible go solution to build from: https://github.com/miekg/dns
