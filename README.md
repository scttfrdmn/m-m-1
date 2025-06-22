# M/M/1 Queue Simulator & HPC Job Scheduler

A comprehensive Python-based educational simulator for M/M/1 queuing systems with both traditional queueing theory and HPC (High Performance Computing) job scheduling contexts.

## 🎯 What is M/M/1?

M/M/1 is a fundamental queuing model with:
- **M**: Markovian (Poisson) arrival process - customers arrive randomly
- **M**: Markovian (exponential) service times - service times are random but predictable
- **1**: Single server - one service point

This model is essential for understanding:
- **Queue behavior** and waiting times
- **System utilization** vs stability trade-offs
- **Little's Law** (L = λW) verification
- **Capacity planning** fundamentals

## 🚀 Features

### Core Simulation
- **Real-time ASCII visualization** - Live queue and server status
- **Compact terminal display** - Fits in 80x24 terminal (13 lines)
- **Multiple simulation modes** - Interactive, step-by-step, continuous
- **Smart parameter controls** - Quick adjustments and manual entry
- **Cross-platform compatibility** - Works on macOS, Linux, Windows

### Educational Enhancements
- **Little's Law verification** - Live demonstration of L = λW
- **Individual customer tracking** - See specific customer journeys
- **Time breakdown analysis** - Wait time vs service time components
- **Statistical confidence indicators** - Learn when measurements are reliable
- **Queue explosion demonstration** - Shows what happens when ρ ≥ 1

### HPC Context Mode
- **HPC terminology** - Jobs, clusters, submission rates, runtimes
- **Realistic scenarios** - Light, normal, busy, overloaded, maintenance
- **Time scaling** - Hours instead of abstract time units
- **Capacity planning insights** - Why clusters target 80-90% utilization
- **Educational connections** - Links theory to HPC system behavior

### Optimization Features
- **Auto-optimization** - Automatically approaches 100% utilization
- **Multiple strategies** - Different approaches to reaching ρ=1
- **Failure demonstration** - Shows why 100% utilization is unstable
- **Real-time adjustment** - Parameter tweaking during simulation

## 📊 Usage

### Basic Usage

#### Traditional Queueing Theory Mode
```bash
# Interactive mode
python3 main.py

# With specific parameters
python3 main.py --arrival-rate 2.0 --service-rate 3.0

# Start with optimization
python3 main.py -a 2.0 -s 3.0 --optimize
```

#### HPC Job Scheduler Mode
```bash
# Normal HPC workload
python3 main.py --hpc normal --hpc-mode

# Overloaded cluster scenario
python3 main.py --hpc overloaded --hpc-mode --continuous

# Research cluster (light usage)
python3 main.py --hpc light --hpc-mode
```

### HPC Scenarios

| Scenario | Submission Rate | Completion Rate | Load (ρ) | Description |
|----------|----------------|-----------------|----------|-------------|
| `light` | 1.0 jobs/hr | 2.0 jobs/hr | 50% | Research cluster - low usage |
| `normal` | 2.0 jobs/hr | 2.5 jobs/hr | 80% | Production cluster - typical workload |
| `busy` | 3.5 jobs/hr | 4.0 jobs/hr | 87.5% | High demand - conference deadlines |
| `overloaded` | 4.0 jobs/hr | 3.5 jobs/hr | 114% | More jobs than capacity |
| `maintenance` | 2.0 jobs/hr | 1.5 jobs/hr | 133% | Reduced capacity scenario |

### Interactive Controls

| Key | Action |
|-----|--------|
| **SPACE** | Pause/Resume simulation |
| **S** | Toggle step-by-step mode |
| **C** | Toggle continuous mode |
| **O** | Toggle auto-optimization |
| **+/-** | Adjust arrival rate by ±0.1 |
| **A** | Manual arrival rate entry |
| **M** | Manual service rate entry |
| **R** | Reset simulation |
| **Q** | Quit |

## 🎓 Educational Value

### Core Queueing Concepts

1. **Little's Law Demonstration**
   - Live verification that L = λW
   - Shows fundamental relationship between queue length, arrival rate, and wait time
   - ✅ indicator when relationship holds within tolerance

2. **Individual vs Average Experience**
   - Tracks specific customers through their journey
   - Shows variation around average wait times
   - Connects abstract statistics to concrete experiences

3. **Utilization vs Stability Trade-off**
   - Demonstrates why 100% utilization leads to instability
   - Shows exponential growth in wait times near capacity
   - Educational messages explain real-world implications

4. **Statistical Confidence**
   - Progress bar shows measurement reliability
   - Teaches when to trust simulation results
   - Emphasizes importance of adequate sample size

### HPC-Specific Learning

1. **Capacity Planning**
   - Why HPC clusters target 80-90% utilization
   - Impact of adding/removing compute nodes
   - Job limit and throttling necessity

