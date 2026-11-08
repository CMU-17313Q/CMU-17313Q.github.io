# Recitation 9: Property-Based Testing

In this recitation, you will write property-based tests using [fast-check](https://fast-check.dev/), run them, and measure how good they are. Your TA will give a brief overview of property-based testing using fast-check. After that, you will fork a repository and write property-based tests for a `mergeIntervals` function, which is a function that merges a list of intervals into the smallest equivalent list of disjoint intervals.

To recieve credit for this recitation, compelete this [Gradescope assignment](https://www.gradescope.com/courses/1360202/assignments/9023116)

## Setup

For this activity, create a fork of [this repository](https://github.com/CMU-17313Q/F26-reci-8) and clone it to your local machine.

You need Node.js 20, 22, or 24+ (`node --version`).

```bash
git clone <your repo URL>
cd <repo>
npm install
npm test # one intervals test fails. That's on purpose.
```

## Commands

| **Command**                  | **What it does**                                                |
| :--------------------------- | :-------------------------------------------------------------- |
| `npm run test:intervals`     | Run your interval properties against the real `mergeIntervals`  |
| `npm run mutants:intervals`  | Run your interval properties against the planted bugs           |

## How you'll know your properties are any good

A property that passes tells you very little on its own. A property that checks nothing passes too. So every function here comes with mutants: copies of the code with a realistic bug planted in them. A good set of properties

- **passes** on the real implementation (no false alarms), and

- **fails** on every mutant ("kills" it).


After every new property, run `test:` first, then `mutants:`

The mutants runner runs everything 5 times with fresh random seeds. For each mutant it says which property killed it and shows the counterexample:

```bash
 ✔ allBlack       killed  by: guessing the secret gives all greens
    Counterexample: ["AAAAA"]
    AssertionError: expected [ 'B', 'B', 'B', 'B', 'B' ] to deeply equal [ 'G', 'G', 'G', 'G', 'G' ]
```

A mutant killed in only some runs is **flaky**. That means your generator only sometimes produces an input that exposes the bug, so improve the generator.

Rules of the game:

* Import only from `../src/<subject>` (for example `../src/wordle`). The runner rejects tests that import the implementation file directly, because then the mutants could never be swapped in.

* Write properties from the specification (the doc comment at the top of each implementation file), not by reading `mutants.ts`. After the deadline you'll get more mutants to try your properties against.

* Label every property with its pattern, on the line above its `it(: // Pattern: invariant. The output is sorted`.

## Merging intervals

Read the specification at the top of `src/intervals/mergeIntervals.ts` **carefully**. Several mutants are about one sentence of it.

`test/intervals.test.ts` has one property and a first-draft generator to start from.

**Checkpoint 1: make the starter honest.** Run `npm run test:intervals`. The test fails on the correct implementation. Read the counterexample: what's wrong, the property or the generator? Fix it by **constructing** valid inputs, not by filtering (.filter or fc.pre).

**Checkpoint 2: one property per pattern.** For each pattern, write one property in English first, then in code:

| **Pattern**    | **Question to ask about `mergeIntervals`**                                                                  |
| :------------- | :---------------------------------------------------------------------------------------------------------- |
| Invariant      | What must *always* be true of the output's shape?                                                           |
| Differential   | Can you write a tiny, obviously correct check of "is point *p* covered?" and compare input with output?     |
| Metamorphic    | What change to the input should *not* change the output?                                                    |
| Algebraic      | What happens if you merge something that's already merged?                                                  |
| Conditional    | If the input intervals already don't overlap or touch, what should the output be? (Generate such inputs directly.) |


After each property, run `npm run test:intervals`, then `npm run mutants:intervals`, and note which mutants it kills.

**Checkpoint 3: hunt the survivors** For each surviving mutant, decide whether you are missing a **property** (the bug is never checked) or a **generator** (the bug is checked, but the inputs never reach it). For the second, ask: could your generator even produce an input that triggers this bug, like two intervals sharing an endpoint exactly? How often?


After making the appropriate edits, commit your code to the `main` branch of your forked repository and link your commit or repo in your [Gradescope submission](https://www.gradescope.com/courses/1360202/assignments/9023116).


## fast-check cheat sheet

```typescript
import fc from 'fast-check';

// Running a property: check it with expect() inside the callback.
fc.assert(
  fc.property(arbA, arbB, (a, b) => {
    expect(f(a, b)).toEqual(/* ... */);
  }),
);

// Generators ("arbitraries")
fc.integer({ min: -20, max: 20 })
fc.nat(10)                                     // 0..10
fc.constantFrom('A', 'B', 'C')
fc.array(arb, { minLength: 1, maxLength: 5 })
fc.tuple(arbA, arbB)
fc.oneof(arbA, arbB)                           // sometimes one, sometimes the other
fc.shuffledSubarray(xs, { minLength: xs.length, maxLength: xs.length }) // a shuffle of xs

// Building new generators from old ones
arb.map(x => f(x))                             // transform each value
arb.chain(x => otherArbBuiltFrom(x))           // second value depends on the first
arb.filter(x => ok(x))                         // discards values; use sparingly
fc.pre(ok(x))                                  // same idea, inside the property
```

Docs: [https://fast-check.dev/docs/introduction/](https://fast-check.dev/docs/introduction/)
