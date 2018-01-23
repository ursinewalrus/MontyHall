import urllib2
import random


# total games
num_games = 10000

# total doors
num_doors = 3

# how many doors will be revealed
doors_revealed = 1

# hide the prize behind all the doors up front using true random numbers
# is has certain quota per day so if it 503's or anything else we can just use the standard random number generator
# if we run out of quota at any point just fall back
try:
	prize_doors = urllib2.urlopen("https://www.random.org/integers/?num="+str(num_games)+"&min=0&max="+str(num_doors-1)+"&col=1&base=10&format=plain&rnd=new").read()
	prize_doors = prize_doors.replace("\n","");
	
	# do all our guesses up front also
	first_guesses = urllib2.urlopen("https://www.random.org/integers/?num="+str(num_games)+"&min=0&max="+str(num_doors-1)+"&col=1&base=10&format=plain&rnd=new").read()
	first_guesses = first_guesses.replace("\n","");
	
	# doing more guesses does nothing without expanding the number of revealed doors so might as well let guess once but expand doors revealed
	# will be the index of the second guess door after the removed door indices and the first guess door index are removed from the list of possible doors to pick
	second_gueses = urllib2.urlopen("https://www.random.org/integers/?num="+str(num_games)+"&min=0&max="+str(num_doors-doors_revealed-2)+"&col=1&base=10&format=plain&rnd=new").read()
	second_gueses = second_gueses.replace("\n","");

except urllib2.HTTPError:
	prize_doors = [random.randint(0,num_doors-1) for _ in range(0,num_games)]
	first_guesses = [random.randint(0,num_doors-1) for _ in range(0,num_games)]
	second_gueses = [random.randint(0,num_doors-doors_revealed-2) for _ in range(0,num_games)]

games = []

# package the doors and the initial guesses nicely together, cast all to int in case they came from the api
for i in range(0,num_games):
	games.append({  "prize":int(prize_doors[i]),
					"first_guess":int(first_guesses[i]),
					"second_guess":int(second_gueses[i])
				})
# for g in games:
# 	print str(g) + "\n"

incorrect_guesses = 0
correct_guesses = 0

output_string = ""
# probably have to redo how choose what doors to remove since those ones are dependant on the first choice
games_output = str(num_doors) + " Doors " + str(doors_revealed) + " Per Round"
for i in range(0,num_games):
	current_game = games[i]
	games_output +=  "\nGame " + str(i) 
	games_output += "\nInitial guess: " + str(current_game["first_guess"])

	possible_doors_to_rm = range(0,num_doors)

	possible_doors_to_guess = range(0,num_doors)
	# remove current door pick for possible to remove and guess again
	possible_doors_to_rm.remove(current_game["first_guess"])
	possible_doors_to_guess.remove(current_game["first_guess"])

	# cant remove the prize door
	#in case they picked the right door the first time and the prize door is already removed
	if(current_game["prize"] in possible_doors_to_rm):
		possible_doors_to_rm.remove(current_game["prize"])
	# now we have a list of all doors we are allowed to remove
	games_output += "\nDoor(s) removed: "
	for i in range(0,doors_revealed):
		# get val of a door we are going to reveal
		remove_val = random.sample(possible_doors_to_rm,1)
		# removed so now it cant be guessed, since revealed
		possible_doors_to_guess.remove(remove_val[0])
		# removed from possible to be removed, so if more to remove same door not double revealed
		possible_doors_to_rm.remove(remove_val[0])
		games_output += "\n"+str(remove_val)
		# going to have to use math.random here and not the api without some confusing stuff
		# because the ones you are allowed to remove are dependant on the first guess, which, is random
	games_output += "\nChange guess to " + str(possible_doors_to_guess[current_game["second_guess"]])
	games_output += "\nWas door " + str(current_game["prize"])
	games_output += "\n____"
	if possible_doors_to_guess[current_game["second_guess"]] == current_game["prize"]:
		correct_guesses += 1
	else:
		incorrect_guesses += 1
games_output += "\nCorrect Guesses |" + str(correct_guesses) + "/" + str(incorrect_guesses) + " |Incorrect Guesses"
print games_output


# if we werent grabbing the random numbers all at the start and didnt want to be able to arbitrarily modify
# doors by just changing a var would probably just have a little loop like

'''
correct = 0
incorrect = 0
for i in range(0,10000):
	# doors 0-2
	doors = range(0,3)
	removeable_doors = range(0,3)
	# prize behind door 0-2
	prize = random.randint(0,2)
	# pick door 0-2
	pick = random.randint(0,2)
	# cant pick your own door again

	removeable_doors.remove(pick)
	# remove prize door from doors we can eliminate if we havnt with the pick door elimination already
	if pick != prize:
		removeable_doors.remove(prize)
	else:#if you picked the right door first, just remove one of the wrong doors at random
		to_remove = random.sample(removeable_doors,1)[0]
		removeable_doors.remove(to_remove)
	# remove an incorrect door
	doors.remove(removeable_doors[0])
	# find the door that is not your pick
	for index,door in enumerate(doors):
		if doors[index] != pick:
			pick2 = doors[index]
	if(pick2 == prize):
		correct += 1
	else:
		incorrect +=1
print str(correct) + "/" + str(incorrect)
'''


# I mean really for any problem such that doors you reveal are n-2 you can do the below,
# if i made to make a calculator for this with the mechanisms all hidden i might be tempted to just do it
# this way, demonstratec for n=3

'''
wins = 0
losses = 0
for i in range(0,10000):
	# for any monty hall such that revealed doors = n-2, you can only loose if switch you choose the right door the first time
	# so say on the left the randint is the prize door and on the right is your guess...
	if random.randint(0,2) == random.randint(0,2):
		losses += 1
	else:
		wins += 1
print str(wins) + "/" + str(losses)

'''