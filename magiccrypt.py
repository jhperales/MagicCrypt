#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys, os, time

try:
	import crypto_random as random
except Exception, e:
	sys.stderr.write("The custom random number generator has failed to load!\nPlease make sure you have one of the following files:\n\n-> crypto_random.py\n-> crypto_random.pyc\n\nNote that .py and .pyw files can be interchanged.\n")
	raise SystemExit
else:
	crypto_random = True
#
# --------
#
# 	THIS ENCRYPTION ALGORITHM IS FOR PEOPLE WHO WANT THEIR DATA SO SECURE THAT GOD CAN'T DECRYPT IT. THERE IS NO FORESEEABLE NEED TO HAVE DATA
# 	THIS SECURE, AT LEAST FOR THE NEXT 1,000 YEARS. FOR ALL PRACTICAL PURPOSES, THIS ENCRYPTION IS ENTIRELY SECURE, EVEN WITH A 5 BYTE RANDOMLY
# 	GENERATED KEY. THIS ENCRYPTION IS DESIGNED TO BE SECURE NOT ONLY NOW, BUT FOR THE REST OF ETERNITY, AND ANY CHANCE OF DECRYPTIING A MESSAGE
# 	USING THIS ALGORITHM WITHOUT THE KEY IS PURELY THEORETICAL. IF SOMEONE'S GOING TO GET YOUR MESSAGE, IT WON'T BE BY GUESSING THE KEY. IT'S MORE
# 	LIKELY THAT THEY'LL EXTRACT THE MESSAGE FROM YOUR BRAIN ONCE THEY KILL YOU, OR THEY'LL HACK THE MATRIX TO READ YOUR MIND.
#
# --------
#
# 	Note that the --human mode is nothing more than an ordinary magic number cipher. Actually, this entire encryption algorithm is just an overcomplicated, overglorified magic number cipher with a bunch of statistics and probabilities in the comments, along with about 200 guarantees that nobody will ever read your message and some cool features.
#
# //// -----------------------------------------
# 
# SOME BASIC INFO:
#
# The term 'key' refers to what a user inputs at the program prompt. The key tells the program how much to shift each letter in a message.
# --human mode refers to the mode the program is put in while passing the --human command-line argument.
#
# This code runs extremely slowly, and for a reason. Slower code allows less keys to be guessed in a gven amount of time. If this is to be used for a large network, run this code on the client-side, not server-side. This can and probably will put stress on your servers if you have many people running the encryption/decryption operations at once. Also, feel free to port this over to other programming languages for better performance, but if you don't use the same random number generators, you won't be able to encrypt/decrypt messages.
#
# When porting this over to other programming languages, make sure that random numbers generated are pseudo-random, not truly random, except where os.urandom(...) is used. This program relies on getting the same numbers for the same seed, and it isn't necessary for random numbers to be cryptographically secure; they just need to be unique to the seed, except when generating keys with the --genkey= argument
#
# When using fake (-f) mode, it's a good idea to make your key at least 2 or 3 bytes longer than your message.
# If the security of the data you have encrypted is important enough, keep the key on a destructable media, such as a USB flash drive or an SD card, so you can completely destroy the key if necessary. If you do that, though, it's a good idea to keep a backup copy of the key so the data itself isn't entirely lost, but don't let the backup fall into the wrong hands, either! Keep the backup on a self-destructable media, too, and create a new backup version once you destroy the first key; if you have to destroy the backup, you want a second backup. Continue the process of destroying and re-backing-up until either (a) the data is safe or (b) you can destroy the data forever.
#
#
#
# I have provided some example messages, encrypted using the -f argument, using the following encoded key: <-- The messages provided are NOT decryptable, since the random number generation has been changed since this was added to the comments
# 
# 	2w+1NMy4kr5j2r83EpRyVtFGtnQ8LmDk <-- This key DOES NOT work, since the random number generation has been changed since this was added to the comments
# 
# To decrypt the messages, use the folllowing command:
# 
# 	./magiccrypt.py --key='("raw", "2w+1NMy4kr5j2r83EpRyVtFGtnQ8LmDk")' -od
# 
# And change "-od" to "-oe" to encrypt using the same key.
# The --key= argument assumes -f, but without --key= you need to use:
# 
# 	./magiccrypt.py -f
# 
# Otherwise, you'll end up using the key unencoded, which is a completely different key.
# Every message here is encrypted and encoded with the default charset, in which the message will only be 1 line once encoded.
# 
# Some example messages are: <-- These message are NOT decryptable, since the random number generation has been changed since this was added to the comments
# 
# 	8VvOPeIcMZVJp1OQf3CxpKfJFEr+9SVOVySpqniDTyuUo+GOTsr5ZJYzciJzf4xaLhp/CWw+=WJy7sP92=ryxMNDzbJB8eA8njBZw/5k8fWClKr0TBqH/ylkdP-eFM5z6zeMFKPhtxVLdd2/tPj0jiTJsChFHJy+uEz9gZkKJ4zWIS1Uc+nJ=Zr77ZtShxIMRml=wtbP0HiZ=J1wOSBwxGOuGZ3376g0N3Rz5Fnf1kVec1GETy2twTHOmH3UUDvyq81tKOfE9oIwyrLiq2kbxC
# ^^^ "Hello world" ^^^
# 
# An encoded key and a regular key are different. An encoded key represents a key; it isn't the key in itself. A regular key is the key itself. A key will be encoded so it can be put into the input prompt when it asks for the key. For example, try typing this:
# 
# 	DïSNuUžÄ6ånûÕ
#
# On my computer, when I pasted the above text, it thought I hit CTRL-C, since the key contains the ASCII character for CTRL-C.
# The text above is the actual key used for encrypting the example messages above, but I encoded it so that it could be used for encrypting and decrypting messages.
# Note that encoding a key or message does not encrypt it. All it does is put it into a charset that can be typed, copied and pasted.
# 
# //// -----------------------------------------


