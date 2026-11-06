
# Czech National Team Goaltender Evaluation Model
# NHL & AHL Advanced Analytics
# Retrospective sample for future national team evaluation
# Milan Cermak 

print("Czech Goaltender Evaluation Model is ready!")

import pandas as pd

# Step 1: Identify our NHL and AHL datasets
nhl_file = "data/raw/nhl/NHL_Goalies.csv"
ahl_file = "data/raw/ahl/AHL_Goalies.csv"

# Step 2: Load both datasets into Python
nhl = pd.read_csv(nhl_file)
ahl = pd.read_csv(ahl_file)

# Step 3: Count the rows in each dataset
print("NHL Dataset:", len(nhl), "rows")
print("AHL Dataset:", len(ahl), "rows")

# Step 4: Display the first five rows
print("\nNHL Dataset Preview:")
print(nhl.head())

print("\nAHL Dataset Preview:")
print(ahl.head())

# Step 5: Display available statistics
print("\nNHL Columns:")
print(nhl.columns.tolist())

print("\nAHL Columns:")
print(ahl.columns.tolist())


# Step 10 - Cleaning NHL and AHL Data

# Select NHL statistics from all game situations
nhl_clean = nhl[nhl["situation"] == "all"].copy()

# Keep all AHL goaltender records
ahl_clean = ahl.copy()

# Calculate NHL save percentage
nhl_clean["save_pct"] = (
    (nhl_clean["ongoal"] - nhl_clean["goals"])
    / nhl_clean["ongoal"]
)

# Convert AHL save percentage to the same scale
ahl_clean["save_pct"] = ahl_clean["save_percent"] / 100

# Confirm the number of goaltenders
print("\nCLEANED DATASETS")
print("NHL Goaltenders:", len(nhl_clean))
print("AHL Goaltenders:", len(ahl_clean))

# Preview the cleaned save percentages
print("\nNHL Save Percentages:")
print(nhl_clean[["name", "save_pct"]].head())

print("\nAHL Save Percentages:")
print(ahl_clean[["full_name", "save_pct"]].head())


# Step 11 - Calculate NHL and AHL League Averages

# NHL totals
nhl_shots = nhl_clean["ongoal"].sum()
nhl_goals = nhl_clean["goals"].sum()
nhl_minutes = nhl_clean["icetime"].sum() / 60

# AHL totals
ahl_shots = ahl_clean["shots_against"].sum()
ahl_goals = ahl_clean["goals_against"].sum()
ahl_minutes = ahl_clean["time_on_ice_in_seconds"].sum() / 60

# Calculate league save percentages
nhl_sv_pct = (nhl_shots - nhl_goals) / nhl_shots
ahl_sv_pct = (ahl_shots - ahl_goals) / ahl_shots

# Calculate goals against per 60 minutes
nhl_gaa = (nhl_goals / nhl_minutes) * 60
ahl_gaa = (ahl_goals / ahl_minutes) * 60

# Create our league comparison table
league_averages = pd.DataFrame({
    "League": ["NHL", "AHL"],
    "Save Percentage": [nhl_sv_pct, ahl_sv_pct],
    "Goals Against Average": [nhl_gaa, ahl_gaa]
})

# Display results
print("\nNHL & AHL LEAGUE AVERAGES")
print(league_averages.round(3).to_string(index=False))

# Save our comparison table
league_averages.to_csv(
    "outputs/tables/league_averages.csv",
    index=False
)

print("\nLeague averages saved successfully!")

# Step 12 - League Benchmarks with Median and Minimum Games

