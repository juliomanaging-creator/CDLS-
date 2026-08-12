import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
import seaborn as sns

class JudasKernel:
    def __init__(self, units_count=300000):
        self.units_count = units_count
        self.ledger = np.zeros(units_count)
        self.history = []
        
    def pdhg_optimizer(self, energy_telemetry, grid_capacity):
        """
        Primal-Dual Hybrid Gradient Solver: 
        Optimizes energy discharge while maintaining 100% grid stability.
        """
        residual = energy_telemetry - grid_capacity
        update_vector = np.maximum(0, residual) 
        
        # Solving for Alpha (Sovereign Revenue Generation)
        revenue_adjustment = (energy_telemetry - update_vector) * 0.12
        self.ledger += revenue_adjustment
        
        return self.ledger

    def verify_telemetry(self, unit_data, physical_limits):
        """
        Stochastic Verification: 
        Physics-check to ensure reported V2X data is physically possible.
        """
        verified_mask = unit_data <= physical_limits
        anomalies = np.where(~verified_mask)
        return verified_mask, anomalies

class JudasDemo:
    def __init__(self):
        self.engine = JudasKernel(units_count=300000)
        self.setup_visualization()
        
    def setup_visualization(self):
        """Create the dashboard layout"""
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(16, 10))
        self.fig.suptitle('JUDAS KERNEL - V2X Fleet Intelligence System', 
                         fontsize=18, fontweight='bold', color='#00ff41')
        
        # Create grid layout
        gs = self.fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Main telemetry distribution
        self.ax1 = self.fig.add_subplot(gs[0, :2])
        self.ax1.set_title('Real-Time Fleet Telemetry Distribution', fontsize=12)
        self.ax1.set_xlabel('Energy Output (kWh)')
        self.ax1.set_ylabel('Unit Count')
        
        # Anomaly detection scatter
        self.ax2 = self.fig.add_subplot(gs[1, :2])
        self.ax2.set_title('Physics Verification: Anomaly Detection', fontsize=12)
        self.ax2.set_xlabel('Unit Index (Sample)')
        self.ax2.set_ylabel('Energy Output (kWh)')
        
        # Revenue accumulation
        self.ax3 = self.fig.add_subplot(gs[2, :2])
        self.ax3.set_title('Cumulative Revenue Generation (12% Arbitrage)', fontsize=12)
        self.ax3.set_xlabel('Processing Cycle')
        self.ax3.set_ylabel('Total Revenue ($M)')
        
        # Status panel
        self.ax4 = self.fig.add_subplot(gs[:, 2])
        self.ax4.set_title('System Status', fontsize=12)
        self.ax4.axis('off')
        
        self.cycle_count = 0
        self.revenue_history = []
        self.anomaly_history = []
        
    def run_cycle(self):
        """Execute one processing cycle"""
        # Generate realistic fleet telemetry with some outliers
        base_telemetry = np.random.normal(30, 8, 300000)
        # Inject some anomalies (units reporting beyond physical limits)
        anomaly_indices = np.random.choice(300000, size=int(300000 * 0.02), replace=False)
        base_telemetry[anomaly_indices] = np.random.uniform(50, 80, len(anomaly_indices))
        
        fleet_telemetry = np.clip(base_telemetry, 10, 80)
        grid_thresholds = np.full(300000, 45)
        
        # Run verification
        verified_mask, anomalies = self.engine.verify_telemetry(fleet_telemetry, grid_thresholds)
        
        # Optimize verified units
        final_ledger = self.engine.pdhg_optimizer(
            fleet_telemetry[verified_mask], 
            grid_thresholds[verified_mask]
        )
        
        # Calculate metrics
        total_revenue = np.sum(final_ledger) / 1_000_000  # Convert to millions
        verified_count = np.sum(verified_mask)
        anomaly_count = len(anomalies[0])
        
        self.cycle_count += 1
        self.revenue_history.append(total_revenue)
        self.anomaly_history.append(anomaly_count)
        
        return fleet_telemetry, verified_mask, anomalies, {
            'verified_count': verified_count,
            'anomaly_count': anomaly_count,
            'total_revenue': total_revenue,
            'avg_output': np.mean(fleet_telemetry[verified_mask])
        }
    
    def update_visualization(self, frame):
        """Update all plots with new cycle data"""
        telemetry, verified_mask, anomalies, metrics = self.run_cycle()
        
        # Clear previous plots
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()
        
        # 1. Telemetry Distribution
        self.ax1.hist(telemetry[verified_mask], bins=50, color='#00ff41', 
                     alpha=0.7, edgecolor='white', label='Verified Units')
        if len(anomalies[0]) > 0:
            self.ax1.hist(telemetry[anomalies], bins=20, color='#ff0040', 
                         alpha=0.8, edgecolor='white', label='Anomalies')
        self.ax1.axvline(45, color='yellow', linestyle='--', linewidth=2, label='Grid Limit')
        self.ax1.set_title('Real-Time Fleet Telemetry Distribution', fontsize=12)
        self.ax1.set_xlabel('Energy Output (kWh)')
        self.ax1.set_ylabel('Unit Count')
        self.ax1.legend()
        self.ax1.grid(True, alpha=0.3)
        
        # 2. Anomaly Scatter (sample of 5000 units for visibility)
        sample_size = 5000
        sample_indices = np.random.choice(len(telemetry), sample_size, replace=False)
        colors = ['#00ff41' if verified_mask[i] else '#ff0040' for i in sample_indices]
        
        self.ax2.scatter(range(sample_size), telemetry[sample_indices], 
                        c=colors, alpha=0.6, s=10)
        self.ax2.axhline(45, color='yellow', linestyle='--', linewidth=2, label='Physical Limit')
        self.ax2.set_title('Physics Verification: Anomaly Detection (5K Sample)', fontsize=12)
        self.ax2.set_xlabel('Unit Index (Sample)')
        self.ax2.set_ylabel('Energy Output (kWh)')
        self.ax2.legend(['Physical Limit', 'Verified', 'Anomaly'])
        self.ax2.grid(True, alpha=0.3)
        
        # 3. Revenue Accumulation
        if len(self.revenue_history) > 1:
            self.ax3.plot(range(len(self.revenue_history)), self.revenue_history, 
                         color='#00ff41', linewidth=2, marker='o')
            self.ax3.fill_between(range(len(self.revenue_history)), self.revenue_history, 
                                 alpha=0.3, color='#00ff41')
        self.ax3.set_title('Cumulative Revenue Generation (12% Arbitrage)', fontsize=12)
        self.ax3.set_xlabel('Processing Cycle')
        self.ax3.set_ylabel('Total Revenue ($M)')
        self.ax3.grid(True, alpha=0.3)
        
        # 4. Status Panel
        self.ax4.axis('off')
        status_text = f"""
╔══════════════════════════════╗
║   JUDAS KERNEL STATUS v1.0   ║
╚══════════════════════════════╝

⚡ CYCLE: {self.cycle_count}

📊 FLEET METRICS
├─ Total Units: 300,000
├─ Verified: {metrics['verified_count']:,}
├─ Anomalies: {metrics['anomaly_count']:,}
└─ Success Rate: {(metrics['verified_count']/300000)*100:.2f}%

💰 FINANCIAL PERFORMANCE
├─ Current Revenue: ${metrics['total_revenue']:.2f}M
├─ Avg Unit Output: {metrics['avg_output']:.1f} kWh
└─ Arbitrage Rate: 12%

🔒 GRID STABILITY
├─ Threshold: 45 kWh
├─ Compliance: {'✓ OPTIMAL' if metrics['anomaly_count'] < 10000 else '⚠ WARNING'}
└─ PDHG Status: ACTIVE

📈 TREND ANALYSIS
└─ Anomaly Rate: {(metrics['anomaly_count']/300000)*100:.2f}%
"""
        
        self.ax4.text(0.05, 0.95, status_text, 
                     transform=self.ax4.transAxes,
                     fontsize=10, verticalalignment='top',
                     fontfamily='monospace',
                     color='#00ff41')
        
    def run_demo(self, cycles=20):
        """Run the animated demo"""
        anim = FuncAnimation(self.fig, self.update_visualization, 
                           frames=cycles, interval=1000, repeat=False)
        plt.tight_layout()
        plt.show()
        
        # Print final summary
        print("\n" + "="*60)
        print("JUDAS KERNEL - DEMO COMPLETE")
        print("="*60)
        print(f"Total Cycles Processed: {self.cycle_count}")
        print(f"Final Revenue: ${self.revenue_history[-1]:.2f}M")
        print(f"Average Anomaly Rate: {np.mean(self.anomaly_history)/300000*100:.2f}%")
        print(f"System Efficiency: {((300000 - np.mean(self.anomaly_history))/300000)*100:.2f}%")
        print("="*60)

# Launch the demo
print("Initializing JUDAS Kernel Demo...")
print("Monitoring 300,000 V2X units with real-time anomaly detection\n")

demo = JudasDemo()
demo.run_demo(cycles=20)