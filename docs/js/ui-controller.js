/**
 * UI Controller for M/M/1 Web Simulator
 * Manages interface interactions and display updates
 */

class UIController {
    constructor() {
        console.log('UIController constructor called');
        this.simulator = null;
        this.isRunning = false;
        this.animationId = null;
        this.hpcMode = false;
        this.timeUnit = "time units";
        this.rateUnit = "customers/time";
        this.terminology = this.getTerminologyMap();
        
        try {
            this.initializeElements();
            this.setupEventListeners();
            this.loadDefaultScenario();
            console.log('UIController initialization complete');
        } catch (e) {
            console.error('Error during UIController initialization:', e);
        }
    }

    initializeElements() {
        console.log('Initializing elements...');
        
        // Control elements
        this.arrivalRateSlider = document.getElementById('arrivalRate');
        this.serviceRateSlider = document.getElementById('serviceRate');
        this.arrivalRateValue = document.getElementById('arrivalRateValue');
        this.serviceRateValue = document.getElementById('serviceRateValue');
        this.startBtn = document.getElementById('startBtn');
        this.resetBtn = document.getElementById('resetBtn');
        this.stepBtn = document.getElementById('stepBtn');
        this.hpcToggle = document.getElementById('hpcMode');
        this.scenarioSelect = document.getElementById('scenarioSelect');

        // Display elements
        this.queueDisplay = document.getElementById('queueDisplay');
        this.serverStatus = document.getElementById('serverStatus');
        this.statsDisplay = document.getElementById('statsDisplay');
        this.educationalDisplay = document.getElementById('educationalDisplay');
        this.graphCanvas = document.getElementById('queueGraph');
        
        // Check for missing elements
        const requiredElements = {
            'arrivalRateSlider': this.arrivalRateSlider,
            'serviceRateSlider': this.serviceRateSlider,
            'startBtn': this.startBtn,
            'scenarioSelect': this.scenarioSelect,
            'queueDisplay': this.queueDisplay,
            'statsDisplay': this.statsDisplay
        };
        
        for (const [name, element] of Object.entries(requiredElements)) {
            if (!element) {
                console.error(`Missing element: ${name}`);
            }
        }
        
        // Initialize canvas
        if (this.graphCanvas) {
            this.graphContext = this.graphCanvas.getContext('2d');
            this.setupCanvas();
        } else {
            console.warn('queueGraph canvas not found');
        }
        
        console.log('Elements initialized');
    }

    setupCanvas() {
        // Set canvas size
        this.graphCanvas.width = this.graphCanvas.offsetWidth * window.devicePixelRatio;
        this.graphCanvas.height = this.graphCanvas.offsetHeight * window.devicePixelRatio;
        this.graphContext.scale(window.devicePixelRatio, window.devicePixelRatio);
        
        // Set display size
        this.graphCanvas.style.width = this.graphCanvas.offsetWidth + 'px';
        this.graphCanvas.style.height = this.graphCanvas.offsetHeight + 'px';
    }

    setupEventListeners() {
        console.log('Setting up event listeners...');
        
        // Parameter sliders
        if (this.arrivalRateSlider) {
            this.arrivalRateSlider.addEventListener('input', () => this.updateArrivalRate());
        }
        if (this.serviceRateSlider) {
            this.serviceRateSlider.addEventListener('input', () => this.updateServiceRate());
        }
        
        // Control buttons
        if (this.startBtn) {
            this.startBtn.addEventListener('click', () => this.toggleSimulation());
        }
        if (this.resetBtn) {
            this.resetBtn.addEventListener('click', () => this.resetSimulation());
        }
        if (this.stepBtn) {
            this.stepBtn.addEventListener('click', () => this.stepSimulation());
        }
        
        // Mode and scenario selection
        if (this.hpcToggle) {
            this.hpcToggle.addEventListener('change', () => this.toggleHPCMode());
        }
        if (this.scenarioSelect) {
            this.scenarioSelect.addEventListener('change', () => this.loadScenario());
        }
        
        // Window resize
        window.addEventListener('resize', () => {
            if (this.graphCanvas) {
                this.setupCanvas();
            }
        });
        
        console.log('Event listeners set up');
    }

