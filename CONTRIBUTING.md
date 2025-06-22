# Contributing to M/M/1 Queue Simulator

Thank you for your interest in contributing to this educational project! This guide will help you get started with contributing code, documentation, educational content, or other improvements.

## 🎯 Project Mission

The M/M/1 Queue Simulator aims to make queueing theory concepts accessible through interactive visualization and real-world applications, particularly in HPC job scheduling contexts.

## 🚀 Quick Start for Contributors

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/scttfrdmn/m-m-1.git
   cd m-m-1
   ```

2. **Test the terminal version**
   ```bash
   python3 main.py
   ```

3. **Test the web version**
   ```bash
   cd docs
   python3 -m http.server 8000
   # Visit http://localhost:8000
   ```

### Project Structure

```
m-m-1/
├── README.md              # Main project documentation
├── ROADMAP.md              # Future development plans
├── CONTRIBUTING.md         # This file
├── main.py                 # Terminal simulator (primary implementation)
├── docs/                   # Web interface (GitHub Pages)
│   ├── index.html         # Main web simulator
│   ├── css/style.css      # Web styling
│   └── js/                # JavaScript implementation
│       ├── mm1-simulator.js    # Core simulation engine
│       ├── ui-controller.js    # Interface management
│       └── hpc-mode.js         # HPC enhancements
├── test_*.py              # Test suite for terminal version
├── demo*.py               # Demo and showcase scripts
└── design/                # Development documentation (legacy)
```

## 🤝 Ways to Contribute

### 1. Code Contributions

#### **Simulation Engine Improvements**
- Performance optimizations
- Additional queue types (M/M/c, priority queues)
- Enhanced statistical analysis
- Bug fixes and reliability improvements

#### **Educational Features**
- New scenario presets
- Interactive tutorials
- Assessment tools
- Visual enhancements

#### **Web Interface**
- Mobile responsiveness improvements
- Accessibility enhancements
- New visualization types
- User experience improvements

### 2. Educational Content

#### **Scenario Development**
- Industry-specific examples (healthcare, manufacturing, etc.)
- Crisis scenarios (system failures, peak demand)
- Historical case studies with real data

#### **Documentation**
- Tutorial content
- Concept explanations
- Use case examples
- Teaching guides

### 3. Testing and Quality Assurance

#### **Testing**
- Write new test cases
- Cross-platform testing
- Browser compatibility testing
- Performance testing

#### **Documentation Review**
- Accuracy verification
- Clarity improvements
- Example validation

### 4. Research and Analysis

#### **Academic Integration**
- Literature review and citations
- Theoretical validation
- Performance benchmarking
- Educational effectiveness studies

## 📋 Development Guidelines

### Code Style

#### **Python Code**
- Follow PEP 8 style guidelines
- Use type hints for function parameters and returns
- Write comprehensive docstrings
- Maintain educational clarity over optimization

#### **JavaScript Code**
- Use modern ES6+ features
- Follow JSDoc documentation standards
- Maintain compatibility with the Python implementation
- Prioritize readability and educational transparency

#### **Documentation**
- Write clear, educational explanations
- Include examples and use cases
- Use proper markdown formatting
- Keep technical accuracy high

### Testing Requirements

#### **Before Submitting**
1. **Run the test suite**
   ```bash
   python3 test_hpc_mode.py
   python3 test_educational.py
   python3 test_compact.py
   ```

2. **Test web interface**
   - Verify functionality in multiple browsers
   - Test mobile responsiveness
   - Check console for errors

3. **Verify educational value**
   - Ensure changes enhance learning outcomes
   - Test with different parameter ranges
   - Validate mathematical accuracy

### Git Workflow

#### **Branch Naming**
- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `educational/description` - Educational content

#### **Commit Messages**
```
Brief description of changes

Detailed explanation of what was changed and why:
- Specific improvements made
- Educational value added
- Testing performed

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

#### **Pull Request Process**
1. Create feature branch from `main`
2. Make changes with clear commits
3. Test thoroughly
4. Update documentation if needed
5. Submit pull request with detailed description

## 🎓 Educational Contribution Guidelines

### Content Standards

