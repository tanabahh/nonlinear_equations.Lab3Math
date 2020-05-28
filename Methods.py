MaxIT = 1000000


class NewtonMethod:
    def __init__(self, a, b, accuracy, function, derived_function, second_derived_function):
        self.a = a
        self.b = b
        self.accuracy = accuracy
        self.function = function
        self.derived_function = derived_function
        self.second_derived_function = second_derived_function
        self.result = False
        self.iteration = 0

    def is_convergence(self):
        a = self.a
        previous = self.derived_function(a)
        while a < self.b:
            if self.derived_function(a)*previous < 0:
                return False
            previous = self.derived_function(a)
            a += (self.b-self.a)/10000
        return self.function(self.a)*self.function(self.b) < 0

    def first_approach(self):
        a = self.a
        while a < self.b:
            if self.derived_function(a)*self.second_derived_function(a) > 0:
                return a
            a += (self.b - self.a) / 10000
        return a

    def second_approach(self, first_x):
        return first_x - self.function(first_x)/self.derived_function(first_x)

    def find_answer(self):
        if self.is_convergence():
            first_x = self.first_approach()
            second_x = self.second_approach(first_x)
            self.iteration += 1
            while abs(first_x - second_x) > self.accuracy:
                self.iteration += 1
                first_x = second_x
                second_x = self.second_approach(first_x)
            self.result = second_x


class SimpleIteration:
    def __init__(self, a, b, accuracy, function, derived_function):
        if a > b:
            s = a
            a = b
            b = s
        self.a = a
        self.b = b
        self.accuracy = accuracy
        self.function = function
        self.derived_function = derived_function
        self.result = False
        maximum = max(self.derived_function(self.a), self.derived_function(self.b), self.derived_function(0))
        minimum = min(self.derived_function(self.a), self.derived_function(self.b), self.derived_function(0))
        if maximum + minimum == 0:
            maximum += 1
        self.const = 2 / (maximum + minimum)
        self.iteration = 0

    def is_convergence(self):
        return (self.function(self.a)*self.function(self.b) < 0) and (abs(self.a - self.b) < 0.2)

    def first_approach(self):
        return self.a

    def second_approach(self, first_x):
        print(first_x)
        return first_x - self.const*self.function(first_x)

    def find_answer(self):
        if self.is_convergence():
            first_x = self.first_approach()
            second_x = self.second_approach(first_x)
            self.iteration += 1
            while (abs(first_x - second_x) > self.accuracy) and (self.iteration <= 10000):
                first_x = second_x
                second_x = self.second_approach(first_x)
                self.iteration += 1
            self.result = second_x


class SimpleIterationForSystems:
    def __init__(self, x, y, accuracy, function, function_y, derived_x, derived_y):
        self.accuracy = accuracy
        self.function = function
        self.function_y = function_y
        self.derived_x = derived_x
        self.derived_y = derived_y
        self.result = [x, y]  # x, y
        self.iteration = 0

    def is_convergence(self):
        try:
            return abs(self.derived_x(self.result[0])) + abs(self.derived_y(self.result[1])) < 1
        except:
            return False

    def next_approach(self):
        if type(self.function(self.result[0])) != bool:
            return [self.function_y(self.result[1]), self.function(self.result[0])]
        else:
            self.iteration = MaxIT
            return self.result

    def get_answer(self):
        self.iteration = 1
        try:
            next_it = self.next_approach()
            if not self.is_convergence():
                return False
            while(self.iteration < MaxIT) and \
                    (max(abs(self.result[0] - next_it[0]), abs(self.result[1] - next_it[1])) > self.accuracy):
                print(self.is_convergence())
                self.result[0] = next_it[0]
                self.result[1] = next_it[1]
                next_it = self.next_approach()
                self.iteration += 1
            if self.iteration >= MaxIT:
                return self.iteration
            else:
                return self.result
        except:
            return False