def calculate_benchmarks(data, league, minimum_games):

    # Filter goalies by games played
    goalies = data[
        data["games_played"] >= minimum_games
    ].copy()

    # Identify each league's statistical columns
    if league == "NHL":
        shots = "ongoal"
        goals = "goals"
        time = "icetime"
    else:
        shots = "shots_against"
        goals = "goals_against"
        time = "time_on_ice_in_seconds"

    # Remove records without shots or playing time
    goalies = goalies[
        (goalies[shots] > 0) &
        (goalies[time] > 0)
    ].copy()

    # Calculate individual goalie statistics
    goalies["goalie_sv_pct"] = (
        (goalies[shots] - goalies[goals]) / goalies[shots]
    )

    goalies["goalie_gaa"] = (
        goalies[goals] / goalies[time]
    ) * 3600

    # Calculate weighted league statistics
    league_sv_pct = (
        1 - goalies[goals].sum() / goalies[shots].sum()
    )

    league_gaa = (
        goalies[goals].sum() / goalies[time].sum()
    ) * 3600

    # Return our comparison results
    return {
        "League": league,
        "Minimum Games": minimum_games,
        "Goalies": len(goalies),
        "League SV%": league_sv_pct,
        "Median SV%": goalies["goalie_sv_pct"].median(),
        "League GAA": league_gaa,
        "Median GAA": goalies["goalie_gaa"].median()
    }


# Compare all goalies and goalies with 5+ games
benchmark_results = []

for league, data in [("NHL", nhl_clean), ("AHL", ahl_clean)]:
    for minimum_games in [1, 5]:
        result = calculate_benchmarks(
            data, league, minimum_games
        )
        benchmark_results.append(result)

# Create our results table
benchmarks = pd.DataFrame(benchmark_results)

print("\nLEAGUE GOALTENDING BENCHMARKS")
print(benchmarks.round(4).to_string(index=False))

# Export our benchmark table
benchmarks.to_csv(
    "outputs/tables/league_benchmarks.csv",
    index=False
)

print("\nBenchmarks saved successfully!")


# Step 13 - Identify Czech NHL and AHL Goaltenders

# Czech NHL goalies (names as written in MoneyPuck)
nhl_czech_names = [
    "Lukas Dostal",
    "Karel Vejmelka",
    "Dan Vladar",
    "Jakub Dobes",
    "Michal Postava"
]

# Czech AHL goalies (names as written in our AHL CSV)
ahl_czech_names = [
    "David Rittich",
    "Vítek Vaněček",
    "Jiří Patera",
    "Michael Hrabal",
    "Michal Postava",
    "Jakub Málek",
    "Simon Zajíček",
    "Tomas Suchanek"
]

# Filter our datasets to Czech goaltenders
nhl_czech = nhl_clean[
    nhl_clean["name"].isin(nhl_czech_names)
].copy()

ahl_czech = ahl_clean[
    ahl_clean["full_name"].isin(ahl_czech_names)
].copy()

# Calculate individual NHL goals against averages
nhl_czech["gaa"] = (
    nhl_czech["goals"] / nhl_czech["icetime"] * 3600
)

# Calculate individual AHL goals against averages
ahl_czech["gaa"] = (
    ahl_czech["goals_against"]
    / ahl_czech["time_on_ice_in_seconds"] * 3600
)

# Standardize names and add league labels
nhl_czech["goalie"] = nhl_czech["name"]
nhl_czech["league"] = "NHL"

ahl_czech["goalie"] = ahl_czech["full_name"]
ahl_czech["league"] = "AHL"

# Combine both leagues into one comparison table
columns = ["goalie", "league", "games_played", "save_pct", "gaa"]

czech_goalies = pd.concat([
    nhl_czech[columns],
    ahl_czech[columns]
], ignore_index=True)

# Flag goalies with fewer than five games
czech_goalies["sample"] = czech_goalies["games_played"].apply(
    lambda games: "5+ Games" if games >= 5 else "Small Sample"
)

# Display our results
print("\nCZECH NHL & AHL GOALTENDERS")
print(czech_goalies.round(3).to_string(index=False))

print("\nNHL Czech Goalies:", len(nhl_czech))
print("AHL Czech Goalies:", len(ahl_czech))

# Export our combined table
czech_goalies.to_csv(
    "outputs/tables/czech_goalies.csv",
    index=False
)

print("\nCzech goaltender table saved successfully!")


# Step 14 - Comprehensive NHL Goaltender Scouting Report

# Create a separate dataset for our scouting analysis
nhl_scout = nhl_clean.copy()

# Avoid division errors for goalies with no ice time or shots
safe_icetime = nhl_scout["icetime"].replace(0, float("nan"))
safe_shots = nhl_scout["ongoal"].replace(0, float("nan"))


# PART 1 - Traditional Goaltending Statistics

