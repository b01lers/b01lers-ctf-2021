# Swirler

**Category**: Reversing \
**Difficulty**: Easy \
**Author**: qxxxb

## Public description

Some idiot posted this image online and used this
[Swirler app](link_to_challenge) to censor it.
Is it even possible to recover the original image now?

Attachments: [flag.png](flag.png)

## Overview

This is a simple web app that lets you upload an image and swirl it to censor
something.

Players are given a swirled image [flag.png](flag.png) and asked to unswirl it.

The unswirled image contains QR code that leads to a
[Gist](https://gist.github.com/qxxxb/d22119c274b5d5d6383e5fc09a490c04)
containing the flag.

## Building

For deployment, this challenge only needs a static HTTP server.

Example:
```sh
docker build -t swirler .
docker run -itp 8888:80 --rm --name swirler swirler
```

Then connect to http://localhost:8000

## Solution 1

Flip the image:
```sh
convert flag.png -flip flag_flip.png
```

Upload it, swirl it, and scan the QR code.

## Solution 2

Negate the swirl factor:
```diff
- float angle = percent * percent * uSwirlFactor * uTime;
+ float angle = percent * percent * -uSwirlFactor * uTime;
```

Upload [flag.png](flag.png), swirl it, and scan the QR code.

## Flag

```
pctf{sw1rly_sw1rly_qr_c0d3}
```
