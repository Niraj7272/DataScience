# Power BI: Task-Based Learning Guide
### From Zero to Job-Ready — No YouTube Required
**Dataset:** `PowerBI_Practice_Dataset.csv` (1,215 rows × 45 columns)

> **How to use this guide:**
> Every task is hands-on. Read the task → open Power BI → do it yourself.
> Struggle first, Google second. That's how real learning happens.
> Tasks go Easy → Medium → Hard within each section.

---

## SETUP — Do This First

1. Download and install **Power BI Desktop** (free) from microsoft.com/power-bi
2. Open Power BI Desktop — you'll see a splash screen, close it
3. Keep `PowerBI_Practice_Dataset.csv` somewhere easy to find (e.g., Desktop)

You're ready. Let's go.

---

---

# PART 1 — Getting Data In (Power Query Basics)

> **What this is:** Before you analyze anything, Power BI needs to read your data. Power Query is where you load, clean, and shape it. Think of it like pandas but with a visual interface.

---

### Task 1.1 — Load the CSV (Easy)

**What to do:**
- Click `Home → Get Data → Text/CSV`
- Find and select `PowerBI_Practice_Dataset.csv`
- In the preview window, click **Transform Data** (not Load — always Transform first)
- You are now in the Power Query Editor

**Observe:** How many rows? How many columns? What data types were auto-detected?

**Your job:** Write down which columns got the wrong data type. (Hint: Month is a number — is that right for everything?)

---

### Task 1.2 — Fix Data Types (Easy)

In Power Query Editor:

**What to do:**
- Change `OrderDate`, `ShipDate`, `DeliveryDate` to **Date** type (click the icon left of column name)
- Change `Year` to **Whole Number**
- Change `Month` to **Whole Number**
- Change `UnitPrice`, `NetSales`, `GrossProfit`, `ProfitMargin`, `COGS`, `EmployeeSalary` to **Decimal Number**
- Change `Discount` to **Percentage** OR **Decimal Number**
- Change `CustomerRating` to **Decimal Number**

**Why this matters:** Wrong data types = wrong visuals and broken DAX formulas later.

---

### Task 1.3 — Find and Remove Duplicates (Easy)

**What to do:**
- Select the `OrderID` column
- Go to `Home → Remove Rows → Remove Duplicates`

**Question to answer:** How many rows were removed? (Check the row count before and after in the bottom bar.)

> The dataset has 15 intentional duplicates — did you catch them all?

---

### Task 1.4 — Handle Null / Blank Values (Easy → Medium)

**What to do:**

Part A — See where nulls are:
- Go to `View → Column Quality` — green/red/white bars appear under each column header
- Which columns have nulls? Note them down.

Part B — Fill nulls in `CustomerRating`:
- Select `CustomerRating` column → `Transform → Fill → Down`
- Alternatively: Right-click column → `Replace Values` → replace `null` with `3` (neutral rating)

Part C — Fill nulls in `ShippingCost`:
- Right-click `ShippingCost` → `Replace Values` → replace `null` with `0`

