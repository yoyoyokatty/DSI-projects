def fizzbuzz():
	number = int(raw_input("What's the highest number you want to iterate through? "))
	numberslist = range(1, number+1)
	for item in numberslist:
		if item % 3 == 0 and item % 5 == 0:
			print "FizzBuzz"
		elif item % 3 == 0:
			print "Fizz"
		elif item % 5 == 0:
			print "Buzz"
		else:
			print item

fizzbuzz()