# NOTE: In --human mode, keys longer than the message they represent will be truncated to the length of the message, so for the message ABCDE, the keys QWERT, QWERTKJUSK, and QWERTIIAICLLAL are treated as the same. This ONLY works in --human mode

# ANOTHER NOTE: Longer keys will usually, if not always, be more secure, even in fake (-f) mode. It's probably best to use the longest key possible, since it's harder to guess, and in fake (-f) mode, it's more likely to look like the wrong one.

# YET ANOTHER NOTE: In --human mode, it's best to choose a key of the exact length of your message, or longer. There's no difference between using a 1-character key and using a Caesar Shift Cipher, which by the way, is easily broken on your average graphing calculator or even on paper.

# WHATEVER COMES AFTER "YET ANOTHER NOTE": Using fake (-f) mode with a non-randomly generated key is like using a supercar at 20mph without showing off how cool it is; the supercar doesn't get you there faster, just as a non-random key with fake (-f) mode doesn't hide your data any better. Seriously, if you're going to drive a supercar at 20mph, at least make people jealous of it!

# A FIFTH NOTE: Chances are that more than 1 key will decrypt your message, but don't worry. Nomatter how bad your practices are when choosing keys, nobody will be able to tell that it also works, unless they already know the message, in which case, they wouldn't even need a key in the first place. Just know that this doesn't protect you from them finding your actual key, just from them finding other keys that also work. The following Python code will tell you the probability that any individual key guessed will decrypt your message:
#
# 	print("1/%s" %((256**len(your_message))*(256**16))) # This works when you're not using --human mode
#
# Note that this does not take into account keys that resolve to an incorrect scope but still decrypt the message. There's more info about those cases below.
# And the probability that any individual key that resolves to the correct scope will decrypt your message is:
#
# 	print("1/%s" %(256**len(your_message))) # This works when you're not using --human mode
#
# So you can assume from the above code that the probability that any key guessed will resolve to the correct scope can be calculated by:
#
# 	print("1/%s" %(256**16))
#
# ^^^ This code should work for both Python2.7 and Python3.4 ^^^

