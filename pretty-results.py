import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import PercentFormatter

# Your data
max_recall=[np.float64(0.2714750643228359), np.float64(0.28795486299006845), np.float64(0.30968574758513495), np.float64(0.33387646012274214), np.float64(0.4596932369338954), np.float64(0.584452470280699)]
max_precision=[np.float64(0.3810927152317881), np.float64(0.3362251655629139), np.float64(0.30701986754966887), np.float64(0.28384933774834437), np.float64(0.2105364238410596), np.float64(0.15481291390728477)]

# Assuming these correspond to different K values or models
x_labels = ['K=5', 'K=10', 'K=15', 'K=20', 'K=50', 'K=100']
# Or if these are for different K values:
k_values = [5, 10, 15, 20, 25, 30]

def create_comprehensive_plots(recall_data, precision_data, x_labels):
    """Create comprehensive visualization of recall and precision metrics"""
    
    # Set up the style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Recall and Precision Metrics Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: Dual-axis line plot
    ax1_line1 = ax1.plot(x_labels, recall_data, 'o-', linewidth=2.5, markersize=8, 
                        label='Recall', color='#2E86AB')
    ax1.set_xlabel('Models / K Values', fontweight='bold')
    ax1.set_ylabel('Recall', color='#2E86AB', fontweight='bold')
    ax1.tick_params(axis='y', labelcolor='#2E86AB')
    ax1.grid(True, alpha=0.3)
    
    ax1_twin = ax1.twinx()
    ax1_line2 = ax1_twin.plot(x_labels, precision_data, 's-', linewidth=2.5, markersize=8, 
                             label='Precision', color='#A23B72')
    ax1_twin.set_ylabel('Precision', color='#A23B72', fontweight='bold')
    ax1_twin.tick_params(axis='y', labelcolor='#A23B72')
    
    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    ax1.set_title('Recall vs Precision Trends', fontweight='bold')
    
    # Plot 2: Side-by-side bar chart
    x_index = np.arange(len(x_labels))
    width = 0.35
    
    bars1 = ax2.bar(x_index - width/2, recall_data, width, label='Recall', 
                   color='#2E86AB', alpha=0.8, edgecolor='black', linewidth=0.5)
    bars2 = ax2.bar(x_index + width/2, precision_data, width, label='Precision', 
                   color='#A23B72', alpha=0.8, edgecolor='black', linewidth=0.5)
    
    ax2.set_xlabel('Models / K Values', fontweight='bold')
    ax2.set_ylabel('Metric Values', fontweight='bold')
    ax2.set_xticks(x_index)
    ax2.set_xticklabels(x_labels)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_title('Side-by-Side Comparison', fontweight='bold')
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom', fontsize=8)
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom', fontsize=8)
    
    # Plot 3: Scatter plot with trend lines
    scatter = ax3.scatter(recall_data, precision_data, s=100, c=range(len(recall_data)), 
                         cmap='viridis', alpha=0.7, edgecolors='black')
    
    # Add labels for each point
    for i, (rec, prec) in enumerate(zip(recall_data, precision_data)):
        ax3.annotate(x_labels[i], (rec, prec), xytext=(5, 5), 
                    textcoords='offset points', fontsize=9, alpha=0.8)
    
    ax3.set_xlabel('Recall', fontweight='bold')
    ax3.set_ylabel('Precision', fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.set_title('Precision-Recall Relationship', fontweight='bold')
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax3)
    cbar.set_label('Model/K Index', fontweight='bold')
    
    # Plot 4: Percentage change analysis
    recall_pct_change = [0] + [((recall_data[i] - recall_data[i-1]) / recall_data[i-1]) * 100 
                              for i in range(1, len(recall_data))]
    precision_pct_change = [0] + [((precision_data[i] - precision_data[i-1]) / precision_data[i-1]) * 100 
                                 for i in range(1, len(precision_data))]
    
    x_index_pct = np.arange(len(x_labels))
    bars3 = ax4.bar(x_index_pct - width/2, recall_pct_change, width, 
                   label='Recall % Change', color='#2E86AB', alpha=0.8)
    bars4 = ax4.bar(x_index_pct + width/2, precision_pct_change, width, 
                   label='Precision % Change', color='#A23B72', alpha=0.8)
    
    ax4.set_xlabel('Models / K Values', fontweight='bold')
    ax4.set_ylabel('Percentage Change (%)', fontweight='bold')
    ax4.set_xticks(x_index_pct)
    ax4.set_xticklabels(x_labels)
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.set_title('Percentage Change Between Models', fontweight='bold')
    
    # Add value labels on percentage bars
    for bar in bars3:
        height = bar.get_height()
        if height != 0:
            ax4.text(bar.get_x() + bar.get_width()/2., height + (1 if height > 0 else -3),
                    f'{height:+.1f}%', ha='center', va='bottom' if height > 0 else 'top', 
                    fontsize=8)
    
    for bar in bars4:
        height = bar.get_height()
        if height != 0:
            ax4.text(bar.get_x() + bar.get_width()/2., height + (1 if height > 0 else -3),
                    f'{height:+.1f}%', ha='center', va='bottom' if height > 0 else 'top', 
                    fontsize=8)
    
    plt.tight_layout()
    plt.show()
    
    # Additional single focused plots
    create_individual_plots(recall_data, precision_data, x_labels)

