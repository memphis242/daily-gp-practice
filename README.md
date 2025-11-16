# :brain: Daily General-Purpose Programming Practice
Although I have separate "practice" repositories for the different programming languages in my toolkit, I'd like a general-purpose program that is quick enough to write in under 30 min in any programming language (once I get efficient enough) and touches many important concepts in programming.

## Program

### Concepts
1. File I/O
2. String Processing
3. Maps/Sets
4. Networking
5. User Input
6. Command-Line Argument Parsing
7. Time-Keeping
8. Kernel Signals

### Spec
Write a program that:

1. can establish a TFTP connection between a client and server on the _same_ host (or with a Raspberry Pi server) in order to transfer a JSON file >100 lines long (structure is up to you).

2. The client is responsible for producing the JSON file by asking for user input via the terminal.

3. A command-line argument is passed to establish a timeout of user entry and file transfer parameters, with defaults assumed if none are given. One of the file transfer parameters needs to be the speed at which the TFTP data packets are sent. This is done to facilitate packet drop simulation to check correct handling of that.

4. At any point, the user of the client may submit an interrupt signal to cancel the session. The client program will handle this gracefully by informing the server that the client has cancelled the session, after which the server also begins its graceful exit. This is going to be on a _different_ port than the TFTP connection, of course.

5. Once user input is complete, the client program establishes the TFTP connection, making a write file request, and starts transfering to completion.
   - At any point, the server may "drop" a packet via user signalling on the server end. The behavior of both endpoints here should abide by the TFTP RFC 1350 standard.

6. Upon completion of the transfer, the server prints out, in dictionary/map form separate from JSON, the contents of the JSON file structure it received. This printout may be on console output of the server or via packet transfers back to the client (protocol of your choosing) which writes the contents to a file.