# Total shots on goal faced
nhl_scout["Shots_Faced"] = nhl_scout["ongoal"]

# Total saves made
nhl_scout["Saves"] = (
    nhl_scout["Shots_Faced"] - nhl_scout["goals"]
)

# Save percentage
nhl_scout["save_pct"] = (
    nhl_scout["Saves"] / safe_shots
)

# Goals against average per 60 minutes
nhl_scout["gaa"] = (
    nhl_scout["goals"] / safe_icetime * 3600
)

# Shots faced per 60 minutes
nhl_scout["Shots_Faced_per60"] = (
    nhl_scout["Shots_Faced"] / safe_icetime * 3600
)


# PART 2 - Expected Goals Against

# Expected goals against per 60 minutes
# Measures expected scoring threat faced by the goalie
nhl_scout["xGA_per60"] = (
    nhl_scout["xGoals"] / safe_icetime * 3600
)

# Goals Saved Above Expected
# Positive GSAx indicates better-than-expected performance
nhl_scout["GSAx"] = (
    nhl_scout["xGoals"] - nhl_scout["goals"]
)

# Goals Saved Above Expected per 60 minutes
nhl_scout["GSAx_per60"] = (
    nhl_scout["GSAx"] / safe_icetime * 3600
)


# PART 3 - High-Danger Scoring Opportunities

# High-danger unblocked attempts faced per 60 minutes
nhl_scout["HD_Attempts_per60"] = (
    nhl_scout["highDangerShots"] / safe_icetime * 3600
)

# High-danger Goals Saved Above Expected
nhl_scout["HD_GSAx"] = (
    nhl_scout["highDangerxGoals"] -
    nhl_scout["highDangerGoals"]
)


# PART 4 - Low-Danger Goals Allowed

# Total low-danger goals allowed
nhl_scout["Low_Danger_Goals_Allowed"] = (
    nhl_scout["lowDangerGoals"]
)

# Low-danger goals allowed above expectation
# Positive means more goals allowed than expected
# Negative means fewer goals allowed than expected
nhl_scout["Low_Danger_Goals_Above_Expected"] = (
    nhl_scout["lowDangerGoals"] -
    nhl_scout["lowDangerxGoals"]
)


# PART 5 - Rebound Control

# Rebounds above expected
# Negative means fewer rebounds than expected
# Positive means more rebounds than expected
nhl_scout["Rebounds_Above_Expected"] = (
    nhl_scout["rebounds"] -
    nhl_scout["xRebounds"]
)


# PART 6 - Minimum Games Requirement

# Identify goalies who played at least five games
nhl_scout["Qualified"] = (
    nhl_scout["games_played"] >= 5
)


# PART 7 - Create Our Scouting Report

# Select the statistics we want in our final report
scouting_columns = [
    "name",
    "team",
    "games_played",
    "Qualified",
    "Shots_Faced",
    "Saves",
    "save_pct",
    "gaa",
    "Shots_Faced_per60",
    "xGA_per60",
    "GSAx",
    "GSAx_per60",
    "highDangerShots",
    "HD_Attempts_per60",
    "HD_GSAx",
    "Low_Danger_Goals_Allowed",
    "Low_Danger_Goals_Above_Expected",
    "Rebounds_Above_Expected"
]

# Create our scouting table
nhl_scouting_report = nhl_scout[scouting_columns].copy()


# PART 8 - Export Our Results

# Save our completed scouting report
nhl_scouting_report.to_csv(
    "outputs/tables/nhl_scouting_report.csv",
    index=False
)

# Display the first five goaltenders
print("\nNHL GOALTENDER SCOUTING REPORT")
print(
    nhl_scouting_report.head().round(3).to_string(index=False)
)

# Confirm the number of goalies evaluated
print("\nTotal NHL Goalies:", len(nhl_scouting_report))

print("\nNHL scouting report saved successfully!")


# Step 15 - Czech NHL and AHL Goaltender Evaluation

# PART 1 - Identify Czech Goaltenders

# Czech NHL goalies
nhl_czech_names = [
    "Lukas Dostal",
    "Karel Vejmelka",
    "Dan Vladar",
    "Jakub Dobes",
    "Michal Postava"
]

