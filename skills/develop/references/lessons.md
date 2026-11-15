# The lessons file

Each repo has one lessons file: `lessons.md` in the directory that `"${CLAUDE_PLUGIN_ROOT}/scripts/tree.sh" shared` prints. Agents read it directly or through the lessons their briefs quote; only you write it, at each batch boundary and at Finish.

Put in only what would change what an agent does next time, in this repo:

- **Building and testing:** slow or flaky checks and how to scope them; dependency setup in review worktrees; commands that need something unusual.
- **Review findings:** problems reviewers kept finding, with how to avoid them while building; escapes, with the check that would have caught them; findings validators kept rejecting, so reviewers stop raising them.
- **Planning:** estimates that were badly off; contracts or boundaries that needed fixing forward; assumptions that a spike would have settled.
- **Conventions:** project rules that aren't written down anywhere else.

Write one line per lesson, `- <lesson>. (<feature>, batch <b>, <date>)`, under those four headings. Keep the file under about 80 lines: merge duplicates, sharpen a lesson when it recurs, and delete lessons the code no longer needs (a fixed flaky test, a removed module). Don't copy what `CLAUDE.md`, `CONTRIBUTING.md` or the docs already say.
