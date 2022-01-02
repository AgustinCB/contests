import numpy
import random
import sys
from typing import Iterator, Tuple


class ALU(object):
    def __init__(self, inputs: str):
        self.inputs = inputs
        self.input_index = 0
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0

    def execute(self, instruction: str):
        instruction_parts = instruction.split(" ")
        if instruction_parts[0] == "inp":
            self.__input(instruction_parts[1])
        elif instruction_parts[0] == 'add':
            self.__add(instruction_parts[1], self.__get_integer(instruction_parts[2]))
        elif instruction_parts[0] == 'mul':
            self.__mul(instruction_parts[1], self.__get_integer(instruction_parts[2]))
        elif instruction_parts[0] == 'div':
            self.__div(instruction_parts[1], self.__get_integer(instruction_parts[2]))
        elif instruction_parts[0] == 'mod':
            self.__mod(instruction_parts[1], self.__get_integer(instruction_parts[2]))
        elif instruction_parts[0] == 'eql':
            self.__eql(instruction_parts[1], self.__get_integer(instruction_parts[2]))

    def __eql(self, variable1: str, variable2: int):
        self[variable1] = int(self[variable1] == variable2)

    def __mod(self, variable1: str, variable2: int):
        self[variable1] = self[variable1] % variable2

    def __div(self, variable1: str, variable2: int):
        self[variable1] = int(self[variable1] / variable2)

    def __mul(self, variable1: str, variable2: int):
        self[variable1] *= variable2

    def __add(self, variable1: str, variable2: int):
        self[variable1] += variable2

    def __input(self, variable: str):
        input_value = int(self.inputs[self.input_index])
        self.input_index += 1
        if variable == 'x':
            self.x = input_value
        elif variable == 'y':
            self.y = input_value
        elif variable == 'w':
            self.w = input_value
        elif variable == 'z':
            self.z = input_value

    def __get_integer(self, variable: str) -> int:
        if variable in ['w', 'x', 'y', 'z']:
            return self[variable]
        return int(variable)

    def __getitem__(self, index: str) -> int:
        if index == 'w':
            return self.w
        elif index == 'x':
            return self.x
        elif index == 'y':
            return self.y
        elif index == 'z':
            return self.z

    def __setitem__(self, index: str, value: int):
        if index == 'w':
            self.w = value
        elif index == 'x':
            self.x = value
        elif index == 'y':
            self.y = value
        elif index == 'z':
            self.z = value


