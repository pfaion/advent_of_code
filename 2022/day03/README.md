# Day 3
## Part 1

<details><summary>Exercise Text (click to expand)</summary>
<article class="day-desc">
  <h2>--- Day 3: Rucksack Reorganization ---</h2>
  <p>
    One Elf has the important job of loading all of the
    <a href="https://en.wikipedia.org/wiki/Rucksack" target="_blank"
      >rucksacks</a
    >
    with supplies for the
    <span title="Where there's jungle, there's hijinxs.">jungle</span> journey.
    Unfortunately, that Elf didn't quite follow the packing instructions, and so
    a few items now need to be rearranged.
  </p>
  <p>
    Each rucksack has two large <em>compartments</em>. All items of a given type
    are meant to go into exactly one of the two compartments. The Elf that did
    the packing failed to follow this rule for exactly one item type per
    rucksack.
  </p>
  <p>
    The Elves have made a list of all of the items currently in each rucksack
    (your puzzle input), but they need your help finding the errors. Every item
    type is identified by a single lowercase or uppercase letter (that is,
    <code>a</code> and <code>A</code> refer to different types of items).
  </p>
  <p>
    The list of items for each rucksack is given as characters all on a single
    line. A given rucksack always has the same number of items in each of its
    two compartments, so the first half of the characters represent items in the
    first compartment, while the second half of the characters represent items
    in the second compartment.
  </p>
  <p>
    For example, suppose you have the following list of contents from six
    rucksacks:
  </p>
  
<pre><code>vJrwpWtwJgWrhcsFMMfFFhFp
    jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
    PmmdzqPrVvPwwTWBwg
    wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
    ttgJtRGJQctTZtZT
    CrZsJsPPZsGzwwsLwLmpwMDw
    </code></pre>
  <ul>
    <li>
      The first rucksack contains the items
      <code>vJrwpWtwJgWrhcsFMMfFFhFp</code>, which means its first compartment
      contains the items <code>vJrwpWtwJgWr</code>, while the second compartment
      contains the items <code>hcsFMMfFFhFp</code>. The only item type that
      appears in both compartments is lowercase <code><em>p</em></code
      >.
    </li>
    <li>
      The second rucksack's compartments contain
      <code>jqHRNqRjqzjGDLGL</code> and <code>rsFMfFZSrLrFZsSL</code>. The only
      item type that appears in both compartments is uppercase
      <code><em>L</em></code
      >.
    </li>
    <li>
      The third rucksack's compartments contain <code>PmmdzqPrV</code> and
      <code>vPwwTWBwg</code>; the only common item type is uppercase
      <code><em>P</em></code
      >.
    </li>
    <li>
      The fourth rucksack's compartments only share item type
      <code><em>v</em></code
      >.
    </li>
    <li>
      The fifth rucksack's compartments only share item type
      <code><em>t</em></code
      >.
    </li>
    <li>
      The sixth rucksack's compartments only share item type
      <code><em>s</em></code
      >.
    </li>
  </ul>
  <p>
    To help prioritize item rearrangement, every item type can be converted to a
    <em>priority</em>:
  </p>
  <ul>
    <li>
      Lowercase item types <code>a</code> through <code>z</code> have priorities
      1 through 26.
    </li>
    <li>
      Uppercase item types <code>A</code> through <code>Z</code> have priorities
      27 through 52.
    </li>
  </ul>
  <p>
    In the above example, the priority of the item type that appears in both
    compartments of each rucksack is 16 (<code>p</code>), 38 (<code>L</code>),
    42 (<code>P</code>), 22 (<code>v</code>), 20 (<code>t</code>), and 19
    (<code>s</code>); the sum of these is <code><em>157</em></code
    >.
  </p>
  <p>
    Find the item type that appears in both compartments of each rucksack.
    <em>What is the sum of the priorities of those item types?</em>
  </p>
</article>

</details>

```python
from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().splitlines()


def find_wrong_item(items: str) -> str:
    mid = len(items) // 2
    first_compartment = items[:mid]
    second_compartment = items[mid:]
    overlapping_items = set(first_compartment) & set(second_compartment)
    return next(iter(overlapping_items))


def item_priority(item: str) -> int:
    code = ord(item)
    # capitals come before lowercase in ascii codes
    if code <= ord("Z"):
        return code - ord("A") + 27
    else:
        return code - ord("a") + 1


print(sum(item_priority(find_wrong_item(items)) for items in data))

```
Runtime: 0.035s, Size: 639, Output:
```
7908
```
## Part 2

<details><summary>Exercise Text (click to expand)</summary>
<article class="day-desc">
  <h2 id="part2">--- Part Two ---</h2>
  <p>
    As you finish identifying the misplaced items, the Elves come to you with
    another issue.
  </p>
  <p>
    For safety, the Elves are divided into groups of three. Every Elf carries a
    badge that identifies their group. For efficiency, within each group of
    three Elves, the badge is the
    <em>only item type carried by all three Elves</em>. That is, if a group's
    badge is item type <code>B</code>, then all three Elves will have item type
    <code>B</code> somewhere in their rucksack, and at most two of the Elves
    will be carrying any other item type.
  </p>
  <p>
    The problem is that someone forgot to put this year's updated authenticity
    sticker on the badges. All of the badges need to be pulled out of the
    rucksacks so the new authenticity stickers can be attached.
  </p>
  <p>
    Additionally, nobody wrote down which item type corresponds to each group's
    badges. The only way to tell which item type is the right one is by finding
    the one item type that is <em>common between all three Elves</em> in each
    group.
  </p>
  <p>
    Every set of three lines in your list corresponds to a single group, but
    each group can have a different badge item type. So, in the above example,
    the first group's rucksacks are the first three lines:
  </p>
  
<pre><code>vJrwpWtwJgWrhcsFMMfFFhFp
    jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
    PmmdzqPrVvPwwTWBwg
    </code></pre>
  <p>And the second group's rucksacks are the next three lines:</p>
  
<pre><code>wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
    ttgJtRGJQctTZtZT
    CrZsJsPPZsGzwwsLwLmpwMDw
    </code></pre>
  <p>
    In the first group, the only item type that appears in all three rucksacks
    is lowercase <code>r</code>; this must be their badges. In the second group,
    their badge item type must be <code>Z</code>.
  </p>
  <p>
    Priorities for these items must still be found to organize the sticker
    attachment efforts: here, they are 18 (<code>r</code>) for the first group
    and 52 (<code>Z</code>) for the second group. The sum of these is
    <code><em>70</em></code
    >.
  </p>
  <p>
    Find the item type that corresponds to the badges of each three-Elf group.
    <em>What is the sum of the priorities of those item types?</em>
  </p>
</article>

</details>

```python
import re
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text()

batches = [
    match[0] for match in re.finditer(r"\w+\n\w+\n\w+(\n|$)", data_raw, re.MULTILINE)
]


def find_badge(batch: str) -> str:
    elf_items = batch.splitlines()
    overlap = set.intersection(*(set(items) for items in elf_items))
    return next(iter(overlap))


def item_priority(item: str) -> int:
    code = ord(item)
    # capitals come before lowercase in ascii codes
    if code <= ord("Z"):
        return code - ord("A") + 27
    else:
        return code - ord("a") + 1


print(sum(item_priority(find_badge(batch)) for batch in batches))

```
Runtime: 0.041s, Size: 656, Output:
```
2838
```