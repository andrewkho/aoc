import fire
from typing import *
import re
from collections import deque
from dataclasses import dataclass, field


def _part_one(data):
    ancestors: Set[str] = set()
    q = deque()

    q.append(data["shiny gold"])

    while len(q) > 0:
        rule = q.popleft()
        for parent in rule.parents:
            parent_rule = data[parent]
            if parent not in ancestors:
                ancestors.add(parent)
                q.append(parent_rule)

    print(ancestors)
    
    return len(ancestors)


def _part_two(data):

    def process_node(bag_name: str) -> int:
        node = data[bag_name]
        
        if len(node.children) == 0:
            return 1

        return 1 + sum(
            n * process_node(child)
            for child, n in node.children.items()
        )

    return process_node("shiny gold") - 1


@dataclass
class Rule:
    bag: str
    children: Dict[str, int]
    parents: Set[str] = field(default_factory=set)

_subrule = re.compile(r"^([0-9]*) (.*) bag*")

def _rule_from_line(line: str) -> Rule:
    print(line)
    l, r = line.split('bags contain')
    bag = l.strip()

    contains = [_.strip() for _ in r.split(',')]

    children = dict()

    for contain in contains:
        try:
            match = _subrule.match(contain)

            n = int(match.group(1))
            subbag = match.group(2)

            children[subbag] = n
        except AttributeError:
            pass

    return Rule(bag, children)


def _process_rules(rules: Dict[str, Rule]):
    for bag, rule in rules.items():
        for child in rule.children:
            rules[child].parents.add(bag)


def run(fname: str, part: int):
    with open(fname, 'r') as f:
        lines = f.readlines()

    print(lines)
    data = {}
    for line in lines:
        rule = _rule_from_line(line)
        data[rule.bag] = rule


    print(f"data: {len(data)} lines: {len(lines)}")

    _process_rules(data)
    print(data)

    if part == 1:
        print('sum ' + str(_part_one(data)))
    elif part == 2:
        print('sum part 2 ' + str(_part_two(data)))
    else:
        print(f"Missing part: {part}")


if __name__ == '__main__':
    fire.Fire(run)

