Over the last 3 or so years we have come up with a (we think) pretty good development process. We're always open to suggestions, of course, but the below is our *current* process that unless we discuss and agree on new practices, we'll be expecting all developers to contribute to. This isn't so much "rules" as just things that if everyone does them will help the development be *much* smoother for everyone.

1. **Use the "Projects" tab** to track progress, assignments, and brainstorm.

The first part of making a CTF is brainstorming what all the challenges will be. We typically use the "Projects" tab for this. We have one board called "Challenge Ideas". This board should be notes *only*, not issues. Any and every idea you have for a challenge can go in there! It's a nice way to organize our ideas with brief descriptions of what a challenge would be.

2. **Every** challenge to be completed (ie. has been discussed and agreed it would be a good one) should be placed into the To Do column of one of the category-specific boards and converted to an issue. The three dots on a Project card allow you to convert it into an issue. Once converted, an approximate difficulty level should be added as well as more details (if necessary) about the challenge. 

3. **Every challenge should have its own branch.** Try and keep the branchnames somewhat consistent. For example if I have an RE challenge called "Pikachu", I would do `git checkout -b re-pikachu`. 

4. **All development on the challenge should be committed to that branch** (**never** to master, and in fact we have protection on to prevent this). 

5. **A challenge is complete when** the following have been done:

- The source code is done and the challenge runs as intended.
- If a remote challenge, the remote service has been made and tested.
- Any required deployment materials ([see here for pwn](https://github.com/b01lers/b01lers-ctf-2021/wiki/Dockerfiles-for-PWN-Challenges)) are included. It should be as easy as running `docker-compose up -d` to start the service if it has a remote component.
- All required distribution files are present (binaries, description, libraries, ciphertext, whatever).
- The solve is complete. A good solve should have a `solve.md` completely explaining how to solve the challenge as well as any required theory about the challenge. See [this writeup](https://github.com/b01lers/bootcamp-2020/blob/master/rev/02-super-spy/solve/solve.md) for an example. The solve should also include any scripts, tools, and additional materials required to solve the challenge. It **must** be reproducible or we cannot use the challenge!

6. **A complete challenge should be pull requested to master.** There are two checks. First, an automated check that the directory contains the required files and is up to date with master. Second, a manual checklist is added to all pull requests. Don't just blindly fill this out! Each challenge needs to have both the author and reviewer go through the checklist to ensure quality.

7. **Done!** Once a challenge is PRed and accepted, it is in the CTF! Congratulations :)

This all looks like a lot, and it is! Writing challenges is a lot of work but is very rewarding. Keep in mind that all this A) will improve your own skills and B) looks incredible on a resume ;) 

If you at *any* point need help with *any* part of the process of writing your challenges, brainstorming your challenges, deploying, anything. Please reach out to the officer team. Some of us have been doing this for many years and we have likely encountered your issue so it'll reduce headache to just ask!! Plus, nobody bites. 

Excited to work on this with y'all. Let's make it a good one!
 