2. **Queue Behavior**
   - How job submission patterns affect wait times
   - Maintenance windows and capacity reductions
   - Conference deadline rush scenarios

3. **System Design Principles**
   - Fair share policies vs FIFO scheduling
   - Resource allocation strategies
   - User experience optimization

## 📈 Display Examples

### Traditional Mode
```
M/M/1 Queue Simulator │ Mode: RUN │ Optimization: ---
──────────────────────────────────────────────────────────────────────────────
Server: ● │ Queue( 3): ███               │ ρ=0.800 (STABLE)
λ= 2.00 │ μ= 2.50 │ Util: 85.0% │ Time:   15.2 │ Arrivals:   32

Queue Length History (last 60 steps):
  5│   ▁ ▁           ▁ ▁▁▄█▄█▄▁▁▁▁▁▁▁▁                   ▁▁▁   ▁
  2│  ▁█▁█▁       ▁ ▁█▁███████████████▁   ▁   ▁       ▁ ▁███▁ ▁█
  1│  █████       █ ███████████████████   █   █       █ █████ ██

Little's Law: L=2.3 │ λ=2.1 │ W=1.12 │ λ×W=2.4 ✅
Recent Customer Journeys:
  C#28: Wait=1.2min + Service=0.8min = Total=2.0min
```

### HPC Mode
```
HPC Job Scheduler │ Mode: RUN │ Load Balancing: ---
──────────────────────────────────────────────────────────────────────────────
Cluster: ● │ Jobs( 3): ███               │ Load=80.0% (STABLE)
Submit= 2.0/hour │ Complete= 2.5/hour │ Util: 85.0% │ Uptime:   15.2hour │ Submissions:   32

Job Queue Length History (last 60 steps):
  5│   ▁ ▁           ▁ ▁▁▄█▄█▄▁▁▁▁▁▁▁▁                   ▁▁▁   ▁
  2│  ▁█▁█▁       ▁ ▁█▁███████████████▁   ▁   ▁       ▁ ▁███▁ ▁█
  1│  █████       █ ███████████████████   █   █       █ █████ ██

Little's Law: Jobs=2.3 │ Rate=2.1/hour │ Time=1.12hour │ Rate×Time=2.4 ✅
Recent Job Completions:
  Job#28: Queued=1.2hour + Runtime=0.8hour = Total=2.0hour
```

## 🔬 Testing & Development

### Run Test Suite
```bash
# Basic functionality
python3 test.py

# Educational features
python3 test_educational.py

# HPC mode functionality
python3 test_hpc_mode.py

# Display optimization
python3 test_compact.py
```

### Demo Scripts
```bash
# Visual demonstration
python3 demo.py

# Educational showcase
python3 educational_showcase.py

# Strategy demonstrations
python3 educational_demo.py
```

## 📚 Implementation Details

### Core Classes

- **Customer**: Individual entity with arrival time, service time, wait time tracking
- **MM1Queue**: Main simulation engine with Poisson arrivals and exponential service
- **SimulatorUI**: Display and interaction handling with mode-specific terminology
- **UtilizationOptimizer**: Auto-optimization strategies for approaching ρ=1

### Key Algorithms

1. **Event-driven simulation** - Next-event time advancement
2. **Exponential random variables** - `random.expovariate()` for realistic timing
3. **Time-weighted averaging** - Proper Little's Law L calculation
4. **Dynamic visualization** - Real-time ASCII graphics with Unicode blocks

### Educational Design Principles

1. **Progressive complexity** - Start simple, add advanced features
2. **Immediate feedback** - Real-time parameter effect visualization
3. **Concrete examples** - Individual customer stories within aggregate statistics
4. **Error demonstration** - Show what happens when theory is violated
5. **Context relevance** - HPC mode connects to student experience

## 🎯 Use Cases

### For Educators
- **Classroom demonstrations** of fundamental queueing principles
- **Homework assignments** exploring parameter relationships
- **Lab exercises** comparing theory to simulation
- **HPC course integration** showing job scheduler behavior

### For Students
- **Hands-on experimentation** with queueing parameters
- **Visual learning** of abstract mathematical concepts
- **Statistical confidence** understanding through simulation
- **Real-world connections** via HPC context

### For Researchers
- **Quick prototyping** of queueing scenarios
- **Parameter exploration** for system design
- **Educational tool development** baseline
- **M/M/1 baseline** for more complex models

## 🚀 Future Extensions

- **M/M/c implementation** (multiple servers)
- **Priority queuing** demonstrations
- **Network of queues** visualization
- **Web interface** for broader accessibility
- **Statistical analysis** output (CSV export)
- **Batch job patterns** for more realistic HPC modeling

## 📄 License

Open source - feel free to use for educational purposes.

## 🤝 Contributing

This project is designed for educational use. Contributions that enhance the learning experience are welcome!

---

**Educational Impact**: Transforms abstract queueing theory into interactive, visual learning experiences that build intuition for system design and performance analysis.