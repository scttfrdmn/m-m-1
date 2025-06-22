/**
 * M/M/1 Queue Simulator - JavaScript Implementation
 * 
 * Web-based port of the Python simulation engine providing identical mathematical
 * behavior for browser-based educational experiences.
 * 
 * @fileoverview Main simulation engine for M/M/1 queue visualization
 * @author Scott Friedman (with Claude Code Assistant)
 * @license MIT License - Copyright (c) 2025 Scott Friedman
 * @version 1.0.0
 */

/**
 * Represents a single customer/job in the M/M/1 queue system.
 * 
 * Tracks the complete customer journey from arrival through service completion,
 * enabling detailed analysis of individual experiences and system behavior.
 * 
 * @class Customer
 */
class Customer {
    /**
     * Creates a new customer instance.
     * 
     * @param {number} id - Unique identifier for the customer
     * @param {number} arrivalTime - When the customer arrived at the system
     * @param {number} serviceTime - How long the customer's service takes
     */
    constructor(id, arrivalTime, serviceTime) {
        this.id = id;
        this.arrivalTime = arrivalTime;
        this.serviceTime = serviceTime;
        this.startServiceTime = null;
        this.departureTime = null;
    }

    /**
     * Time spent waiting in queue before service begins.
     * @returns {number} Wait time in time units
     */
    get waitTime() {
        if (this.startServiceTime === null) return 0.0;
        return this.startServiceTime - this.arrivalTime;
    }

    /**
     * Total time spent in the system (wait + service).
     * @returns {number} Total system time in time units
     */
    get timeInSystem() {
        if (this.departureTime === null) return 0.0;
        return this.departureTime - this.arrivalTime;
    }

    /**
     * Whether the customer has completed service and left the system.
     * @returns {boolean} True if customer has departed
     */
    get isCompleted() {
        return this.departureTime !== null;
    }
}

/**
 * M/M/1 Queue Simulation Engine - JavaScript Implementation
 * 
 * Faithful port of the Python MM1Queue class providing identical mathematical
 * behavior for web-based educational experiences. Implements discrete-event
 * simulation of a single-server queue with Poisson arrivals and exponential
 * service times.
 * 
 * Features:
 * - Event-driven simulation with precise timing
 * - Real-time statistics collection and analysis  
 * - Little's Law verification (L = λW)
 * - Individual customer journey tracking
 * - Educational insights and confidence assessment
 * 
 * Mathematical Background:
 * - λ (lambda): Arrival rate (customers per time unit)
 * - μ (mu): Service rate (customers per time unit)
 * - ρ (rho): Traffic intensity = λ/μ (system is stable when ρ < 1)
 * 
 * @class MM1Queue
 * @example
 * const queue = new MM1Queue(2.0, 3.0);
 * for (let i = 0; i < 100; i++) {
 *     queue.step();
 * }
 * const stats = queue.getStatistics();
 * console.log(`Average queue length: ${stats.queueLength}`);
 */
class MM1Queue {
    /**
     * Creates a new M/M/1 queue simulation.
     * 
     * @param {number} arrivalRate - Average customer arrivals per time unit (λ)
     * @param {number} serviceRate - Average service completions per time unit (μ)
     */
    constructor(arrivalRate, serviceRate) {
        this.arrivalRate = arrivalRate;
        this.serviceRate = serviceRate;
        this.queue = [];
        this.serverBusy = false;
        this.currentTime = 0.0;
        this.nextArrivalTime = 0.0;
        this.nextDepartureTime = Infinity;
        this.totalCustomers = 0;
        this.customersServed = 0;
        this.totalWaitTime = 0.0;
        this.totalServiceTime = 0.0;

        // Statistics tracking
        this.queueLengthHistory = [];
        this.timeHistory = [];
        this.utilizationHistory = [];
        this.serverBusyTime = 0.0;
        this.lastUpdateTime = 0.0;

        // Enhanced educational tracking
        this.nextCustomerId = 1;
        this.completedCustomers = [];
        this.currentCustomer = null;
        this.recentJourneys = [];
        this.totalTimeInSystem = 0.0;

        // Little's Law tracking
        this.timeWeightedCustomers = 0.0;
        this.lastMeasurementTime = 0.0;

        // Steady-state detection
        this.steadyStateThreshold = 100;
        this.confidenceLevel = 0.0;

        // Generate first arrival
        this.scheduleNextArrival();
    }

    // Exponential random variable generation
    exponentialRandom(rate) {
        return -Math.log(1 - Math.random()) / rate;
    }

