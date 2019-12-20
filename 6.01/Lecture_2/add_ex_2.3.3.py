from state_machine import SM


class CountingStateMachine(SM):
    startState = 0

    def getNextValues(self, state, inp):
        output = self.getOutput(state, inp)
        return state + 1, output


class AlternateZeros(CountingStateMachine):
    def getOutput(self, state, inp):
        return inp if state % 2 == 0 else 0