    getTerminologyMap() {
        if (this.hpcMode) {
            return {
                customer: 'job',
                customers: 'jobs',
                server: 'cluster',
                queue: 'job queue',
                service_time: 'runtime',
                wait_time: 'queue wait',
                arrival_rate: 'submission rate',
                service_rate: 'completion rate',
                utilization: 'cluster utilization',
                arrivals: 'submissions',
                served: 'completed',
                simulator: 'scheduler'
            };
        } else {
            return {
                customer: 'customer',
                customers: 'customers',
                server: 'server',
                queue: 'queue',
                service_time: 'service time',
                wait_time: 'wait time',
                arrival_rate: 'arrival rate',
                service_rate: 'service rate',
                utilization: 'utilization',
                arrivals: 'arrivals',
                served: 'served',
                simulator: 'simulator'
            };
        }
    }

    term(key) {
        return this.terminology[key] || key;
    }

    loadDefaultScenario() {
        console.log('Loading default scenario...');
        this.simulator = new MM1Queue(2.0, 2.5);
        console.log('Simulator created:', this.simulator);
        this.updateParameterDisplays();
        this.updateScenarioOptions(); // Initialize scenario options
        this.updateDisplay();
        console.log('Default scenario loaded');
    }

    updateArrivalRate() {
        const rate = parseFloat(this.arrivalRateSlider.value);
        this.arrivalRateValue.textContent = rate.toFixed(1);
        if (this.simulator) {
            this.simulator.setParameters(rate, this.simulator.serviceRate);
        }
    }

    updateServiceRate() {
        const rate = parseFloat(this.serviceRateSlider.value);
        this.serviceRateValue.textContent = rate.toFixed(1);
        if (this.simulator) {
            this.simulator.setParameters(this.simulator.arrivalRate, rate);
        }
    }

    updateParameterDisplays() {
        if (this.simulator) {
            this.arrivalRateSlider.value = this.simulator.arrivalRate;
            this.serviceRateSlider.value = this.simulator.serviceRate;
            this.arrivalRateValue.textContent = this.simulator.arrivalRate.toFixed(1);
            this.serviceRateValue.textContent = this.simulator.serviceRate.toFixed(1);
        }
    }

    toggleSimulation() {
        if (this.isRunning) {
            this.stopSimulation();
        } else {
            this.startSimulation();
        }
    }

    startSimulation() {
        console.log('Starting simulation...');
        this.isRunning = true;
        this.startBtn.textContent = 'Pause';
        this.startBtn.classList.remove('btn-primary');
        this.startBtn.classList.add('btn-warning');
        console.log('About to call animate()');
        this.animate();
    }

    stopSimulation() {
        this.isRunning = false;
        this.startBtn.textContent = 'Start';
        this.startBtn.classList.remove('btn-warning');
        this.startBtn.classList.add('btn-primary');
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
    }

    resetSimulation() {
        this.stopSimulation();
        if (this.simulator) {
            this.simulator.reset();
            this.updateDisplay();
        }
    }

    stepSimulation() {
        if (this.simulator) {
            this.simulator.step();
            this.updateDisplay();
        }
    }

    toggleHPCMode() {
        this.hpcMode = this.hpcToggle.checked;
        this.timeUnit = this.hpcMode ? "hours" : "time units";
        this.rateUnit = this.hpcMode ? "jobs/hr" : "customers/time";
        this.terminology = this.getTerminologyMap();
        
        // Update scenario options
        this.updateScenarioOptions();
        
        // Update all display elements
        this.updateDisplay();
        this.updateLabels();
    }