# Czech AHL goalies
ahl_czech_names = [
    "David Rittich",
    "Vítek Vaněček",
    "Jiří Patera",
    "Michael Hrabal",
    "Michal Postava",
    "Jakub Málek",
    "Simon Zajíček",
    "Tomas Suchanek"
]


# PART 2 - Filter NHL Goaltenders

# Select Czech goalies from our completed NHL scouting report
nhl_czech = nhl_scouting_report[
    nhl_scouting_report["name"].isin(nhl_czech_names)
].copy()

# Standardize NHL column names
nhl_czech = nhl_czech.rename(columns={
    "name": "Goalie",
    "team": "Team",
    "games_played": "GP",
    "save_pct": "SV%",
    "gaa": "GAA"
})

nhl_czech["League"] = "NHL"


# PART 3 - Filter AHL Goaltenders

ahl_czech = ahl_clean[
    ahl_clean["full_name"].isin(ahl_czech_names)
].copy()

# Standardize AHL column names
ahl_czech["Goalie"] = ahl_czech["full_name"]
ahl_czech["Team"] = ahl_czech["team_abbreviation"]
ahl_czech["League"] = "AHL"
ahl_czech["GP"] = ahl_czech["games_played"]

# Calculate AHL traditional statistics
ahl_czech["Shots_Faced"] = ahl_czech["shots_against"]

ahl_czech["Saves"] = ahl_czech["saves"]

ahl_czech["SV%"] = (
    ahl_czech["Saves"] /
    ahl_czech["Shots_Faced"].replace(0, float("nan"))
)

ahl_czech["GAA"] = (
    ahl_czech["goals_against"] /
    ahl_czech["time_on_ice_in_seconds"].replace(
        0, float("nan")
    ) * 3600
)

# Mark goalies with at least five games played
ahl_czech["Qualified"] = ahl_czech["GP"] >= 5


# PART 4 - Combine Comparable Statistics

# These statistics are available in both leagues
common_columns = [
    "Goalie",
    "League",
    "Team",
    "GP",
    "Qualified",
    "Shots_Faced",
    "Saves",
    "SV%",
    "GAA"
]

czech_overview = pd.concat([
    nhl_czech[common_columns],
    ahl_czech[common_columns]
], ignore_index=True)

# Organize goalies by league and games played
czech_overview = czech_overview.sort_values(
    ["League", "GP"],
    ascending=[False, False]
)


# PART 5 - Save Our Scouting Tables

# Combined Czech NHL and AHL overview
czech_overview.to_csv(
    "outputs/tables/czech_goalie_overview.csv",
    index=False
)

# NHL report includes all our advanced NHL statistics
nhl_czech.to_csv(
    "outputs/tables/czech_nhl_scouting.csv",
    index=False
)

# AHL report contains currently available statistics
ahl_czech[common_columns].to_csv(
    "outputs/tables/czech_ahl_scouting.csv",
    index=False
)


# PART 6 - Display Results

print("\nCZECH NATIONAL TEAM GOALTENDER OVERVIEW")

print(
    czech_overview.round(3).to_string(index=False)
)

print("\nNHL Goaltender Records:", len(nhl_czech))
print("AHL Goaltender Records:", len(ahl_czech))

# Verify that all expected names were found
print(
    "Missing NHL Players:",
    set(nhl_czech_names) - set(nhl_czech["Goalie"])
)

print(
    "Missing AHL Players:",
    set(ahl_czech_names) - set(ahl_czech["Goalie"])
)

print("\nCzech scouting tables saved successfully!")


# Step 16 - NHL and AHL Goaltender Rankings

# Rank all goalies for now
# We can change this to 5, 10, or 15 later
MIN_GAMES_FOR_RANKING = 1