#### **Mathematical Accuracy**
- All equations and formulas must be correct
- Theoretical predictions should match simulation results
- Include proper statistical confidence measures

#### **Pedagogical Effectiveness**
- Start with simple concepts before complex ones
- Provide clear explanations of mathematical relationships
- Include real-world context and applications
- Make abstract concepts concrete through visualization

#### **Accessibility**
- Content should be accessible to undergraduate students
- Include glossaries for technical terms
- Provide multiple learning modalities (visual, interactive, analytical)

### Scenario Development

#### **Realistic Parameters**
- Use parameter values based on real-world data
- Include appropriate time scales (seconds, minutes, hours)
- Provide context for parameter choices

#### **Educational Value**
- Each scenario should teach specific concepts
- Include clear learning objectives
- Provide guided exploration suggestions

## 🐛 Bug Reports

### What to Include
1. **Environment**: OS, Python version, browser (for web issues)
2. **Reproduction steps**: Exact steps to reproduce the issue
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Screenshots**: If applicable, especially for web interface issues

### Example Bug Report
```
**Environment**: macOS 14.5, Python 3.11, Safari 17
**Issue**: Queue blocks not updating in web interface

**Steps to reproduce**:
1. Open https://scttfrdmn.github.io/m-m-1/
2. Click Start button
3. Observe queue display area

**Expected**: Queue blocks should appear and change
**Actual**: Queue display remains empty
**Console errors**: [Include any JavaScript errors]
```

## 💡 Feature Requests

### Format
1. **Use case**: Who would benefit and how?
2. **Description**: What should the feature do?
3. **Educational value**: How does it enhance learning?
4. **Implementation ideas**: Suggestions for how to implement

### Priority Considerations
- **High**: Directly improves educational outcomes
- **Medium**: Enhances user experience or accessibility
- **Low**: Nice-to-have improvements

## 🔧 Technical Architecture

### Core Principles

#### **Educational First**
- All features must enhance learning outcomes
- Maintain mathematical accuracy and theoretical validity
- Prioritize clarity over performance optimization

#### **Platform Consistency**
- Web and terminal versions should behave identically
- Maintain feature parity where possible
- Ensure consistent educational messaging

#### **Accessibility**
- Support keyboard navigation
- Provide screen reader compatibility
- Ensure color-blind friendly visualizations

### Key Components

#### **Simulation Engine** (`main.py` / `mm1-simulator.js`)
- Event-driven M/M/1 queue implementation
- Statistical tracking and analysis
- Educational insight generation

#### **User Interface** (Terminal / Web)
- Real-time visualization
- Interactive parameter control
- Educational content display

#### **Educational Features**
- Little's Law verification
- Individual customer tracking
- Scenario management
- Statistical confidence assessment

## 📞 Community and Support

### Getting Help
- **Questions**: Open a GitHub Discussion
- **Bugs**: Create a GitHub Issue
- **Feature ideas**: Start a GitHub Discussion
- **General chat**: Comment on existing issues/discussions

### Communication Guidelines
- Be respectful and constructive
- Focus on educational value
- Provide clear examples and use cases
- Help others learn and understand

### Recognition
All contributors will be acknowledged in:
- Git commit co-authorship
- Documentation credits
- Release notes
- Project acknowledgments

## 🎯 Roadmap Alignment

Before starting major contributions, please review the [ROADMAP.md](ROADMAP.md) to ensure your work aligns with project priorities:

- **Near-term** (3-6 months): Educational content, UX improvements
- **Medium-term** (6-12 months): Advanced analytics, M/M/c implementation
- **Long-term** (1+ years): Platform ecosystem, AI integration

## 📄 License and Legal

### Code License
All code contributions are subject to the project's open source license for educational use.

### Educational Content License
Educational content (scenarios, tutorials, explanations) should be freely usable for educational purposes.

### Attribution
- Contributors will be credited in git history
- Significant contributions may be acknowledged in documentation
- Academic contributors are encouraged to cite the project in research

---

**Thank you for contributing to making queueing theory education more accessible and engaging!**

For questions about contributing, please open a GitHub Discussion or contact the maintainers through the project repository.