# A SIXTH NOTE: If you use the same key for multiple messages, a brute-force attempt may not be entirely impossible; if someone can guess every possible key for 2 or more messages using the same key, they can notice that the same key decrypts both messages to what looks like it might be the original message. For that reason, it's best to switch keys with every message. A good way to do this if you can't securely get another key to the recipient is to encode the second key in the first message. Even still, this could reveal the key, but you'd need to send many thousands of messages in order to provide any significant vulnerability. Using a longer key will further reduce this risk, but if even a single key is insecure enough to be cracked, it could reveal every message in the chain.

# A SEVENTH NOTE: Still, don't worry! As of when this program was made (early 2016), there is no computer in the world known to be able to guess the key to a message, even if you don't use fake (-f) mode.

# AN EIGHTH NOTE: There is a very, very, very small chance that a key could look human-made, and generate a message that looks human-made saying something you really don't want being said and wasn't the intended message. There is an even smaller chance that a key that looks human-made, but still isn't your actual key, generates your actual message. If you happen to be so unlucky, you'll probably have a really tough time convincing people that that's not the message you sent. Of course, if someone guesses enough keys, they will eventually find one that looks human-made and generates a message that makes you look evil. They just have to be trying hard enough.

# A NINTH NOTE: With the default Python RNG (random number generator), there are actually only 27814431486576 possible unique states, which isn't enough to hide anything longer than a 5-character message. For that reason, I have redesigned it to offer unlimited unique states, based on the given seed.

# A TENTH NOTE: The custom random number generator used by this program is cryptographically secure and will generate an unlimited amount of unique sequences, based on the seed given. Each seed will generate a 100% unique sequence of pseudo-random numbers ranging in values from 1 to infinity, depending on the seed (and your CPU/RAM). The larger the seed, the larger and more random-esque the numbers generated will be. Feel free to use my random number generator, which is an adaptation to the Wichmann-Hill pseudo-random number generating algorithm.

