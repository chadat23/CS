from state_machine import SM


class Vending(SM):
    startState = 0

    def getNextValues(self, state, input):
        if input == 'quarter':
            state += 1
            return state, (0, False)
        elif input == 'cancel':
            return 0, (state * 25, False)
        else:
            if state > 2:
                return 0, ((state - 3) * 25, True)
            return 0, (0, False)


print(Vending().transduce(['dispense', 'quarter',
                           'quarter', 'quarter',
                           'quarter', 'dispense',
                           'quarter', 'cancel',
                           'dispense']))
