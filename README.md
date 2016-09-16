# Overview

This is the Marathon charm for use with Apache Mesos. Marathon allows the deployment of Docker containers on top of the Mesos framework.

# Usage

    juju deploy cs:~spicule/marathon
    juju deploy openjdk
    juju add-relation marathon openjdk
    juju add-relation marathon zookeeper
    juju expose marathon


## Scale out Usage

Marathon runs in HA mode, so to scale and provide failure support

    juju add unit -n2 marathon

## Known Limitations and Issues


# Configuration

# Contact Information

- tom@analytical-labs.com
- spicule.co.uk

[service]: http://example.com
[icon guidelines]: https://jujucharms.com/docs/stable/authors-charm-icon
