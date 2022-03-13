import numpy as np


class Experience:
    def __init__(self):
        self._experience = self.sort_exp(np.load('data.npy', allow_pickle='TRUE').item())

    @staticmethod
    def sort_exp(exp):
        for key in exp:
            exp[key].sort(reverse=True, key=lambda a: (a[1], len(a[0])))
        return exp

    def __iter__(self):
        return iter(self._experience)

    def __getitem__(self, name):
        return self._experience[name]

    def safe(self, exp, num_moves):
        for key in exp:
            if key in self._experience:
                for l in self._experience[key]:
                    if l[0] == num_moves:
                        l[1] += 1
                        break
                else:
                    self._experience[key].append([num_moves, 0])
            else:
                self._experience[key] = []
                self._experience[key].append([num_moves, 0])
        np.save('data.npy', self._experience)

    def move(self, state, free_moves):
        if state in self._experience:
            # print(state)
            # print(self._experience[state][0])
            for move in self._experience[state][0][0]:
                if move in free_moves:
                    return move


if __name__ == '__main__':
    ex = Experience()

    for i in ex:
        print(i)
        print(ex[i])