def create_rankings(data, league, czech_names):

    # PART 1 - Prepare our data

    goalies = data.copy()

    if league == "NHL":
        goalies["Goalie"] = goalies["name"]
        goalies["Team"] = goalies["team"]
        goalies["Shots_Faced"] = goalies["ongoal"]
        goalies["Goals_Allowed"] = goalies["goals"]
        goalies["Ice_Time"] = goalies["icetime"]

    else:
        goalies["Goalie"] = goalies["full_name"]
        goalies["Team"] = goalies["team_abbreviation"]
        goalies["Shots_Faced"] = goalies["shots_against"]
        goalies["Goals_Allowed"] = goalies["goals_against"]
        goalies["Ice_Time"] = goalies["time_on_ice_in_seconds"]

    goalies["GP"] = goalies["games_played"]

    # PART 2 - Calculate comparable statistics

    goalies["Saves"] = (
        goalies["Shots_Faced"] - goalies["Goals_Allowed"]
    )

    goalies["SV%"] = (
        goalies["Saves"] /
        goalies["Shots_Faced"].replace(0, float("nan"))
    )

    goalies["GAA"] = (
        goalies["Goals_Allowed"] /
        goalies["Ice_Time"].replace(0, float("nan"))
        * 3600
    )

    # Advanced statistics currently available for NHL
    metrics = [
        ("SV%", False),
        ("GAA", True)
    ]

    if league == "NHL":
        goalies["GSAx/60"] = (
            (goalies["xGoals"] - goalies["goals"]) /
            goalies["Ice_Time"].replace(0, float("nan"))
            * 3600
        )

        metrics.append(("GSAx/60", False))

    # Apply minimum games requirement
    goalies = goalies[
        goalies["GP"] >= MIN_GAMES_FOR_RANKING
    ].copy()

    results = []

    # PART 3 - Calculate league and Czech rankings

    for metric, lower_is_better in metrics:

        ranked = goalies.dropna(subset=[metric]).copy()

        # Rank against everyone in the league
        ranked["League_Rank"] = ranked[metric].rank(
            method="min",
            ascending=lower_is_better
        )

        # Select Czech goalies
        czech = ranked[
            ranked["Goalie"].isin(czech_names)
        ].copy()

        # Rank Czech goalies against Czech league peers
        czech["Czech_Rank"] = czech[metric].rank(
            method="min",
            ascending=lower_is_better
        )

        # PART 4 - Calculate averages

        def group_average(group):

            if metric == "SV%":
                return (
                    group["Saves"].sum() /
                    group["Shots_Faced"].sum()
                )

            if metric == "GAA":
                return (
                    group["Goals_Allowed"].sum() /
                    group["Ice_Time"].sum() * 3600
                )

            return (
                (group["xGoals"].sum() -
                 group["Goals_Allowed"].sum()) /
                group["Ice_Time"].sum() * 3600
            )

        league_avg = group_average(ranked)
        czech_avg = group_average(czech)

        # PART 5 - Build our comparison table

        for _, goalie in czech.iterrows():

            results.append({
                "Goalie": goalie["Goalie"],
                "League": league,
                "Team": goalie["Team"],
                "GP": goalie["GP"],
                "Statistic": metric,
                "Player_Value": goalie[metric],
                "League_Rank": (
                    f"{int(goalie['League_Rank'])}/{len(ranked)}"
                ),
                "League_Average": league_avg,
                "Czech_Rank": (
                    f"{int(goalie['Czech_Rank'])}/{len(czech)}"
                ),
                "Czech_Average": czech_avg,
                "Qualified_5_GP": goalie["GP"] >= 5
            })

    print(f"\n{league} Czech goalie rankings completed!")

    return results


# PART 6 - Run calculations for both leagues

ranking_results = (
    create_rankings(nhl_clean, "NHL", nhl_czech_names) +
    create_rankings(ahl_clean, "AHL", ahl_czech_names)
)

# Convert our results into a DataFrame
czech_rankings = pd.DataFrame(ranking_results)

# PART 7 - Export the rankings

czech_rankings.to_csv(
    "outputs/tables/czech_league_rankings.csv",
    index=False
)

print("\nCZECH GOALTENDER RANKINGS")
print(czech_rankings.head(12).round(3).to_string(index=False))

print("\nTotal comparison rows:", len(czech_rankings))
print("\nCzech rankings saved successfully!")


# Step 17 - Advanced NHL Goaltender Rankings

# PART 1 - Prepare Advanced Statistics

nhl_advanced = nhl_scout.copy()

# Calculate high-danger attempts that did not become goals
nhl_advanced["HD_Non_Goals"] = (
    nhl_advanced["highDangerShots"] -
    nhl_advanced["highDangerGoals"]
)

