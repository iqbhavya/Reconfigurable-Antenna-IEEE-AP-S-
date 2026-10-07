import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# PROJECT PATHS
# ============================================================

# Get the project root:
# Bluetooth_RF_analysis/
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Raw data folder
DATA_FOLDER = os.path.join(
    PROJECT_ROOT,
    "data"
)

# Results folder
RESULTS_FOLDER = os.path.join(
    PROJECT_ROOT,
    "results"
)

# Plot output folder
PLOTS_FOLDER = os.path.join(
    RESULTS_FOLDER,
    "plots"
)

# Create output folder if it doesn't exist
os.makedirs(PLOTS_FOLDER, exist_ok=True)


# ============================================================
# CONFIGURATION
# ============================================================

# Bluetooth device that we want to analyze
TARGET_DEVICE = "TestPhone2"


# ============================================================
# PARSE LOG FILE
# ============================================================

def parse_log_file(filepath):

    bluetooth_data = []

    angle = None
    distance = None

    # --------------------------------------------------------
    # Extract angle from filename
    #
    # Example:
    # log_2020-05-05_16.09.53.682_45.txt
    #
    #                         ^^
    #                       angle
    # --------------------------------------------------------

    filename = os.path.basename(filepath)

    try:
        angle_text = filename.rsplit("_", 1)[1]
        angle_text = angle_text.replace(".txt", "")
        angle = float(angle_text)
    except (IndexError, ValueError):
        angle = None

    print("\nReading file:")
    print(os.path.basename(filepath))

    with open(
        filepath,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            parts = line.split(",")

            # ------------------------------------------------
            # RANGE
            # ------------------------------------------------

            if len(parts) >= 3 and parts[1] == "Range":

                try:
                    distance = float(parts[2])
                except ValueError:
                    pass

            # ------------------------------------------------
            # ANGLE
            # ------------------------------------------------

            elif len(parts) >= 3 and parts[1] == "Angle":

                # The experiment angle is encoded in the filename.
                # Ignore the internal Angle field because it is
                # recorded as 0 for these files.
                pass

            # ------------------------------------------------
            # BLUETOOTH
            # ------------------------------------------------

            elif len(parts) >= 7 and parts[1] == "Bluetooth":

                timestamp = parts[0]

                device_id = parts[2]

                # RSSI
                try:
                    rssi = float(parts[3])
                except ValueError:
                    continue

                device_name = parts[4]

                # TX power
                try:
                    tx_power = float(parts[5])
                except ValueError:
                    tx_power = np.nan

                # Internal timestamp
                try:
                    internal_timestamp = float(parts[6])
                except ValueError:
                    continue

                # ------------------------------------------------
                # SELECT TARGET DEVICE
                # ------------------------------------------------

                if device_name == TARGET_DEVICE:

                    bluetooth_data.append({

                        "timestamp": timestamp,

                        "device_id": device_id,

                        "device_name": device_name,

                        "rssi": rssi,

                        "tx_power": tx_power,

                        "internal_timestamp":
                            internal_timestamp
                    })

    df = pd.DataFrame(bluetooth_data)

    return df, angle, distance


# ============================================================
# PROCESS ONE FILE
# ============================================================

def process_file(filepath):

    df, angle, distance = parse_log_file(filepath)

    # --------------------------------------------------------
    # Check whether data exists
    # --------------------------------------------------------

    if df.empty:

        print(
            f"No data found for {TARGET_DEVICE}"
        )

        return None

    # --------------------------------------------------------
    # Remove duplicate measurements
    # --------------------------------------------------------

    original_count = len(df)

    df = df.drop_duplicates(
        subset=[
            "internal_timestamp",
            "rssi"
        ]
    )

    removed_duplicates = (
        original_count - len(df)
    )

    print(
        f"Removed duplicate readings: "
        f"{removed_duplicates}"
    )

    # --------------------------------------------------------
    # Sort according to time
    # --------------------------------------------------------

    df = df.sort_values(
        by="internal_timestamp"
    )

    # --------------------------------------------------------
    # Create relative time
    # --------------------------------------------------------

    first_timestamp = (
        df["internal_timestamp"].iloc[0]
    )

    df["time"] = (
        df["internal_timestamp"]
        - first_timestamp
    )

    # ========================================================
    # RSSI STATISTICS
    # ========================================================

    mean_rssi = df["rssi"].mean()

    median_rssi = df["rssi"].median()

    std_rssi = df["rssi"].std()

    min_rssi = df["rssi"].min()

    max_rssi = df["rssi"].max()

    rssi_range = (
        max_rssi - min_rssi
    )

    sample_count = len(df)

    # ========================================================
    # PRINT RESULTS
    # ========================================================

    print("\n----------------------------------------")
    print("Experiment Information")
    print("----------------------------------------")

    print(
        f"Device       : {TARGET_DEVICE}"
    )

    print(
        f"Angle        : {angle} degrees"
    )

    print(
        f"Distance     : {distance}"
    )

    print(
        f"Samples      : {sample_count}"
    )

    print("\nRSSI Statistics")

    print(
        f"Mean RSSI    : {mean_rssi:.2f} dBm"
    )

    print(
        f"Median RSSI  : {median_rssi:.2f} dBm"
    )

    print(
        f"Std Dev      : {std_rssi:.2f} dB"
    )

    print(
        f"Minimum RSSI : {min_rssi:.2f} dBm"
    )

    print(
        f"Maximum RSSI : {max_rssi:.2f} dBm"
    )

    print(
        f"RSSI Range   : {rssi_range:.2f} dB"
    )

    print("----------------------------------------")

    # ========================================================
    # SAVE PROCESSED DATA
    # ========================================================

    angle_name = (
        str(angle).replace(".", "_")
        if angle is not None
        else "unknown"
    )

    processed_filename = (
        f"processed_angle_{angle_name}.csv"
    )

    processed_path = os.path.join(
        RESULTS_FOLDER,
        processed_filename
    )

    df.to_csv(
        processed_path,
        index=False
    )

    print(
        f"\nProcessed data saved to:"
    )

    print(processed_path)

    # ========================================================
    # PLOT 1
    # RSSI VS TIME
    # ========================================================

    plt.figure(
        figsize=(10, 5)
    )

    plt.plot(
        df["time"],
        df["rssi"],
        linewidth=1
    )

    plt.xlabel(
        "Time (s)"
    )

    plt.ylabel(
        "RSSI (dBm)"
    )

    title = (
        f"{TARGET_DEVICE} RSSI vs Time"
    )

    if angle is not None:

        title += (
            f" | Angle = {angle}°"
        )

    if distance is not None:

        title += (
            f" | Range = {distance}"
        )

    plt.title(title)

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    rssi_time_path = os.path.join(
        PLOTS_FOLDER,
        f"rssi_vs_time_angle_{angle_name}.png"
    )

    plt.savefig(
        rssi_time_path,
        dpi=300
    )

    plt.close()

    print(
        f"Plot saved to:"
    )

    print(rssi_time_path)

    # ========================================================
    # RETURN SUMMARY
    # ========================================================

    result = {

        "file":
            os.path.basename(filepath),

        "angle":
            angle,

        "distance":
            distance,

        "device":
            TARGET_DEVICE,

        "samples":
            sample_count,

        "mean_rssi":
            mean_rssi,

        "median_rssi":
            median_rssi,

        "std_rssi":
            std_rssi,

        "min_rssi":
            min_rssi,

        "max_rssi":
            max_rssi,

        "rssi_range":
            rssi_range
    }

    return result


# ============================================================
# PROCESS ALL LOG FILES
# ============================================================

def process_all_files():

    # Find every TXT file inside data/
    files = glob.glob(
        os.path.join(
            DATA_FOLDER,
            "*.txt"
        )
    )

    print("\n========================================")
    print("Bluetooth RSSI Analysis")
    print("========================================")

    print(
        f"\nData folder:"
    )

    print(DATA_FOLDER)

    print(
        f"\nFiles found: {len(files)}"
    )

    # --------------------------------------------------------
    # Check files
    # --------------------------------------------------------

    if not files:

        print(
            "\nERROR:"
        )

        print(
            "No .txt files were found "
            "inside the data folder."
        )

        return

    # --------------------------------------------------------
    # Process every file
    # --------------------------------------------------------

    all_results = []

    for filepath in files:

        result = process_file(
            filepath
        )

        if result is not None:

            all_results.append(
                result
            )

    # --------------------------------------------------------
    # Check results
    # --------------------------------------------------------

    if not all_results:

        print(
            "\nNo valid Bluetooth measurements found."
        )

        return

    # ========================================================
    # CREATE SUMMARY DATAFRAME
    # ========================================================

    summary = pd.DataFrame(
        all_results
    )

    # Sort by angle if available
    if "angle" in summary.columns:

        summary = summary.sort_values(
            by="angle",
            na_position="last"
        )

    # ========================================================
    # SAVE SUMMARY CSV
    # ========================================================

    summary_path = os.path.join(
        RESULTS_FOLDER,
        "rssi_summary.csv"
    )

    summary.to_csv(
        summary_path,
        index=False
    )

    print("\n========================================")
    print("SUMMARY")
    print("========================================")

    print(
        summary.to_string(
            index=False
        )
    )

    print(
        f"\nSummary saved to:"
    )

    print(summary_path)

    # ========================================================
    # RSSI VS ANGLE
    # ========================================================

    valid_angle = summary.dropna(
        subset=["angle"]
    )

    # Need at least two different angles
    unique_angles = (
        valid_angle["angle"]
        .nunique()
    )

    if unique_angles >= 2:

        print(
            "\nGenerating RSSI vs Angle plot..."
        )

        # ----------------------------------------------------
        # Plot
        # ----------------------------------------------------

        plt.figure(
            figsize=(9, 5)
        )

        plt.errorbar(

            valid_angle["angle"],

            valid_angle["mean_rssi"],

            yerr=valid_angle["std_rssi"],

            marker="o",

            capsize=5
        )

        plt.xlabel(
            "Angle (degrees)"
        )

        plt.ylabel(
            "Mean RSSI (dBm)"
        )

        plt.title(
            f"{TARGET_DEVICE}: "
            "RSSI vs Angle"
        )

        plt.grid(
            True,
            alpha=0.3
        )

        plt.tight_layout()

        angle_plot_path = os.path.join(
            PLOTS_FOLDER,
            "rssi_vs_angle.png"
        )

        plt.savefig(
            angle_plot_path,
            dpi=300
        )

        plt.close()

        print(
            f"Saved: {angle_plot_path}"
        )

        # ====================================================
        # POLAR PLOT
        # ====================================================

        print(
            "Generating polar plot..."
        )

        angles_rad = np.deg2rad(
            valid_angle["angle"].values
        )

        rssi_values = (
            valid_angle[
                "mean_rssi"
            ].values
        )

        # RSSI is negative.
        # Convert to relative strength
        # for visualization.
        strength = (
            rssi_values
            - rssi_values.min()
            + 1
        )

        plt.figure(
            figsize=(7, 7)
        )

        ax = plt.subplot(
            111,
            projection="polar"
        )

        ax.plot(
            angles_rad,
            strength,
            marker="o"
        )

        ax.set_title(
            f"{TARGET_DEVICE}: "
            "Relative RSSI vs Direction",
            pad=20
        )

        polar_path = os.path.join(
            PLOTS_FOLDER,
            "polar_rssi.png"
        )

        plt.savefig(
            polar_path,
            dpi=300
        )

        plt.close()

        print(
            f"Saved: {polar_path}"
        )

    else:

        print(
            "\nRSSI vs Angle plot was not generated."
        )

        print(
            "Reason: fewer than 2 different "
            "angles were found."
        )

    # ========================================================
    # FINAL MESSAGE
    # ========================================================

    print("\n========================================")
    print("PROCESSING COMPLETE")
    print("========================================")

    print(
        f"\nProcessed device: {TARGET_DEVICE}"
    )

    print(
        f"Output directory: {RESULTS_FOLDER}"
    )

    print(
        "\nGenerated files can be found "
        "inside the results folder."
    )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    process_all_files()