#!/bin/bash

# LegalBot+ Setup Script
# Automates the installation and setup process

echo "======================================================================"
echo "                    LegalBot+ Setup Script"
echo "======================================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.10.0"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then 
    echo "✓ Python $python_version detected"
else
    echo "✗ Python 3.10+ required, found $python_version"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "✗ Failed to install dependencies"
    exit 1
fi

echo ""
echo "✓ Dependencies installed successfully"

# Build FAISS index
echo ""
echo "======================================================================"
echo "Building FAISS index from legal documents..."
echo "======================================================================"
echo ""

python core/build_faiss_index.py

if [ $? -ne 0 ]; then
    echo "✗ Failed to build FAISS index"
    exit 1
fi

echo ""
echo "✓ FAISS index built successfully"

# Run tests
echo ""
echo "======================================================================"
echo "Running system tests..."
echo "======================================================================"
echo ""

python test_system.py <<EOF
n
EOF

# Final instructions
echo ""
echo "======================================================================"
echo "✓ Setup Complete!"
echo "======================================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Get a Telegram Bot Token from @BotFather:"
echo "   - Open Telegram and message @BotFather"
echo "   - Send /newbot and follow instructions"
echo "   - Copy your bot token"
echo ""
echo "2. Set the token as environment variable:"
echo "   export TELEGRAM_BOT_TOKEN='your_token_here'"
echo ""
echo "3. Run the bot:"
echo "   source venv/bin/activate  # If not already activated"
echo "   python bot/main.py"
echo ""
echo "Or run in demo mode (no Telegram token needed):"
echo "   python bot/main.py"
echo ""
echo "======================================================================"
echo "Documentation:"
echo "  - README.md - Full documentation"
echo "  - EXAMPLES.md - Example conversations"
echo "  - test_system.py - System verification"
echo "======================================================================"
echo ""

