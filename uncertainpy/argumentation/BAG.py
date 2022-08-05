import os
import re
import string
from .Argument import Argument
from .Support import Support
from .Attack import Attack


class BAG:
    arguments = {}
    attacks = []
    supports = []

    def __init__(self, content=None, is_path=False):
        self.content = content
        self.is_path = is_path
        self.arguments.clear()

        if (content is None):
            pass
        else:
            BAG_lines = []

            if (is_path):
                with open(os.path.abspath(content), "r") as f:
                    content = f.read()

            content = content.replace("\n", "")  # Convert to one line
            BAG_lines = content.split(";")  # Split at semi colons
            BAG_lines = list(filter(None, BAG_lines))  # Removes empty strings

            for line in BAG_lines:
                k_name = line.split("(")[0]
                k_args = re.findall(rf"{k_name}\((.*?)\)", line)[0].replace(" ", "").split(",")
                if k_name == "arg":
                    argument = Argument(k_args[0], float(k_args[1]), None, [], [])
                    self.arguments[argument.name] = argument

                elif k_name == "att":
                    attacker = self.arguments[k_args[0]]
                    attacked = self.arguments[k_args[1]]
                    self.add_attack(attacker, attacked)

                elif k_name == "sup":
                    supporter = self.arguments[k_args[0]]
                    supported = self.arguments[k_args[1]]
                    self.add_support(supporter, supported)

    def add_attack(self, attacker, attacked):
        if type(attacker) != Argument:
            raise TypeError("attacker must be of type Argument")

        if type(attacked) != Argument:
            raise TypeError("attacked must be of type Argument")

        self.arguments[attacker.name] = attacker
        self.arguments[attacked.name] = attacked
        attacked.add_attacker(attacker)

        self.attacks.append(Attack(attacker, attacked))

    def add_support(self, supporter, supported):
        if type(supporter) != Argument:
            raise TypeError("supporter must be of type Argument")

        if type(supported) != Argument:
            raise TypeError("supported must be of type Argument")

        self.arguments[supporter.name] = supporter
        self.arguments[supported.name] = supported
        supported.add_supporter(supporter)

        self.supports.append(Support(supporter, supported))

    def reset_strength_values(self):
        for a in list(self.arguments.values()):
            a.strength = a.initial_weight

    def get_arguments(self):
        return list(self.arguments.values())

    def __str__(self) -> str:
        return f"BAG set to read from {self.path} with arguments: {self.arguments}, attacks: {self.attacks} and supports: {self.supports}"

    def __repr__(self) -> str:
        return f"BAG({self.path}) Arguments: {self.arguments} Attacks: {self.attacks} Supports: {self.supports}"