# Identify low-danger goals allowed above expectation
nhl_advanced["LD_Excess_Goals"] = (
    nhl_advanced["lowDangerGoals"] -
    nhl_advanced["lowDangerxGoals"]
)


# PART 2 - Define Our Advanced Statistics

# Format:
# Statistic, Numerator, Denominator, Scale, Lower is Better

advanced_metrics = [
    ("Shots Faced/60", "ongoal", "icetime", 3600, False),

    ("xGA/60", "xGoals", "icetime", 3600, False),

    ("High-Danger Attempts/60",
     "highDangerShots", "icetime", 3600, False),

    ("High-Danger Non-Goal Rate",
     "HD_Non_Goals", "highDangerShots", 1, False),

    ("High-Danger GSAx/60",
     "HD_GSAx", "icetime", 3600, False),

    ("Low-Danger Goals Above Expected/100",
     "LD_Excess_Goals", "lowDangerShots", 100, True),

    ("Rebounds Above Expected/100",
     "Rebounds_Above_Expected", "ongoal", 100, True)
]


# PART 3 - Calculate League and Czech Rankings

advanced_results = []

for metric, numerator, denominator, scale, lower_better in advanced_metrics:

    # Keep goalies meeting our current games requirement
    ranked = nhl_advanced[
        (nhl_advanced["games_played"] >= MIN_GAMES_FOR_RANKING) &
        (nhl_advanced[denominator] > 0)
    ].copy()

    # Calculate the statistic for each goalie
    ranked["Player_Value"] = (
        ranked[numerator] / ranked[denominator] * scale
    )

    # Rank all NHL goaltenders
    ranked["League_Rank"] = ranked["Player_Value"].rank(
        method="min",
        ascending=lower_better
    )

    # Identify Czech NHL goalies
    czech = ranked[
        ranked["name"].isin(nhl_czech_names)
    ].copy()

    # Rank Czech NHL goalies
    czech["Czech_Rank"] = czech["Player_Value"].rank(
        method="min",
        ascending=lower_better
    )

    # Calculate weighted league and Czech averages
    league_average = (
        ranked[numerator].sum() /
        ranked[denominator].sum() * scale
    )

    czech_average = (
        czech[numerator].sum() /
        czech[denominator].sum() * scale
    )

    # PART 4 - Store Each Goalie's Results

    for _, goalie in czech.iterrows():

        advanced_results.append({
            "Goalie": goalie["name"],
            "League": "NHL",
            "Team": goalie["team"],
            "GP": goalie["games_played"],
            "Statistic": metric,
            "Player_Value": goalie["Player_Value"],
            "League_Rank": (
                f"{int(goalie['League_Rank'])}/{len(ranked)}"
            ),
            "League_Average": league_average,
            "Czech_Rank": (
                f"{int(goalie['Czech_Rank'])}/{len(czech)}"
            ),
            "Czech_Average": czech_average,
            "Qualified_5_GP": goalie["games_played"] >= 5
        })


# PART 5 - Create Advanced Rankings Table

advanced_rankings = pd.DataFrame(advanced_results)

advanced_rankings.to_csv(
    "outputs/tables/czech_nhl_advanced_rankings.csv",
    index=False
)


# PART 6 - Add Advanced Rankings to Our Existing Table

all_rankings = pd.concat([
    czech_rankings,
    advanced_rankings
], ignore_index=True)

all_rankings.to_csv(
    "outputs/tables/czech_league_rankings.csv",
    index=False
)


# PART 7 - Display Results

print("\nADVANCED NHL GOALTENDER RANKINGS")

print(
    advanced_rankings.head(10).round(3).to_string(index=False)
)

print("\nAdvanced Ranking Rows:", len(advanced_rankings))
print("Total Comparison Rows:", len(all_rankings))

print("\nAdvanced NHL rankings saved successfully!")


# Step 18 - Expanded AHL Goaltender Rankings

# Create a separate copy of our AHL dataset
ahl_scout = ahl_clean.copy()

# Calculate additional workload statistics
ahl_scout["Shots_Faced_per60"] = (
    ahl_scout["shots_against"] /
    ahl_scout["time_on_ice_in_seconds"] * 3600
)

