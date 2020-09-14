Checklist For PRs (Your PR won't be approved without all of the following):

1. Issue related to the PR

`There should be an issue linked to this PR. Delete this text and add the issue.`

2. The checklist should be completed:

- [ ] Is solvable (you don't have to solve it blind, just go through the solve and validate it and sanity check it)
- [ ] `flag.txt` is present  in `./solve` and contains just the flag.
- [ ] Flag is in `flag{...}` format (if impossible, the format is noted in `description.md`)
- [ ] Writeup is in the Wiki under the correct category. Link should go [here]()
- [ ] Writeup is present in `solve.md` under `./solve`
- [ ] Writeup is high quality and completely explains how to solve the challenge from scratch
- [ ] `description.md` is present in `./dist` and contains:
  - [ ] Challenge Title
  - [ ] Challenge Author
  - [ ] Challenge Difficulty `[Easy, Medium, Hard, Wizard]`
  - [ ] Challenge Description (for distribution, this is your flavor text)
- [ ] Local build files are present in `./src` if applicable
- [ ] Remote deployment files are present in `./deploy` if applicable
  - [ ] Xinetd config
  - [ ] Dockerfile
  - [ ] docker-compose.yml
  - [ ] Makefile (for on-docker builds, see [here](https://github.com/b01lers-ctf/b01lers-ctf-pwn/tree/master/kobayashi) for example)
- [ ] Directory structure is as so:

```
.
+-+ deploy (Files to go on remote and build the service. This directory can be omitted if no remote)
| +- docker-compose.yml
| +- Dockerfile
| +- challengename.xinetd
+-+ dist (Files to be distributed to players)
| +- description.md
+-+ src (Source files and build files like Makefile, etc)
+-+ solve (Solution and any images/resources/solve scripts/etc)
  +- flag.txt
  +- solve.md
  ```
  
  3. An approving review must be obtained before merging your PR!
