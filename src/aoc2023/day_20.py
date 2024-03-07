from collections import deque
from enum import IntEnum
from pathlib import Path
from typing import NamedTuple, Protocol


def main():
    input_path = Path("input/input_20.txt")
    print(solve_part_one(input_path))
    print(solve_part_two(input_path))


class FlipFlopState(IntEnum):
    OFF = 0
    ON = 1


class Pulse(IntEnum):
    LOW = 0
    HIGH = 1


class PulseMessage(NamedTuple):
    sender: str
    pulse: Pulse
    receiver: str


class Module(Protocol):
    def receive(self, pulse: Pulse, sender: str):
        ...

    def connect_input(self, other: str):
        ...

    def connect_output(self, other: str):
        ...


class FlipFlop:
    def __init__(self, name: str, state: FlipFlopState = FlipFlopState.OFF):
        self._name = name
        self._state = state
        self._outputs = []
        self._inputs = []

    @property
    def state(self):
        return self._state

    def receive(self, signal: Pulse, sender: str):
        if signal == Pulse.LOW:
            self._state = (self._state + 1) % 2
            return [
                PulseMessage(self._name, Pulse(self._state), output)
                for output in self._outputs
            ]
        return []

    def connect_output(self, other: str):
        self._outputs.append(other)

    def connect_input(self, other: str):
        self._inputs.append(other)

    @property
    def outputs(self):
        return self._outputs


class Conjunction:
    def __init__(self, name: str):
        self._name = name
        self._memory = {}
        self._inputs = []
        self._outputs = []

    def connect_input(self, other: str):
        self._memory[other] = Pulse.LOW
        self._inputs.append(other)

    def connect_output(self, other: str):
        self._outputs.append(other)

    def receive(self, pulse: Pulse, sender: str):
        self._memory[sender] = pulse
        if all(module_pulse == Pulse.HIGH for module_pulse in self._memory.values()):
            pulse_to_emit = Pulse.LOW
        else:
            pulse_to_emit = Pulse.HIGH
        return [
            PulseMessage(self._name, pulse_to_emit, output) for output in self._outputs
        ]

    @property
    def outputs(self):
        return self._outputs


class Broadcast:
    def __init__(self, name: str):
        self._name = name
        self._inputs = []
        self._outputs = []

    def connect_input(self, other: str):
        self._inputs.append(other)

    def connect_output(self, other: str):
        self._outputs.append(other)

    def receive(self, pulse: Pulse, sender: str):
        return [PulseMessage(self._name, pulse, module) for module in self._outputs]

    @property
    def outputs(self):
        return self._outputs


class Button:
    def __init__(self, name: str):
        self._name = name
        self._input = None
        self._output = None

    def connect_output(self, other: str):
        self._output = other

    def push(self):
        return [PulseMessage(self._name, Pulse.LOW, self._output)]

    @property
    def outputs(self):
        return [self._output]


class Dispatcher:
    def __init__(self, modules):
        self._queue = PulseQueue()
        self._modules = modules

    def push_button(self):
        self._queue.put(self._modules["button"].push())
        while self._queue:
            input_pulse = self._queue.next()
            if input_pulse.receiver not in self._modules:
                continue
            output_pulses = self._modules[input_pulse.receiver].receive(
                input_pulse.pulse, input_pulse.sender
            )
            self._queue.put(output_pulses)
        return self._queue.total()


class PulseQueue(deque):
    def __init__(self):
        super().__init__()
        self._high_pulses = 0
        self._low_pulses = 0

    def put(self, pulses: list[PulseMessage]):
        for pulse in pulses:
            super().append(pulse)
            if pulse.pulse == Pulse.LOW:
                self._low_pulses += 1
            elif pulse.pulse == Pulse.HIGH:
                self._high_pulses += 1
            else:
                raise ValueError

    def next(self) -> PulseMessage:
        return super().popleft()

    def total(self):
        return self._low_pulses, self._high_pulses


def solve_part_one(input_path: Path):
    modules = parse_input(input_path)
    dispatcher = Dispatcher(modules)
    for _ in range(1000):
        low_pulses, high_pulses = dispatcher.push_button()
    return low_pulses * high_pulses


def solve_part_two(input_path: Path):
    ...


def parse_input(input_path: Path):
    modules = {}
    conjunctions = []
    for row in input_path.read_text().splitlines():
        raw_module, raw_destinations = row.split(" -> ")
        if raw_module == "broadcaster":
            module = Broadcast(raw_module)
            for destination in raw_destinations.split(", "):
                module.connect_output(destination)
            modules[raw_module] = module
        elif raw_module[0] == "%":
            name = raw_module[1:]
            module = FlipFlop(name)
            for destination in raw_destinations.split(", "):
                module.connect_output(destination)
            modules[name] = module
        elif raw_module[0] == "&":
            name = raw_module[1:]
            module = Conjunction(name)
            for destination in raw_destinations.split(", "):
                module.connect_output(destination)
            modules[name] = module
            conjunctions.append(name)

    for conjunction in conjunctions:
        for name, module in modules.items():
            if conjunction in module.outputs:
                modules[conjunction].connect_input(name)

    button = Button("button")
    button.connect_output("broadcaster")
    modules["button"] = button

    return modules


if __name__ == "__main__":
    main()
