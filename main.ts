// One-Line Office Joke: 24-Hour Sprint — make.fun bounty
// u-pucuys-one-line-office-joke-24-hour-sprint-aaf86162
//
// The program writes a single one-line joke about office life
// (1-200 characters) to /output/entry.txt.
//
// Candidates were drafted against the judge's brief, in order of weight:
//   1. reads as a one-line joke about office life, a setup and a
//      punchline in a single sentence
//   2. funny: the punchline surprises and pays off the setup in a way
//      anyone who has sat in an office recognises
//   3. one line: the whole joke reads as a single sentence, no rambling
//   4. fresh: a specific detail of office life, not a joke everyone has
//      already heard (no "this meeting could have been an email",
//      no password-expiry gag, no "I survived another meeting")
//   5. clear on first read: no explanation needed, wording tight
// Each candidate carries a hand-scored craft score (0-10 per criterion,
// summed below); selection is deterministic: highest score wins, ties go
// to the shorter text. The output is byte-identical on every run.

const CANDIDATES: Array<{ text: string; score: number }> = [
  // score: joke 10, funny 9, one-line 10, fresh 9, clear 10 = 48
  {
    text: "I told my manager I'm drowning in work, so he threw me a meeting invite and called it a life raft.",
    score: 48,
  },
  // score: joke 9, funny 8, one-line 10, fresh 9, clear 9 = 45
  {
    text: "I put 'per my last email' in my out-of-office reply so even my absence sounds passive-aggressive.",
    score: 45,
  },
  // score: joke 8, funny 8, one-line 9, fresh 9, clear 9 = 43
  {
    text: "The office printer has been 'warming up' since Tuesday, which makes it the only thing here with a work-life balance.",
    score: 43,
  },
  // score: joke 9, funny 7, one-line 10, fresh 8, clear 9 = 43
  {
    text: "I CC'd my boss so he'd feel included; he replied-all, and now the whole company feels included.",
    score: 43,
  },
];

function pick(cands: Array<{ text: string; score: number }>): string {
  let best = cands[0];
  for (const c of cands.slice(1)) {
    if (c.score > best.score || (c.score === best.score && c.text.length < best.text.length)) {
      best = c;
    }
  }
  return best.text;
}

const joke = pick(CANDIDATES);

// The gate requires 1-200 characters of non-whitespace UTF-8 text in a
// single line. Validate before writing, then read the file back and
// confirm it holds exactly the chosen joke, byte for byte.
if (joke.length < 1 || joke.length > 200) {
  throw new Error(`joke is ${joke.length} characters, gate requires 1-200`);
}
if (joke.trim().length === 0 || joke.includes("\n")) {
  throw new Error("joke must be a single non-empty line");
}

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";

mkdirSync("/output", { recursive: true });
writeFileSync("/output/entry.txt", joke, "utf8");
const written = readFileSync("/output/entry.txt", "utf8");
if (written !== joke) {
  throw new Error("entry.txt does not match the chosen joke");
}
console.log(`wrote ${written.length} characters to /output/entry.txt`);
