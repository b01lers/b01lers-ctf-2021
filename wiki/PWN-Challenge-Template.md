PWN challenges aren't too hard to develop but there are a few gotchas. I'll start listing them here.

We need to set our IO to non-buffered mode if we want it to work over `xinetd` and networking because...well, because reasons.

Probably you want to use a template like this:

```c
#include <stdio.h>

int main() {
    setvbuf(stdout, NULL, 2, 0);
    setvbuf(stderr, NULL, 2, 0);

    /* challenge code here */
}
```

