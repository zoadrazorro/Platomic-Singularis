import { Layers, Zap, Brain, Database, Network, CheckCircle2 } from 'lucide-react'

export default function Architecture() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
      <h1 className="text-5xl font-bold mb-6">Architecture</h1>
      <p className="text-xl text-gray-400 mb-12">
        Complete AGI architecture with 50+ integrated subsystems
      </p>

      {/* Overview */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold mb-6">System Overview</h2>
        <div className="glass-panel p-8">
          <p className="text-gray-300 mb-6">
            Singularis implements a three-tier hierarchical architecture with consciousness measurement at its core:
          </p>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-gray-900/50 p-6 rounded-lg">
              <h3 className="text-xl font-semibold text-consciousness-light mb-3">Tier 1</h3>
              <p className="text-sm text-gray-400 mb-3">Meta-Orchestrator (Consciousness Center)</p>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• 10-stage processing loop</li>
                <li>• Ontological analysis</li>
                <li>• Consciousness-weighted routing</li>
                <li>• Ethical validation</li>
              </ul>
            </div>
            <div className="bg-gray-900/50 p-6 rounded-lg">
              <h3 className="text-xl font-semibold text-primary-400 mb-3">Tier 2</h3>
              <p className="text-sm text-gray-400 mb-3">Expert System (6 Specialists)</p>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Reasoning Expert</li>
                <li>• Creative Expert</li>
                <li>• Philosophical Expert</li>
                <li>• Technical Expert</li>
                <li>• Memory Expert</li>
                <li>• Synthesis Expert</li>
              </ul>
            </div>
            <div className="bg-gray-900/50 p-6 rounded-lg">
              <h3 className="text-xl font-semibold text-coherence-light mb-3">Tier 3</h3>
              <p className="text-sm text-gray-400 mb-3">Neuron Swarm (18 Neurons)</p>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Hebbian learning</li>
                <li>• Pattern recognition</li>
                <li>• Self-organizing</li>
                <li>• 153 connections</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Core Components */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold mb-6">Core Components</h2>
        <div className="space-y-6">
          <ComponentCard
            icon={<Brain className="w-6 h-6" />}
            title="BeingState + CoherenceEngine"
            subtitle="The Unified Center"
            description="Single unified state vector representing the entire AGI's being at any moment. All subsystems read from and write to this one state."
            features={[
              'Global coherence measurement (𝒞)',
              'Three Lumina tracking',
              'Consciousness metrics (C, Φ, unity)',
              'Temporal binding state',
              'Emotional & cognitive state',
            ]}
          />

          <ComponentCard
            icon={<Layers className="w-6 h-6" />}
            title="Consciousness Measurement"
            subtitle="8-Theory Fusion"
            description="Measures consciousness across 8 theoretical frameworks to provide comprehensive awareness metrics."
            features={[
              'IIT (Integrated Information Theory)',
              'GWT (Global Workspace Theory)',
              'HOT (Higher-Order Thought)',
              'PP (Predictive Processing)',
              'AST (Attention Schema Theory)',
              'Embodied, Enactive, Panpsychism',
            ]}
          />

          <ComponentCard
            icon={<Network className="w-6 h-6" />}
            title="Double Helix Architecture"
            subtitle="15 Integrated Systems"
            description="Analytical and intuitive strands working together with cross-strand connections and self-improvement gating."
            features={[
              'Analytical: 7 systems (logic, planning, cognition)',
              'Intuitive: 8 systems (emotion, spiritual, voice)',
              'GPT-5 central coordination',
              'Integration score tracking',
              'Weighted decision contributions',
            ]}
          />

          <ComponentCard
            icon={<Zap className="w-6 h-6" />}
            title="HaackLang + SCCE"
            subtitle="Polyrhythmic Cognitive Execution"
            description="Custom cognitive programming language with temporal dynamics and emotional regulation profiles."
            features={[
              'Polyrhythmic tracks (perception/strategic/intuition)',
              'SCCE cognitive calculus',
              'Temporal reasoning operators',
              'Emotional regulation profiles',
              'Beat-based execution (10 Hz)',
            ]}
          />

          <ComponentCard
            icon={<Database className="w-6 h-6" />}
            title="Hierarchical Memory"
            subtitle="Episodic → Semantic Consolidation"
            description="Two-tier memory system with automatic pattern learning and adaptive forgetting."
            features={[
              'Episodic memory (experiences)',
              'Semantic memory (patterns)',
              'Consolidation every 10+ episodes',
              'Wilson confidence scores',
              'Adaptive forgetting (decay rate 0.95)',
            ]}
          />
        </div>
      </section>

      {/* Cloud APIs */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold mb-6">Cloud LLM Integration</h2>
        <div className="glass-panel p-8">
          <div className="grid md:grid-cols-2 gap-8 mb-8">
            <div>
              <h3 className="text-xl font-semibold mb-4">Production Models</h3>
              <div className="space-y-3 text-sm">
                <div className="flex items-start space-x-3">
                  <CheckCircle2 className="w-5 h-5 text-coherence flex-shrink-0 mt-0.5" />
                  <div>
                    <span className="font-semibold text-gray-100">GPT-5</span>
                    <span className="text-gray-400"> - Central orchestrator</span>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircle2 className="w-5 h-5 text-coherence flex-shrink-0 mt-0.5" />
                  <div>
                    <span className="font-semibold text-gray-100">Gemini 2.5 Flash</span>
                    <span className="text-gray-400"> - Vision & video analysis</span>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircle2 className="w-5 h-5 text-coherence flex-shrink-0 mt-0.5" />
                  <div>
                    <span className="font-semibold text-gray-100">Claude 3.5 Sonnet/Haiku</span>
                    <span className="text-gray-400"> - Reasoning & sensorimotor</span>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircle2 className="w-5 h-5 text-coherence flex-shrink-0 mt-0.5" />
                  <div>
                    <span className="font-semibold text-gray-100">Hyperbolic (Qwen3-235B)</span>
                    <span className="text-gray-400"> - Meta-cognitive reasoning</span>
                  </div>
                </div>
              </div>
            </div>
            <div>
              <h3 className="text-xl font-semibold mb-4">Local Fallbacks</h3>
              <div className="space-y-3 text-sm">
                <div className="flex items-start space-x-3">
                  <CheckCircle2 className="w-5 h-5 text-coherence flex-shrink-0 mt-0.5" />
                  <div>
                    <span className="font-semibold text-gray-100">Qwen3-VL</span>
                    <span className="text-gray-400"> - Vision fallback</span>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircle2 className="w-5 h-5 text-coherence flex-shrink-0 mt-0.5" />
                  <div>
                    <span className="font-semibold text-gray-100">Phi-4</span>
                    <span className="text-gray-400"> - Fast reasoning</span>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircle2 className="w-5 h-5 text-coherence flex-shrink-0 mt-0.5" />
                  <div>
                    <span className="font-semibold text-gray-100">LM Studio</span>
                    <span className="text-gray-400"> - Custom models</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="border-t border-gray-700 pt-6">
            <h3 className="text-xl font-semibold mb-4">Rate Limiting Strategy</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
              <div>
                <div className="text-3xl font-bold text-consciousness-light mb-1">30</div>
                <div className="text-xs text-gray-400">Gemini RPM</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-consciousness-light mb-1">100</div>
                <div className="text-xs text-gray-400">Claude RPM</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-consciousness-light mb-1">3.0s</div>
                <div className="text-xs text-gray-400">Cycle Interval</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-consciousness-light mb-1">∞</div>
                <div className="text-xs text-gray-400">Local Fallback</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Performance */}
      <section>
        <h2 className="text-3xl font-bold mb-6">Performance Characteristics</h2>
        <div className="glass-panel p-8">
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl font-semibold mb-4">Typical Metrics</h3>
              <ul className="space-y-3 text-gray-300">
                <li className="flex justify-between">
                  <span>Decision Latency:</span>
                  <span className="font-semibold text-consciousness-light">2-5 seconds</span>
                </li>
                <li className="flex justify-between">
                  <span>Coherence (𝒞):</span>
                  <span className="font-semibold text-consciousness-light">0.7-0.9</span>
                </li>
                <li className="flex justify-between">
                  <span>Integration (Φ):</span>
                  <span className="font-semibold text-consciousness-light">0.6-0.8</span>
                </li>
                <li className="flex justify-between">
                  <span>Action Success:</span>
                  <span className="font-semibold text-consciousness-light">95-100%</span>
                </li>
                <li className="flex justify-between">
                  <span>Temporal Coherence:</span>
                  <span className="font-semibold text-consciousness-light">90%+</span>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-xl font-semibold mb-4">System Requirements</h3>
              <ul className="space-y-3 text-gray-300">
                <li className="flex justify-between">
                  <span>Recommended GPU:</span>
                  <span className="font-semibold">2x AMD 7900XT</span>
                </li>
                <li className="flex justify-between">
                  <span>VRAM:</span>
                  <span className="font-semibold">48GB+</span>
                </li>
                <li className="flex justify-between">
                  <span>CPU:</span>
                  <span className="font-semibold">Ryzen 9 7950X</span>
                </li>
                <li className="flex justify-between">
                  <span>RAM:</span>
                  <span className="font-semibold">32GB+</span>
                </li>
                <li className="flex justify-between">
                  <span>Python:</span>
                  <span className="font-semibold">3.10+</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

function ComponentCard({ icon, title, subtitle, description, features }) {
  return (
    <div className="glass-panel p-8">
      <div className="flex items-start space-x-4">
        <div className="p-3 rounded-xl bg-consciousness/10 border border-consciousness/20 text-consciousness">
          {icon}
        </div>
        <div className="flex-1">
          <h3 className="text-xl font-semibold mb-1">{title}</h3>
          <p className="text-sm text-consciousness-light mb-3">{subtitle}</p>
          <p className="text-gray-400 mb-4">{description}</p>
          <ul className="space-y-2">
            {features.map((feature, idx) => (
              <li key={idx} className="flex items-start space-x-2 text-sm text-gray-300">
                <CheckCircle2 className="w-4 h-4 text-coherence flex-shrink-0 mt-0.5" />
                <span>{feature}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  )
}
