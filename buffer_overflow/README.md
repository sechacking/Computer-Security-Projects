####Song
####Spring 2015
####CS 161
####Computer Security Project 1
####Due: Feb. 24, 11:59PM
####Version 1: Feb. 1, 2015

####Background

It is a time of rebellion. The evil empire of Caltopia oppresses its people with relentless
surveillance, and the emperor has recently unveiled his latest grim weapon: a supremely
powerful botnet, called Calnet, that aims to pervasively observe the citizenry and squash
their cherished Internet freedoms.

Yet in the enlightened city of Birkland, a 
icker of hope remains. The brilliant University of
Caltopia alumnus Neo, famed for not only his hacking skills but also the excellent YouTube
videos he produces illustrating his techniques, has infiltrated the empire's byzantine networks
and hacked his way to the very heart of the Calnet source code repository. As the emperor's
dark lieutenant, Prof. Evil of Junior University, attempts to hunt him down, Neo feverishly
scours the Calnet source code hunting for weaknesses. He's in luck! He realizes that Prof. Evil
enlisted ill-trained CS students from Junior University in writing Calnet, and unbeknownst
to the empire, the code is assuredly not memory-safe.

Alas, just as Neo begins to code up some righteous exploits to pwn Calnet's components, a
barista at the coffeeshop where Neo gets his free WiFi betrays him to Prof. Evil, who brutally
deletes Neo's YouTube account and swoops in with a SWAT team to make an arrest. As
the thugs smash through the coffeeshop's doors, Neo gets off one final piazza post for help.
Such are his hacking skillz that he crams a veritable boatload of key information into his
final message, exhorting the University of Birkland's virtuous computer security students to
carry forth the flame of knowledge, seize control of Calnet, and let freedom ring once more
throughout Caltopia : : :

####Getting Started

Neo has determined that the correct mojo for this task is you must work on it
in teams of 2 students. He expects your team to develop exploits for 5 vulnerabilities in
Calnet's components. As they topple you will move closer and closer towards pwning the
nefarious botnet. All you have to go by are your wits, your grit, and Neo's legacy: guidelines
on how to proceed, and, most precious, a virtual machine (VM) image that contains code
samples from the main Calnet components.

#####Software Setup

You can run and investigate the VM on your own computer. You will need the following
software:

VirtualBox1, the virtualization server<br>
Your favorite text editor<br>
Your favorite shell2<br>
Your favorite SSH client3<br>
nmap security scanner4<br>
netcat5

On Linux and Mac, you can install nmap, nc and ssh from your package manager. On
Windows, you can install Cygwin2 and use its package manager.

Note: Only use these tools against your own infrastructure. You violate campus policy
when directing them against parties who do not provide their informed consent!

Start VirtualBox and go to File6 ! Preferences ! Network. Make sure there is a network
adapter listed under \Host-only Networks" named vboxnet0.7 If the adapter list is empty,
click the plus on the right side which will add a new interface. Confirm with OK.

Neo placed the VM image pwnable.ova at http://goo.gl/EzYsEJ. Download it and import
it via File ! Import Appliance.

You will run the vulnerable programs and their exploits inside the VM. The image is a barebones
Ubuntu Linux server installation on a 32-bit Intel architecture. The first time you
boot the image, you have to enter your class accounts in the format cs161-x1x2,cs161-x3x4,
where x1; : : : ; x4 are the letters of your class accounts. You need to list the accounts in alphabetical
order. For example, if a student with class account cs161-we teams with a student
with class account cs161-vv, then you would enter the string \cs161-vv,cs161-we".

Once the VM is booted and configured, you will see a \ready for pwning" message on the
screen.

#####Some Important Advice Concerning Execution Environments

Note: This advice does not concern Question 1.

Exploit development can lead to serious headaches if you don't adequately account for factors
that introduce non-determinism into the debugging process. In particular, the stack
addresses in the debugger may not match the addresses during normal execution. This artifact
occurs because the operating system loader places both environment variables and
program arguments before the beginning of the stack:

Stack<br>
program arguments<br>
environment vars<br>
Kernel<br>
0xc0000000<br>
0xbffff???<br>
variable<br>
size

Already installed in the VM you'll find a small helper utility, invoke, that makes sure
environment and arguments remain at the same location, regardless of whether using the
debugger or not. For example, instead of invoking the program foo directly via ./foo, you
should instead use invoke foo:

% ./foo arg1 arg2 # invocation dependent on environment state :-(<br>
% invoke foo arg1 arg2 # deterministic invocation<br>
% invoke -d foo arg1 arg2 # deterministic invocation in gdb

You may find it useful to pass an extra environment to the program. The -e switch serves
that purpose:

% invoke -e X=Y foo arg1 # sets environment variable X=Y in foo

Note: You must always use invoke to launch (or debug via -d) the provided executables
because invoke additionally parameterizes the execution environment based on the ID you
entered during the first boot. More broadly, since our grading tool uses the exact same
VM that you downloaded, do not perform any system modidications, only add/upload new
content. (For example, do not attempt to recompile the given executables, otherwise you
will have to reinstall the VM.) This way you ensure that your solutions will work with our
grading tool and you do not run the risk of losing unnecessary points.


####The Task

Unfortunately Neo did not have enough time to figure out the necessary login credentials. It
is up to you to break into the VM and continue his mission, with the ultimate goal to gain
root privileges on the machine to have full control over Calnet. Neo's intelligence sources
revealed that, once broken in the system, the required login credentials necessary for further
access are located inside the system itself.

You know from having watched his YouTube channel that Neo advocates a three-step approach
for breaking into a system:

<b>Step 1: Reconnaissance.</b> Investigate what software/which services is/are running (hint: nmap).
Determine if there is anything you can access (hint: netcat). What can you discover
about the software (e.g., in terms of version; do you have the source code)? Using this
information you can seek out potential vulnerabilities. Do not hesitate to fire up your
favourite search engine and search for related materials. Outside sources will be very
helpful when you are unclear about some concepts or information in this project.

<b>Step 2: Development.</b> After you have found a vulnerability, you can create an exploit using
the found bugs(generally, as an attacker, this means crafting a malicious input to the
buggy program).

<b>Step 3: Profit.</b>

Use Neo's three-step plan to solve the following problems.

#####Question 1 Gaining VM Access (20 points)

Neo knew that it could prove daunting to find yourself confronted with an unknown
system without login credentials. Upon skimming his messages, you find out that one
standard procedure to break into systems begins with a port scan via nmap, which tells
you what services run on the machine. Moreover, you learn about netcat. Familiarize
yourself with these tools by reading their man pages or help messages (e.g. man nmap
or nmap -h or just search online!) and try to use them to get a foothold in the system!
Also, searching for the welcome messages of the machines services on the Internet is
always a good start for finding known vulnerabilities.

Note: You need to gain access to the VM via the network, as opposed to mounting the
filesystem locally and browsing the contents.

#####Submission and Grading.

For this problem you will submit a shell script named
exploit which takes an IP address as first argument. Our grading tool executes your
script as ./exploit address where address represents the IP address of our grading
VM9. Our tool tests whether the end of the execution spawns a shell with effective
privileges of the user vsftpd10 (10 points).

Moreover, you will submit a file called NETCAT that includes the first line from the output
of nc -h where nc stands for the netcat 
avor you use. You must also submit a file,
q1.txt, that includes a brief description of the vulnerability, how it could be exploited,
and a walkthrough of your solution. You should also include output from any tools you
used in your discovery of the exploit. This document should be no more than one page.
We will use it to verify that your understanding of the problem matches your exploit
code. Moreover, we will use it to award you partial credit in the event that your exploit
does not work with our automated grading system (10 points).

#####Question 2 Behind the Scenes (40 points)

Neo's message assures you that given its hasty development by poorly educated programmers,
Calnet's components contain a number of memory-safety vulnerabilities. In
the VM that Neo provided, you will find the first code piece located in the directory
/home/vsftpd.

You are to continue his work and write an exploit that spawns a shell, for which you can
use the following shellcode:

shellcode = <br>
"\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07" +<br>
"\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d" +<br>
"\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80" +<br>
"\xe8\xdc\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68"

Note: Recall that x86 has little-endian byte order, e.g., the first four bytes of the above
shellcode will appear as 0x895e1feb in the debugger.

Neo already provided an exploit scaffold that takes your malicious buffer and feeds it to
the vulnerable program via a script called exploit:

#!/bin/sh<br>
( ./egg ; cat ) | invoke dejavu

