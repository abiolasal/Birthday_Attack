from hashlib import sha256  # sha256 package from hashlib library
from binascii import hexlify  # converts string bytes to hexadecimal
import random  # gets random string
import string  # For all ascii characters
import time  # for time capture
import itertools  # helped to produce complex ranges for the search in order to avoid nested for statements
import argparse  # for parsing of the command line argument
import os  # needed to clear the display console

start_time = time.time()
N = 32  # input string Length. This will set size of input messages to 256 bits
TRUNC = 10  # Number of hexdigest characters to consider from the sha256 output
s = string.digits+string.ascii_letters  # All possible string and digit characters. That is 0-9a-zA-Z
evaluations = 0  # evaluations done before finishing
hashed_dict = {}  # to save the input/hashed output pair


def BadHash40(input_string):

    '''
    Returns the first 40 bits of its argument. If the input is bytes, they
    will be hashed directly; otherwise they will be encoded to ascii
    before being hashed.
    '''

    if type(input_string) is bytes:
        # Already encoded, just hash the bytes.
        return sha256(input_string).hexdigest()[:TRUNC]
    else:
        # Convert it to ascii, then hash.
        return sha256(input_string.encode('ascii')).hexdigest()[:TRUNC]


def get_random():
    '''
    Get random characters from s of length N and returns rand_input of 32 characters
    '''
    rand_input = ''.join(random.sample(s, N))
    return rand_input


# checks if the hash.data file is already in path, deletes it if found
if os.path.isfile('hash.data'):
    os.remove('hash.data')

'''
This block of code finds the collision.
NN represents the -lhash parameter which sets the size of input/output pairs.
It generates input messages of size NN, hash them and stores in a dictionary.
It then checks for collision among the hashes henerated, if collision found, it
outputs the inputs and their collision, else, it start afresh by generating new list 
of input/output pairs and store in the dictionary.
'''
parser = argparse.ArgumentParser()
parser.add_argument("-lhash", required=True)
NN = int(parser.parse_args().lhash)
ranges = [range(NN), range(NN)]

for i, j in itertools.product(*ranges):
    evaluations += 1
    message = get_random()  # gets a random message input
    message2hex = str(hexlify(message.encode("ascii")), "ascii")  # converts to 64 hexadecimal characters
    message_hash = BadHash40(message)
	
	#  catches memory error, incase we are search for a too big collision
    if message_hash not in hashed_dict.keys():
        try:  # Let's expect a MemoryError if we search a too big collision
            hashed_dict[message_hash] = message
        except MemoryError:
            print("LOG: MemoryError")
            hashed_dict = {}
    else:
        if hashed_dict[message_hash] == message:
            print("String Already Used!")
            print("Number of evaluations made so far", evaluations)
        else:
            break
'''
If a collision is found, the colliding inputs are identified using the dictionary keys method
and they are converted to hexadecimal format before display on console or saved to file.

Opens the hash.data file and creates the header for the inputs and their hashes
stores the collided messages in hex format and also populates the entire dictionary which holds the 
input/output pairs
'''
colliding = hashed_dict[message_hash]
colliding2hex = str(hexlify(colliding.encode("ascii")), "ascii")  # converts to 64 hexadecimal characters
collHash = BadHash40(colliding)
os.system('clear')

with open('hash.data', 'a+') as f:
    f.writelines('---------------------------------------------------------------'
                 '-Collision Found!----------------------------------------------\n')
    f.writelines(['Message 1(in Hex): ', message2hex, '\tMessage 1 Hash: ', message_hash,
                  '\nMessage 2(in Hex): ', colliding2hex, '\t Message 2 Hash: ', collHash, '\n'])
    f.writelines('-' * 126)
    f.writelines(['\n', 'Input Message'.ljust(64, ' '), '\t\t Message Hash'.ljust(10, ' '), '\n'])
    for key in hashed_dict:
        hashed_dict[key] = str(hexlify(hashed_dict[key].encode("ascii")), "ascii")
        in_out_pairs = [hashed_dict[key], '\t\t', key, '\n']
        f.writelines(in_out_pairs)
print('---------------------------Collision Results----------------------------')
print("                      Number of evaluations made: ", str(evaluations)+'  ')
print("                         Time Taken: %.2f seconds   " % (time.time() - start_time))
print('                                Input(in Hex)'.ljust(64, ' ') + ' | '+'Hash'.ljust(10, ' '))
print('-----------------------------------------------------------------+-------')
print(colliding2hex+' | '+collHash+'\n' +message2hex+' | '+message_hash)
print('-----------------------------------------------------------------+-------')