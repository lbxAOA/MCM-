import numpy as np


def check(x):
	if x.sum() > 400:
		return False
	if x[0]+2*x[1]+2*x[2]+x[3]+6*x[4] > 800:
		return False
	if 2*x[0]+x[1]+6*x[2]>200:
		return False
	if x[2]+x[3]+5*x[3]>200:
		return False

	return True


def get_radom():
	x = np.random.randint(100, size=5)
	while not check(x):
		x = get_radom()
	return x


lim = 10**6
ans = -1

for i in range(lim):
	num = get_radom()
	ans = max(ans, num.all())
	if i % 10000 == 0:
		print(i)

print('ans=' + ans)
