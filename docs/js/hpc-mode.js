/**
 * HPC Mode Enhancements
 * Additional functionality specific to HPC job scheduling context
 */

class HPCEnhancements {
    constructor(uiController) {
        this.ui = uiController;
        this.initializeHPCFeatures();
    }

    initializeHPCFeatures() {
        // Add HPC-specific event listeners and setup
        this.setupHPCEducationalMessages();
        this.addHPCContextualHelp();
    }

    setupHPCEducationalMessages() {
        // Enhanced educational messages for HPC context
        this.hpcInsights = {
            stable_low: "💡 UNDERUTILIZED: Cluster has spare capacity - consider workload optimization",
            stable_good: "✅ OPTIMAL: Good balance of throughput and responsiveness",
            stable_high: "⚡ BUSY: High utilization - monitor queue growth carefully",
            critical: "⚠️ CRITICAL: Near capacity limit - small increases cause long waits",
            unstable: "🚨 OVERLOADED: Job queue growing - need more nodes or job limits",
            maintenance: "🔧 MAINTENANCE: Reduced capacity - expect longer wait times"
        };

        this.hpcEducation = {
            little_law: "Jobs in system = Submission rate × Average completion time",
            utilization: "HPC clusters typically target 80-90% utilization for stability",
            queue_growth: "This is why clusters implement job limits and priority scheduling",
            wait_times: "Queue wait time grows exponentially near 100% utilization",
            capacity_planning: "Adding 10% capacity can reduce wait times by 50%+"
        };
    }

    addHPCContextualHelp() {
        // Add tooltips and contextual help for HPC mode
        this.addTooltips();
        this.addHPCGlossary();
    }

    addTooltips() {
        const tooltips = {
            'arrivalRate': 'Job submission rate - how fast users submit jobs to the cluster',
            'serviceRate': 'Job completion rate - cluster throughput capacity',
            'hpcMode': 'Switch between traditional queueing theory and HPC job scheduler terminology',
            'queueDisplay': 'Jobs waiting in the scheduler queue for available compute nodes',
            'serverStatus': 'Cluster compute status - busy processing jobs or idle'
        };

        Object.entries(tooltips).forEach(([elementId, tooltip]) => {
            const element = document.getElementById(elementId);
            if (element) {
                element.title = tooltip;
                element.addEventListener('mouseenter', (e) => this.showTooltip(e, tooltip));
                element.addEventListener('mouseleave', () => this.hideTooltip());
            }
        });
    }

    showTooltip(event, text) {
        // Create and show tooltip
        const tooltip = document.createElement('div');
        tooltip.className = 'hpc-tooltip';
        tooltip.textContent = text;
        tooltip.style.cssText = `
            position: absolute;
            background: #333;
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 0.8rem;
            z-index: 1000;
            max-width: 250px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            pointer-events: none;
        `;
        
        document.body.appendChild(tooltip);
        
        const rect = event.target.getBoundingClientRect();
        tooltip.style.left = (rect.left + rect.width / 2 - tooltip.offsetWidth / 2) + 'px';
        tooltip.style.top = (rect.top - tooltip.offsetHeight - 8) + 'px';
        
        this.currentTooltip = tooltip;
    }

    hideTooltip() {
        if (this.currentTooltip) {
            this.currentTooltip.remove();
            this.currentTooltip = null;
        }
    }

    addHPCGlossary() {
        // Add expandable HPC glossary to the page
        const glossaryHTML = `
            <div class="hpc-glossary" style="margin-top: 2rem;">
                <details>
                    <summary style="cursor: pointer; font-weight: bold; color: #007bff;">
                        📚 HPC Terms Glossary
                    </summary>
                    <div style="margin-top: 1rem; padding: 1rem; background: #f8f9fa; border-radius: 0.375rem;">
                        <dl style="margin: 0;">
                            <dt><strong>Job Submission Rate (λ)</strong></dt>
                            <dd>How frequently users submit jobs to the cluster (jobs per hour)</dd>
                            
                            <dt><strong>Job Completion Rate (μ)</strong></dt>
                            <dd>Cluster's maximum processing capacity (jobs per hour)</dd>
                            
                            <dt><strong>Load Factor (ρ = λ/μ)</strong></dt>
                            <dd>System utilization ratio - should stay below 1.0 for stability</dd>
                            
                            <dt><strong>Queue Wait Time</strong></dt>
                            <dd>Time a job spends waiting for available compute nodes</dd>
                            
                            <dt><strong>Job Runtime</strong></dt>
                            <dd>Time a job spends actually executing on compute nodes</dd>
                            
                            <dt><strong>Little's Law</strong></dt>
                            <dd>Jobs in system = Submission rate × Average total time</dd>
                        </dl>
                    </div>
                </details>
            </div>
        `;

        const footer = document.querySelector('.footer');
        if (footer) {
            footer.insertAdjacentHTML('beforebegin', glossaryHTML);
        }
    }