Part D — Leave `ReturnReason` nulls alone (blank = not returned, that's valid data)
- Instead, right-click → `Replace Values` → replace `null` with `N/A`

**Think:** Why did we treat each null column differently?

---

### Task 1.5 — Add Conditional Column (Medium)

**What to do:**
- Go to `Add Column → Conditional Column`
- Name it `SalesSize`
- Rules:
  - If `NetSales` >= 5000 → `Large`
  - If `NetSales` >= 1000 → `Medium`
  - Else → `Small`

**Then:** Add another conditional column called `ProfitCategory`:
- If `ProfitMargin` >= 30 → `High Margin`
- If `ProfitMargin` >= 15 → `Medium Margin`
- Else → `Low Margin`

---

### Task 1.6 — Split and Merge Columns (Medium)

**What to do:**

Part A — Extract year from OrderDate:
- Select `OrderDate` → `Add Column → Date → Year → Year`
- Compare it to the existing `Year` column — are they the same?
- Delete the one you just made (just practice)

Part B — Merge CustomerID and CustomerName:
- `Add Column → Merge Columns`
- Select `CustomerID` and `CustomerName`, separator = ` | `
- Name it `CustomerFullRef`
- Then delete it (just practice)

---

### Task 1.7 — Group By (Medium)

**What to do:**
- Go to `Home → Group By`
- Group by `Category`
- Aggregation: Sum of `NetSales`, name it `TotalSalesByCategory`
- Click OK — observe the result

**Then undo** (`Ctrl+Z`) — this was just to understand grouping. You'll do real aggregation in DAX.

---

### Task 1.8 — Rename Columns & Reorder (Easy)

**What to do:**
- Rename `COGS` to `CostOfGoodsSold`
- Rename `IsReturned` to `ReturnFlag`
- Reorder columns: drag `OrderDate` right after `OrderID`

---

### Task 1.9 — Create a Parameters (Hard)

**What to do:**
- Go to `Home → Manage Parameters → New Parameter`
- Name: `MinSalesThreshold`
- Type: `Decimal Number`
- Default value: `100`
- Click OK

Now use it:
- Add a Step: Filter `NetSales` where value >= `MinSalesThreshold` parameter
- Change the parameter value to `500` — notice the filter updates automatically

**This is how dynamic data loading works in production reports.**

---

### Task 1.10 — M Language: View & Edit a Step (Hard)

**What to do:**
- In Query Settings (right panel), click any Applied Step
- Go to `View → Advanced Editor`
- You'll see M language code
- Find the step where you replaced nulls in `ShippingCost`
- Read the line — what does it say?
- Manually change the replacement value from `0` to `10` directly in the code
- Click Done

**Now you know:** Every click in Power Query writes M code behind the scenes.

---

### ✅ After Part 1 — Click `Close & Apply`

Your cleaned data is now loaded into Power BI.

---

---

# PART 2 — Data Modeling

> **What this is:** Your CSV is one flat table. Real Power BI uses multiple related tables — like a database. This section teaches you to think in tables and relationships.

---

### Task 2.1 — Explore the Model View (Easy)

**What to do:**
- Click the **Model View** icon (left sidebar, looks like 3 connected boxes)
- You'll see your single table — not much to see yet
- Click a column name — observe the properties panel on the right

---

### Task 2.2 — Create a Separate Date Table (Medium)

**Why:** Power BI Time Intelligence functions REQUIRE a proper Date Table.

**What to do:**
- Go to `Home → Transform Data` (back to Power Query)
- `New Source → Blank Query`
- Open Advanced Editor, paste this M code:

```
let
    StartDate = #date(2021, 1, 1),
    EndDate = #date(2024, 12, 31),
    Duration = Duration.Days(EndDate - StartDate) + 1,
    Dates = List.Dates(StartDate, Duration, #duration(1, 0, 0, 0)),
    Table = Table.FromList(Dates, Splitter.SplitByNothing(), {"Date"}),
    ChangedType = Table.TransformColumnTypes(Table, {{"Date", type date}}),
    AddYear = Table.AddColumn(ChangedType, "Year", each Date.Year([Date]), Int64.Type),
    AddMonth = Table.AddColumn(AddYear, "Month", each Date.Month([Date]), Int64.Type),
    AddMonthName = Table.AddColumn(AddMonth, "MonthName", each Date.MonthName([Date]), type text),
    AddQuarter = Table.AddColumn(AddMonthName, "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date])), type text),
    AddWeek = Table.AddColumn(AddQuarter, "WeekNumber", each Date.WeekOfYear([Date]), Int64.Type),
    AddDayName = Table.AddColumn(AddWeek, "DayOfWeek", each Date.DayOfWeek([Date]), Int64.Type),
    AddDayNameText = Table.AddColumn(AddDayName, "DayName", each Date.DayOfWeekName([Date]), type text)
in
    AddDayNameText
```

- Name this query `DateTable`
- Close & Apply

---

### Task 2.3 — Create a Relationship (Medium)

**What to do:**
- Go to Model View
- Drag `DateTable[Date]` onto `PowerBI_Practice_Dataset[OrderDate]`
- A line appears — that's a relationship!
- Double-click the line to see:
  - Cardinality: One-to-Many (1 date → many orders) ✓
  - Cross-filter direction: Single ✓

**Now your Date Table controls your time visuals.**

---

### Task 2.4 — Create Separate Lookup Tables (Hard)

**Goal:** Normalize your flat table into a Star Schema.

Go back to Power Query and create these Reference Tables:

**Customer Table:**
- Right-click your main query → `Reference`
- Keep only: `CustomerID`, `CustomerName`, `Segment`
- Remove duplicates on `CustomerID`
- Name it `DimCustomer`

**Product Table:**
- Right-click main query → `Reference`
- Keep only: `ProductID`, `Category`, `SubCategory`
- Remove duplicates on `ProductID`
- Name it `DimProduct`

**Employee Table:**
- Right-click main query → `Reference`
- Keep only: `EmployeeID`, `EmployeeName`, `Department`, `ManagerID`, `EmployeeAge`, `ExperienceYears`, `EmployeeSalary`
- Remove duplicates on `EmployeeID`
- Name it `DimEmployee`

**Geography Table:**
- Right-click main query → `Reference`
- Keep only: `Region`, `Country`
- Remove duplicates (both columns)
- Name it `DimGeography`

Close & Apply.

---

### Task 2.5 — Build the Star Schema (Hard)

In Model View, create relationships:

- `DimCustomer[CustomerID]` → `FactSales[CustomerID]`
- `DimProduct[ProductID]` → `FactSales[ProductID]`
- `DimEmployee[EmployeeID]` → `FactSales[EmployeeID]`
- `DateTable[Date]` → `FactSales[OrderDate]`

Arrange your tables: put `FactSales` in the center, dimension tables around it like a star.

**Verify:** Every relationship should show 1 → * (one-to-many). If it shows *, * (many-to-many), something is wrong — fix duplicates in your dimension tables.

---

### Task 2.6 — Create a Hierarchy (Medium)

In Model View, inside `DimProduct`:
- Right-click `Category` → `Create Hierarchy`
- Name it `Product Hierarchy`
- Drag `SubCategory` into the hierarchy below `Category`

In `DateTable`:
- Create a hierarchy: `Year → Quarter → MonthName`
- Name it `Date Hierarchy`

**You'll use these for Drill Down in Part 5.**

---

### Task 2.7 — Role-Playing Dimension (Hard)

Your fact table has THREE date columns: `OrderDate`, `ShipDate`, `DeliveryDate` — but your DateTable can only be connected to one at a time (active relationship).

**What to do:**
- Create relationship: `DateTable[Date]` → `FactSales[OrderDate]` (active)
- Create relationship: `DateTable[Date]` → `FactSales[ShipDate]` (inactive — dashed line)
- Create relationship: `DateTable[Date]` → `FactSales[DeliveryDate]` (inactive)

**You'll use `USERELATIONSHIP()` in DAX to activate the inactive ones when needed.**

---

---

# PART 3 — DAX (Data Analysis Expressions)

> **What this is:** DAX is the formula language of Power BI. If you know SQL aggregations and Excel formulas, DAX will feel familiar — but it's more powerful. This is the most important section for becoming job-ready.

> **Where to write DAX:** In Report View, click your table in the Fields pane → `New Measure` (for measures) or `New Column` (for calculated columns).

---

## 3A — Calculated Columns vs Measures

### Task 3.1 — Your First Calculated Column (Easy)

On the `FactSales` table, create a calculated column:

```dax
DeliveryDays = DATEDIFF(FactSales[OrderDate], FactSales[DeliveryDate], DAY)
```

**Observe:** This creates a new column with a value for EVERY row. It's stored in memory.

Create another:
```dax
RevenuePerUnit = FactSales[NetSales] / FactSales[Quantity]
```

---

### Task 3.2 — Your First Measure (Easy)

```dax
Total Sales = SUM(FactSales[NetSales])
```

```dax
Total Orders = COUNTROWS(FactSales)
```

```dax
Total Profit = SUM(FactSales[GrossProfit])
```

**Key difference from calculated column:** A measure has NO row — it calculates based on whatever filter context exists in your visual. Drag `Total Sales` into a Card visual — it shows the grand total. Put it in a Bar Chart by Region — it shows sales per region automatically.

---

### Task 3.3 — Understand the Difference (Easy)

Add both to a Table visual: `Category`, your `Total Sales` measure, and the `NetSales` column.

**Observe:**
- The measure aggregates correctly per category
- If you put the `NetSales` column in a table, it shows individual row values

> **Rule to memorize:** Always use Measures for aggregations shown in visuals. Use Calculated Columns only for row-level attributes.

---

## 3B — Aggregation Functions

### Task 3.4 — Basic Aggregations (Easy)

```dax
Avg Order Value = AVERAGE(FactSales[NetSales])
```
```dax
Max Sale = MAX(FactSales[NetSales])
```
```dax
Min Sale = MIN(FactSales[NetSales])
```
```dax
Unique Customers = DISTINCTCOUNT(FactSales[CustomerID])
```
```dax
Total COGS = SUM(FactSales[CostOfGoodsSold])
```
```dax
Overall Profit Margin % = DIVIDE(SUM(FactSales[GrossProfit]), SUM(FactSales[NetSales])) * 100
```

> Always use `DIVIDE()` instead of `/` — it handles division by zero gracefully.

---

## 3C — Logical Functions

### Task 3.5 — IF and SWITCH (Easy)

Calculated column:
```dax
PerformanceFlag = IF(FactSales[ProfitMargin] >= 30, "High", IF(FactSales[ProfitMargin] >= 15, "Medium", "Low"))
```

Measure using SWITCH:
```dax
Sales Tier = 
SWITCH(
    TRUE(),
    [Total Sales] >= 100000, "Platinum",
    [Total Sales] >= 50000, "Gold",
    [Total Sales] >= 10000, "Silver",
    "Bronze"
)
```

---

## 3D — CALCULATE — The Most Important DAX Function

### Task 3.6 — CALCULATE Basics (Medium)

```dax
Online Sales = CALCULATE(SUM(FactSales[NetSales]), FactSales[SalesChannel] = "Online")
```
```dax
Completed Orders Revenue = CALCULATE(SUM(FactSales[NetSales]), FactSales[OrderStatus] = "Completed")
```
```dax
North Region Sales = CALCULATE(SUM(FactSales[NetSales]), FactSales[Region] = "North")
```
```dax
Electronics Sales = CALCULATE(SUM(FactSales[NetSales]), FactSales[Category] = "Electronics")
```

**Now put `Online Sales` and `Total Sales` side by side in a table — observe the difference.**

---

### Task 3.7 — CALCULATE with ALL (Medium)

```dax
% of Total Sales = 
DIVIDE(
    SUM(FactSales[NetSales]),
    CALCULATE(SUM(FactSales[NetSales]), ALL(FactSales))
) * 100
```

Put this in a table with `Category` — each category shows its % of the GRAND total, even when you filter. The `ALL()` removes the filter.

```dax
% of Region Total = 
DIVIDE(
    SUM(FactSales[NetSales]),
    CALCULATE(SUM(FactSales[NetSales]), ALL(FactSales[Category]))
) * 100
```

---

### Task 3.8 — FILTER Function (Medium)

```dax
High Value Orders = 
CALCULATE(
    COUNTROWS(FactSales),
    FILTER(FactSales, FactSales[NetSales] > 1000)
)
```

```dax
Premium Customer Revenue = 
CALCULATE(
    SUM(FactSales[NetSales]),
    FILTER(FactSales, FactSales[Segment] = "Enterprise" && FactSales[NetSales] > 500)
)
```

---

## 3E — Iterator Functions (X Functions)

### Task 3.9 — SUMX, AVERAGEX (Medium)

```dax
Recalculated Revenue = SUMX(FactSales, FactSales[UnitPrice] * FactSales[Quantity] * (1 - FactSales[Discount]))
```

**Compare this to your `Total Sales` measure — they should be close (minor rounding differences).**

```dax
Avg Profit Per Order = AVERAGEX(FactSales, FactSales[GrossProfit])
```

```dax
Weighted Avg Discount = 
DIVIDE(
    SUMX(FactSales, FactSales[Discount] * FactSales[GrossSales]),
    SUM(FactSales[GrossSales])
)
```

---

## 3F — Time Intelligence

> **Prerequisite:** Your `DateTable` must be marked as a Date Table. Right-click `DateTable` in Fields → `Mark as Date Table` → select `Date` column.

### Task 3.10 — Year-over-Year Comparison (Medium)

```dax
Sales LY = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(DateTable[Date]))
```

```dax
YoY Growth = [Total Sales] - [Sales LY]
```

```dax
YoY Growth % = DIVIDE([YoY Growth], [Sales LY]) * 100
```

Put `Year`, `Total Sales`, `Sales LY`, `YoY Growth %` in a table — instant business insight.

---

### Task 3.11 — Running Totals (Medium)

```dax
Sales YTD = TOTALYTD([Total Sales], DateTable[Date])
```

```dax
Sales MTD = TOTALMTD([Total Sales], DateTable[Date])
```

```dax
Sales QTD = TOTALQTD([Total Sales], DateTable[Date])
```

Put `MonthName`, `Total Sales`, `Sales YTD` in a line chart. See the cumulative curve build up.

---

### Task 3.12 — DATEADD for Rolling Periods (Hard)

```dax
Sales Last 3 Months = 
CALCULATE(
    [Total Sales],
    DATEADD(DateTable[Date], -3, MONTH)
)
```

```dax
Sales Last 30 Days = 
CALCULATE(
    [Total Sales],
    DATESINPERIOD(DateTable[Date], LASTDATE(DateTable[Date]), -30, DAY)
)
```

---

## 3G — Advanced DAX

### Task 3.13 — VAR & RETURN (Hard)

Rewrite your YoY Growth % using VAR for clarity:

```dax
YoY Growth % Clean = 
VAR CurrentSales = [Total Sales]
VAR LastYearSales = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(DateTable[Date]))
VAR Growth = DIVIDE(CurrentSales - LastYearSales, LastYearSales) * 100
RETURN
    IF(ISBLANK(LastYearSales), BLANK(), Growth)
```

---

### Task 3.14 — RANKX (Hard)

```dax
Category Rank by Sales = 
RANKX(
    ALL(FactSales[Category]),
    [Total Sales],
    ,
    DESC,
    DENSE
)
```

Put `Category`, `Total Sales`, `Category Rank by Sales` in a table → sort by rank → now you have a leaderboard.

```dax
Country Rank = 
RANKX(ALL(FactSales[Country]), [Total Sales],, DESC, DENSE)
```

---

### Task 3.15 — USERELATIONSHIP (Hard)

```dax
Sales by Ship Date = 
CALCULATE(
    [Total Sales],
    USERELATIONSHIP(DateTable[Date], FactSales[ShipDate])
)
```

```dax
Sales by Delivery Date = 
CALCULATE(
    [Total Sales],
    USERELATIONSHIP(DateTable[Date], FactSales[DeliveryDate])
)
```

Put all three measures in a line chart — see how the curves differ based on which date you use.

---

### Task 3.16 — SELECTEDVALUE & Dynamic Titles (Hard)

```dax
Selected Region = SELECTEDVALUE(FactSales[Region], "All Regions")
```

```dax
Dynamic Chart Title = "Sales Performance — " & [Selected Region]
```

You'll use this in Part 5 for Dynamic Titles.

---

---

# PART 4 — Building Visualizations

> **Where:** Report View (the default page you see when opening Power BI Desktop)
> **How:** Drag fields from the Fields pane on the right into your canvas, or click a visual type first then assign fields.

---

## 4A — Basic Visuals

### Task 4.1 — KPI Cards (Easy)

Add 4 **Card** visuals to the canvas:
- `Total Sales`
- `Total Orders`
- `Total Profit`
- `Unique Customers`

Format each: `Format Visual → Callout Value` → increase font size to 28+
Add a title to each card.

**This becomes your executive summary row.**

---

### Task 4.2 — Bar and Column Charts (Easy)

Create these charts:
- **Clustered Bar Chart:** Axis = `Region`, Values = `Total Sales`
- **Clustered Column Chart:** Axis = `Category`, Values = `Total Sales`, `Total Profit`
- **Stacked Bar Chart:** Axis = `Country`, Values = `Total Sales`, Legend = `SalesChannel`

Format: Add data labels, change colors, add a title.

---

### Task 4.3 — Line Chart (Easy)

- **Line Chart:** X-axis = `MonthName` from DateTable, Y-axis = `Total Sales`, `Sales LY`
- See both years on the same chart for comparison

Then change X-axis to your `Date Hierarchy` — now you can drill down from Year → Quarter → Month.

---

### Task 4.4 — Pie and Donut Chart (Easy)

- **Donut Chart:** Legend = `Category`, Values = `Total Sales`
- **Pie Chart:** Legend = `SalesChannel`, Values = `Total Orders`

> Note: These work well with 5-7 slices max. More than that = confusing.

---

### Task 4.5 — Table and Matrix (Medium)

**Table visual:**
- Columns: `Category`, `Total Sales`, `Total Profit`, `Overall Profit Margin %`, `Category Rank by Sales`
- Sort by `Total Sales` descending
- Apply conditional formatting: `Total Sales` → Background Color scale (red → green)

**Matrix visual:**
- Rows = `Category`, Columns = `Year`, Values = `Total Sales`
- This gives you a pivot table inside Power BI
- Enable `+/-` expand buttons to drill into SubCategory

---

### Task 4.6 — Scatter Chart (Medium)

- X-axis = `Avg Order Value`
- Y-axis = `Overall Profit Margin %`
- Details = `Category`
- Size = `Total Orders`

**This reveals which categories have high value AND high margin simultaneously.**

---

### Task 4.7 — Maps (Medium)

**Map visual:**
- Location = `Country`
- Bubble size = `Total Sales`
- Color = `Total Profit`

**Filled Map:**
- Location = `Country`
- Color saturation = `Total Sales`

> Note: Power BI uses Bing Maps. Country names must be spelled correctly to geocode.

---

### Task 4.8 — Waterfall Chart (Medium)

- Category = `Category`
- Y-axis = `Total Sales`

**This shows which categories ADD to or SUBTRACT from the overall total — great for variance analysis.**

---

### Task 4.9 — KPI Visual (Medium)

- Value = `Total Sales`
- Trend axis = `OrderDate` (from DateTable)
- Target = create a measure: `Sales Target = [Sales LY] * 1.10` (10% growth target)

---

### Task 4.10 — Treemap (Medium)

- Group = `Category`
- Subgroup = `SubCategory`
- Values = `Total Sales`

**Drill down from Category → SubCategory by clicking the drill icon.**

---

### Task 4.11 — Decomposition Tree (Hard)

- Insert → Decomposition Tree
- Analyze = `Total Sales`
- Explain By = `Region`, `Category`, `SalesChannel`, `Country`

Click the `+` button → choose which dimension to expand → Power BI finds where the value comes from.

**This is an AI visual. Use it in interviews to impress.**

---

### Task 4.12 — Key Influencers (Hard)

- Insert → Key Influencers
- Analyze = `CustomerRating`
- Explain By = `Category`, `Region`, `SalesChannel`, `ShipMode`, `PaymentMethod`

Power BI automatically identifies what factors drive high/low customer ratings.

---

## 4B — Formatting

### Task 4.13 — Themes and Colors (Easy)

- `View → Themes` → try 3 different themes
- Customize a theme: change primary color to dark blue (#1a2e4a)
- Apply to all visuals at once

---

### Task 4.14 — Conditional Formatting (Medium)

On your Matrix visual:
- Right-click `Total Sales` value → Conditional Formatting → Background Color
- Use a red-white-green scale
- Also add: Data Bars on the `Total Sales` column in your Table visual

On your Table visual:
- Add `YoY Growth %` column
- Conditional format: Red if negative, Green if positive (use Rules-based formatting)

---

### Task 4.15 — Tooltips (Medium)

On your bar chart (Sales by Region):
- Hover over a bar — default tooltip shows
- Now add custom tooltip fields: `Total Orders`, `Overall Profit Margin %`, `Avg Order Value`
- Right-click visual → Format → Tooltips → add the measures

**Advanced:** Create a separate Tooltip Page (small canvas page) with mini visuals — set that page as tooltip for your main chart.

---

---

# PART 5 — Interactive Reports

> **What this is:** Making your report respond to user clicks and selections. This is what separates a static chart from an actual dashboard.

---

### Task 5.1 — Slicers (Easy)

Add these slicers to your report page:
- `Year` (from DateTable) — Dropdown style
- `Category` — List style
- `Region` — Tile style (Format → Slicer Settings → Style = Tile)
- `SalesChannel` — Dropdown

Now click different values — observe ALL visuals updating together.

---

### Task 5.2 — Sync Slicers Across Pages (Medium)

- Create a second report page
- Add a chart showing `Sales by Country`
- Go to `View → Sync Slicers`
- Check which slicers should sync to Page 2
- Now filtering on Page 1 also filters Page 2

---

### Task 5.3 — Drill Down (Medium)

On your line chart with `Date Hierarchy`:
- Click the drill down arrow icon (↓) in the visual header
- Click on a Year bar → it drills into Quarters → Months → Days

On your treemap:
- Enable drill → click a Category → see SubCategories

---

### Task 5.4 — Drill Through (Hard)

**Goal:** Click on a Category in your main page → jump to a detail page for that category.

**Steps:**
1. Create a new page, name it `Category Detail`
2. Add these visuals: Sales by SubCategory (bar), Sales trend by Month (line), Top Customers (table)
3. In the `Category Detail` page, drag `Category` from Fields into the **Drill Through** well (Format pane → Page Information → Drill Through)
4. Go back to main page → right-click a category bar → Drill Through → Category Detail

**Boom — context-aware navigation.**

---

### Task 5.5 — Bookmarks and Buttons (Hard)

**Goal:** Toggle between two views of the same page.

**Steps:**
1. Create two visuals on the same canvas: a Bar Chart and a Table showing the same data
2. Show the Bar Chart, hide the Table → `View → Bookmarks → Add Bookmark` → name it "Chart View"
3. Hide the Bar Chart, show the Table → Add Bookmark → "Table View"
4. Add two buttons (`Insert → Buttons → Blank`)
5. Label them "📊 Chart" and "📋 Table"
6. Action for each button: Bookmark → select the corresponding bookmark
7. Now clicking the button switches between views

---

### Task 5.6 — Dynamic Titles (Hard)

Add a Text Box or a Card visual with your `Dynamic Chart Title` measure from Task 3.16.

When a user selects "North" in the Region slicer, the title automatically reads:
**"Sales Performance — North"**

When nothing is selected:
**"Sales Performance — All Regions"**

---

### Task 5.7 — Cross-Filtering and Cross-Highlighting (Medium)

By default, clicking a bar in one visual highlights related items in others.

**Try:** Click "Electronics" in the donut chart — observe the map, bar chart, and table all respond.

**Change behavior:**
- Click `Format → Edit Interactions` (in the Format tab)
- Click your donut chart
- Small icons appear on other visuals: Filter (funnel), Highlight (binoculars), None (🚫)
- Change a visual from Highlight to Filter — now it fully filters instead of highlighting

---

---

# PART 6 — Security (Row Level Security)

> **What this is:** Making sure a sales manager for "North" region can ONLY see North region data when they log in.

---

### Task 6.1 — Static RLS (Medium)

**Steps:**
1. Go to `Modeling → Manage Roles`
2. Click `+ New Role` → name it `North Region`
3. In the table filter for `FactSales`: `[Region] = "North"`
4. Click Save
5. Go to `Modeling → View as` → select `North Region`
6. Observe: ALL your visuals now only show North data

Create roles for: `South Region`, `East Region`, `West Region`, `Central Region`

---

### Task 6.2 — Dynamic RLS (Hard)

**Goal:** One role that automatically filters based on who is logged in.

**Steps:**
1. Create a table called `UserRegionAccess` (manually in Power Query):
   - Two columns: `Email`, `Region`
   - Add some rows: `north.manager@company.com | North`, etc.

2. Create a relationship: `UserRegionAccess[Region]` → `FactSales[Region]`

3. Create a role `Dynamic RLS` with DAX filter on `UserRegionAccess`:
```dax
[Email] = USERPRINCIPALNAME()
```

4. When a user logs in, `USERPRINCIPALNAME()` returns their email → matches their region → they only see their data.

---

---

# PART 7 — Full Dashboard Projects

> **This is your portfolio work.** Build each dashboard from scratch using everything you learned.

---

### Project 1 — Sales Analytics Dashboard (Medium)

**Page 1: Executive Summary**
- 4 KPI Cards: Total Sales, Total Profit, Total Orders, Profit Margin %
- Sales Trend by Month (line chart with Sales LY comparison)
- Sales by Region (map)
- Sales by Category (donut)
- Slicers: Year, Region, Category

**Page 2: Product Performance**
- Matrix: Category × Year (Total Sales)
- Top 10 Products by Sales (bar chart)
- Profit Margin by Category (column chart)
- Decomposition Tree: analyze Total Sales

**Page 3: Customer Analysis**
- Customer Segment distribution (pie)
- Sales Channel performance (bar)
- Avg Customer Rating by Category
- Top 20 Customers (table with conditional formatting)

---

### Project 2 — HR Analytics Dashboard (Medium)

**Use columns:** `EmployeeID`, `EmployeeName`, `Department`, `ManagerID`, `EmployeeAge`, `ExperienceYears`, `EmployeeSalary`

**Build:**
- Headcount by Department (bar)
- Avg Salary by Department (column)
- Age Distribution (histogram — use a column chart with age buckets)
- Salary vs Experience scatter chart
- Salary Band measure:
```dax
Salary Band = 
SWITCH(TRUE(),
    FactSales[EmployeeSalary] >= 120000, "Senior",
    FactSales[EmployeeSalary] >= 80000, "Mid",
    FactSales[EmployeeSalary] >= 50000, "Junior",
    "Entry"
)
```
- Apply RLS: each department manager sees only their department

---

### Project 3 — Finance Dashboard (Hard)

**Measures to create:**

```dax
Gross Margin % = DIVIDE(SUM(FactSales[GrossProfit]), SUM(FactSales[NetSales])) * 100
```

```dax
Revenue Growth MoM = 
VAR CurrentMonth = [Total Sales]
VAR PrevMonth = CALCULATE([Total Sales], DATEADD(DateTable[Date], -1, MONTH))
RETURN DIVIDE(CurrentMonth - PrevMonth, PrevMonth) * 100
```

```dax
Cumulative Revenue = 
CALCULATE([Total Sales], DATESYTD(DateTable[Date]))
```

```dax
Budget Variance = [Total Sales] - [Sales Target]
```

**Build:**
- Revenue vs Target (KPI visual with trend)
- Monthly Revenue with Budget line
- Waterfall chart: Revenue by Category
- YoY comparison table
- Finance summary matrix: Month × Category

---

### Project 4 — Executive Dashboard (Hard)

**One single page. Must show everything at a glance.**

Rules:
- Max 6 visuals on one page
- Every visual must have a clear title
- Use bookmarks for Show/Hide detail panels
- Dynamic title that changes with slicer selection
- Color coding: Green = good, Red = bad (conditional formatting)
- Navigation buttons to other dashboard pages
- Custom tooltip on the main chart

**This is your interview piece. Make it beautiful.**

---

---

# PART 8 — Performance & Optimization

> **What this is:** Real-world Power BI reports can slow down. You need to know how to diagnose and fix performance issues.

---

### Task 8.1 — Performance Analyzer (Medium)

- Go to `View → Performance Analyzer → Start Recording`
- Interact with your visuals — click slicers, drill down
- Stop recording
- Read the results: which visual takes longest? Is it DAX query or visual rendering?

**If a visual takes >500ms consistently → it needs optimization.**

---

### Task 8.2 — Optimize Your DAX (Medium)

Bad pattern (slow):
```dax
Slow Measure = COUNTROWS(FILTER(FactSales, FactSales[NetSales] > 1000))
```

Good pattern (fast):
```dax
Fast Measure = CALCULATE(COUNTROWS(FactSales), FactSales[NetSales] > 1000)
```

Rewrite 3 of your FILTER-based measures to use CALCULATE instead.

---

### Task 8.3 — Reduce Model Size (Medium)

In Power Query:
- Remove columns you don't use (e.g., `CostRatio` if you already have `COGS` and `NetSales`)
- Remove the `Year`, `Month`, `Quarter` columns from `FactSales` — you have them in `DateTable`
- Check: does your model still work?

**Rule:** Never store in the fact table what you can calculate or get from a dimension table.

---

---

# PART 9 — Publishing & Sharing

> **Requires:** Free Power BI account at app.powerbi.com

---

### Task 9.1 — Publish to Power BI Service (Easy)

- `Home → Publish`
- Sign in with your Microsoft account
- Select "My Workspace"
- Go to app.powerbi.com — your report is there

---

### Task 9.2 — Create a Dashboard (Medium)

In Power BI Service (web browser):
- Open your published report
- Hover over a visual → click the **pin icon** → pin to a new Dashboard
- Pin 4-5 visuals from different pages
- Open the Dashboard — visuals are now on one screen, live

**Difference:** Reports = pages with filters. Dashboards = pinned tiles, no filter interaction.

---

### Task 9.3 — Schedule Refresh (Medium)

- In Power BI Service → Datasets → your dataset → Settings
- If you had a real database, you'd set up a Gateway and schedule refresh
- For CSV: understand the concept — in production, your data source refreshes automatically (daily, hourly, etc.)

---

### Task 9.4 — Share and Permissions (Easy)

- Open your report in Power BI Service
- Click `Share` → enter an email address
- Set permissions: Can view / Can share / Can edit
- Generate a shareable link

---

---

# PART 10 — Interview Prep Tasks

> **Do these last. They simulate real interview tasks and business problems.**

---

### Task 10.1 — Business Questions to Answer with Visuals

Use your dashboard to answer these — build a visual for each:

1. Which region has the highest profit margin (not just sales)?
2. Which sales channel has the best and worst customer ratings?
3. Is the business growing YoY? By how much %?
4. Which product category has the most returns? Why might that be?
5. What day of the week sees the most orders?
6. Which employee department generates the most revenue per person?
7. What discount level maximizes profit (not just sales)?
8. Is there a relationship between delivery days and customer rating?

---

### Task 10.2 — DAX Interview Questions — Solve These

```
Q1: Calculate sales for only the last full quarter (dynamically, no hardcoding)

Q2: Create a measure that shows "↑ 12.3%" or "↓ 5.1%" as text based on YoY growth

Q3: Rank customers by total spend — show only Top 10

Q4: Calculate the 3-month rolling average of sales

Q5: Show % contribution of each SubCategory within its Category (not total)
```

---

### Task 10.3 — Build a Report in 45 Minutes

**Simulate an interview task:**

> "We need a quick Sales Overview dashboard. It should show total revenue, YoY comparison, regional breakdown, top 5 categories, and trend over time. Users should be able to filter by year and region."

Set a 45-minute timer. Build it. Judge yourself:
- Does it load fast?
- Is it readable without explanation?
- Do the numbers make sense?
- Is it visually clean?

---

### Task 10.4 — Explain Your Model

Prepare answers to these interview questions using YOUR model as example:

1. "Walk me through your data model — why did you choose a star schema?"
2. "What's the difference between a measure and a calculated column in your report?"
3. "How did you implement Row Level Security?"
4. "What does CALCULATE do? Give me a real example from your work."
5. "If your report is running slow, what are the first 3 things you check?"
6. "How does context transition work in DAX?"

---

---

# QUICK REFERENCE

## DAX Measures Cheat Sheet

| Measure | DAX |
|---|---|
| Total Sales | `SUM(FactSales[NetSales])` |
| Total Orders | `COUNTROWS(FactSales)` |
| Profit Margin % | `DIVIDE(SUM([GrossProfit]), SUM([NetSales])) * 100` |
| YoY Sales | `CALCULATE([Total Sales], SAMEPERIODLASTYEAR(DateTable[Date]))` |
| Sales YTD | `TOTALYTD([Total Sales], DateTable[Date])` |
| % of Total | `DIVIDE([Total Sales], CALCULATE([Total Sales], ALL(FactSales))) * 100` |
| Rank | `RANKX(ALL(FactSales[Category]), [Total Sales],, DESC, DENSE)` |
| Rolling 3M | `CALCULATE([Total Sales], DATESINPERIOD(DateTable[Date], LASTDATE(DateTable[Date]), -3, MONTH))` |

## Common Errors & Fixes

| Error | Likely Cause | Fix |
|---|---|---|
| Blank measure value | Filter eliminates all rows | Use `IF(ISBLANK(...), 0, ...)` |
| Time intelligence not working | Date table not marked | Right-click DateTable → Mark as Date Table |
| Circular dependency | Calculated column references itself | Rewrite as measure |
| Many-to-many relationship | Duplicates in dimension table | Deduplicate the lookup table |
| Slow visual | FILTER inside measure | Replace with CALCULATE |

## Power BI Keyboard Shortcuts

| Action | Shortcut |
|---|---|
| New measure | `Alt + Enter` (in formula bar) |
| Undo | `Ctrl + Z` |
| Multi-select visuals | `Ctrl + Click` |
| Align visuals | Select multiple → Format → Align |
| Preview data | Click table in Fields → View data |

---

## What Job-Ready Looks Like

You are ready when you can:

- [ ] Build a Star Schema from a flat CSV
- [ ] Write CALCULATE, ALL, FILTER, RANKX, SAMEPERIODLASTYEAR without looking them up
- [ ] Set up Row Level Security (static and dynamic)
- [ ] Build a drill-through report with bookmarks and navigation
- [ ] Explain filter context and row context in plain English
- [ ] Diagnose a slow report using Performance Analyzer
- [ ] Publish, share, and schedule refresh in Power BI Service
- [ ] Build a complete dashboard in under an hour

---

*Built for hands-on learning. Every task uses `PowerBI_Practice_Dataset.csv`.*
*Total tasks: 50+ | Estimated time: 40–60 hours of focused practice*