ahl_scout["Saves_per60"] = (
    ahl_scout["saves"] /
    ahl_scout["time_on_ice_in_seconds"] * 3600
)

# Define the statistics we want to rank
ahl_metrics = [
    "Shots_Faced_per60",
    "Saves_per60",
    "shots_against",
    "saves"
]

ahl_metric_names = [
    "Shots Faced/60",
    "Saves/60",
    "Total Shots Faced",
    "Total Saves"
]

ahl_results = []

# Calculate rankings for each statistic
for column, metric in zip(ahl_metrics, ahl_metric_names):

    # Apply our minimum games requirement
    ranked = ahl_scout[
        ahl_scout["games_played"] >= MIN_GAMES_FOR_RANKING
    ].copy()

    # Rank every AHL goalie
    ranked["League_Rank"] = ranked[column].rank(
        ascending=False,
        method="min"
    )

    # Identify Czech AHL goalies
    czech = ranked[
        ranked["full_name"].isin(ahl_czech_names)
    ].copy()

    # Rank the Czech goalies
    czech["Czech_Rank"] = czech[column].rank(
        ascending=False,
        method="min"
    )

    # Calculate averages
    if metric.endswith("/60"):
        numerator = (
            "shots_against" if "Shots" in metric else "saves"
        )

        league_avg = (
            ranked[numerator].sum() /
            ranked["time_on_ice_in_seconds"].sum() * 3600
        )

        czech_avg = (
            czech[numerator].sum() /
            czech["time_on_ice_in_seconds"].sum() * 3600
        )

    else:
        league_avg = ranked[column].mean()
        czech_avg = czech[column].mean()

    # Save each Czech goalie's results
    for _, goalie in czech.iterrows():

        ahl_results.append({
            "Goalie": goalie["full_name"],
            "League": "AHL",
            "Team": goalie["team_abbreviation"],
            "GP": goalie["games_played"],
            "Statistic": metric,
            "Player_Value": goalie[column],
            "League_Rank": (
                f"{int(goalie['League_Rank'])}/{len(ranked)}"
            ),
            "League_Average": league_avg,
            "Czech_Rank": (
                f"{int(goalie['Czech_Rank'])}/{len(czech)}"
            ),
            "Czech_Average": czech_avg,
            "Qualified_5_GP": goalie["games_played"] >= 5
        })


# Create our new AHL ranking table
ahl_workload_rankings = pd.DataFrame(ahl_results)

# Add the new rankings to our existing model
all_rankings = pd.concat(
    [all_rankings, ahl_workload_rankings],
    ignore_index=True
)

# Export our updated scouting rankings
all_rankings.to_csv(
    "outputs/tables/czech_league_rankings.csv",
    index=False
)

print("\nEXPANDED AHL SCOUTING RANKINGS")
print(ahl_workload_rankings.head().round(3).to_string(index=False))

print("\nNew AHL Ranking Rows:", len(ahl_workload_rankings))
print("Total Comparison Rows:", len(all_rankings))

print("\nAHL scouting rankings updated successfully!")


# Step 19 - Export Rankings for HTML Dashboard

from pathlib import Path

# Create a folder for our website data
dashboard_folder = Path("docs/data")
dashboard_folder.mkdir(parents=True, exist_ok=True)

# Prepare our completed rankings
dashboard_rankings = all_rankings.copy()

# Check that our important columns exist
required_columns = [
    "Goalie",
    "League",
    "Team",
    "GP",
    "Statistic",
    "Player_Value",
    "League_Rank",
    "League_Average",
    "Czech_Rank",
    "Czech_Average"
]

missing_columns = [
    col for col in required_columns
    if col not in dashboard_rankings.columns
]

if missing_columns:
    raise ValueError(
        f"Missing dashboard columns: {missing_columns}"
    )

# Export the rankings as JSON
dashboard_rankings.to_json(
    "docs/data/goalie_rankings.json",
    orient="records",
    indent=2,
    force_ascii=False
)

# Confirm the export
print("\nHTML DASHBOARD DATA")
print("Exported ranking rows:", len(dashboard_rankings))
print("JSON file created successfully!")
