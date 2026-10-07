import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy import stats


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

RESULTS_FOLDER = os.path.join(
    PROJECT_ROOT,
    "results"
)

PLOTS_FOLDER = os.path.join(
    RESULTS_FOLDER,
    "plots"
)

os.makedirs(PLOTS_FOLDER, exist_ok=True)


# ============================================================
# CONFIGURATION
# ============================================================

TARGET_DEVICE = "TestPhone2"


# ============================================================
# LOAD PROCESSED DATA
# ============================================================

def load_data():

    pattern = os.path.join(
        RESULTS_FOLDER,
        "processed_angle_*.csv"
    )

    files = glob.glob(pattern)

    if not files:
        print("No processed CSV files found.")
        print(
            "Run process_rssi.py first."
        )
        return None

    all_data = []

    for filepath in files:

        df = pd.read_csv(filepath)

        if "rssi" not in df.columns:
            continue

        # Extract angle from CSV
        if "time" in df.columns:
            pass

        # The angle is easier to obtain from
        # the filename.
        filename = os.path.basename(filepath)

        angle_text = (
            filename
            .replace("processed_angle_", "")
            .replace(".csv", "")
        )

        try:
            angle = float(
                angle_text.replace("_", ".")
            )
        except ValueError:
            continue

        df["angle"] = angle

        all_data.append(df)

    if not all_data:
        return None

    combined = pd.concat(
        all_data,
        ignore_index=True
    )

    return combined


# ============================================================
# BASIC STATISTICS
# ============================================================

def calculate_statistics(df):

    statistics = (
        df
        .groupby("angle")["rssi"]
        .agg(
            samples="count",
            mean="mean",
            median="median",
            std="std",
            minimum="min",
            maximum="max"
        )
        .reset_index()
    )

    statistics["range"] = (
        statistics["maximum"]
        - statistics["minimum"]
    )

    # Standard error
    statistics["standard_error"] = (
        statistics["std"]
        / np.sqrt(statistics["samples"])
    )

    # 95% confidence interval
    statistics["ci_95"] = (
        1.96
        * statistics["standard_error"]
    )

    statistics["ci_lower"] = (
        statistics["mean"]
        - statistics["ci_95"]
    )

    statistics["ci_upper"] = (
        statistics["mean"]
        + statistics["ci_95"]
    )

    return statistics


# ============================================================
# PRINT STATISTICS
# ============================================================

def print_statistics(statistics):

    print("\n")
    print("=" * 80)
    print("ANGLE-WISE RSSI STATISTICS")
    print("=" * 80)

    print(
        statistics[
            [
                "angle",
                "samples",
                "mean",
                "median",
                "std",
                "ci_lower",
                "ci_upper"
            ]
        ].to_string(
            index=False,
            float_format=lambda x: f"{x:.2f}"
        )
    )


# ============================================================
# CONFIDENCE INTERVAL PLOT
# ============================================================