def create_individual_plots(recall_data, precision_data, x_labels):
    """Create individual focused plots"""
    
    # Plot 1: Recall progression
    plt.figure(figsize=(10, 6))
    plt.plot(x_labels, recall_data, 'o-', linewidth=3, markersize=10, 
             color='#2E86AB', markerfacecolor='white', markeredgewidth=2)
    plt.xlabel('Models / K Values', fontweight='bold', fontsize=12)
    plt.ylabel('Recall', fontweight='bold', fontsize=12)
    plt.title('Recall Metric Progression', fontweight='bold', fontsize=14)
    plt.grid(True, alpha=0.3)
    
    # Add value annotations
    for i, value in enumerate(recall_data):
        plt.annotate(f'{value:.3f}', (x_labels[i], recall_data[i]), 
                    xytext=(0, 10), textcoords='offset points', 
                    ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    # Plot 2: Precision progression
    plt.figure(figsize=(10, 6))
    plt.plot(x_labels, precision_data, 's-', linewidth=3, markersize=10, 
             color='#A23B72', markerfacecolor='white', markeredgewidth=2)
    plt.xlabel('Models / K Values', fontweight='bold', fontsize=12)
    plt.ylabel('Precision', fontweight='bold', fontsize=12)
    plt.title('Precision Metric Progression', fontweight='bold', fontsize=14)
    plt.grid(True, alpha=0.3)
    
    # Add value annotations
    for i, value in enumerate(precision_data):
        plt.annotate(f'{value:.3f}', (x_labels[i], precision_data[i]), 
                    xytext=(0, 10), textcoords='offset points', 
                    ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.show()

def create_summary_statistics(recall_data, precision_data):
    """Print summary statistics"""
    print("="*50)
    print("SUMMARY STATISTICS")
    print("="*50)
    
    print(f"\nRECALL:")
    print(f"  Mean: {np.mean(recall_data):.4f}")
    print(f"  Std:  {np.std(recall_data):.4f}")
    print(f"  Min:  {np.min(recall_data):.4f}")
    print(f"  Max:  {np.max(recall_data):.4f}")
    
    print(f"\nPRECISION:")
    print(f"  Mean: {np.mean(precision_data):.4f}")
    print(f"  Std:  {np.std(precision_data):.4f}")
    print(f"  Min:  {np.min(precision_data):.4f}")
    print(f"  Max:  {np.max(precision_data):.4f}")
    
    print(f"\nTRADE-OFF ANALYSIS:")
    print(f"  Best Recall: {np.max(recall_data):.4f} (Model {np.argmax(recall_data) + 1})")
    print(f"  Best Precision: {np.max(precision_data):.4f} (Model {np.argmax(precision_data) + 1})")
    
    # Calculate correlation
    correlation = np.corrcoef(recall_data, precision_data)[0, 1]
    print(f"  Correlation between Recall and Precision: {correlation:.4f}")

# Generate the plots
create_comprehensive_plots(max_recall, max_precision, x_labels)

# Print summary statistics
create_summary_statistics(max_recall, max_precision)

# If you want to use K values instead of model names, uncomment this:
# create_comprehensive_plots(max_recall, max_precision, [f'K={k}' for k in k_values])