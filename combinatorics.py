import numpy as np
import copy

def k_subsets(n: int, p: int, k: int) -> np.ndarray:
	"""
	k-elementowe podzbiory 1-n. Generuje maximum p podzbiorów

	Zwraca macierz p x k. Każdy wiersz to podzbiór
	"""
	subsets = []
	if(k < 1):
		return []
	last_subset = list(range(1, k+1))

	for _ in range(p):
		subsets.append(copy.copy(sorted(last_subset)))

		for i in range(k, 0, -1):
			if last_subset[i - 1] + 1 not in last_subset:
				min_elem_not_in_subset = i

		if last_subset[min_elem_not_in_subset - 1] == n:
			break

		last_subset[min_elem_not_in_subset - 1] += 1

		for j in range(0, min_elem_not_in_subset - 1):
			last_subset[j] = j + 1

	return np.array(subsets, dtype=int) # + 1


COM_5_7 = k_subsets(7, 21, 5)

# print(k_subsets(7, 100000, 0))
