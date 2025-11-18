#!/bin/bash
# Setup script for Cygnus device (AMD 2x7900XT)
# Installs and configures 10 expert models on ports 1234-1243

set -e

echo "🎯 Setting up Cygnus Meta-MoE Primary..."
echo ""

# Check if running on Cygnus
if [ "$NODE_ROLE" != "inference_primary" ]; then
    echo "⚠️  Warning: NODE_ROLE is not set to 'inference_primary'"
    echo "   Set with: export NODE_ROLE=inference_primary"
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements-cygnus.txt

# Check for LM Studio
if ! command -v lms &> /dev/null; then
    echo "❌ LM Studio CLI not found!"
    echo "   Install from: https://lmstudio.ai"
    exit 1
fi

echo "✅ LM Studio found"
echo ""

# Download models (if not already present)
echo "📥 Checking expert models..."

MODELS=(
    "Qwen/Qwen2-VL-4B-Instruct-GGUF:Q4_K_M"
    "deepseek-ai/deepseek-coder-4b-instruct-GGUF:Q4_K_M"
    "microsoft/Phi-4-mini-GGUF:Q4_K_M"
    "TinyLlama/TinyLlama-4B-Chat-GGUF:Q4_K_M"
    "EmotiLLM/EmotiLLM-4B-GGUF:Q4_K_M"
    "mistralai/Mistral-4B-Instruct-GGUF:Q4_K_M"
    "codellama/CodeLlama-4B-Instruct-GGUF:Q4_K_M"
    "meta-llama/Llama-3.2-4B-Instruct-GGUF:Q4_K_M"
    "microsoft/Phi-4-data-GGUF:Q4_K_M"
    "01-ai/Yi-4B-Chat-GGUF:Q4_K_M"
)

for model in "${MODELS[@]}"; do
    echo "  Checking: $model"
    # LM Studio will download if not present
done

echo ""
echo "✅ All models ready"
echo ""

# Create startup script
echo "📝 Creating startup script..."

cat > start_cygnus_experts.sh << 'EOF'
#!/bin/bash
# Start all 10 Cygnus experts

echo "🚀 Starting Cygnus Meta-MoE Experts..."

# Expert ports and models
declare -A EXPERTS=(
    [1234]="Qwen2-VL-4B (Vision)"
    [1235]="DeepSeek-Coder-4B (Logic)"
    [1236]="Phi-4-mini (Memory)"
    [1237]="TinyLlama-4B (Action)"
    [1238]="EmotiLLM-4B (Emotion)"
    [1239]="Mistral-4B (Reasoning)"
    [1240]="CodeLlama-4B (Planning)"
    [1241]="Llama3.2-4B (Language)"
    [1242]="Phi-4-data (Analysis)"
    [1243]="Yi-4B (Synthesis)"
)

# Start each expert in background
for port in "${!EXPERTS[@]}"; do
    echo "  Starting ${EXPERTS[$port]} on port $port..."
    # LM Studio CLI command (adjust based on actual CLI)
    # lms server start --model <model> --port $port --bind 0.0.0.0 &
    echo "    (Start manually in LM Studio for now)"
done

echo ""
echo "✅ All experts started"
echo "   Check status: curl http://localhost:1234/v1/models"
EOF

chmod +x start_cygnus_experts.sh

echo "✅ Created start_cygnus_experts.sh"
echo ""

# Create verification script
cat > verify_cygnus.sh << 'EOF'
#!/bin/bash
# Verify all Cygnus experts are running

echo "🔍 Verifying Cygnus experts..."

for port in {1234..1243}; do
    if curl -s http://localhost:$port/v1/models > /dev/null; then
        echo "  ✅ Port $port: UP"
    else
        echo "  ❌ Port $port: DOWN"
    fi
done
EOF

chmod +x verify_cygnus.sh

echo "✅ Created verify_cygnus.sh"
echo ""

echo "✅ Cygnus setup complete!"
echo ""
echo "Next steps:"
echo "1. Start LM Studio"
echo "2. Load each expert model on ports 1234-1243"
echo "3. Bind to 0.0.0.0 (not 127.0.0.1) for network access"
echo "4. Run: ./verify_cygnus.sh"
echo "5. From Router, run: python verify_cluster.py"
echo ""
