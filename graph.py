import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os


class EVSalesVisualizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EV Sales Analysis - Data Visualization")
        # Make window fullscreen
        self.root.state('zoomed')
        self.root.geometry("1920x1080")
        
        # Load dataset
        self.df = pd.read_csv("dataset.csv")
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_tabs()
    
    def create_tabs(self):
        """Create 5 tabs for different graphs"""
        # Configure notebook style with smaller font, light gray background and black text
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), padding=[15, 10], background='lightgray', foreground='black')
        style.configure('TNotebook', background='lightgray')
        
        # Tab 1: Customer Segment Pie Chart
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Pie Graph")
        self.create_customer_segment_chart(self.tab1)
        
        # Tab 2: Region Sales Area Chart
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Stacked Area Graph")
        self.create_region_sales_chart(self.tab2)
        
        # Tab 3: Top 5 Brands Radar Chart
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="Radar Graph")
        self.create_top_brands_radar_chart(self.tab3)
        
        # Tab 4: Discount Percentage Control Chart
        self.tab4 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab4, text="Control Graph")
        self.create_control_chart(self.tab4)
        
        # Tab 5: Scatter Plot - Discount vs Units Sold
        self.tab5 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab5, text="Scatter Plot Graph")
        self.create_scatter_plot(self.tab5)
        
        # Tab 6: Correlation Heatmap
        self.tab6 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab6, text="Heatmap Graph")
        self.create_correlation_heatmap(self.tab6)
    
    def create_customer_segment_chart(self, parent):
        """Create pie chart for customer segment distribution"""
        # Count customer segments
        segment_counts = self.df['Customer_Segment'].value_counts()
        
        # Create figure with larger size
        fig = Figure(figsize=(10.2, 7.27), dpi=100)
        ax = fig.add_subplot(111)
        
        # Create pie chart
        colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFD700', '#FF99CC']
        wedges, texts, autotexts = ax.pie(
            segment_counts.values,
            labels=segment_counts.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors[:len(segment_counts)]
        )
        
        # Enhance text appearance with larger fonts
        for text in texts:
            text.set_fontsize(16)
            text.set_weight('bold')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(14)
            autotext.set_weight('bold')
        
        ax.set_title('Customer Segment Distribution', fontsize=20, fontweight='bold', pad=20)
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_region_sales_chart(self, parent):
        """Create stacked area chart for sales by region"""
        # Get unique regions
        regions = self.df['Region'].unique()
        
        # Define colors for each region
        colors_map = {
            'North America': '#FF6B6B',
            'Oceania': '#4ECDC4',
            'Europe': '#BA55D3',
            'Asia': '#FFA07A',
            'Africa': '#228B22',
            'South America': '#F7DC6F'
        }
        
        # Create figure with larger size
        fig = Figure(figsize=(10.2, 7.27), dpi=100)
        ax = fig.add_subplot(111)
        
        # Get month-region data for stacked areas
        self.df['YearMonth'] = pd.to_datetime(self.df['Date']).dt.to_period('M')
        region_monthly = self.df.groupby(['YearMonth', 'Region'])['Revenue'].sum().unstack(fill_value=0)
        region_monthly.index = region_monthly.index.to_timestamp()
        
        # Prepare data for stacked area chart
        x = range(len(region_monthly))
        colors_list = [colors_map.get(region, '#808080') for region in region_monthly.columns]
        
        # Create stacked area chart
        ax.stackplot(
            x,
            *[region_monthly[region].values for region in region_monthly.columns],
            labels=region_monthly.columns,
            colors=colors_list,
            alpha=0.7
        )
        
        # Customize chart
        ax.set_xticks(range(len(region_monthly)))
        ax.set_xticklabels([date.strftime('%Y-%m') for date in region_monthly.index], fontsize=8, fontweight='bold', rotation=45)
        ax.set_ylabel('Total Revenue', fontsize=12, fontweight='bold')
        ax.set_title('Sales Revenue by Region (Stacked)', fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Format y-axis labels
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
        ax.tick_params(axis='y', labelsize=10)
        
        # Add legend with region names and colors on the side
        legend = ax.legend(
            loc='center left',
            bbox_to_anchor=(1.05, 0.5),
            fontsize=11,
            frameon=True,
            fancybox=True,
            shadow=True
        )
        
        # Make legend more readable
        for text in legend.get_texts():
            text.set_weight('bold')
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_vehicle_type_radar_chart(self, parent):
        """Create radar chart for vehicle types with multiple metrics"""
        import numpy as np
        
        # Get vehicle types
        vehicle_types = self.df['Vehicle_Type'].unique()
        
        # Define colors for each vehicle type
        colors_vehicle = {
            'Sedan': '#FF6B6B',
            'SUV': '#4ECDC4',
            'Coupe': '#BA55D3',
            'Truck': '#FFA07A',
            'Crossover': '#228B22',
            'Hatchback': '#F7DC6F'
        }
        
        # Calculate metrics for each vehicle type
        metrics = ['Avg Battery Capacity', 'Avg Discount %', 'Avg Units Sold', 'Avg Revenue (M)', 'Fast Charge %']
        
        vehicle_metrics = {}
        for vehicle_type in vehicle_types:
            vehicle_data = self.df[self.df['Vehicle_Type'] == vehicle_type]
            
            # Calculate normalized metrics (0-10 scale for better visualization)
            avg_battery = (vehicle_data['Battery_Capacity_kWh'].mean() / 100) * 10
            avg_discount = vehicle_data['Discount_Percentage'].mean()
            avg_units = (vehicle_data['Units_Sold'].mean() / 400) * 10
            avg_revenue = vehicle_data['Revenue'].mean() / 1e6
            fast_charge_pct = (vehicle_data['Fast_Charging_Option'].eq('Yes').sum() / len(vehicle_data)) * 10
            
            vehicle_metrics[vehicle_type] = [avg_battery, avg_discount, avg_units, avg_revenue, fast_charge_pct]
        
        # Create radar chart
        fig = Figure(figsize=(10.2, 7.27), dpi=100)
        ax = fig.add_subplot(111, projection='polar')
        
        # Number of variables
        num_vars = len(metrics)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        # Plot each vehicle type
        for vehicle_type, values in vehicle_metrics.items():
            values += values[:1]  # Complete the circle
            ax.plot(angles, values, 'o-', linewidth=2, label=vehicle_type, 
                   color=colors_vehicle.get(vehicle_type, '#808080'))
            ax.fill(angles, values, alpha=0.25, color=colors_vehicle.get(vehicle_type, '#808080'))
        
        # Customize chart
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics, fontsize=11, fontweight='bold')
        ax.set_ylim(0, 10)
        ax.set_yticks([2, 4, 6, 8, 10])
        ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=9)
        ax.grid(True, alpha=0.3)
        
        # Add title and legend
        ax.set_title('Vehicle Type Comparison - Radar Chart', fontsize=16, fontweight='bold', pad=20)
        legend = ax.legend(
            loc='upper left',
            bbox_to_anchor=(1.1, 1.1),
            fontsize=11,
            frameon=True,
            fancybox=True,
            shadow=True
        )
        
        for text in legend.get_texts():
            text.set_weight('bold')
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_top_brands_radar_chart(self, parent):
        """Create radar chart for top 5 brands by total units sold"""
        import numpy as np
        
        # Get top 5 brands by total units sold
        brand_units = self.df.groupby('Brand')['Units_Sold'].sum().sort_values(ascending=False)
        top_5_brands = brand_units.head(5)
        
        # Define colors for each brand
        colors_brands = {
            'Toyota': '#FF6B6B',
            'Tesla': '#4ECDC4',
            'BYD': '#BA55D3',
            'Ford': '#FFA07A',
            'Kia': '#228B22',
            'Nissan': '#F7DC6F',
            'Volkswagen': '#FFB347',
            'BMW': '#87CEEB',
            'Hyundai': '#DDA0DD'
        }
        
        # Create radar chart
        fig = Figure(figsize=(10.2, 7.27), dpi=100)
        ax = fig.add_subplot(111, projection='polar')
        
        # Number of brands
        num_brands = len(top_5_brands)
        angles = np.linspace(0, 2 * np.pi, num_brands, endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        # Prepare values (normalize for better visualization)
        values = (top_5_brands.values / top_5_brands.max() * 10).tolist()
        values += values[:1]  # Complete the circle
        
        # Plot the radar area
        ax.plot(angles, values, 'o-', linewidth=2.5, color='#0066CC', markersize=8)
        ax.fill(angles, values, alpha=0.4, color='#66B2FF')
        
        # Customize chart
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(top_5_brands.index, fontsize=13, fontweight='bold')
        ax.set_ylim(0, 10)
        ax.set_yticks([2, 4, 6, 8, 10])
        ax.set_yticklabels(['2k', '4k', '6k', '8k', '10k'], fontsize=9)
        ax.grid(True, alpha=0.3)
        
        # Add title
        ax.set_title('Top 5 Brands by Total Units Sold', fontsize=16, fontweight='bold', pad=20)
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_control_chart(self, parent):
        """Create control chart for average discount percentage over time"""
        import numpy as np
        
        # Get monthly average discount percentage
        self.df['YearMonth'] = pd.to_datetime(self.df['Date']).dt.to_period('M')
        monthly_discount = self.df.groupby('YearMonth')['Discount_Percentage'].mean()
        monthly_discount.index = monthly_discount.index.to_timestamp()
        
        # Calculate statistics
        mean = monthly_discount.mean()
        std_dev = monthly_discount.std()
        ucl = mean + 3 * std_dev  # Upper Control Limit
        lcl = mean - 3 * std_dev  # Lower Control Limit
        
        # Ensure LCL doesn't go below 0
        lcl = max(lcl, 0)
        
        # Create figure
        fig = Figure(figsize=(10.2, 7.27), dpi=100)
        ax = fig.add_subplot(111)
        
        # Plot data points
        x = range(len(monthly_discount))
        ax.plot(x, monthly_discount.values, 'o-', linewidth=2, color='#0066CC', markersize=8, label='Avg Discount %')
        
        # Plot control limits
        ax.axhline(y=mean, color='green', linestyle='-', linewidth=2.5, label='Center Line (Mean)', alpha=0.8)
        ax.axhline(y=ucl, color='red', linestyle='--', linewidth=2, label='UCL (Mean + 3σ)', alpha=0.8)
        ax.axhline(y=lcl, color='red', linestyle='--', linewidth=2, label='LCL (Mean - 3σ)', alpha=0.8)
        
        # Shade out-of-control region
        ax.fill_between(x, lcl, ucl, alpha=0.1, color='green', label='Control Region')
        
        # Highlight points outside control limits
        out_of_control = monthly_discount[(monthly_discount > ucl) | (monthly_discount < lcl)]
        if len(out_of_control) > 0:
            out_x = [monthly_discount.index.get_loc(idx) for idx in out_of_control.index]
            ax.scatter(out_x, out_of_control.values, color='red', s=150, marker='X', 
                      zorder=5, label='Out of Control')
        
        # Customize chart
        ax.set_xticks(x[::2])  # Show every 2nd month
        ax.set_xticklabels([date.strftime('%Y-%m') for date in monthly_discount.index[::2]], 
                           fontsize=8, fontweight='bold', rotation=45)
        ax.set_xlabel('Month', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Discount %', fontsize=12, fontweight='bold')
        ax.set_title('Control Chart - Average Discount Percentage', fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Add legend
        legend = ax.legend(loc='upper left', fontsize=10, frameon=True, fancybox=True, shadow=True)
        for text in legend.get_texts():
            text.set_weight('bold')
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_scatter_plot(self, parent):
        """Create scatter plot - Units Sold vs Discount Percentage for Asia region only"""
        
        # Filter data for Asia region only
        asia_data = self.df[self.df['Region'] == 'Asia']
        
        # Create figure
        fig = Figure(figsize=(10.2, 7.27), dpi=100)
        ax = fig.add_subplot(111)
        
        # Plot scatter points
        ax.scatter(
            asia_data['Discount_Percentage'],
            asia_data['Units_Sold'],
            alpha=0.6,
            s=100,
            color='#FFA07A',
            edgecolors='black',
            linewidth=0.5,
            label='Asia Region'
        )
        
        # Customize chart
        ax.set_xlabel('Discount Percentage (%)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Units Sold', fontsize=12, fontweight='bold')
        ax.set_title('Discount Percentage vs Units Sold - Asia Region', fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.tick_params(axis='both', labelsize=10)
        
        # Add legend
        legend = ax.legend(
            loc='upper left',
            fontsize=11,
            frameon=True,
            fancybox=True,
            shadow=True
        )
        for text in legend.get_texts():
            text.set_weight('bold')
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_correlation_heatmap(self, parent):
        """Create correlation heatmap showing relationships between numeric variables"""
        import numpy as np
        
        # Select numeric columns for correlation analysis
        numeric_cols = self.df[['Battery_Capacity_kWh', 'Discount_Percentage', 'Units_Sold', 'Revenue']].copy()
        
        # Add derived metric: Find if Fast_Charging_Option correlates with other variables
        self.df['Has_Fast_Charging'] = (self.df['Fast_Charging_Option'] == 'Yes').astype(int)
        numeric_cols['Fast_Charging'] = self.df['Has_Fast_Charging']
        
        # Calculate correlation matrix
        correlation_matrix = numeric_cols.corr()
        
        # Create figure
        fig = Figure(figsize=(10.2, 7.27), dpi=100)
        ax = fig.add_subplot(111)
        
        # Create heatmap using imshow
        im = ax.imshow(correlation_matrix, cmap='RdYlGn', aspect='auto', vmin=-1, vmax=1)
        
        # Set ticks and labels
        ax.set_xticks(range(len(correlation_matrix.columns)))
        ax.set_yticks(range(len(correlation_matrix.columns)))
        ax.set_xticklabels(correlation_matrix.columns, fontsize=11, fontweight='bold', rotation=45, ha='right')
        ax.set_yticklabels(correlation_matrix.columns, fontsize=11, fontweight='bold')
        
        # Add correlation values as text
        for i in range(len(correlation_matrix)):
            for j in range(len(correlation_matrix)):
                value = correlation_matrix.iloc[i, j]
                text_color = 'white' if abs(value) > 0.5 else 'black'
                text = ax.text(j, i, f'{value:.2f}', ha='center', va='center',
                             color=text_color, fontsize=12, fontweight='bold')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Correlation Coefficient', fontsize=11, fontweight='bold')
        cbar.ax.tick_params(labelsize=10)
        
        # Customize chart
        ax.set_title('Correlation Heatmap - Key Variables', fontsize=16, fontweight='bold', pad=20)
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_placeholder(self, parent, title):
        """Create placeholder for future graphs"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        label = ttk.Label(
            frame,
            text=f"{title}\n\nGraph to be added",
            font=("Arial", 36, "bold"),
            foreground="gray"
        )
        label.pack(expand=True)


def main():
    root = tk.Tk()
    app = EVSalesVisualizationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