def plot_confidence_intervals(statistics):

    plt.figure(
        figsize=(10, 6)
    )

    plt.errorbar(

        statistics["angle"],

        statistics["mean"],

        yerr=statistics["ci_95"],

        marker="o",

        capsize=5,

        linewidth=1.5
    )

    plt.xlabel(
        "Angle (degrees)"
    )

    plt.ylabel(
        "Mean RSSI (dBm)"
    )

    plt.title(
        "Mean Bluetooth RSSI with 95% Confidence Intervals"
    )

    plt.xticks(
        statistics["angle"]
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    output = os.path.join(
        PLOTS_FOLDER,
        "rssi_confidence_intervals.png"
    )

    plt.savefig(
        output,
        dpi=300
    )

    plt.close()

    print(
        f"\nSaved: {output}"
    )


# ============================================================
# BOXPLOT
# ============================================================

def plot_boxplot(df):

    angles = sorted(
        df["angle"].unique()
    )

    data = []

    for angle in angles:

        values = df[
            df["angle"] == angle
        ]["rssi"]

        data.append(values)

    plt.figure(
        figsize=(11, 6)
    )

    plt.boxplot(
        data,
        tick_labels=angles
    )

    plt.xlabel(
        "Angle (degrees)"
    )

    plt.ylabel(
        "RSSI (dBm)"
    )

    plt.title(
        "Bluetooth RSSI Distribution by Angle"
    )

    plt.grid(
        axis="y",
        alpha=0.3
    )

    plt.tight_layout()

    output = os.path.join(
        PLOTS_FOLDER,
        "rssi_boxplot_by_angle.png"
    )

    plt.savefig(
        output,
        dpi=300
    )

    plt.close()

    print(
        f"Saved: {output}"
    )


# ============================================================
# ONE-WAY ANOVA
# ============================================================

def perform_anova(df):

    groups = []

    angles = sorted(
        df["angle"].unique()
    )

    for angle in angles:

        values = df[
            df["angle"] == angle
        ]["rssi"].dropna()

        groups.append(values)

    # One-way ANOVA
    f_statistic, p_value = (
        stats.f_oneway(*groups)
    )

    print("\n")
    print("=" * 80)
    print("ONE-WAY ANOVA")
    print("=" * 80)

    print(
        f"F-statistic : {f_statistic:.4f}"
    )

    print(
        f"p-value     : {p_value:.8f}"
    )

    if p_value < 0.05:

        print(
            "\nResult:"
        )

        print(
            "The RSSI means are statistically "
            "different across at least some angles "
            "at the 5% significance level."
        )

    else:

        print(
            "\nResult:"
        )

        print(
            "No statistically significant difference "
            "between angle groups was detected "
            "at the 5% significance level."
        )

    return f_statistic, p_value


# ============================================================
# EFFECT SIZE
# ============================================================

def calculate_eta_squared(df):

    overall_mean = df["rssi"].mean()

    # Between-group sum of squares
    between_ss = 0

    # Total sum of squares
    total_ss = np.sum(
        (
            df["rssi"]
            - overall_mean
        ) ** 2
    )

    for angle in df["angle"].unique():

        group = df[
            df["angle"] == angle
        ]["rssi"]

        n = len(group)

        group_mean = group.mean()

        between_ss += (
            n
            * (group_mean - overall_mean) ** 2
        )

    eta_squared = (
        between_ss / total_ss
    )

    print("\n")
    print("=" * 80)
    print("EFFECT SIZE")
    print("=" * 80)

    print(
        f"Eta-squared (η²): "
        f"{eta_squared:.4f}"
    )

    if eta_squared < 0.01:

        interpretation = "Very small effect"

    elif eta_squared < 0.06:

        interpretation = "Small effect"

    elif eta_squared < 0.14:

        interpretation = "Medium effect"

    else:

        interpretation = "Large effect"

    print(
        f"Interpretation: {interpretation}"
    )

    return eta_squared


# ============================================================
# STRONGEST / WEAKEST DIRECTIONS
# ============================================================

def find_best_worst_angles(statistics):

    strongest = statistics.loc[
        statistics["mean"].idxmax()
    ]

    weakest = statistics.loc[
        statistics["mean"].idxmin()
    ]

    difference = (
        strongest["mean"]
        - weakest["mean"]
    )

    print("\n")
    print("=" * 80)
    print("SPATIAL RSSI DIFFERENCE")
    print("=" * 80)

    print(
        f"Strongest direction : "
        f"{strongest['angle']:.0f}°"
    )

    print(
        f"Mean RSSI           : "
        f"{strongest['mean']:.2f} dBm"
    )

    print(
        f"\nWeakest direction   : "
        f"{weakest['angle']:.0f}°"
    )

    print(
        f"Mean RSSI           : "
        f"{weakest['mean']:.2f} dBm"
    )

    print(
        f"\nDifference           : "
        f"{difference:.2f} dB"
    )


# ============================================================
# SAVE STATISTICAL RESULTS
# ============================================================

def save_statistics(statistics):

    output = os.path.join(
        RESULTS_FOLDER,
        "statistical_summary.csv"
    )

    statistics.to_csv(
        output,
        index=False
    )

    print(
        f"\nStatistical summary saved to:"
    )

    print(output)


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("=" * 80)
    print("EXPERIMENT 01 - STATISTICAL RSSI ANALYSIS")
    print("=" * 80)

    # --------------------------------------------------------
    # Load data
    # --------------------------------------------------------

    df = load_data()

    if df is None:
        return

    print(
        f"\nTotal RSSI samples: {len(df)}"
    )

    print(
        f"Angles analyzed: "
        f"{sorted(df['angle'].unique())}"
    )

    # --------------------------------------------------------
    # Calculate statistics
    # --------------------------------------------------------

    statistics = calculate_statistics(
        df
    )

    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    print_statistics(
        statistics
    )

    # --------------------------------------------------------
    # Confidence interval plot
    # --------------------------------------------------------

    plot_confidence_intervals(
        statistics
    )

    # --------------------------------------------------------
    # Boxplot
    # --------------------------------------------------------

    plot_boxplot(
        df
    )

    # --------------------------------------------------------
    # ANOVA
    # --------------------------------------------------------

    perform_anova(
        df
    )

    # --------------------------------------------------------
    # Effect size
    # --------------------------------------------------------

    calculate_eta_squared(
        df
    )

    # --------------------------------------------------------
    # Strongest / weakest
    # --------------------------------------------------------

    find_best_worst_angles(
        statistics
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    save_statistics(
        statistics
    )

    print("\n")
    print("=" * 80)
    print("STATISTICAL ANALYSIS COMPLETE")
    print("=" * 80)


if __name__ == "__main__":

    main()

