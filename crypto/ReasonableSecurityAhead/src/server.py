class Server:

    def __init__(self, key, flagfn):
       (p, q, e) = key
       self.p = p
       self.q = q
       self.e = e
       self.N = p * q
       self.flag = open(flagfn, "r").read().strip()
       self.debug = False
       self.testing = False

    def encrypt(self, msg):
       m = msg.encode("ascii")
       x = int.from_bytes(m, "big")
       c = pow(x, self.e, self.N)
       return hex(c)

    def output(self, msg):
       if self.debug: print(msg)
       else:          print(self.encrypt(msg))

    def showEncrypt(self, msg):
       c = self.encrypt(msg)
       self.output(f"encryption of '{msg}' gives:")
       self.output(f"{c}")

    def menu(self):
       self.output("1) show key")
       self.output("2) encryption test")
       self.output("3) encrypt something")
       self.output("4) show secret")
       self.output("5) encrypt secret")
       self.output("6) display menu")
       if self.debug: self.output("7) toggle testing mode [available on TEST SERVER ONLY]")

    def main(self):
       self.menu()
       while True:
          try:
             self.output("Choose:")
             r = int(input())
          except ValueError:
             break

          if r == 1:
             self.output(f"p={self.p}")
             self.output(f"q={self.q}")
             self.output(f"e={self.e}")

          elif r == 2: self.showEncrypt('THIS IS A TEST')

          elif r == 3:
             self.output("Message:")
             msg = input().strip()
             self.showEncrypt(msg)

          elif r == 4: self.output(f"{self.flag}")

          elif r == 5: self.showEncrypt(self.flag)

          elif r == 6: self.menu()

          elif self.testing and r == 7: self.debug = not self.debug

          else: break


class TestServer(Server):
   def __init__(self, key, flagfn):
      Server.__init__(self, key, flagfn)
      self.debug = True
      self.testing = True




import sys


if __name__ == "__main__":

   mode =  int(sys.argv[1])   if len(sys.argv) > 1   else  0

   # test server
   if mode == 0:
      #from Crypto.Util.number import getPrime
      #p0 = getPrime(768)
      #q0 = getPrime(768)
      #print(p0)
      #print(q0)
      #768-bit primes
      p0 = 1511161812866285898011156507911487824354265588664775980823178181721546740082122753522924902783387185099756752418975552788713561001278125555282797834263687632658450691342628423985076424816041990411577284050886902395290095712325403377
      q0 = 975446076687579483401910475818559181969000767662394052229615516755848686262647148760671312135608886181424364000402518458472664347008769595629289755997870064447968585289009316493551119460333730411721909800946541991573059299626258337
      e0 = 11111
      server = TestServer((p0, q0, e0), "fakeflag.txt")

   # real server
   elif mode == 1:
      #1024-bit primes
      p1 = 177061687868411673098517297843797355519704244055225870855711770298233650457562813891743115010053796419935795567465488965655218557522811244158417823293501241670852690210418043108225178378395523946051412920531846360192780659585185822907024373005094034415009440616392806631446427013886625667031118733410770544689
      q1 = 128619021587781044069167685900135537228818006462770586377423210435070146784594057646892834808021570989541558385948902641308131584924314479679114755723635861446758998006604114804091408912011467229767651096693645446838105285501002642044039403566198881111190382738186020589330233971460918988298428524008200898863
      e1 = 12397
      server = Server((p1, q1, e1), "flag.txt")

   # real server but with test server params
   else:
      p0 = 1511161812866285898011156507911487824354265588664775980823178181721546740082122753522924902783387185099756752418975552788713561001278125555282797834263687632658450691342628423985076424816041990411577284050886902395290095712325403377
      q0 = 975446076687579483401910475818559181969000767662394052229615516755848686262647148760671312135608886181424364000402518458472664347008769595629289755997870064447968585289009316493551119460333730411721909800946541991573059299626258337
      e0 = 11111
      server = Server((p0, q0, e0), "fakeflag.txt")


   server.main()


#END
