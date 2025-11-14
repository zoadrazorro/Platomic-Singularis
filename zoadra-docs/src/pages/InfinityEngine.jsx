import { Zap, Brain, Layers, Database, CheckCircle2 } from 'lucide-react'

export default function InfinityEngine() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
      <div className="mb-12">
        <div className="inline-flex items-center space-x-2 px-4 py-2 rounded-full bg-consciousness-light/10 border border-consciousness-light/20 mb-6">
          <Zap className="w-4 h-4 text-consciousness-light" />
          <span className="text-sm text-consciousness-light font-medium">Phase 2A/2B Complete</span>
        </div>
        <h1 className="text-5xl font-bold mb-6">Infinity Engine</h1>
        <p className="text-xl text-gray-400 max-w-3xl">
          The next generation of cognitive architecture with adaptive rhythmic intelligence, 
          temporal memory encoding, and autonomous meta-logic interventions.
        </p>
      </div>

      {/* Overview */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold mb-6">Overview</h2>
        <div className="glass-panel p-8">
          <p className="text-gray-300 mb-4">
            The Infinity Engine transforms static cognition into <strong>adaptive rhythmic intelligence</strong>. 
            It consists of five integrated systems that work together to create a self-regulating, 
            context-aware cognitive architecture.
          </p>
          <div className="grid md:grid-cols-2 gap-4 mt-6">
            <div className="bg-gray-900/50 p-4 rounded-lg">
              <h3 className="font-semibold text-consciousness-light mb-2">Phase 2A - Foundation</h3>
              <ul className="space-y-1 text-sm text-gray-400">
                <li>• Coherence Engine V2</li>
                <li>• Meta-Context System</li>
                <li>• HaackLang 2.0 Operators</li>
              </ul>
            </div>
            <div className="bg-gray-900/50 p-4 rounded-lg">
              <h3 className="font-semibold text-coherence-light mb-2">Phase 2B - Rhythm & Memory</h3>
              <ul className="space-y-1 text-sm text-gray-400">
                <li>• Polyrhythmic Learning</li>
                <li>• Memory Engine V2</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Systems */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold mb-6">Core Systems</h2>
        <div className="space-y-6">
          <SystemCard
            icon={<Brain className="w-6 h-6" />}
            title="1. Coherence Engine V2"
            subtitle="Meta-Logic Interventions"
            description="Actively monitors and corrects cognitive inconsistencies across polyrhythmic tracks."
            features={[
              'Detects contradictions across tracks',
              'Measures cognitive tension',
              'Applies dynamic corrections (dampen/boost)',
              'Forces context shifts when needed',
            ]}
          />

          <SystemCard
            icon={<Layers className="w-6 h-6" />}
            title="2. Meta-Context System"
            subtitle="Hierarchical Temporal Contexts"
            description="Manages cognitive contexts with automatic transitions and temporal awareness."
            features={[
              'Context stacks (micro/macro/conditional)',
              'Auto-expiring contexts with timers',
              'Conditional transitions based on state',
              'Predefined: exploration, survival, learning',
            ]}
          />

          <SystemCard
            icon={<Zap className="w-6 h-6" />}
            title="3. HaackLang 2.0 Operators"
            subtitle="Full Cognitive DSL"
            description="Extended operator set for advanced cognitive reasoning."
            features={[
              'Fuzzy logic: ⊕ (blend), ⊗ (product), ⊞ (sum)',
              'Paraconsistent: ⊓ (and), ⊔ (or)',
              'Temporal: Δ (derivative), last(n), future(n)',
              'Multi-track: sync, interfere, align',
            ]}
          />

          <SystemCard
            icon={<Zap className="w-6 h-6" />}
            title="4. Polyrhythmic Learning"
            subtitle="Adaptive Track Periods"
            description="Track periods become learnable parameters that optimize for current task."
            features={[
              'Adapts based on reward signals',
              'Harmonic constraints between tracks',
              'Context-specific rhythm profiles',
              'Novel: Habituation as harmonic learning',
            ]}
          />

          <SystemCard
            icon={<Database className="w-6 h-6" />}
            title="5. Memory Engine V2"
            subtitle="Temporal-Rhythmic Encoding"
            description="Memories encoded as rhythm patterns rather than static vectors."
            features={[
              'Rhythm signatures (phases + periods)',
              'Interference-based recall',
              'Episodic → semantic consolidation',
              'Harmonic forgetting',
            ]}
          />
        </div>
      </section>

      {/* Integration */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold mb-6">Runtime Integration</h2>
        <div className="glass-panel p-8">
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl font-semibold mb-4">Performance</h3>
              <ul className="space-y-2 text-gray-400">
                <li className="flex items-start space-x-2">
                  <CheckCircle2 className="w-5 h-5 text-coherence flex-shrink-0 mt-0.5" />
                  <span>Runs every 2 cycles (~5-10ms overhead)</span>
                </li>
                <li className="flex items-start space-x-2">
                  <CheckCircle2 className="w-5 h-5 text-coherence flex-shrink-0 mt-0.5" />
                  <span>~2-3MB additional memory</span>
                </li>
                <li className="flex items-start space-x-2">
                  <CheckCircle2 className="w-5 h-5 text-coherence flex-shrink-0 mt-0.5" />
                  <span>Negligible compared to LLM calls</span>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-xl font-semibold mb-4">Integration Points</h3>
              <ul className="space-y-2 text-gray-400">
                <li className="flex items-start space-x-2">
                  <CheckCircle2 className="w-5 h-5 text-coherence flex-shrink-0 mt-0.5" />
                  <span>Connects to HaackLang/SCCE</span>
                </li>
                <li className="flex items-start space-x-2">
                  <CheckCircle2 className="w-5 h-5 text-coherence flex-shrink-0 mt-0.5" />
                  <span>Uses consciousness coherence as reward</span>
                </li>
                <li className="flex items-start space-x-2">
                  <CheckCircle2 className="w-5 h-5 text-coherence flex-shrink-0 mt-0.5" />
                  <span>Consolidates memories every 100 cycles</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Example Flow */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold mb-6">Example Flow</h2>
        <div className="glass-panel p-8">
          <div className="space-y-4 font-mono text-sm">
            <div className="bg-gray-900/50 p-4 rounded">
              <span className="text-gray-500">// Exploration Phase</span><br/>
              <span className="text-consciousness">Context:</span> exploration<br/>
              <span className="text-primary-400">Rhythms:</span> perception=100, reflection=200, strategic=500
            </div>
            <div className="text-center text-gray-500">↓</div>
            <div className="bg-gray-900/50 p-4 rounded">
              <span className="text-gray-500">// Danger Detected</span><br/>
              <span className="text-red-400">[SCCE]</span> Danger: P=0.80 (enemy spotted)<br/>
              <span className="text-consciousness">[INFINITY]</span> Context shift triggered
            </div>
            <div className="text-center text-gray-500">↓</div>
            <div className="bg-gray-900/50 p-4 rounded">
              <span className="text-gray-500">// Survival Mode</span><br/>
              <span className="text-consciousness">Context:</span> survival<br/>
              <span className="text-primary-400">Rhythms:</span> perception=94 (faster!), fast_response=48, reflection=60 (suppressed)<br/>
              <span className="text-coherence">[COHERENCE V2]</span> Intervention: 3 adjustments
            </div>
            <div className="text-center text-gray-500">↓</div>
            <div className="bg-gray-900/50 p-4 rounded">
              <span className="text-gray-500">// Combat Resolved</span><br/>
              <span className="text-consciousness">[INFINITY]</span> Context shift to learning<br/>
              <span className="text-primary-400">[MEMORY]</span> Consolidating combat episodes
            </div>
          </div>
        </div>
      </section>

      {/* Configuration */}
      <section>
        <h2 className="text-3xl font-bold mb-6">Configuration</h2>
        <div className="glass-panel p-8">
          <pre className="bg-gray-900/50 p-6 rounded-lg overflow-x-auto">
            <code className="text-sm">{`config = SkyrimConfig(
    use_infinity_engine=True,  # Master switch
    infinity_verbose=False,     # Debug logging
    
    # Coherence Engine V2
    coherence_v2_threshold=0.4,
    
    # Meta-Context System
    meta_context_enabled=True,
    
    # Polyrhythmic Learning
    polyrhythmic_learning_enabled=True,
    rhythm_learning_rate=0.01,
    harmonic_attraction=0.1,
    
    # Memory Engine V2
    memory_v2_enabled=True,
    memory_v2_capacity=1000,
    memory_consolidation_threshold=3,
    memory_decay_rate=0.001,
)`}</code>
          </pre>
        </div>
      </section>
    </div>
  )
}

function SystemCard({ icon, title, subtitle, description, features }) {
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
