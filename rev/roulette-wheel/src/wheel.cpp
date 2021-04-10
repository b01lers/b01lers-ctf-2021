/*Challege idea:
  - Create a menu in which players can choose the following:
  - 	1: "Hint" -> Doesn't actually do anything. Print dummy string, then exit
  -	2: "Pick" -> Adds number to queue of choices, can be chosen a max of 6 times.
  -	3: "Spin" -> Will "spin" the wheel. Generate 6 numbers, which should not be the same as the user chose.
  Should always end up saying "Sorry, try again".
  -	4: (Hidden) "Cheat" -> Compare user choices against the (seeded) srand() generated numbers.
  This part is hidden in dead code, however.
  - If the numbers were correct, spit out several 8 byte chunks.
  Each chunk is a part of the base32-encoded flag.

  String will be obfuscated by splitting it into several chunks as hex.
  Player must merge these back together (manually, or via script).
Then decode the string (base32 encoded) to get the flag.

- Anti-debugging with ptrace will be in use.

- Stripped c++ + srand() + anti-debugging + basic encoding. Not a warmup challenege, 
but not nearly as difficult as one with movfuscator or ADVobfuscator.
*/

#include <queue>
#include <iostream>
#include <string>
#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include <sys/syscall.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <sys/unistd.h>
#include <sys/types.h>

using namespace std;
class Wheel{
	public:
		int val1,val2,val3,val4,val5,val6;
		int max_choices = 5;
		queue <double> choices;
		void init(){
			srand(2019);
			val1 = rand();
			val2 = rand();
			val3 = rand();
			val4 = rand();
			val5 = rand();
			val6 = rand();
			cout<<"Welcome to the roulette wheel"<<endl;
		}
		//step 1: "Hint"
		void hint(){
			cout<<"VHJ5IGhhcmRlcgo="<<endl;
			//base64, "Try harder"
		}
		//step 2: "Choose"
		void choose(){
			double temp_choice;
			if(this->max_choices<0){
				cout<<"Stop being so greedy!"<<endl;
				exit(1);
			}
			cout<<"What's your lucky number?"<<endl;
			cin>>temp_choice;
			this->choices.push(temp_choice);
			this->max_choices--;
		}
		//step 3: "Play"
		void play(){
			cout<<"Let's see what happens"<<endl;
			sleep(1);
			cout<<"You chose: "<<endl;
			for (int i = 0; i < 6; i++){
				cout<<this->choices.front()<<endl;
				sleep(1);
				this->choices.pop();
			}
			sleep(1);
			cout<<"The wheel chose...."<<endl;
			cout<<val1<<endl;
			sleep(1);
			cout<<val2<<endl;
			sleep(1);
			cout<<val3<<endl;
			sleep(1);
			cout<<val4<<endl;
			sleep(1);
			cout<<val5<<endl;
			sleep(1);
			cout<<val6<<endl;
			sleep(1);
			cout<<"Better luck next time, come again soon"<<endl;
			exit(0);
		}
		//step 4: "Cheat"
		void cheat(){
			int temp = 0x12 + 0x30;
			int comp = 0x3ab;
			if(temp!=comp){
				cout<<"Quit looking for cheats you big baby!"<<endl;
				exit(1);
			}

			//dead code, won't show up in decompiler
			//have to patch binary to get it to show up
			//alternatively, the reader can statically analyze the assembly to get the "strings" they need
			int correct = 1;
			queue <int> tempq;
			tempq.push(val1);
			tempq.push(val2);
			tempq.push(val3);
			tempq.push(val4);
			tempq.push(val5);
			tempq.push(val6);
			for (int i = 0; i < 6; i++){
				int b = tempq.front();
				int c = this->choices.front();
				if(b != c){
					correct = 0;
					break;
				}
				tempq.pop();
				this->choices.pop();
			}
			if(correct){
				printf("0x%x\n", 0x4d4a5258); //4 bytes chunks of the encoded flag
				printf("0x%x\n",0x495a5433); // The user can turn this back into hex, or just examine this snippet and determine that
				//these are ascii chars  
				printf("0x%x\n", 0x47525657);
				printf("0x%x\n", 0x51595255);
				printf("0x%x\n", 0x47525a44);
				printf("0x%x\n", 0x434e4a55);
				printf("0x%x\n", 0x4e555948);
				printf("0x%x\n", 0x454d444f);
				printf("0x%x\n", 0x50554641);
				printf("0x%x\n", 0x3d3d3d3d);
			}
			else{
				cout<<"Join us...."<<endl; //hint that the above numbers have to be merged together somehow
			}
		}
};




int main(){
	Wheel w;
	w.init();
	//use syscall to make the use of ptrace not blatantly obvious in decompilation
	//not a major barrier to reversing, of course
	long result = syscall(101, PTRACE_TRACEME,0, NULL, NULL);
	if(result == -1){
		exit(0);
	}

	while(1){
		while(1){
			int option = 0;
			cout<<"What do you want to do?"<<endl;
			cout<<"Press 1 for a hint"<<endl;
			cout<<"Press 2 to choose"<<endl;
			cout<<"Press 3 to play"<<endl;
			cin>>option;

			if(option == 1){
				w.hint();
				break;
			}
			else if(option ==  2){ w.choose();break;}
			else if (option == 3){ w.play();break;}
			else if (option ==  4){w.cheat();break;}
			else{
				cout<<"Illegal option"<<endl;
				break;
			}
		}
	}

}
