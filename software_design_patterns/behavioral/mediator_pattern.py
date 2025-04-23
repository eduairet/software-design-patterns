class Event(list):
    def __call__(self, *args, **kwargs):
        for item in self:
            item(*args, **kwargs)


class Ring:
    def __init__(self):
        self.events = Event()

    def fire(self, args):
        self.events(args)


class Knockout:
    def __init__(self, who_knocked_out, who_knocked_out_by, round):
        self.who_knocked_out = who_knocked_out
        self.who_knocked_out_by = who_knocked_out_by
        self.round = round


class Boxer:
    def __init__(self, name, ring):
        self.name = name
        self.ring = ring
        self.knockouts = 0

    def KnockOut(self, opponent):
        self.knockouts += 1
        args = Knockout(self, opponent, 1)
        self.ring.fire(args)
        return args


class Referee:
    def __init__(self, ring):
        self.ring = ring
        self.ring.events.append(self)

    def __call__(self, args):
        return f"Referee: {args.who_knocked_out_by.name} was knocked out by {args.who_knocked_out.name} in round {args.round}"
