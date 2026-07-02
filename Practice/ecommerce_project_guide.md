# Q2 Orders Data — Cleanup + Insights Needed

**From:** Priya (Data Analytics Lead)
**To:** You (Data Analyst Intern)
**Dataset:** `ecommerce_orders.csv` (565 rows, 11 columns)

Hey — the ops team dumped raw order export data on us. It's never been cleaned. I need it audit-ready and I need answers for leadership by **end of this week**.

**Deadline:** 3 days. Day 1 = clean, Day 2 = EDA, Day 3 = polish + summary.

---

## Known problems (client already flagged these)
1. Some order IDs look duplicated — is that a system bug or real re-orders?
2. City names are inconsistent — reports are undercounting Mumbai because of casing issues
3. Customer ages have garbage in them (someone's "150 years old") — fix before this goes to marketing
4. Some quantities are 0 or negative — refunds? Data entry error? Your call, but document it
5. I don't trust the price column — check for outliers

---

## Day 1: Clean the data

Work column by column. For each, ask *is this valid?*

- **Column names** — inconsistent spacing/casing. Normalize to snake_case first, makes everything else easier.
- **Load + first look** — `.shape`, `.head()`, `.info()`, `.dtypes`. Get oriented before changing anything.
- **Missing values** — `.isna().sum()` to see where. Then per column, decide: drop, fill with mean/median/mode, fill "Unknown", or leave? Don't use the same strategy everywhere — justify each one.
- **Duplicates**
  - Full-row duplicates: `.duplicated()`
  - Suspicious ID duplicates: same OrderID with *different* data in other columns — that's not a real duplicate, that's a data entry error. Check `.duplicated(subset=['OrderID'])` and inspect those rows.
- **Invalid values**
  - Ages: check `.describe()` / sort values — anything negative or above ~100 is garbage
  - Quantity: 0 or negative doesn't make sense for an order — decide drop vs investigate
  - City: `.unique()` — you'll see casing/spacing issues. `.str.strip().str.title()` is your friend
  - Price: after grouping by category, look for values way outside the normal range for that category (boxplot helps a lot here)
  - Dates: check if all values actually parsed correctly after converting to datetime — mixed formats will silently produce NaT if you're not careful
- **Data types** — dates → datetime, IDs → string, quantity/price → numeric

Keep a running log in markdown cells: what you found → what you did → why. Priya will ask "why did you drop that row" in the meeting — have an answer.

**End of Day 1 output:** a clean CSV.

---

## Day 2: Answer the 5 business questions

Don't jump straight to charts. First write down what each question actually needs.

1. **Which category brings in the most revenue?**
   → derive a revenue column first (quantity × price, minus discount if applicable). Group by category, sum, sort, bar chart.

2. **Which city has the most orders (after fixing casing)?**
   → value_counts on the cleaned city column, bar chart.

3. **Does a bigger discount actually sell more units?**
   → group by discount level, look at average quantity. Scatter or bar chart. Correlation isn't causation — say what the data shows, not more.

4. **What's our average rating, and does it differ by category?**
   → overall mean first, then group by category. Boxplot or bar chart.

5. **Are orders trending up or down month over month?**
   → extract month from order_date, count orders per month, line chart. Watch for the two-format date issue from Day 1 biting you here if you didn't fully fix it.

For every chart, write one sentence: what does this actually tell me?

**End of Day 2 output:** 5 charts, 5 one-line takeaways.

---

## Day 3: Polish

- Re-read your Day 1 cleaning log — is every decision explainable in one sentence?
- Write a **5-bullet Key Findings summary** — this is what gets read out loud in the meeting, so it should stand alone without the code.
- Sanity check: open the cleaned CSV fresh, does it look right? No leftover "150 year old" customers, no "mumbai"/"Mumbai" split.

---

## Rules
- Document every cleaning decision.
- If unsure whether a value is an error, check the data — don't assume.
- Come back with the actual code/error when stuck, not "it's not working."

**Day 1 starts now — get the data loaded and cleaned.**
