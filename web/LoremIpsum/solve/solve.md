Flask's debug pin is insecure. See https://book.hacktricks.xyz/pentesting/pentesting-web/werkzeug and https://github.com/pallets/werkzeug/blob/master/src/werkzeug/debug/__init__.py#L126

Arbitrary file read in `animal` argument. Werkzeug debug is visibile if an invalid file is given.

Use file leaks to get the information required to leak the pin, then recreate the pin and send it to Flask's debug interface to gain a python console. Use the python console to read the rest of the contents in `flag`.

`/proc/net/arp` for device id, -> `/sys/class/net/<id>/address`, convert to integer.

`/proc/sys/kernel/random/boot_id` and `/proc/self/cgroup` for device id as calculated in `https://github.com/pallets/werkzeug/blob/master/src/werkzeug/debug/__init__.py#L41`.

Path to app.py and username are visibile in debug output