    updateScenarioOptions() {
        // Clear existing options
        this.scenarioSelect.innerHTML = '<option value="">Choose a scenario...</option>';
        
        if (this.hpcMode) {
            // Add HPC scenarios
            if (typeof HPC_SCENARIOS !== 'undefined') {
                Object.entries(HPC_SCENARIOS).forEach(([key, scenario]) => {
                    const option = document.createElement('option');
                    option.value = key;
                    option.textContent = `${key.charAt(0).toUpperCase() + key.slice(1)} (ρ=${(scenario.arrivalRate/scenario.serviceRate).toFixed(2)})`;
                    this.scenarioSelect.appendChild(option);
                });
                console.log(`Added ${Object.keys(HPC_SCENARIOS).length} HPC scenarios`);
            } else {
                console.error('HPC_SCENARIOS not defined');
            }
        } else {
            // Add traditional scenarios
            const scenarios = [
                { key: 'stable_low', rate1: 1.5, rate2: 3.0, desc: 'Stable Low (ρ=0.50)' },
                { key: 'stable_med', rate1: 2.0, rate2: 2.5, desc: 'Stable Medium (ρ=0.80)' },
                { key: 'stable_high', rate1: 2.8, rate2: 3.0, desc: 'Stable High (ρ=0.93)' },
                { key: 'critical', rate1: 2.95, rate2: 3.0, desc: 'Critical (ρ=0.98)' },
                { key: 'unstable', rate1: 3.1, rate2: 3.0, desc: 'Unstable (ρ=1.03)' }
            ];
            
            scenarios.forEach(scenario => {
                const option = document.createElement('option');
                option.value = scenario.key;
                option.textContent = scenario.desc;
                option.dataset.arrival = scenario.rate1;
                option.dataset.service = scenario.rate2;
                this.scenarioSelect.appendChild(option);
            });
            console.log(`Added ${scenarios.length} traditional scenarios`);
        }
    }

    loadScenario() {
        const selectedValue = this.scenarioSelect.value;
        if (!selectedValue) return;

        // Stop any running simulation
        this.stopSimulation();

        if (this.hpcMode && HPC_SCENARIOS[selectedValue]) {
            const scenario = HPC_SCENARIOS[selectedValue];
            this.simulator = new MM1Queue(scenario.arrivalRate, scenario.serviceRate);
            console.log(`Loaded HPC scenario: ${selectedValue}`, scenario);
        } else if (!this.hpcMode) {
            const option = this.scenarioSelect.selectedOptions[0];
            if (option.dataset.arrival && option.dataset.service) {
                const arrivalRate = parseFloat(option.dataset.arrival);
                const serviceRate = parseFloat(option.dataset.service);
                this.simulator = new MM1Queue(arrivalRate, serviceRate);
                console.log(`Loaded scenario: ${selectedValue} (λ=${arrivalRate}, μ=${serviceRate})`);
            }
        }
        
        this.updateParameterDisplays();
        this.updateDisplay();
    }

    updateLabels() {
        // Update parameter labels
        document.querySelector('label[for="arrivalRate"]').textContent = 
            `${this.term('arrival_rate')} (λ)`;
        document.querySelector('label[for="serviceRate"]').textContent = 
            `${this.term('service_rate')} (μ)`;
        
        // Update other labels throughout interface
        const queueLabel = document.querySelector('.queue-label');
        if (queueLabel) {
            queueLabel.textContent = this.term('queue').charAt(0).toUpperCase() + this.term('queue').slice(1);
        }
        
        const serverLabel = document.querySelector('.server-label');
        if (serverLabel) {
            serverLabel.textContent = this.term('server').charAt(0).toUpperCase() + this.term('server').slice(1);
        }
    }

