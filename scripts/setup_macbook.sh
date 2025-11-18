#!/bin/bash
# Setup script for MacBook Pro M3 (Orchestra Mode)
# Installs Large MoE + AURA-Brain bio-simulator

set -e

echo "🎼 Setting up MacBook Orchestra Mode..."
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  Warning: This script is designed for macOS"
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements-macbook.txt

# Check for Metal support
echo "🔍 Checking Metal support..."
python3 << 'PYEOF'
import torch
if torch.backends.mps.is_available():
    print("✅ Metal Performance Shaders available")
else:
    print("⚠️  MPS not available, will use CPU")
PYEOF

echo ""

# Download Large MoE model
echo "📥 Checking Large MoE model..."
echo "   Recommended: Qwen2.5-14B-MoE or Mixtral-8x7B (Q4 quantized)"
echo "   Download via LM Studio or Ollama"
echo ""

# Create AURA-Brain server startup script
echo "📝 Creating AURA-Brain server script..."

cat > start_aura_brain.sh << 'EOF'
#!/bin/bash
# Start AURA-Brain Bio-Simulator server

export NODE_ROLE=orchestra
export AURA_BRAIN_PORT=3000
export AURA_BRAIN_NEURONS=1024
export AURA_BRAIN_DEVICE=mps

echo "🧠 Starting AURA-Brain Bio-Simulator..."
echo "   Port: $AURA_BRAIN_PORT"
echo "   Neurons: $AURA_BRAIN_NEURONS"
echo "   Device: $AURA_BRAIN_DEVICE"
echo ""

python -m singularis.aura_brain.server
EOF

chmod +x start_aura_brain.sh

echo "✅ Created start_aura_brain.sh"
echo ""

# Create MoE startup script
cat > start_moe.sh << 'EOF'
#!/bin/bash
# Start Large MoE model via LM Studio

echo "🤖 Starting Large MoE model..."
echo "   Port: 2000"
echo "   Model: Qwen2.5-14B-MoE or Mixtral-8x7B"
echo ""
echo "Start manually in LM Studio:"
echo "1. Load model: Qwen2.5-14B-MoE (Q4_K_M)"
echo "2. Set port: 2000"
echo "3. Set context: 32768"
echo "4. Enable Metal acceleration"
echo "5. Start server"
EOF

chmod +x start_moe.sh

echo "✅ Created start_moe.sh"
echo ""

# Create orchestra startup script
cat > start_orchestra.sh << 'EOF'
#!/bin/bash
# Start both MoE and AURA-Brain in orchestra mode

echo "🎼 Starting Orchestra Mode..."
echo ""

# Start AURA-Brain in background
echo "1. Starting AURA-Brain..."
./start_aura_brain.sh &
AURA_PID=$!

sleep 5

# Start MoE (manual for now)
echo ""
echo "2. Start Large MoE manually in LM Studio on port 2000"
echo ""

echo "✅ Orchestra mode starting..."
echo "   AURA-Brain PID: $AURA_PID"
echo "   MoE: Start manually in LM Studio"
echo ""
echo "Verify with: curl http://localhost:3000/health"
echo "             curl http://localhost:2000/v1/models"
EOF

chmod +x start_orchestra.sh

echo "✅ Created start_orchestra.sh"
echo ""

# Create verification script
cat > verify_macbook.sh << 'EOF'
#!/bin/bash
# Verify MacBook orchestra components

echo "🔍 Verifying MacBook Orchestra Mode..."
echo ""

# Check MoE
if curl -s http://localhost:2000/v1/models > /dev/null; then
    echo "  ✅ Large MoE (port 2000): UP"
else
    echo "  ❌ Large MoE (port 2000): DOWN"
fi

# Check AURA-Brain
if curl -s http://localhost:3000/health > /dev/null; then
    echo "  ✅ AURA-Brain (port 3000): UP"
else
    echo "  ⚠️  AURA-Brain (port 3000): DOWN (optional)"
fi

echo ""
EOF

chmod +x verify_macbook.sh

echo "✅ Created verify_macbook.sh"
echo ""

echo "✅ MacBook setup complete!"
echo ""
echo "Next steps:"
echo "1. Install LM Studio for macOS"
echo "2. Download Qwen2.5-14B-MoE or Mixtral-8x7B (Q4 quantized)"
echo "3. Run: ./start_orchestra.sh"
echo "4. Verify: ./verify_macbook.sh"
echo "5. From Router: python verify_cluster.py"
echo ""
echo "RAM allocation: 9GB MoE + 9GB AURA = 18GB total"
echo ""
