import matplotlib.pyplot as plt
import pandas as pd

def format_items_multiline(items_text, max_per_line=3):
    if not items_text:
        return "None"
    gear_items = items_text.split("+")
    lines = [
        ", ".join(gear_items[i:i + max_per_line])
        for i in range(0, len(gear_items), max_per_line)
    ]
    return "\n".join(lines)


def format_comma_list_multiline(items_text, max_per_line=3):
    if not items_text:
        return "None"
    items = items_text.split(", ")
    lines = [
        ", ".join(items[i:i + max_per_line])
        for i in range(0, len(items), max_per_line)
    ]
    return "\n".join(lines)

def plot_gridsearch(df_results: pd.DataFrame, filter_by):

    if filter_by == "mean":
        filter_key = "mean_dmg"
    elif filter_by == "median":
        filter_key = "median_dmg"
    else:
        raise(f"invalid filter key: {filter_by}")
    
    # Calculate average damage and standard deviation for each configuration
    results_summary = {
        "lts": [],
        "mean_dmg": [],
        "median_dmg": [],
        "std_dev_damage": []
    }

    for idx, row in df_results.iterrows():
        results_summary["lts"].append(row["lt_combo"])
        results_summary["mean_dmg"].append(row["sim_mean_eff_dmg"])
        results_summary["median_dmg"].append(row["sim_median_dmg"])
        results_summary["std_dev_damage"].append(row["sim_std_dmg"])

    summary_df = pd.DataFrame(results_summary)

    # Sort ascending by mean damage
    summary_sorted = summary_df.sort_values(filter_key, ascending=True).reset_index(drop=True)

    # Find top 5 and top 1 based on the *sorted* DataFrame
    top5_value = summary_sorted[filter_key].nlargest(5).min()
    top1_value = summary_sorted[filter_key].max()

    plt.figure(figsize=(13, 15))

    bars = []
    for lts, value, std in zip(
        summary_sorted["lts"],
        summary_sorted[filter_key],
        summary_sorted["std_dev_damage"]
    ):
        if value == top1_value:
            color = "gold"
            edgecolor = "black"
            linewidth = 2
        elif value >= top5_value:
            color = "silver"
            edgecolor = "black"
            linewidth = 1
        else:
            color = "skyblue"
            edgecolor = None
            linewidth = 0
        
        bar = plt.barh(
            lts,
            value,
            xerr=std,
            capsize=5,
            color=color,
            edgecolor=edgecolor,
            linewidth=linewidth,
            zorder=1
        )
        bars.append(bar)

    plt.ylabel("Configuration (LTS)")
    plt.xlabel(f"Average Damage across 100k hits")
    plt.title(f"{filter_key} Damage with Standard Deviation for Each Configuration (Sorted Descending)")

    # Annotate with white-boxed labels
    for bar_group, mean, std in zip(bars, summary_sorted[filter_key], summary_sorted["std_dev_damage"]):
        bar = bar_group[0]
        plt.text(
            bar.get_width() + (0.01 * summary_sorted[filter_key].max()),
            bar.get_y() + bar.get_height() / 2,
            f"{mean:.2f} ± {std:.2f}",
            va='center',
            ha='left',
            fontsize=8,
            zorder=2,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.5, alpha=1)
        )
        
    gear_text = format_items_multiline(df_results["gear_combo"].iloc[0])
    lt_pool_text = format_comma_list_multiline(df_results["lt_pool"].iloc[0], max_per_line=2)
    lt_specific_gear_text = format_items_multiline(
        df_results["lt_specific_gear_combo"].iloc[0],
        max_per_line=2
    )

    plt.figtext(
        0.16, 0.095,
        f"Gear Used:\n{gear_text}",
        ha="center",
        va="top",
        fontsize=9,
        bbox=dict(facecolor="white", edgecolor="gray", alpha=0.9)
    )

    plt.figtext(
        0.5, 0.095,
        f"LTs In Big Comparison:\n{lt_pool_text}",
        ha="center",
        va="top",
        fontsize=9,
        bbox=dict(facecolor="white", edgecolor="gray", alpha=0.9)
    )

    plt.figtext(
        0.84, 0.095,
        f"LT-Specific Gear:\n{lt_specific_gear_text}",
        ha="center",
        va="top",
        fontsize=9,
        bbox=dict(facecolor="white", edgecolor="gray", alpha=0.9)
    )

    plt.tight_layout(rect=[0, 0.11, 1, 1])
    plt.show()
