This is a vanilla RSA challenge with two twists. First, they need to infer the public key. Then, they 
need to get the flag via a related message attack. Absolutely no source code is provided.

There is a test server, so they can play with encryptions, test how messages get converted to 
integers, etc. The test server is also useful to run solvers against. Its main purpose, however, is to 
provide plaintexts. Based on those, one can i) use (ptxt,ctxt) pairs to extract the public key. That 
is trial and error, you cycle through exponents one by one - under 10 mins on my notebook on single 
core. In addition, one can ii) see which options give related messages. The related message solver is 
just a large polynomial GCD in sage (the same technique was on a VolgaCTF qual a few years ago). Here, 
however, there is an unknown parameter in the relationship that depends on the message length (i.e., 
flag length). So they must do another search - about 2.5 hours on 2 cores on my notebook.

Both searches are embarrassingly parallel, so with enough cores and preparation can be finished super 
quickly.

---

First run sol.py, which finds the public key (e,n) and constructs some constants for the related 
message attack (C1, C2, b0, b1, Npost). The public key search is fairly quick and is also parallelized 
for Ncores cores.

The resulting e,N,C1,C2,b0,b1 are already cut-and-pasted into sol.sage. Run that to do the GCD and get 
the flag. It searches through flag lengths in a certain range [Nlo, Nhi), given by the 1st and 2nd 
arguments you pass to it via

    sage sol.sage Nlo Nhi

You can break the search interval up into pieces and run multiple sage invocations concurrently on 
those.

For educational purposes, the parameters for the test server's fake flag are also included in 
sol.sage, so one can experiment with how that solution is found (testing = True).

===END===



      
