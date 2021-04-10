Reasonable Security Ahead  (by DM)
-------------------------

We have infiltrated the shadowy organization and set up a tunnel to 
their secret mainframe (nc FIXME FIXME). Unfortunately, any server 
output is encrypted via plain RSA. All is not lost, however, because a 
trusted insider can provide temporary access to their test server (nc 
FIXME FIXME). The test server has an additional feature that allows for 
toggling encryption on and off through a modified output function

   def output(self, msg):
       if self.debug: print(msg)
       else:          normal_encrypted_output(msg)

Your mission, should you accept it, is to leverage the given access and 
extract the secret data from the mainframe within the next 48 hours. Time 
is critical, so manage resources wisely. This message will self-destruct 
in 5.. 4.. 3.. 2.. 1..

===