(As one of Neo's message explains in a concise but strikingly lucid fashion, the expression
before the shell pipe is necessary so that if the attack input generated by egg succeeds,
then you will be able to interact with the shell that the exploit spawns by typing via
stdin.)

To get started, read "Smashing The Stack For Fun And Profit" by AlephOne. Neo
recommended that you try to absorb the high-level concepts of exploiting stack overflows
rather than every single line of assembly. He also warned you that some of the example
codes are outdated and may not work as-is.

#####Submission and Grading. 

For this problem you will submit the missing script egg,
which can be written in your favorite scripting language (e.g., Python, Ruby, Perl, Bash).
Your code should print the buffer used by the exploit script to spawn a shell. Make
sure it works by invoking ./exploit. Our grading tool will log into a clean VM image
as user vsftpd and put your submission into the directory /home/vsftpd. A script will
then invoke the script exploit exactly as given above and check for the existence of a
shell prompt with effective privileges of user smith (25 points).

You must also submit a file, q2.txt, that includes a brief description of the vulnerability,
how it could be exploited, how you determined which address to jump to, and a sketch
of your solution. This includes gdb output that very clearly demonstrates the effects of
your exploit (before/after). As before, keep it to no more than one page (15 points).

#####Question 3 Compromising Further (40 points)

Calnet uses a sequence of stages to protect intruders from gaining root access. The
inept Junior University programmers actually attempted a half-hearted fix to address
the overt buffer overflow vulnerability from the previous stage. In this problem you must
bypass these mediocre security measures and, again, inject code that spawns a shell.

In the home directory of this stage, /home/smith, you will find a sample input file
anderson.txt illustrating the input format that the program agent-smith expects
(which is an initial byte specifying the length of the input, followed by the input itself):

% ./agent-smith anderson.txt

Neo realized that nothing prevents you from feeding agent-smith an arbitrary file of
your choice. In particular, Neo started a script exploit representing an initial exploit
attempt:

#!/bin/sh<br>
./egg > pwnzerized<br>
invoke agent-smith pwnzerized

#####Submission and Grading. 

As in the previous question, you will submit a script egg,
written in your favorite scripting language, that integrates with the above displayed
script exploit. Your script should inject shellcode to spawn a shell. Make sure it works
by invoking ./exploit. Our grading tool will log into a clean VM image as user smith
and put your submission into the directory /home/smith. A script will then invoke
exploit and check for the existence of a shell prompt with effective privileges of user
brown (25 points).

You must also submit a file, q3.txt, that includes the same type of information as for
the previous Question (15 points).

#####Question 4 Deep Infiltration (50 points)

Calnet is a pernicious and invasive piece of malcode. But Prof. Evil undertook all of
his own studies at Junior University, and as such he never really learned how to count
without occasionally screwing it up. Find the subtle vulnerability in this code, and inject
code that spawns a shell.

Neo, again on top of it, started a scaffold called exploit that you can use:

#!/bin/sh<br>
invoke -e egg=$(./egg) agent-brown $(./arg)

