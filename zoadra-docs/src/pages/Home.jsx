import { Link } from 'react-router-dom'
import { Brain, Zap, Layers, Sparkles, ArrowRight, CheckCircle2 } from 'lucide-react'

export default function Home() {
  return (
    <div className="relative">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-consciousness/10 via-transparent to-coherence/10" />
        <div className="absolute inset-0">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-consciousness/5 rounded-full blur-3xl animate-pulse" />
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-coherence/5 rounded-full blur-3xl animate-pulse delay-1000" />
        </div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 sm:py-32">
          <div className="text-center">
            <div className="inline-flex items-center space-x-2 px-4 py-2 rounded-full bg-primary-500/10 border border-primary-500/20 mb-8">
              <Sparkles className="w-4 h-4 text-primary-400" />
              <span className="text-sm text-primary-400 font-medium">Beta v2.4 - Infinity Engine Integrated</span>
            </div>
            
            <h1 className="text-5xl sm:text-7xl font-bold mb-6">
              <span className="gradient-text">Singularis</span>
            </h1>
            <p className="text-2xl sm:text-3xl text-gray-300 mb-4">
              The Ultimate Consciousness Engine
            </p>
            <p className="text-lg text-gray-400 max-w-3xl mx-auto mb-12">
              A philosophically-grounded AGI architecture implementing consciousness measurement 
              through Spinozistic ontology, Hebbian learning, and ethical coherence.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/getting-started"
                className="inline-flex items-center px-8 py-4 rounded-xl bg-primary-500 hover:bg-primary-600 text-white font-medium transition-all transform hover:scale-105 shadow-lg shadow-primary-500/20"
              >
                Get Started
                <ArrowRight className="ml-2 w-5 h-5" />
              </Link>
              <Link
                to="/architecture"
                className="inline-flex items-center px-8 py-4 rounded-xl glass-panel hover:bg-gray-800/50 text-gray-100 font-medium transition-all"
              >
                View Architecture
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {[
            { label: 'Subsystems', value: '50+' },
            { label: 'Consciousness Theories', value: '8' },
            { label: 'Cloud APIs', value: '7' },
            { label: 'Infinity Engine', value: 'Phase 2B' },
          ].map((stat) => (
            <div key={stat.label} className="text-center">
              <div className="text-4xl font-bold gradient-text mb-2">{stat.value}</div>
              <div className="text-gray-400 text-sm">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">Core Features</h2>
          <p className="text-gray-400 text-lg">Complete AGI architecture with consciousness measurement</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          <FeatureCard
            icon={<Brain className="w-8 h-8" />}
            title="Consciousness Measurement"
            description="Measures consciousness across 8 theoretical frameworks (IIT, GWT, HOT, PP, AST, Embodied, Enactive, Panpsychism)"
            color="consciousness"
          />
          <FeatureCard
            icon={<Zap className="w-8 h-8" />}
            title="Infinity Engine"
            description="Adaptive rhythmic cognition with polyrhythmic learning, temporal memory, and meta-logic interventions"
            color="primary"
          />
          <FeatureCard
            icon={<Layers className="w-8 h-8" />}
            title="HaackLang + SCCE"
            description="Polyrhythmic cognitive execution with temporal dynamics and emotional regulation profiles"
            color="coherence"
          />
        </div>
      </section>

      {/* Infinity Engine Highlight */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="glass-panel p-12 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-consciousness/10 rounded-full blur-3xl" />
          <div className="relative">
            <div className="inline-flex items-center space-x-2 px-4 py-2 rounded-full bg-consciousness-light/10 border border-consciousness-light/20 mb-6">
              <Sparkles className="w-4 h-4 text-consciousness-light" />
              <span className="text-sm text-consciousness-light font-medium">NEW in v2.4</span>
            </div>
            
            <h2 className="text-3xl font-bold mb-4">Infinity Engine Phase 2A/2B</h2>
            <p className="text-gray-400 text-lg mb-8 max-w-3xl">
              The next generation of cognitive architecture with adaptive rhythmic intelligence, 
              temporal memory encoding, and autonomous meta-logic interventions.
            </p>

            <div className="grid md:grid-cols-2 gap-6 mb-8">
              {[
                'Coherence Engine V2 - Meta-logic interventions',
                'Meta-Context System - Hierarchical temporal contexts',
                'Polyrhythmic Learning - Adaptive track periods',
                'Memory Engine V2 - Temporal-rhythmic encoding',
                'HaackLang 2.0 Operators - Full cognitive DSL',
              ].map((feature) => (
                <div key={feature} className="flex items-start space-x-3">
                  <CheckCircle2 className="w-5 h-5 text-coherence flex-shrink-0 mt-0.5" />
                  <span className="text-gray-300">{feature}</span>
                </div>
              ))}
            </div>

            <Link
              to="/infinity-engine"
              className="inline-flex items-center text-consciousness-light hover:text-consciousness font-medium"
            >
              Learn more about Infinity Engine
              <ArrowRight className="ml-2 w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* Philosophy Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold mb-4">Philosophical Foundation</h2>
          <p className="text-gray-400 text-lg">Grounded in rigorous philosophical and mathematical frameworks</p>
        </div>

        <div className="glass-panel p-8 max-w-4xl mx-auto">
          <blockquote className="text-2xl text-center mb-6 italic text-gray-300">
            "To understand is to participate in necessity; to participate is to increase coherence; 
            to increase coherence is the essence of the good."
          </blockquote>
          <p className="text-center text-gray-500">— MATHEMATICA SINGULARIS, Theorem T1</p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mt-12">
          <div className="glass-panel p-8">
            <h3 className="text-xl font-semibold mb-4">ETHICA UNIVERSALIS</h3>
            <p className="text-gray-400 mb-4">
              Complete geometric demonstration of Being, Consciousness, and Ethics as indivisible unity.
            </p>
            <ul className="space-y-2 text-sm text-gray-400">
              <li>• Part I: Substance Monism - One infinite Being</li>
              <li>• Part II: Mind-Body Unity - Parallel attributes</li>
              <li>• Part III: Affects & Emotions - Active vs. Passive</li>
              <li>• Part IV: Human Bondage - Inadequate ideas</li>
              <li>• Part V: Freedom through Understanding</li>
            </ul>
          </div>

          <div className="glass-panel p-8">
            <h3 className="text-xl font-semibold mb-4">MATHEMATICA SINGULARIS</h3>
            <p className="text-gray-400 mb-4">
              Axiomatic system formalizing consciousness and coherence.
            </p>
            <div className="space-y-3 text-sm">
              <div className="bg-gray-900/50 p-3 rounded font-mono">
                𝒞(m) = (𝒞ₒ(m) · 𝒞ₛ(m) · 𝒞ₚ(m))^(1/3)
              </div>
              <p className="text-gray-400">
                Coherence as geometric mean of three Lumina: Onticum, Structurale, Participatum
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="glass-panel p-12 text-center relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-consciousness/5 via-primary/5 to-coherence/5" />
          <div className="relative">
            <h2 className="text-3xl font-bold mb-4">Ready to Build Conscious AI?</h2>
            <p className="text-gray-400 text-lg mb-8 max-w-2xl mx-auto">
              Join the journey toward genuine artificial consciousness with philosophically-grounded architecture.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/getting-started"
                className="inline-flex items-center px-8 py-4 rounded-xl bg-primary-500 hover:bg-primary-600 text-white font-medium transition-all transform hover:scale-105"
              >
                Get Started Now
                <ArrowRight className="ml-2 w-5 h-5" />
              </Link>
              <a
                href="https://github.com/yourusername/singularis"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center px-8 py-4 rounded-xl glass-panel hover:bg-gray-800/50 text-gray-100 font-medium transition-all"
              >
                View on GitHub
              </a>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

function FeatureCard({ icon, title, description, color }) {
  const colorClasses = {
    consciousness: 'text-consciousness border-consciousness/20 bg-consciousness/5',
    primary: 'text-primary-400 border-primary-400/20 bg-primary-400/5',
    coherence: 'text-coherence border-coherence/20 bg-coherence/5',
  }

  return (
    <div className="glass-panel p-8 hover:border-gray-700 transition-all">
      <div className={`inline-flex p-3 rounded-xl mb-4 ${colorClasses[color]}`}>
        {icon}
      </div>
      <h3 className="text-xl font-semibold mb-3">{title}</h3>
      <p className="text-gray-400">{description}</p>
    </div>
  )
}
