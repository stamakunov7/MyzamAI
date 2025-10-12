# Contributing to LegalBot+

Thank you for your interest in contributing to LegalBot+! 🎉

---

## 🤝 How to Contribute

### Reporting Bugs
1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)
   - Relevant logs or error messages

### Suggesting Features
1. Search existing issues to avoid duplicates
2. Create a new issue with:
   - Clear description of the feature
   - Use case and benefits
   - Proposed implementation (if applicable)

### Code Contributions

#### Prerequisites
- Python 3.10+
- Git
- Basic understanding of the codebase architecture

#### Setup Development Environment
```bash
# Fork and clone the repository
git clone https://github.com/yourusername/legalbot.git
cd legalbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install pytest black flake8 mypy

# Build FAISS index
python core/build_faiss_index.py
```

#### Development Workflow
1. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Follow the existing code style
   - Add docstrings to new functions/classes
   - Update documentation if needed

3. **Test your changes:**
   ```bash
   python test_system.py
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: Add your feature description"
   ```
   
   Use conventional commit messages:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `style:` Code style changes
   - `refactor:` Code refactoring
   - `test:` Test additions/changes
   - `chore:` Build/config changes

5. **Push and create PR:**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub.

---

## 📝 Coding Standards

### Python Style
- Follow PEP 8
- Use type hints where possible
- Maximum line length: 100 characters
- Use meaningful variable names

### Documentation
- Add docstrings to all public functions/classes
- Use Google-style docstrings:
  ```python
  def function(arg1: str, arg2: int) -> bool:
      """
      Brief description of function.
      
      Args:
          arg1: Description of arg1
          arg2: Description of arg2
          
      Returns:
          Description of return value
          
      Raises:
          ValueError: When X happens
      """
  ```

### Logging
- Use Python's `logging` module
- Log levels:
  - `DEBUG`: Detailed diagnostic information
  - `INFO`: General informational messages
  - `WARNING`: Warning messages
  - `ERROR`: Error messages
  - `CRITICAL`: Critical errors

Example:
```python
import logging

logger = logging.getLogger(__name__)
logger.info("Processing query...")
```

---

## 🧪 Testing

### Running Tests
```bash
# Run full test suite
python test_system.py

# Test specific component
python core/law_retriever.py
python core/agents/legal_expert.py
```

### Writing Tests
When adding new features, include tests:
```python
def test_new_feature():
    """Test description"""
    # Arrange
    input_data = ...
    
    # Act
    result = your_function(input_data)
    
    # Assert
    assert result == expected_output
```

---

## 🎯 Priority Areas for Contribution

### High Priority
- [ ] Adding more legal documents
- [ ] Improving translation quality
- [ ] Performance optimizations
- [ ] Better error handling
- [ ] Additional tests

### Medium Priority
- [ ] Web interface (Streamlit/Gradio)
- [ ] Voice message support
- [ ] Additional language support
- [ ] Fine-tuning models on legal texts
- [ ] Conversation context awareness

### Low Priority
- [ ] Mobile app
- [ ] Additional output formats
- [ ] Integration with other platforms
- [ ] Analytics dashboard

---

## 📦 Adding New Agents

To add a new agent to the system:

1. **Create agent file:**
   ```python
   # core/agents/your_agent.py
   import logging
   
   logger = logging.getLogger(__name__)
   
   class YourAgent:
       """
       Description of your agent
       """
       
       def __init__(self):
           logger.info("Your Agent initialized")
       
       def process(self, input_data):
           """
           Process input data
           
           Args:
               input_data: Input description
               
           Returns:
               Processed result
           """
           # Implementation
           pass
   ```

2. **Register in `__init__.py`:**
   ```python
   from .your_agent import YourAgent
   
   __all__ = [..., 'YourAgent']
   ```

3. **Integrate in orchestrator:**
   ```python
   # In bot/main.py
   self.your_agent = YourAgent()
   
   # Use in pipeline
   result = self.your_agent.process(data)
   ```

4. **Add tests:**
   ```python
   def main():
       agent = YourAgent()
       result = agent.process(test_data)
       print(result)
   
   if __name__ == "__main__":
       main()
   ```

---

## 🌐 Adding New Languages

To add support for a new language:

1. **Add translation model:**
   ```python
   # In core/agents/translator.py
   self.xx_to_en_model = "Helsinki-NLP/opus-mt-xx-en"
   self.en_to_xx_model = "Helsinki-NLP/opus-mt-en-xx"
   ```

2. **Update language detection:**
   ```python
   def detect_language(self, text: str) -> str:
       # Add detection logic for new language
       pass
   ```

3. **Add translation methods:**
   ```python
   def translate_xx_to_en(self, text: str) -> str:
       # Implementation
       pass
   ```

---

## 📚 Adding Legal Documents

To add new legal documents:

1. **Prepare text file:**
   ```
   data/new_code.txt
   ```
   Format: Plain text with clear article structure

2. **Update index builder:**
   ```python
   # Optionally modify chunking strategy
   def chunk_text(self, text: str):
       # Custom chunking for new document type
       pass
   ```

3. **Rebuild index:**
   ```bash
   python core/build_faiss_index.py
   ```

---

## 🐛 Debugging Tips

### Common Issues

**Issue: Model download fails**
```bash
# Set HuggingFace cache directory
export HF_HOME=/path/to/cache
```

**Issue: Out of memory**
```python
# Use smaller model
model_name = "microsoft/phi-2"  # 2.7B instead of 7B
```

**Issue: Slow inference**
```python
# Use quantization
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(load_in_8bit=True)
```

### Logging
Enable debug logging:
```python
logging.basicConfig(level=logging.DEBUG)
```

---

## 📄 Documentation Updates

When updating documentation:

1. **README.md** - User-facing documentation
2. **ARCHITECTURE.md** - Technical architecture
3. **EXAMPLES.md** - Example conversations
4. **Code docstrings** - Inline documentation

---

## 🎨 UI/UX Improvements

When improving user interface:

1. Test with real users
2. Keep messages concise
3. Use emojis appropriately
4. Maintain consistent formatting
5. Provide helpful error messages

---

## ⚖️ Legal Considerations

When contributing legal content:

- Ensure accuracy of legal information
- Cite sources appropriately
- Add appropriate disclaimers
- Respect copyright laws
- Consider jurisdictional differences

---

## 📞 Getting Help

- **Questions:** Open a GitHub Discussion
- **Bugs:** Open a GitHub Issue
- **Chat:** Join our community (if applicable)
- **Email:** support@legalbot.example

---

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

---

## 📜 Code of Conduct

### Our Pledge
We pledge to make participation in our project a harassment-free experience for everyone.

### Our Standards
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Accepting constructive criticism gracefully
- Focusing on what is best for the community

### Unacceptable Behavior
- Trolling, insulting, or derogatory comments
- Public or private harassment
- Publishing others' private information
- Other unethical or unprofessional conduct

---

## 📝 License

By contributing to LegalBot+, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to LegalBot+! 🤖⚖️**