    animate() {
        if (!this.isRunning) {
            console.log('Animation stopped - isRunning is false');
            return;
        }
        
        if (!this.simulator) {
            console.log('Animation stopped - no simulator');
            return;
        }
        
        // Run multiple simulation steps per frame for smoother animation
        for (let i = 0; i < 3; i++) {
            try {
                this.simulator.step();
            } catch (e) {
                console.error('Error in simulator.step():', e);
                this.stopSimulation();
                return;
            }
        }
        
        try {
            this.updateDisplay();
        } catch (e) {
            console.error('Error in updateDisplay():', e);
        }
        
        this.animationId = requestAnimationFrame(() => this.animate());
    }

    updateDisplay() {
        if (!this.simulator) {
            console.log('updateDisplay: no simulator');
            return;
        }
        
        let stats;
        try {
            stats = this.simulator.getStatistics();
        } catch (e) {
            console.error('Error getting statistics:', e);
            return;
        }
        
        try {
            this.updateQueueDisplay(stats);
            this.updateServerDisplay(stats);
            this.updateStatsDisplay(stats);
            this.updateEducationalDisplay(stats);
            this.updateGraph(stats);
        } catch (e) {
            console.error('Error in display update methods:', e);
        }
    }

    updateQueueDisplay(stats) {
        const queueLength = stats.queueLength;
        const maxDisplay = 20;
        
        let queueHTML = '';
        
        // Show queue blocks
        for (let i = 0; i < Math.min(queueLength, maxDisplay); i++) {
            queueHTML += '<span class="queue-block">█</span>';
        }
        
        // Show overflow indicator if needed
        if (queueLength > maxDisplay) {
            queueHTML += `<span class="queue-overflow">+${queueLength - maxDisplay}</span>`;
        }
        
        // Show queue count
        queueHTML += ` <span class="queue-count">(${queueLength})</span>`;
        
        this.queueDisplay.innerHTML = queueHTML;
    }

    updateServerDisplay(stats) {
        const serverBusy = stats.serverBusy;
        this.serverStatus.innerHTML = serverBusy 
            ? '<span class="server-busy">●</span> BUSY'
            : '<span class="server-idle">○</span> IDLE';
    }

    updateStatsDisplay(stats) {
        const rho = this.simulator.arrivalRate / this.simulator.serviceRate;
        const timeLabel = this.hpcMode ? 'hr' : 'time';
        
        let statusText = '';
        if (rho >= 1.0) {
            statusText = '<span class="status-unstable">UNSTABLE</span>';
        } else if (rho > 0.95) {
            statusText = '<span class="status-critical">CRITICAL</span>';
        } else {
            statusText = '<span class="status-stable">STABLE</span>';
        }
        
        this.statsDisplay.innerHTML = `
            <div class="stat-row">
                <strong>λ = ${this.simulator.arrivalRate.toFixed(1)}</strong> │ 
                <strong>μ = ${this.simulator.serviceRate.toFixed(1)}</strong> │ 
                <strong>ρ = ${rho.toFixed(3)}</strong> ${statusText}
            </div>
            <div class="stat-row">
                ${this.term('utilization')}: ${(stats.avgUtilization * 100).toFixed(1)}% │ 
                Time: ${stats.currentTime.toFixed(1)} ${timeLabel} │ 
                ${this.term('served')}: ${stats.customersServed}
            </div>
        `;
    }