class Evolution(object):
    def __init__(self, program: Iterator[str], max_generations: int = 10000, initial_population_size: int = 50):
        self.program = program
        self.max_generations = max_generations
        self.initial_population_size = initial_population_size
        self.better = None
        self.worse_index = None

        chromosomes = set()
        while len(chromosomes) < self.initial_population_size:
            chromosomes.add(random_monad_input())
        self.chromosomes = list(chromosomes)
        self.chromosome_values = []
        self.evaluate()

    def start(self) -> int:
        generation = 0
        while generation < self.max_generations:
            if generation % 100 == 0:
                print("Generation {}, better chromosome {}, better value {}, unique values {}".format(generation, self.better, self.evaluate_chromosome(self.better), len(set(self.chromosomes))))
                print("Zeros {}".format([c for (v, c) in zip(self.chromosome_values, self.chromosomes) if v[0] == 0]))
            self.reproduce()
            self.mutate()
            self.chromosomes.sort(key=lambda c: self.evaluate_chromosome(c))
            self.chromosomes = self.chromosomes[:len(self.chromosomes) // 2]
            self.evaluate()
            generation += 1
        return self.better

    def reproduce(self):
        new_chromosomes = set(self.chromosomes)
        weights = [100 - r[0] if r[0] < 99 else 1 for r in self.chromosome_values]
        sum_weights = sum(weights)
        ps = [w / sum_weights for w in weights]
        while len(new_chromosomes) < len(self.chromosomes) * 2:
            parent1, parent2 = numpy.random.choice(self.chromosomes, 2, replace=False, p=ps)
            new_chromosomes = new_chromosomes.union(set(Evolution.reproduce_chromosomes(parent1, parent2)))
        self.chromosomes = list(new_chromosomes)

    def mutate(self):
        # 4% chance of mutation. Chosen arbitrarily.
        mutate_indexes = random.sample(range(len(self.chromosomes)), len(self.chromosomes) // 25)
        for index in mutate_indexes:
            if self.chromosomes[index] == self.better or self.evaluate_chromosome(self.chromosomes[index])[0] == 0:
                self.chromosomes.append(self.chromosomes[index])
            self.chromosomes[index] = Evolution.mutate_chromosome(self.chromosomes[index])

    def evaluate(self):
        better_value = None
        worse_value = None
        self.better = None
        self.worse_index = None
        self.chromosome_values = []
        for (i, chromosome) in enumerate(self.chromosomes):
            v = self.evaluate_chromosome(chromosome)
            self.chromosome_values.append(v)
            if better_value is None or v < better_value:
                better_value = v
                self.better = chromosome
            if worse_value is None or v > worse_value:
                worse_value = v
                self.worse_index = i

    def evaluate_chromosome(self, chromosome: str) -> (int, int):
        (_, _, _, z) = run_monad_program(chromosome, self.program)
        return abs(z), -int(chromosome)

    @staticmethod
    def mutate_chromosome(chromosome: str) -> str:
        new_chromosome = list(chromosome)
        for _ in range(random.randint(1, 4)):
            index = random.randint(0, len(new_chromosome) - 1)
            # we want to bias for increasing the current number
            digit = random.randint(int(new_chromosome[index]), 9)
            new_chromosome[index] = str(digit)
        return ''.join(new_chromosome)

    @staticmethod
    def reproduce_chromosomes(chromosome1: str, chromosome2: str) -> Tuple[str, str]:
        limit = random.randrange(len(chromosome1))
        return chromosome1[:limit] + chromosome2[limit:], chromosome2[:limit] + chromosome1[limit:]


def random_monad_input() -> str:
    monad_input = []
    for _ in range(14):
        digit = random.randint(1, 9)
        monad_input.append(str(digit))
    return ''.join(monad_input)


monad_cache = {}


def run_monad_program(monad_input: str, program: Iterator[str]) -> (int, int, int, int):
    if monad_input in monad_cache:
        return monad_cache[monad_input]
    alu = ALU(monad_input)
    for line in program:
        alu.execute(line.strip())
    monad_cache[monad_input] = (alu.w, alu.x, alu.y, alu.z)
    return alu.w, alu.x, alu.y, alu.z


def test_both_monad_programs(program1: Iterator[str], program2: Iterator[str], monad_input: str):
    expected = run_monad_program(monad_input, program1)
    got = run_monad_program(monad_input, program2)
    print("TESTING {}. GOT {}, EXPECTED {}".format(monad_input, expected, got))
    assert expected == got


def run_random_tests():
    inputs = set()
    while len(inputs) < 1000:
        inputs.add(random_monad_input())
    with open("./inputs/problem45monad.txt") as f:
        control = list(f.readlines())
    with open("./inputs/problem45monadsimplified.txt") as f:
        test = list(f.readlines())
    for monad_input in inputs:
        test_both_monad_programs(control, test, monad_input)


def find_zeros():
    inputs = set()
    while len(inputs) < 20000000:
        inputs.add(random_monad_input())
    with open("./inputs/problem45monadsimplified.txt") as f:
        program = list(f.readlines())
    for monad_input in inputs:
        (_, _, _, z) = run_monad_program(monad_input, program)
        if z == 0:
            print("Found valid monad input: {}".format(monad_input))


def brute_force() -> str:
    with open("./inputs/problem45monadsimplified.txt") as f:
        program = list(f.readlines())
    c = 91297295
    biggest_zero = 91297295
    i = 0
    while c < 99999999:
        if i % 10000 == 0:
            print("On {}".format(c))
        (_, _, _, z) = run_monad_program(str(c) + "919993", program)
        if z == 0:
            print("ZERO FOUND: {}919993".format(c))
            biggest_zero = c
        c += 1
        i += 1
    return str(biggest_zero) + "919993"


def solve():
    if sys.argv[1] == "tests":
        run_random_tests()
    elif sys.argv[1] == "find-zeros":
        find_zeros()
    elif sys.argv[1] == "evolution":
        with open("./inputs/problem45monadsimplified.txt") as f:
            program = list(f.readlines())
        e = Evolution(program, initial_population_size=400, max_generations=20000)
        return e.start()
    elif sys.argv[1] == "bruteforce":
        return brute_force()
    elif sys.argv[1] == "run":
        return run_monad_program(sys.argv[2], "/dev/stdin")


if __name__ == '__main__':
    print(solve())