    scheduleNextArrival() {
        const interArrivalTime = this.exponentialRandom(this.arrivalRate);
        this.nextArrivalTime = this.currentTime + interArrivalTime;
    }

    scheduleNextDeparture(customer) {
        const serviceTime = this.exponentialRandom(this.serviceRate);
        customer.serviceTime = serviceTime;
        customer.startServiceTime = this.currentTime;
        this.nextDepartureTime = this.currentTime + serviceTime;
    }

    arriveCustomer() {
        const customer = new Customer(
            this.nextCustomerId++,
            this.currentTime,
            0.0
        );

        this.totalCustomers++;
        this.queue.push(customer);

        // Schedule next arrival
        this.scheduleNextArrival();

        // Start service if server is free
        if (!this.serverBusy) {
            this.startService();
        }
    }

    startService() {
        if (this.queue.length > 0 && !this.serverBusy) {
            this.currentCustomer = this.queue.shift();
            this.serverBusy = true;
            this.scheduleNextDeparture(this.currentCustomer);
        }
    }

    departCustomer() {
        if (this.currentCustomer) {
            // Complete the customer
            this.currentCustomer.departureTime = this.currentTime;
            
            // Update statistics
            this.customersServed++;
            this.totalWaitTime += this.currentCustomer.waitTime;
            this.totalServiceTime += this.currentCustomer.serviceTime;
            this.totalTimeInSystem += this.currentCustomer.timeInSystem;
            
            // Add to completed customers and recent journeys
            this.completedCustomers.push(this.currentCustomer);
            this.recentJourneys.push(this.currentCustomer);
            if (this.recentJourneys.length > 5) {
                this.recentJourneys.shift();
            }

            // Server becomes free
            this.serverBusy = false;
            this.currentCustomer = null;
            this.nextDepartureTime = Infinity;

            // Start serving next customer if queue not empty
            this.startService();
        }
    }

    updateStatistics() {
        const deltaTime = this.currentTime - this.lastUpdateTime;
        
        if (deltaTime > 0) {
            // Update server busy time
            if (this.serverBusy) {
                this.serverBusyTime += deltaTime;
            }

            // Update Little's Law tracking
            const customersInSystem = this.queue.length + (this.serverBusy ? 1 : 0);
            this.timeWeightedCustomers += customersInSystem * deltaTime;

            // Record history for visualization
            this.queueLengthHistory.push(this.queue.length);
            this.timeHistory.push(this.currentTime);
            
            const instantUtilization = this.serverBusy ? 1.0 : 0.0;
            this.utilizationHistory.push(instantUtilization);

            // Limit history length
            const maxHistory = 60;
            if (this.queueLengthHistory.length > maxHistory) {
                this.queueLengthHistory.shift();
                this.timeHistory.shift();
                this.utilizationHistory.shift();
            }
        }

        this.lastUpdateTime = this.currentTime;
    }

    step() {
        // Determine next event
        const nextEventTime = Math.min(this.nextArrivalTime, this.nextDepartureTime);
        
        // Update statistics before time advance
        this.updateStatistics();
        
        // Advance time
        this.currentTime = nextEventTime;

        // Process event
        if (this.nextArrivalTime <= this.nextDepartureTime) {
            this.arriveCustomer();
        } else {
            this.departCustomer();
        }

        // Update statistics after event
        this.updateStatistics();
    }

    getLittleLawVerification() {
        if (this.customersServed < 10 || this.currentTime <= 0) {
            return null;
        }

        // L = time-weighted average number in system
        const L = this.timeWeightedCustomers / this.currentTime;
        
        // λ = arrival rate (observed)
        const lambdaObserved = this.totalCustomers / this.currentTime;
        
        // W = average time in system
        const W = this.totalTimeInSystem / this.customersServed;
        
        // Calculate λW
        const lambdaTimesW = lambdaObserved * W;
        
        // Verification
        const error = Math.abs(L - lambdaTimesW);
        const relativeError = error / Math.max(L, 0.001);
        
        return {
            L: L,
            lambda: lambdaObserved,
            W: W,
            lambdaTimesW: lambdaTimesW,
            error: error,
            relativeError: relativeError,
            verified: relativeError < 0.20
        };
    }