    updateEducationalDisplay(stats) {
        let html = '';
        
        // Little's Law verification
        if (stats.littleLaw) {
            const ll = stats.littleLaw;
            const verified = ll.verified ? '✅' : '❌';
            const timeLabel = this.hpcMode ? 'hr' : 'time';
            
            if (this.hpcMode) {
                html += `<div class="little-law">Little's Law: Jobs=${ll.L.toFixed(1)} │ Rate=${ll.lambda.toFixed(2)}/${timeLabel} │ Time=${ll.W.toFixed(2)}${timeLabel} │ Rate×Time=${ll.lambdaTimesW.toFixed(1)} ${verified}</div>`;
            } else {
                html += `<div class="little-law">Little's Law: L=${ll.L.toFixed(1)} │ λ=${ll.lambda.toFixed(2)} │ W=${ll.W.toFixed(2)} │ λ×W=${ll.lambdaTimesW.toFixed(1)} ${verified}</div>`;
            }
        }
        
        // Time breakdown
        if (stats.timeBreakdown) {
            const tb = stats.timeBreakdown;
            const timeLabel = this.hpcMode ? 'hr' : 'time';
            
            if (this.hpcMode) {
                html += `<div class="time-breakdown">Time Breakdown: Total=${tb.avgTimeInSystem.toFixed(2)}${timeLabel} = Queued=${tb.avgWaitTime.toFixed(2)}${timeLabel} + Runtime=${tb.avgServiceTime.toFixed(2)}${timeLabel}</div>`;
            } else {
                html += `<div class="time-breakdown">Time Breakdown: System=${tb.avgTimeInSystem.toFixed(2)} = Wait=${tb.avgWaitTime.toFixed(2)} + Service=${tb.avgServiceTime.toFixed(2)}</div>`;
            }
        }
        
        // Recent journeys
        if (stats.recentJourneys && stats.recentJourneys.length > 0) {
            const customerTerm = this.hpcMode ? 'Job' : 'Customer';
            const timeLabel = this.hpcMode ? 'hr' : 'min';
            
            html += `<div class="recent-journeys">Recent ${customerTerm} Journeys:</div>`;
            stats.recentJourneys.slice(-3).forEach(customer => {
                const wait = customer.waitTime;
                const service = customer.serviceTime;
                const total = customer.timeInSystem;
                const waitLabel = this.hpcMode ? 'Queued' : 'Wait';
                const serviceLabel = this.hpcMode ? 'Runtime' : 'Service';
                
                html += `<div class="journey">${customerTerm}#${customer.id}: ${waitLabel}=${wait.toFixed(1)}${timeLabel} + ${serviceLabel}=${service.toFixed(1)}${timeLabel} = Total=${total.toFixed(1)}${timeLabel}</div>`;
            });
        }
        
        // Confidence indicator
        if (stats.steadyState) {
            const ss = stats.steadyState;
            const progressWidth = Math.round(ss.progress * 100);
            html += `<div class="confidence">Statistics Confidence: ${ss.confidence} <div class="progress-bar"><div class="progress-fill" style="width: ${progressWidth}%"></div></div> ${ss.reliability}</div>`;
        }
        
        this.educationalDisplay.innerHTML = html;
    }

    updateGraph(stats) {
        if (!this.graphContext || !stats.queueLengthHistory.length) return;
        
        const canvas = this.graphCanvas;
        const ctx = this.graphContext;
        const width = canvas.offsetWidth;
        const height = canvas.offsetHeight;
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        const history = stats.queueLengthHistory;
        const maxLength = Math.max(...history, 5);
        const points = history.length;
        
        if (points < 2) return;
        
        // Draw grid
        ctx.strokeStyle = '#e0e0e0';
        ctx.lineWidth = 0.5;
        
        // Horizontal grid lines
        for (let i = 0; i <= 5; i++) {
            const y = height * (1 - i / 5);
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
            ctx.stroke();
        }
        
        // Draw queue length line
        ctx.strokeStyle = '#007bff';
        ctx.lineWidth = 2;
        ctx.beginPath();
        
        for (let i = 0; i < points; i++) {
            const x = (i / (points - 1)) * width;
            const y = height * (1 - history[i] / maxLength);
            
            if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        }
        
        ctx.stroke();
        
        // Draw axis labels
        ctx.fillStyle = '#666';
        ctx.font = '12px monospace';
        ctx.textAlign = 'left';
        ctx.fillText('0', 5, height - 5);
        ctx.textAlign = 'right';
        ctx.fillText(maxLength.toString(), width - 5, 15);
        
        // Queue length label
        ctx.textAlign = 'center';
        ctx.fillText(`${this.term('queue')} Length History`, width / 2, height - 5);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.uiController = new UIController();
});