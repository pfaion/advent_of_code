# Day 2
## Part 1

<details><summary>Exercise Text (click to expand)</summary>
<article class="day-desc">
  <h2>--- Day 2: Rock Paper Scissors ---</h2>
  <p>
    The Elves begin to set up camp on the beach. To decide whose tent gets to be
    closest to the snack storage, a giant
    <a href="https://en.wikipedia.org/wiki/Rock_paper_scissors" target="_blank"
      >Rock Paper Scissors</a
    >
    tournament is already in progress.
  </p>
  <p>
    Rock Paper Scissors is a game between two players. Each game contains many
    rounds; in each round, the players each simultaneously choose one of Rock,
    Paper, or Scissors using a hand shape. Then, a winner for that round is
    selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats
    Rock. If both players choose the same shape, the round instead ends in a
    draw.
  </p>
  <p>
    Appreciative of your help yesterday, one Elf gives you an
    <em>encrypted strategy guide</em> (your puzzle input) that they say will be
    sure to help you win. "The first column is what your opponent is going to
    play: <code>A</code> for Rock, <code>B</code> for Paper, and
    <code>C</code> for Scissors. The second column--" Suddenly, the Elf is
    called away to help with someone's tent.
  </p>
  <p>
    The second column,
    <span title="Why do you keep guessing?!">you reason</span>, must be what you
    should play in response: <code>X</code> for Rock, <code>Y</code> for Paper,
    and <code>Z</code> for Scissors. Winning every time would be suspicious, so
    the responses must have been carefully chosen.
  </p>
  <p>
    The winner of the whole tournament is the player with the highest score.
    Your <em>total score</em> is the sum of your scores for each round. The
    score for a single round is the score for the <em>shape you selected</em> (1
    for Rock, 2 for Paper, and 3 for Scissors) plus the score for the
    <em>outcome of the round</em> (0 if you lost, 3 if the round was a draw, and
    6 if you won).
  </p>
  <p>
    Since you can't be sure if the Elf is trying to help you or trick you, you
    should calculate the score you would get if you were to follow the strategy
    guide.
  </p>
  <p>For example, suppose you were given the following strategy guide:</p>
  
<pre><code>A Y
    B X
    C Z
    </code></pre>
  <p>This strategy guide predicts and recommends the following:</p>
  <ul>
    <li>
      In the first round, your opponent will choose Rock (<code>A</code>), and
      you should choose Paper (<code>Y</code>). This ends in a win for you with
      a score of <em>8</em> (2 because you chose Paper + 6 because you won).
    </li>
    <li>
      In the second round, your opponent will choose Paper (<code>B</code>), and
      you should choose Rock (<code>X</code>). This ends in a loss for you with
      a score of <em>1</em> (1 + 0).
    </li>
    <li>
      The third round is a draw with both players choosing Scissors, giving you
      a score of 3 + 3 = <em>6</em>.
    </li>
  </ul>
  <p>
    In this example, if you were to follow the strategy guide, you would get a
    total score of <code><em>15</em></code> (8 + 1 + 6).
  </p>
  <p>
    <em
      >What would your total score be if everything goes exactly according to
      your strategy guide?</em
    >
  </p>
</article>

</details>

### Overview
| Variant | Runtime | Size |
| --- | --- | --- |
|1|0.04s|607|
|2|0.037s|442|
|3|0.026s|250|

### Variant 1
```python
from itertools import starmap
from pathlib import Path

here = Path(__file__).parent

data = [line.split(" ") for line in (here / "input.txt").read_text().splitlines()]


def score(opponent_move: str, own_move: str) -> int:
    game_score = {
        ("A", "Z"): 0,
        ("B", "X"): 0,
        ("C", "Y"): 0,
        ("A", "X"): 3,
        ("B", "Y"): 3,
        ("C", "Z"): 3,
        ("A", "Y"): 6,
        ("B", "Z"): 6,
        ("C", "X"): 6,
    }[(opponent_move, own_move)]

    move_value = {"X": 1, "Y": 2, "Z": 3}[own_move]

    return game_score + move_value


print(sum(starmap(score, data)))

```
Runtime: 0.04s, Size: 607, Output:
```
12772
```
### Variant 2
```python
from itertools import starmap
from pathlib import Path

here = Path(__file__).parent

data = [line.split(" ") for line in (here / "input.txt").read_text().splitlines()]


def score(opponent_move: str, own_move: str) -> int:
    # computing the result based on the ascii values of the characters
    a = ord(opponent_move) - ord("A")
    b = ord(own_move) - ord("X")
    return ((b - a + 4) % 3) * 3 + b + 1


print(sum(starmap(score, data)))

```
Runtime: 0.037s, Size: 442, Output:
```
12772
```
### Variant 3
```python
from pathlib import Path

data = (Path(__file__).parent / "input.txt").read_text().splitlines()

print(
    sum(
        1
        + (b := ord((p := l.split(" "))[1]) - 88)
        + 3 * ((b + 4 - (ord(p[0]) - 65)) % 3)
        for l in data
    )
)

```
Runtime: 0.026s, Size: 250, Output:
```
12772
```
## Part 2

<details><summary>Exercise Text (click to expand)</summary>
<article class="day-desc">
  <h2 id="part2">--- Part Two ---</h2>
  <p>
    The Elf finishes helping with the tent and sneaks back over to you. "Anyway,
    the second column says how the round needs to end: <code>X</code> means you
    need to lose, <code>Y</code> means you need to end the round in a draw, and
    <code>Z</code> means you need to win. Good luck!"
  </p>
  <p>
    The total score is still calculated in the same way, but now you need to
    figure out what shape to choose so the round ends as indicated. The example
    above now goes like this:
  </p>
  <ul>
    <li>
      In the first round, your opponent will choose Rock (<code>A</code>), and
      you need the round to end in a draw (<code>Y</code>), so you also choose
      Rock. This gives you a score of 1 + 3 = <em>4</em>.
    </li>
    <li>
      In the second round, your opponent will choose Paper (<code>B</code>), and
      you choose Rock so you lose (<code>X</code>) with a score of 1 + 0 =
      <em>1</em>.
    </li>
    <li>
      In the third round, you will defeat your opponent's Scissors with Rock for
      a score of 1 + 6 = <em>7</em>.
    </li>
  </ul>
  <p>
    Now that you're correctly decrypting the ultra top secret strategy guide,
    you would get a total score of <code><em>12</em></code
    >.
  </p>
  <p>
    Following the Elf's instructions for the second column,
    <em
      >what would your total score be if everything goes exactly according to
      your strategy guide?</em
    >
  </p>
</article>

</details>

```python
from itertools import starmap
from pathlib import Path

here = Path(__file__).parent

data = [line.split(" ") for line in (here / "input.txt").read_text().splitlines()]


def score(opponent_move: str, outcome: str) -> int:
    own_move = {
        ("A", "X"): "C",
        ("A", "Y"): "A",
        ("A", "Z"): "B",
        ("B", "X"): "A",
        ("B", "Y"): "B",
        ("B", "Z"): "C",
        ("C", "X"): "B",
        ("C", "Y"): "C",
        ("C", "Z"): "A",
    }[(opponent_move, outcome)]

    game_score = {"X": 0, "Y": 3, "Z": 6}[outcome]
    move_value = {"A": 1, "B": 2, "C": 3}[own_move]

    return game_score + move_value


print(sum(starmap(score, data)))

```
Runtime: 0.028s, Size: 672, Output:
```
11618
```