    getHPCInsight(rho, customersServed) {
        if (customersServed < 10) {
            return "🔄 INITIALIZING: Gathering initial job statistics...";
        }

        if (rho >= 1.0) {
            return this.hpcInsights.unstable;
        } else if (rho > 0.95) {
            return this.hpcInsights.critical;
        } else if (rho > 0.85) {
            return this.hpcInsights.stable_high;
        } else if (rho < 0.5) {
            return this.hpcInsights.stable_low;
        } else {
            return this.hpcInsights.stable_good;
        }
    }

    formatHPCTime(timeValue, abbreviated = false) {
        if (timeValue < 0.01) {
            return abbreviated ? "0h" : "0.0 hours";
        } else if (timeValue < 1.0) {
            const minutes = Math.round(timeValue * 60);
            return abbreviated ? `${minutes}m` : `${minutes} minutes`;
        } else {
            return abbreviated ? `${timeValue.toFixed(1)}h` : `${timeValue.toFixed(1)} hours`;
        }
    }

    generateHPCReport(stats) {
        if (!stats || !this.ui.hpcMode) return null;

        const rho = this.ui.simulator.arrivalRate / this.ui.simulator.serviceRate;
        const report = {
            cluster_status: rho >= 1.0 ? "OVERLOADED" : rho > 0.9 ? "CRITICAL" : "STABLE",
            utilization_target: "80-90%",
            current_utilization: `${(stats.avgUtilization * 100).toFixed(1)}%`,
            jobs_per_day: Math.round(this.ui.simulator.arrivalRate * 24),
            capacity_per_day: Math.round(this.ui.simulator.serviceRate * 24),
            estimated_wait: this.formatHPCTime(stats.avgWaitTime),
            insight: this.getHPCInsight(rho, stats.customersServed)
        };

        return report;
    }

    addHPCVisualizationEnhancements() {
        // Add HPC-specific visual elements
        this.addClusterUtilizationMeter();
        this.addJobQueueVisualization();
    }

    addClusterUtilizationMeter() {
        const meterHTML = `
            <div class="cluster-utilization-meter" style="margin: 1rem 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Cluster Utilization</span>
                    <span id="utilizationPercent">0%</span>
                </div>
                <div style="background: #e9ecef; height: 20px; border-radius: 10px; overflow: hidden;">
                    <div id="utilizationBar" style="height: 100%; background: linear-gradient(90deg, #28a745 0%, #ffc107 70%, #dc3545 90%); width: 0%; transition: width 0.3s ease;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #666; margin-top: 0.25rem;">
                    <span>0%</span>
                    <span>Target: 80-90%</span>
                    <span>100%</span>
                </div>
            </div>
        `;

        const statsDisplay = document.getElementById('statsDisplay');
        if (statsDisplay) {
            statsDisplay.insertAdjacentHTML('afterend', meterHTML);
        }
    }

    updateUtilizationMeter(utilization) {
        const bar = document.getElementById('utilizationBar');
        const percent = document.getElementById('utilizationPercent');
        
        if (bar && percent) {
            const percentage = Math.round(utilization * 100);
            bar.style.width = `${percentage}%`;
            percent.textContent = `${percentage}%`;
            
            // Color coding based on HPC best practices
            if (percentage > 95) {
                bar.style.background = '#dc3545'; // Red - overloaded
            } else if (percentage > 85) {
                bar.style.background = '#ffc107'; // Yellow - high
            } else if (percentage > 70) {
                bar.style.background = '#28a745'; // Green - good
            } else {
                bar.style.background = '#17a2b8'; // Blue - underutilized
            }
        }
    }

    addJobQueueVisualization() {
        // Enhanced queue visualization for HPC context
        // This could include job priority indicators, estimated wait times, etc.
        // Implementation would extend the existing queue display
    }
}

// Initialize HPC enhancements when UI controller is ready
document.addEventListener('DOMContentLoaded', () => {
    // Wait for UI controller to be initialized
    setTimeout(() => {
        if (window.uiController) {
            window.hpcEnhancements = new HPCEnhancements(window.uiController);
        }
    }, 100);
});