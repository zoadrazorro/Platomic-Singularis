#!/bin/bash
# Setup script for NVIDIA Laptop (RTX 5060 8GB)
# Installs Abductive Positronic Network

set -e

echo "🔬 Setting up NVIDIA Positronic Network..."
echo ""

# Check for CUDA
echo "🔍 Checking CUDA support..."
if command -v nvidia-smi &> /dev/null; then
    echo "✅ NVIDIA GPU detected"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
else
    echo "⚠️  nvidia-smi not found. Install CUDA toolkit."
fi

echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements-nvidia.txt

# Verify PyTorch CUDA
echo "🔍 Verifying PyTorch CUDA..."
python3 << 'PYEOF'
import torch
if torch.cuda.is_available():
    print(f"✅ CUDA available: {torch.cuda.get_device_name(0)}")
    print(f"   CUDA version: {torch.version.cuda}")
    print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
else:
    print("❌ CUDA not available!")
    print("   Install PyTorch with CUDA support:")
    print("   pip install torch --index-url https://download.pytorch.org/whl/cu121")
PYEOF

echo ""

# Create Positronic Network server startup script
echo "📝 Creating Positronic Network server script..."

cat > start_positronic.sh << 'EOF'
#!/bin/bash
# Start Abductive Positronic Network server

export NODE_ROLE=positronic
export POSITRONIC_PORT=4000
export POSITRONIC_NODES=512
export POSITRONIC_DEVICE=cuda

echo "🔬 Starting Abductive Positronic Network..."
echo "   Port: $POSITRONIC_PORT"
echo "   Nodes: $POSITRONIC_NODES"
echo "   Device: $POSITRONIC_DEVICE"
echo ""

python -m singularis.positronic.server
EOF

chmod +x start_positronic.sh

echo "✅ Created start_positronic.sh"
echo ""

# Create verification script
cat > verify_nvidia.sh << 'EOF'
#!/bin/bash
# Verify NVIDIA Positronic Network

echo "🔍 Verifying Positronic Network..."
echo ""

# Check server
if curl -s http://localhost:4000/health > /dev/null; then
    echo "  ✅ Positronic Network (port 4000): UP"
else
    echo "  ❌ Positronic Network (port 4000): DOWN"
fi

# Test hypothesis generation
echo ""
echo "Testing hypothesis generation..."
curl -X POST http://localhost:4000/generate_hypotheses \
  -H "Content-Type: application/json" \
  -d '{
    "observations": ["User slept poorly", "Heart rate elevated"],
    "max_hypotheses": 3
  }' | python -m json.tool

echo ""
EOF

chmod +x verify_nvidia.sh

echo "✅ Created verify_nvidia.sh"
echo ""

# Create test script
cat > test_positronic.py << 'PYEOF'
#!/usr/bin/env python3
"""Test Positronic Network locally"""

import asyncio
from singularis.positronic import AbductivePositronicNetwork, HypothesisType

async def main():
    print("🔬 Testing Abductive Positronic Network...")
    print()
    
    # Create network
    network = AbductivePositronicNetwork(
        num_nodes=512,
        num_modules=5,
        device="cuda",
        enable_cuda=True,
    )
    
    print(f"✅ Network created: {network.num_nodes} nodes")
    print()
    
    # Test observations
    observations = [
        "User slept poorly last night",
        "Heart rate was elevated",
        "Stress levels high during day"
    ]
    
    print("Observations:")
    for obs in observations:
        print(f"  - {obs}")
    print()
    
    # Generate hypotheses
    print("Generating hypotheses...")
    hypotheses = await network.generate_hypotheses(
        observations=observations,
        max_hypotheses=5,
        min_confidence=0.3,
    )
    
    print(f"✅ Generated {len(hypotheses)} hypotheses:")
    print()
    
    for i, h in enumerate(hypotheses, 1):
        print(f"{i}. [{h.hypothesis_type.value}] {h.content}")
        print(f"   Confidence: {h.confidence:.2f}")
        print(f"   Plausibility: {h.plausibility:.2f}")
        print(f"   Score: {h.score():.2f}")
        print()

if __name__ == "__main__":
    asyncio.run(main())
PYEOF

chmod +x test_positronic.py

echo "✅ Created test_positronic.py"
echo ""

echo "✅ NVIDIA setup complete!"
echo ""
echo "Next steps:"
echo "1. Ensure CUDA 12.1+ is installed"
echo "2. Install PyTorch with CUDA: pip install torch --index-url https://download.pytorch.org/whl/cu121"
echo "3. Test locally: python test_positronic.py"
echo "4. Start server: ./start_positronic.sh"
echo "5. Verify: ./verify_nvidia.sh"
echo "6. From Router: python verify_cluster.py"
echo ""
echo "VRAM usage: ~6GB (fits in 8GB RTX 5060)"
echo ""
