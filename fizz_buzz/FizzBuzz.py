def FizBuz(n, m):
	for x in range(n, m):
		print(((x % 3 == 0) * 'Fizz' + (x % 5 == 0) * 'Buzz') or x)
	print("\n")

FizBuz(3, 16)