def main():
	write = sys.stdout.write # If necessary, this can be changed later to output data differently
	err = sys.stderr.write # If necessary, this can be changed later to output data differently
	def rsort(lst, seed=False): # pseudo-randomly sorts a list of elements and returns the result
		lst = list(lst)[:]
		if seed == False:
			return lst
		if seed != None:
			random.seed(seed)
		ret = []
		while len(lst) > 0:
			r = random.randlong() % len(lst)
			ret += [lst[r]]
			del lst[r]
		return ret
	rsort2 = rsort
	def stoi(s): # Converts a string into an integer representing it
		ret = 0
		for char in s:
			ret += ord(char)
			ret *= 256
		ret /= 256
		return ret
	def itos(i): # Converts an integer into the string it represents
		ret = ""
		while i > 0:
			ret += chr(i % 256)
			i /= 256
		return ret[::-1]
	global fin, kin, op, fake, quiet, gkey, kkey, hash_algo, your_key_here, defaultkey # Ensures these variables get defined at a program-wide level
	gkey = lambda: stoi("3.14159265359") # Some arbitrary string; This needs to be the same for both encryptor and decryptor
	kkey = lambda: stoi(str(gkey()))
	fin = None # Input message, format '(type, value)'; possible types are "file" and "raw" and both type and value must be quoted, this is changed using the --in= parameter
	kin = None # Key to use, format '(type, value)'; possible types are "file" and "raw" and both type and value must be quoted, this is changed using the --key= parameter
	op = None # This specifies the operation to perform; possible values are E D and Q where E encrypts, D decrypts and Q just quits doing nothing.
	cryptdepth = 1 # This does nothing, I may or may not do something with it later - feel free to delete it from the code
	fake = False # If this is set to True, keys can be made to look like they don't decrypt the message - this ruins any ability to do a brute-force attack, assuming someone had the computing power to do one in the first place, as long as the key is sufficiently long. A 1-byte key won't fool anyone but a 243-byte key probably will.
	quiet = False # This does nothing, I may or may not do something with it later - feel free to delete it from the code
	all_bytes = list(chr(a) for a in xrange(256)) # A list enumerating every possible byte value; This should be kept at this original value
	cryptcharset = True # The range of values that can be encrypted; This needs to be the same for both encryptor and decryptor. True assumes all possible values.
	hash_algo = False # Set this to True to turn this program into a hashing algorithm. Once you do this, messages can't be decrypted once you encrypt them, unless you're willing to guess every possible message, hash it, and compare it to the value of the hash you're given, assuming you already know the key.
	outcharset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789=/+-" # The character set that can be produced as output; This needs to be the same for both encryptor and decryptor
	defaultkey = "DEFAULTKEY" # The key to use if none else is specified
	maxval = 256 # Keep this at 256
	reminv = False # By default leave non-encryptable characters in the message without encrypting them - this is only used with the --human parameter
	rseed = stoi("The year this program was made in is %s, all bytes are %s, the encrypting charset is %s and the output charset is %s" %(2016, all_bytes, cryptcharset, outcharset)) # Some arbitrary value used for ensuring the same random numbers get generated each time; This needs to be the same for both encryptor and decryptor

	your_key_here = lambda: stoi("Whatever you want goes here, just keep it as a string") # See the comment directly below to see what this changes

	# If you really want to be infinitely secure, uncomment the following line of code and change the value of the variable `your_key_here`
	#outcharset = rsort(outcharset, your_key_here())

	
	function = type(main) # This allows the code to test for executable statements
	

	def process(string, *argsL, **argsD): # Processes a string and returns the result, messages are left alone while keys undergo some manipulations for security
		if "type" in argsD:
			if argsD["type"] == "key":
				random.seed(stoi(string))
				ret = itos(random.randlong())
				return encode(ret, cryptcharset)
		return string
	def returnuppercharset(string, reminval=lambda: reminv, **argsD): # Replaces process(...) in --human mode
		if not isinstance(cryptcharset, (list, tuple)):
			return string
		a = ""
		reminval = reminval()
		for s in string:
			if s.upper() in cryptcharset:
				a += s.upper()
			elif s.lower() in cryptcharset:
				a += s.lower()
			elif not reminval:
				a += s
		return a
	def getmaxval(*argsL, **argsD): # Returns the value of the `maxval` variable dynamically
		return maxval
	def getAndReturn(value=None, *argsL, **argsD): # Used in certain conditions to avoid an operation that would normally occur
		return value
	def encrypt(message, key=defaultkey, charset=cryptcharset, depth=1): # Encrypts a message with a certain key and character set
		if type(message) != str:
			raise TypeError("The input encryption must be a string!")
		okey = key
		key = process(key, type="key") # Convert the external key to an internal key
		if returnuppercharset(okey) == key:
			for char in key:
				if char not in charset:
					raise ValueError("The key provided is not in the required charset!")
		del okey # Remove unneeded variable `okey`
		ret = ""
		if charset == True:
			for a in xrange(len(message)):
				ret += chr((ord(message[a]) + ord(key[a % len(key)])) % 256)
		else:
			for a in xrange(len(message)):
				if message[a] in charset:
					ret += charset[(charset.index(message[a]) + charset.index(key[a % len(key)])) % len(charset)]
				else:
					ret += message[a]
		if hash_algo:
			ret = process(ret, type="key")
			if isinstance(hash_algo, (int, long)) and (not isinstance(hash_algo, bool)):
				return encode(ret, outcharset)[:hash_algo]
		return encode(ret, outcharset)
	def encode(message, charset=outcharset, maxReq=getmaxval): # Encodes a message (a sequence of bytes) into the specified character set and returns the result; This can be used to perform encryption, but that's not its purpose, and the encryption will be significantly less secure
		try:
			len(charset)
		except TypeError:
			return message
		if len(charset) <= 1:
			raise ValueError("You must have more than 1 character in a charset!")
		if type(maxReq) == function:
			maxReq = maxReq()
		message = str(message)
		powr = 1
		while len(charset)**powr < maxReq:
			powr += 1
		lst = ()
		a = [0]*powr
		for x in xrange(len(charset)**powr):
			if a[-1] >= len(charset):
				a[-1] %= len(charset)
				a[-2] += 1
			b = ""
			for char in a:
				b += charset[char]
			lst += (b,)
			a[-1] += 1
		ret = ""
		if isinstance(cryptcharset, (list, tuple)):
			for byte in message:
				ret += lst[cryptcharset.index(byte)]
		else:
			for byte in message:
				ret += lst[ord(byte)]
		return ret	
	def decrypt(message, key=defaultkey, charset=cryptcharset, depth=1): # Encrypts a message with a certain key and character set
		if type(message) != str:
			raise TypeError("The input encryption must be a string!")
		okey = key
		key = process(key, type="key") # Convert the external key to an internal key
		if returnuppercharset(okey) == key:
			for char in key:
				if char not in charset:
					raise ValueError("The key provided is not in the required charset!")
		del okey # Remove unneeded variable `okey`
		message = decode(message, outcharset)
		ret = ""
		if charset == True:
			for a in xrange(len(message)):
				ret += chr((ord(message[a]) - ord(key[a % len(key)])) % 256)
		else:
			for a in xrange(len(message)):
				if message[a] in charset:
					ret += charset[(charset.index(message[a]) - charset.index(key[a % len(key)])) % len(charset)]
				else:
					ret += message[a]
		return ret
	def decode(message, charset=outcharset, maxReq=getmaxval): # Encodes a message (a sequence of bytes) into the specified character set and returns the result; This can be used to perform encryption, but that's not its purpose, and the encryption will be significantly less secure
		try:
			len(charset)
		except TypeError:
			return message
		if len(charset) <= 1:
			raise ValueError("You must have more than 1 character in a charset!")
		if type(maxReq) == function:
			maxReq = maxReq()
		message = str(message)
		powr = 1
		while len(charset)**powr < maxReq:
			powr += 1
		lst = ()
		a = [0]*powr
		for x in xrange(len(charset)**powr):
			if a[-1] >= len(charset):
				a[-1] %= len(charset)
				a[-2] += 1
			b = ""
			for char in a:
				b += charset[char]
			lst += (b,)
			a[-1] += 1
		ret = ""
		if isinstance(cryptcharset, (list, tuple)):
			for bytes in xrange(0, len(message), 2):
				bytes = message[bytes:bytes+2]
				ret += cryptcharset[lst.index(bytes)]
		else:
			for bytes in xrange(0, len(message), 2):
				bytes = message[bytes:bytes+2]
				ret += chr(lst.index(bytes))
		return ret
	def UI(): # Basic console user-interface
		global fin, kin, op, fake # `fin` is the input message, `kin` is the key, `op` is the operation to perform, and fake allows keys to made to appear incorrect to anyone trying to brute-force the message. See the comments at the top of this program for more details.
		try:
			try:
				if not op:
					err("Encrypt/Decrypt/Quit? (E/D/Q) ")
					op = raw_input()
				ed = op[0].lower()
			except IndexError:
				err("Error: Could not determine what operation to perform!")
				return ""
			if ed == "q":
				return ed
			if ed != "e" and ed != "d":
				err("Error: Could not determine what operation to perform!")
				return ed
			try:
				if fin:
					fin = tuple(eval(fin))
					typ = fin[0]
					val = fin[1]
					if typ == "file":
						f = open(val, "rb")
						msg = f.read()
						f.close()
					elif typ == "raw":
						msg = val
					else:
						raise ValueError("Unknown input type '%s'" %(typ))
				else:
					err("Message: ")
					msg = raw_input()
				if kin:
					kin = tuple(eval(kin))
					typ = kin[0]
					val = kin[1]
					fake = True
					if typ == "file":
						f = open(val, "rb")
						key = f.read()
						f.close()
					elif typ == "raw":
						key = val
					else:
						raise ValueError("Unknown input type '%s'" %(typ))
				else:
					err("Key: ")
					key = raw_input()
				key = process(key, lambda: False)
				if fake:
					key = decode(key)
				if key == "":
					key = defaultkey
				if ed == "e":
					write("%s" %(encrypt(process(msg), key, cryptcharset)))
				elif ed == "d":
					try:
						write("%s" %(decrypt(process(msg), key, cryptcharset)))
					except ValueError, e:
						if (str(e).endswith("' is not in list") and str(e).startswith("'")) or str(e) == "tuple.index(x): x not in tuple" or str(e) == "chr() arg not in range(256)":
							raise ValueError("The message given is either not properly encoded or not encoded at all.")
						else:
							raise e
					except IndexError, e:
						raise ValueError("The message given is either not properly encoded or not encoded at all.")
			except Exception, e:
				err(str(e)+"\n")
		except:
			return "q"
			return ed
	def loopUI(): # Unused since it causes weird output, probably having to do with sys.stdout.write(...)
		while UI() != "q":
			pass
	if "--code" in sys.argv: # Prints this program's own code to stdout
		f = open(sys.argv[0], "r")
		d = f.read()
		f.close()
		write(d)
		return
	if "-r" in sys.argv: # Removes invalid data from a message when processed; only for --human mode
		reminv = True
		del sys.argv[sys.argv.index("-r")]
	if "-f" in sys.argv: # Allows keys to be made to appear incorrect; see the comments on the `fake` variable for more information
		fake = True
		del sys.argv[sys.argv.index("-f")]
	av = sys.argv[1:] # A duplicate list of arguments passed into the program; used to delete elements while looping through them
	for arg in av:
		if "-q" == arg: # Quiet mode; this currently does nothing
			quiet = True
			del sys.argv[sys.argv.index(arg)]
		elif "--human" == arg: # Generates messages that can be encrypted and decrypted by hand; This can be used to communicate between someone with a computer and someone without a computer. Encryptions generated may be less secure if the message contains characters that can't be encrypted, such as a comma or period, or if the key is poorly chosen.
			rsort = getAndReturn
			cryptcharset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
			outcharset = cryptcharset
			defaultkey = cryptcharset[0]
			maxval = len(cryptcharset)
			rseed = False
			encode = getAndReturn
			decode = getAndReturn
			process = returnuppercharset
			err("All informaton encrypted will be human-decryptable until program exit and all information decrypted will be assumed to have been encrypted by a human or this program in --human mode.")
			del sys.argv[sys.argv.index(arg)]
		elif "--icharset" == arg: # Allows changing of the input charset upon runtime; it's best to only use this with --human mode
			cryptcharset = eval(raw_input("Input charset: "))
			defaultkey = cryptcharset[0]
			del sys.argv[sys.argv.index(arg)]
		elif "--ocharset" == arg: # Allows changing of the output charset, for example, if you're storing the message in a database where only alphanumerics are supported
			outcharset = evaal(raw_input("Output charset: "))
			del sys.argv[sys.argv.index(arg)]
		elif "--charset" == arg: # Changes both the input and output charsets at once; Again, it's best to only use this with --human mode
			cryptcharset = eval(raw_input("Charset: "))
			outcharset = cryptcharset
			defaultkey = cryptcharset[0]
			del sys.argv[sys.argv.index(arg)]
		elif "--maxval" == arg: # Use of this is discouraged, and I can't remember what it's even good for
			maxval = eval(raw_input("Maximum acceptable value: "))
			del sys.argv[sys.argv.index(arg)]
		elif arg[:2] == "-o": # Allows specifying the operation (encrypt/decrypt/quit uselessly) as a parameter
			op = arg[2:]
			del sys.argv[sys.argv.index(arg)]
		elif arg[:6] == "--key=": # Allows specifying the key to use as a parameter; assumes fake (-f) mode
			kin = arg[6:]
			del sys.argv[sys.argv.index(arg)]
		elif arg[:5] == "--in=": # Allows specifying the input message or file as a parameter
			fin = arg[5:]
			del sys.argv[sys.argv.index(arg)]
		elif arg[:9] == "--genkey=": # Generates a random key to use while encrypting
			err("Generating a random key...\n")
			params = dict(eval(arg[9:]))
			for elem in params:
				if elem != "length":
					if elem != "charset":
						if elem != "seed":
							if elem != "maxreps":
								if elem != "bytes":
									pass # This may or may not be changed later - right now this does nothing
			charset, length, maxreps, seed = None, None, 1, None
			if "seed" in params:
				err("Warning: Using custom seeds is not cryptographically secure, unless the seed is created entirely randomly, using a cryptographically secure random number generator (ex. rolling a 26-sided die 30 times and converting each value to a letter in the alphabet, then converting it into an integer representing it, not mentally thinking of a number)! One way to get secure random number is to use 'random.randlong()'\nIf possible, use the -f option for maximum security; for example, use\n\t%s -f --genkey='{\"bytes\":4096}'\n\n       -> Use this feature at your own risk\n" %(sys.argv[0]))
			err("\n")
			random.seed()
			if "human" in params: # Allows generating secure keys for human-decryptable messages
				if params["human"] == "default":
					rsort = getAndReturn
					cryptcharset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
					outcharset = cryptcharset
					defaultkey = cryptcharset[0]
					maxval = len(cryptcharset)
					rseed = False
					process = returnuppercharset
					del sys.argv[sys.argv.index(arg)]
					params = {"length":512, "charset":outcharset[:-1]}
			if fake:
				if "bits" in params:
					if "bytes" in params:
						err("You can't specify both bit and byte lengths of a key!")
						return
					write(encode(random.getrandbits(params["bits"])))
				elif "bytes" in params:
					hsh = ""
					for i in xrange(params["bytes"]):
						hsh += chr(random.randint(0, 255))
					write(encode(hsh))
				else:
					err("You must specify either the bit or byte length of your key!")
					return
			else:
				if "charset" in params: # Allows specifying the character set of generated keys, otherwise uses the default
					charset = params["charset"]
				else:
					charset = outcharset
				if "length" in params: # Allows specifying the length of the key to generate, otherwise uses the length of the charset in use
					length = params["length"]
				else:
					length = len(charset)
				if "seed" in params: # Allows specifying the seed to use when encrypting, otherwise uses a random number provided by the operating system as the seed
					seed = params["seed"]
				else:
					seed = None
				if "maxreps" in params: # Specifies the maximum repetitions of each character in the generated key; defaults to 1
					maxreps = params["maxreps"]
				ret = ""
				reps = {}
				for char in charset:
					reps.update({char: 0})
				charset *= maxreps
				r = rsort2(charset, seed)
				for char in r[:length]:
					ret += char
				if fake:
					ret = encode(process(ret, lambda: True), outcharset)
				write(ret)
			return
		elif arg[:7] == "--hash=":
			hash_algo = arg[7:]
			try:
				hash_algo = int(hash_algo, 0)
			except Exception, e:
				hash_algo = True
			if hash_algo <= 0:
				hash_algo = True
			del sys.argv[sys.argv.index(arg)]
	if len(sys.argv) == 1:
		UI()
		return
	elif len(sys.argv) == 3:
		a = sys.argv[1]
		if a == "-l":
			try:
				int(sys.argv[2], 0)
			except:
				err("Invalid parameter: -l takes an int")
				raise SystemExit
			r = int(sys.argv[2], 0)
			for b in xrange(r):
				if UI() == "q":
					return
			return
	elif len(sys.argv) == 2:
		if sys.argv[1] == "-e":
			if fin:
				fin = tuple(eval(fin))
				typ = fin[0]
				val = fin[1]
				if typ == "file":
					f = open(val, "rb")
					msg = f.read()
					f.close()
				elif typ == "raw":
					msg = val
				else:
					raise ValueError("Unknown input type '%s'" %(typ))
			else:
				err("Message: ")
				msg = raw_input()
			write(encode(msg, outcharset))
			return
		elif sys.argv[1] == "-d":
			if fin:
				fin = tuple(eval(fin))
				typ = fin[0]
				val = fin[1]
				if typ == "file":
					f = open(val, "rb")
					msg = f.read()
					f.close()
				elif typ == "raw":
					msg = val
				else:
					raise ValueError("Unknown input type '%s'" %(typ))
			else:
				err("Message: ")
				msg = raw_input()
			write(decode(msg, outcharset))
			return
	err("Invalid argument(s)! Usage: %s [-l count] [-q] | %s [-e/-d] [-q] | %s [--code] | See the code for more info" %(sys.argv[0], sys.argv[0], sys.argv[0]))
try:
	main()
except KeyboardInterrupt, SystemExit:
	pass
del main
