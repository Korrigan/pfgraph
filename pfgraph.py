#!/usr/local/bin/python
import sys

from pf.status import PFStatus


metric_name_fmt = "{hostname}.pf.{metric}"

def send_metrics(host, port, metrics):
    """
    Sends message to host `host` on port `port` well formated with the
    pickle protocol

    """
    import pickle
    import struct
    import socket
    
    payload = pickle.dumps(metrics, -1)
    header = struct.pack("!L", len(payload))
    message = header + payload
    sock = None
    for srv in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, stype, proto, cname, sa = srv
        try:
            sock = socket.socket(af, stype, proto)
        except socket.error:
            sock = None
            continue
        try:
            sock.connect(sa)
        except socket.error:
            sock = None
            continue
    if not sock:
        print "Cannot connect to server {host}:{port}".format(host=host, port=port)
        sys.exit(1)
    sock.sendall(message)
    sock.close()

def collect_metrics():
    """Collect PF metrics"""
    import time
    import platform

    status = PFStatus.retrieve()
    ts = int(time.time())
    hostname = platform.node()
    metrics = []
    for (metric, value) in status.collect_metrics().iteritems():
        path = metric_name_fmt.format(
            hostname=hostname,
            metric=metric,
            )
        metrics.append((path, (ts, value)))
    return metrics

def usage():
    """Prints out the usage and exits"""
    print "Usage: pfgraph.py <host> [port]"
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    host = sys.argv[1]
    port = 2004
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    metrics = collect_metrics()
    send_metrics(host, port, metrics)
    