(Note that a shell expression like \$(foo)" means \run the command foo and substitute
its stdout output here." So \egg=$(./egg)$" means \run the command ./egg and
assign the output it generates to the variable $egg.")

To solve this problem, you are pretty sure that a cryptic reference in Neo's message
indicates you'd benefit from reading Section 10 of \ASLR Smack & Laugh Reference"
by Tilo Muller. (Although the title suggests that you have to deal with ASLR, you
can ignore any ASLR-related content in the paper for this question.)

#####Submission and Grading. 

For this question question, you will submit a script arg
and a script egg written in your favorite scripting language. Your code should integrate
with the script exploit as shown above. Make sure your scripts work by invoking
./exploit. Our grading tool will log into a clean VM image as user brown and put your
submission into the directory /home/brown. A script will then invoke exploit and check
for the existence of a shell prompt with effective privileges of user jz (30 points).

As for the previous question, you must also submit a file, q4.txt, that includes a brief
description of the vulnerability, how it could be exploited, how you determined which
address to jump to, and a sketch of your solution. This includes gdb output that very
clearly demonstrates the effects of your exploit (before/after) (20 points).

#####Question 5 The Last Bastion (50 points)

To protect the Calnet source from advanced hackers, Prof. Evil's minions persuaded him
that he must enable address layout randomization (ASLR) as a final layer of defense for
the VM. They assured him that it was inconceivable that anyone even of super-
human intelligence would possess the uber-h4x0r skillz required to overcome this.

Yo, Birkland! Your mission, should you choose to accept it, is to bypass the ASLR
protection and spawn a shell with root privileges. Full control of the box : : : and thus
Calnet itself awaits you! Neo didn't dare hope you might hack your way this far and this
deeply : : : but he could never abandon his dream of freedom, and to that end provided
an exceedingly cryptic clue in his final message that after a caffeine-fueled all-nighter
you eventually realize suggests you should consider reading Section 8 of \ASLR Smack
& Laugh Reference" by Tilo Muller. He also told you that you could get the password
to jones directly from /home/jz, but as soon as you logged in as jones, ASLR would
be launched.

One detail Neo could figure out for you is that the service to exploit listens locally on
TCP port 42000 (try netstat -tulpn | grep 42000). It turns out that the operating
system watches the service and restarts it shortly when it crashes. You have to send the
malicious shellcode to that service to successfully complete this task. Looking through
Neo's past messages, you find guidance to develop this in the form of a TCP \bind shell"
listening on 127.0.0.1:6666.

# Linux (x86) TCP shell binding to port 6666.<br>
bind_shell =<br>
"\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66\xcd" +<br>
"\x80\x5b\x5e\x52\x68\x02\x00\x1a\x0a\x6a\x10\x51\x50\x89" +<br>
"\xe1\x6a\x66\x58\xcd\x80\x89\x41\x04\xb3\x04\xb0\x66\xcd" +<br>
"\x80\x43\xb0\x66\xcd\x80\x93\x59\x6a\x3f\x58\xcd\x80\x49" +<br>
"\x79\xf8\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3" +<br>
"\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

This should finally suffice to pull off the Final Stage! Somehow you must code up the
program egg so that Neo's exploit script can launch the final, fatal strike:

#!/bin/sh<br>
echo "sending exploit"<br>
./egg | nc 127.0.0.1 42000 &<br>
sleep 1<br>
nc ...

Alas, the battery in Neo's ultra-thin BlueTooth keyboard died just as he was finnishing
typing here. To successfully employ the script, you'll need to replace \..." with the
required arguments to access the root shell.

The freedom of cybercitizens throughout Caltopia rests in your hands ...

#####Submission and Grading.

For this question question, you will submit a complete
shell script exploit that carries out the attack and spawns a shell with root privileges.
You will also submit a script egg, written in your favorite scripting language, that prints
the exploit buffer to standard output and pipes it to netcat. Make sure your scripts
work by invoking ./exploit. Our grading tool will log into a clean VM image as user
jones and put your submission into the directory /home/jones. A script will then
invoke exploit and check for the existence of a shell prompt with effective privileges of
user root (30 points).

You must also submit a file, q5.txt, in the same fashion as for the previous question
(20 points).

#####Question 6 Feedback (optional) (0 points)

If you wish, submit a text file, feedback.txt, with any feedback you may have about
this project. What was the hardest part of this project in terms of understanding? In
Project 1 Page 8 of 9 CS 161 { Sp 15
terms of effort? (We also, as always, welcome feedback about other aspects of the class.)
Your comments will not in any way affect your grade.

####Submission Summary

In addition to the above files, you should also submit a file named partner.txt and include
your partner's ID in that file (or leave it blank if you work on your own).
In summary, you must submit the following directory tree:

q1/exploit<br>
q1/q1.txt<br>
q1/NETCAT<br>
q2/egg<br>
q2/q2.txt<br>
q3/egg<br>
q3/q3.txt<br>
q4/arg<br>
q4/egg<br>
q4/q4.txt<br>
q5/egg<br>
q5/exploit<br>
q5/q5.txt<br>
partner.txt<br>
feedback.txt (optional)

Details on how to submit your solutions will be posted on piazza a week before the submission
deadline.

Congratz! And continue from here (https://code.google.com/p/it-sec-catalog/wiki/
Exploitation) if you really enjoyed it and want to become an exploitation ninja! :)

####References

Aleph One. Smashing The Stack For Fun And Profit. Phrack, 7(49), November 1996.
http://goo.gl/EzYsEJ.
Tilo Muller. ASLR Smack & Laugh Reference. http://goo.gl/EzYsEJ, February 2008.