import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def som(x, w, eta, neigh_size):

    min_dist = np.inf
    for i in range(Nhidden):
        for j in range(Nhidden):
            dist = (x - w[i, j, :].reshape((-1, 1))).T.dot(x - w[i, j, :].reshape((-1, 1)))

            if min_dist > dist:
                min_dist = dist
                min_idx = [i, j]

    for i in range(min_idx[0] - neigh_size, min_idx[0] + neigh_size + 1):
        if i < Nhidden and i >= 0:
            for j in range(min_idx[1] - neigh_size, min_idx[1] + neigh_size + 1):
                if j < Nhidden and j >= 0:
                    #n = ((0.9 - 1)/a) * max(abs(min_idx[0] - i), abs(min_idx[1] - j)) + 1
                    n = 1
                    w[i, j, :] += eta * n * np.squeeze(x.T - w[i, j, :])
    return w, min_idx


votes = pd.read_csv('senato.csv')
votes = votes.values[:, 1:].astype(dtype=np.float32)
mp_party = pd.read_csv('partiti.csv')

mps_number = np.shape(votes)[0]
votes_number = np.shape(votes)[1]

print(votes_number)

Nhidden = 20
a = Nhidden
w = np.random.rand(Nhidden, Nhidden, votes_number)
eta = 0.1
epoch = 500

color = dict()
color['M5S'] = 'y'
color['FI-PdL'] = 'b'
color['PD'] = 'r'
color['Lega'] = 'g'
color['Art.1-MDP-LeU'] = 'm'

for e in range(epoch):
    output = []
    counter = np.zeros((Nhidden, Nhidden))

    neigh_size = int((-(a / (epoch-1)) * e + a) / 2)
    print(neigh_size)

    for i, mp in enumerate(votes):
        if i % 100 == 0:
            print(i)
        w, out = som(mp.reshape((-1, 1)), w, eta, neigh_size)
        output.append(out)
        counter[out[0], out[1]] += 1

for i in range(mps_number):
    if mp_party.values[i, 1] in color:
        plt.scatter(output[i][0], output[i][1], c=color[mp_party.values[i, 1]], s=500)
plt.show()

print()