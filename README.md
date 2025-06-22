# M/M/1 Queue Simulator & HPC Job Scheduler

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Try_Now-blue?style=for-the-badge)](https://scttfrdmn.github.io/m-m-1/)
[![Python Terminal](https://img.shields.io/badge/🐍_Terminal_Version-GitHub-green?style=for-the-badge)](https://github.com/scttfrdmn/m-m-1/blob/main/main.py)
[![Support](https://img.shields.io/badge/☕_Support-Ko--fi-orange?style=for-the-badge)](https://ko-fi.com/scttfrdmn)

A comprehensive educational simulator for M/M/1 queuing systems with both **interactive web interface** and **Python terminal implementation**. Perfect for teaching queueing theory concepts and HPC job scheduling behavior.

## 🚀 Quick Start

### **🌐 Try the Interactive Web Demo**
**👉 [**Launch Web Simulator**](https://scttfrdmn.github.io/m-m-1/) 👈**

- **Zero installation** - runs in any web browser
- **Mobile friendly** - works on tablets and phones  
- **Interactive controls** - sliders, buttons, real-time visualization
- **Perfect for classrooms** - immediate engagement

### **🐍 Run the Terminal Version**
```bash
# Clone the repository
git clone https://github.com/scttfrdmn/m-m-1.git
cd m-m-1

# Run interactive terminal simulator
python3 main.py

# Or with parameters
python3 main.py --arrival-rate 2.0 --service-rate 3.0

# HPC job scheduler mode
python3 main.py --hpc normal --hpc-mode
```

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

## ✨ Features

### 🌐 **Web Interface** (Zero Installation)
- **Real-time visualization** with interactive controls
- **Parameter sliders** for immediate experimentation
- **Queue animation** and live graphing
- **Mobile responsive** design
- **HPC mode** with job scheduler terminology
- **Educational tooltips** and contextual help

### 🖥️ **Terminal Interface** (Full Implementation)
- **ASCII visualization** with compact display
- **Keyboard controls** for parameter adjustment  
- **Detailed statistics** and educational insights
- **Cross-platform** compatibility
- **Scripting support** for automation
- **Educational transparency** - view the source code

### 🎓 **Educational Features** (Both Versions)
- **Little's Law verification** - Live demonstration of L = λW
- **Individual customer tracking** - See specific journeys
- **Time breakdown analysis** - Wait time vs service time
- **Statistical confidence indicators** - Learn when to trust results
- **Queue explosion demonstration** - Shows instability at ρ ≥ 1
- **HPC context mode** - Job scheduler terminology and scenarios

## 📊 Usage Comparison

| Feature | 🌐 Web Version | 🐍 Terminal Version |
|---------|---------------|-------------------|
| **Installation** | None required | Python 3.6+ |
| **Platform** | Any browser | Windows/Mac/Linux |
| **Mobile Support** | ✅ Full support | ❌ Not applicable |
| **Classroom Demo** | ✅ Perfect | ⚠️ Limited visibility |
| **Code Learning** | ❌ Hidden | ✅ Full transparency |
| **Customization** | ⚠️ Interface only | ✅ Full source access |
| **Automation** | ❌ Interactive only | ✅ CLI scripting |
| **Best For** | Concept introduction | Implementation study |

## 🎮 Interactive Examples

### **Web Simulator Scenarios**
Try these in the [**live demo**](https://scttfrdmn.github.io/m-m-1/):

1. **Stable System**: λ=2.0, μ=2.5 (ρ=0.8) - watch steady behavior
2. **Critical Load**: λ=2.9, μ=3.0 (ρ=0.97) - see sensitivity to changes  
3. **Overloaded**: λ=3.1, μ=3.0 (ρ=1.03) - observe queue explosion
4. **HPC Normal**: Enable HPC mode, select "normal" scenario
5. **HPC Overloaded**: Switch to "overloaded" - see job queue growth

### **Terminal Simulator Examples**
```bash
# Stable system demonstration
python3 main.py -a 2.0 -s 3.0

# Watch optimization attempt 100% utilization
python3 main.py -a 1.5 -s 3.0 --optimize

# HPC cluster scenarios
python3 main.py --hpc busy --hpc-mode --continuous
python3 main.py --hpc overloaded --hpc-mode
```

## 📚 Educational Value

### **For Instructors**
- **Classroom demos**: Web version for immediate visual impact
- **Lab exercises**: Terminal version for hands-on coding
- **Progressive learning**: Visual concepts → Code implementation
- **Assessment flexibility**: Web exploration + Programming assignments

### **For Students**  
- **Concept building**: Interactive web exploration
- **Theory verification**: See Little's Law in action
- **Implementation learning**: Study Python source code
- **Real-world connection**: HPC job scheduler context

### **Core Learning Objectives**
1. **Little's Law** - Fundamental relationship L = λW
2. **Utilization vs Stability** - Why 100% utilization fails
3. **Individual vs Average** - Variation around expected values
4. **Statistical Confidence** - When to trust measurements
5. **Capacity Planning** - Non-linear relationship between load and performance

## 🖥️ HPC Context Mode

Both versions include HPC job scheduler context:

### **Traditional Mode**
```
Server: ● │ Queue( 3): ███ │ ρ=0.800 (STABLE)
Customer #28: Wait=1.2min + Service=0.8min = Total=2.0min
```

### **HPC Mode**  
```
Cluster: ● │ Jobs( 3): ███ │ Load=80.0% (STABLE)
Job #28: Queued=1.2hr + Runtime=0.8hr = Total=2.0hr
```

**HPC Scenarios Available:**
- **Light** (ρ=0.5): Research cluster, low usage
- **Normal** (ρ=0.8): Production cluster, typical workload  
- **Busy** (ρ=0.875): Conference deadlines, high demand
- **Overloaded** (ρ=1.14): More jobs than capacity
- **Maintenance** (ρ=1.33): Reduced capacity scenario

## 🛠️ Development & Testing

### **Web Development**
The web version uses vanilla JavaScript for educational transparency:
```bash
# Serve locally for development
cd docs
python3 -m http.server 8000
# Visit http://localhost:8000
```

### **Testing Both Versions**
```bash
# Test terminal functionality
python3 test_hpc_mode.py
python3 test_educational.py

# Test web version
# Open docs/index.html in browser
# Or visit https://scttfrdmn.github.io/m-m-1/
```

## 📂 Project Structure

```
m-m-1/
├── 🌐 docs/                    # GitHub Pages web interface
│   ├── index.html             # Main web simulator
│   ├── css/style.css          # Responsive styling
│   └── js/                    # JavaScript implementation
│       ├── mm1-simulator.js   # Core simulation engine
│       ├── ui-controller.js   # Interface management
│       └── hpc-mode.js        # HPC enhancements
├── 🐍 main.py                 # Terminal simulator
├── 📁 test_*.py              # Comprehensive test suite
├── 🎬 demo*.py               # Demo and showcase scripts
└── 📋 design/                # Implementation documentation
```

## 🔗 Links & References

- **🌐 [Live Web Demo](https://scttfrdmn.github.io/m-m-1/)** - Try the interactive simulator
- **🐍 [Python Source](https://github.com/scttfrdmn/m-m-1/blob/main/main.py)** - View terminal implementation  
- **📖 [Documentation](https://github.com/scttfrdmn/m-m-1/tree/main/design)** - Implementation details
- **🧪 [Test Suite](https://github.com/scttfrdmn/m-m-1/tree/main)** - Verification scripts

## 🎯 Use Cases

| Scenario | Recommended Version | Why |
|----------|-------------------|-----|
| **Classroom introduction** | 🌐 Web | Visual, immediate, mobile-friendly |
| **Student exploration** | 🌐 Web | Zero barrier, interactive learning |
| **Programming assignment** | 🐍 Terminal | Code study, modification, extension |
| **Research baseline** | 🐍 Terminal | Full control, scriptable, extensible |
| **Conference demo** | 🌐 Web | Professional, responsive, accessible |

## 🚀 Getting Started Recommendations

### **For Educators**
1. **Start with web version** for concept introduction
2. **Assign terminal exploration** for implementation study  
3. **Use both versions** for comprehensive understanding
4. **Reference HPC mode** for real-world connections

### **For Students**
1. **🌐 [Try web demo](https://scttfrdmn.github.io/m-m-1/)** - build intuition
2. **Experiment with parameters** - see immediate effects
3. **🐍 Study Python code** - understand implementation
4. **Compare both versions** - verify consistent behavior

### **For Researchers**
1. **Web version for quick prototyping** of scenarios
2. **Terminal version for detailed analysis** and scripting
3. **Extend Python code** for custom research needs
4. **Reference implementation** for M/M/1 baseline

---

**🎓 Educational Impact**: Transforms abstract queueing theory into interactive, visual learning experiences that build intuition for system design and performance analysis.

**🤝 Contributing**: This project is designed for educational use. Contributions that enhance the learning experience are welcome!