    getTimeBreakdown() {
        if (this.customersServed < 5) return null;

        const totalWait = this.totalWaitTime;
        const totalService = this.completedCustomers.reduce((sum, c) => sum + c.serviceTime, 0);
        const totalSystem = this.totalTimeInSystem;

        const avgWait = totalWait / this.customersServed;
        const avgService = totalService / this.customersServed;
        const avgSystem = totalSystem / this.customersServed;

        return {
            avgWaitTime: avgWait,
            avgServiceTime: avgService,
            avgTimeInSystem: avgSystem,
            waitFraction: avgWait / Math.max(avgSystem, 0.001),
            serviceFraction: avgService / Math.max(avgSystem, 0.001)
        };
    }

    getSteadyStateInfo() {
        const customersNeeded = this.steadyStateThreshold;
        const progress = Math.min(this.customersServed / customersNeeded, 1.0);

        let confidence, reliability;
        if (this.customersServed < 20) {
            confidence = "Very Low";
            reliability = "Not reliable";
        } else if (this.customersServed < 50) {
            confidence = "Low";
            reliability = "Use with caution";
        } else if (this.customersServed < 100) {
            confidence = "Medium";
            reliability = "Moderately reliable";
        } else {
            confidence = "High";
            reliability = "Reliable";
        }

        return {
            progress: progress,
            confidence: confidence,
            reliability: reliability,
            customersServed: this.customersServed,
            customersNeeded: customersNeeded
        };
    }

    getStatistics() {
        const queueLength = this.queue.length;
        const instantaneousUtilization = this.serverBusy ? 1.0 : 0.0;
        
        let avgUtilization = 0.0;
        let avgWaitTime = 0.0;
        
        if (this.currentTime > 0) {
            avgUtilization = this.serverBusyTime / this.currentTime;
        }
        
        if (this.customersServed > 0) {
            avgWaitTime = this.totalWaitTime / this.customersServed;
        }

        // Theoretical values for M/M/1 queue
        const rho = this.arrivalRate / this.serviceRate;
        const theoreticalAvgQueueLength = rho < 1 ? (rho * rho) / (1 - rho) : Infinity;
        const theoreticalUtilization = rho < 1 ? rho : 1.0;

        // Educational metrics
        const littleLaw = this.getLittleLawVerification();
        const timeBreakdown = this.getTimeBreakdown();
        const steadyState = this.getSteadyStateInfo();

        return {
            queueLength: queueLength,
            serverBusy: this.serverBusy,
            utilization: instantaneousUtilization,
            avgUtilization: avgUtilization,
            totalCustomers: this.totalCustomers,
            customersServed: this.customersServed,
            avgWaitTime: avgWaitTime,
            currentTime: this.currentTime,
            theoreticalQueueLength: theoreticalAvgQueueLength,
            theoreticalUtilization: theoreticalUtilization,
            littleLaw: littleLaw,
            timeBreakdown: timeBreakdown,
            steadyState: steadyState,
            recentJourneys: [...this.recentJourneys]
        };
    }

    reset() {
        this.queue = [];
        this.serverBusy = false;
        this.currentTime = 0.0;
        this.nextArrivalTime = 0.0;
        this.nextDepartureTime = Infinity;
        this.totalCustomers = 0;
        this.customersServed = 0;
        this.totalWaitTime = 0.0;
        this.totalServiceTime = 0.0;
        this.queueLengthHistory = [];
        this.timeHistory = [];
        this.utilizationHistory = [];
        this.serverBusyTime = 0.0;
        this.lastUpdateTime = 0.0;
        this.nextCustomerId = 1;
        this.completedCustomers = [];
        this.currentCustomer = null;
        this.recentJourneys = [];
        this.totalTimeInSystem = 0.0;
        this.timeWeightedCustomers = 0.0;
        this.lastMeasurementTime = 0.0;
        this.scheduleNextArrival();
    }

    setParameters(arrivalRate, serviceRate) {
        this.arrivalRate = arrivalRate;
        this.serviceRate = serviceRate;
    }
}

// HPC Scenarios (matching Python version)
const HPC_SCENARIOS = {
    light: {
        arrivalRate: 1.0,
        serviceRate: 2.0,
        description: "Research cluster - low usage period"
    },
    normal: {
        arrivalRate: 2.0,
        serviceRate: 2.5,
        description: "Production cluster - typical workload"
    },
    busy: {
        arrivalRate: 3.5,
        serviceRate: 4.0,
        description: "High demand period - conference deadlines"
    },
    overloaded: {
        arrivalRate: 4.0,
        serviceRate: 3.5,
        description: "Oversubscribed - more jobs than capacity"
    },
    maintenance: {
        arrivalRate: 2.0,
        serviceRate: 1.5,
        description: "Maintenance period - reduced capacity"
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { MM1Queue, Customer, HPC_SCENARIOS };
}