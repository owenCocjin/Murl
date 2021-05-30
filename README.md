# Murl

> MITM attack that spoofs a DNS server. This will redirect a target's traffic through you, where you will make their requests on their behalf, and effectively strip the TLS layer.

Real server <-TLS-> You <-Plaintext-> Victim

---

## Dependencies
- [Sockets](https://docs.python.org/3/howto/sockets.html)
