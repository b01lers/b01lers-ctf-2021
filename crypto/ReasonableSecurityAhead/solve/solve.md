This is a vanilla RSA challenge with two twists. First, they need to infer the public key. Then, they 
need to get the flag via a related message attack. Absolutely no source code is provided.

There is a test server, so they can play with encryptions, test how messages get converted to 
integers, etc. The test server is also useful to run solvers against. Its main purpose, however, is to 
provide plaintexts. Based on those, one can i) use (ptxt,ctxt) pairs to extract the public key. That 
is trial and error, you cycle through exponents one by one - under 10 mins on my notebook with sage. 
In addition, one can ii) see which options give related messages. The related message solver is just a 
large polynomial GCD (the same technique was on a VolgaCTF qual a few years ago). Here, however, there 
is an unknown parameter in the relationship that depends on the message length (i.e., flag length). So 
they must do another search - about 2.5 hours on 2 cores on my notebook.

Both searches are embarrassingly parallel, so with enough cores and preparation can be finished super 
quickly.
