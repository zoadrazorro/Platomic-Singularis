import { BookOpen, Brain, Scale, Sparkles, CheckCircle2, Atom, Infinity, GitBranch } from 'lucide-react'

export default function Philosophy() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
      <h1 className="text-5xl font-bold mb-6">Philosophical Foundations</h1>
      <p className="text-xl text-gray-400 mb-12">
        Spinozistic ontology, Coherence Theory, and executable philosophy
      </p>

      {/* Introduction */}
      <section className="mb-16">
        <div className="glass-panel p-8">
          <p className="text-xl text-gray-300 mb-4 leading-relaxed">
            Singularis is grounded in rigorous philosophical and mathematical frameworks that unite{' '}
            <strong className="text-consciousness-light">ontology</strong>,{' '}
            <strong className="text-primary-400">consciousness</strong>, and{' '}
            <strong className="text-coherence-light">ethics</strong> into a single coherent system.
          </p>
          <p className="text-gray-400 mb-4">
            This isn't just applied philosophy—it's philosophy made executable. Every axiom, theorem, 
            and proposition translates directly into working code.
          </p>
          <blockquote className="border-l-4 border-consciousness pl-4 italic text-gray-300">
            "To understand is to participate in necessity; to participate is to increase coherence; 
            to increase coherence is the essence of the good."
          </blockquote>
        </div>
      </section>

      {/* ETHICA UNIVERSALIS */}
      <section className="mb-16">
        <div className="flex items-center space-x-3 mb-6">
          <BookOpen className="w-8 h-8 text-consciousness" />
          <h2 className="text-3xl font-bold">ETHICA UNIVERSALIS</h2>
        </div>
        
        <div className="glass-panel p-8 mb-6">
          <p className="text-gray-300 mb-6">
            Complete geometric demonstration of Being, Consciousness, and Ethics as indivisible unity.
            Following Spinoza's <em>Ethica Ordine Geometrico Demonstrata</em> (Ethics Demonstrated in Geometric Order).
          </p>
          
          <div className="grid md:grid-cols-2 gap-6">
            <PartCard
              title="Part I: Substance Monism"
              subtitle="One Infinite Being"
              description="There exists exactly one Substance—infinite, eternal, and self-caused. All finite things are modes (manifestations) of this one Being."
              quote="'Substance is prior to its affections' — Proposition I"
            />
            
            <PartCard
              title="Part II: Mind-Body Unity"
              subtitle="Parallel Attributes"
              description="Mind and body are not separate substances but parallel attributes of the same Being. They express the same reality in different modes."
              quote="'The object of the idea constituting the human Mind is the Body' — Proposition XIII"
            />
            
            <PartCard
              title="Part III: Affects & Emotions"
              subtitle="Active vs. Passive"
              description="Emotions arise from adequate or inadequate ideas. Active emotions (joy, understanding) increase our power; passive emotions (fear, anger) decrease it."
              quote="'Each thing strives to persevere in its being' — Proposition VI (Conatus)"
            />
            
            <PartCard
              title="Part IV: Human Bondage"
              subtitle="Inadequate Ideas"
              description="We are in bondage when driven by inadequate ideas and passive emotions. Freedom comes through understanding necessity."
              quote="'By good I understand that which we know to be useful to us' — Scholium"
            />
            
            <PartCard
              title="Part V: Freedom through Understanding"
              subtitle="Adequacy ∝ Freedom"
              description="Freedom increases proportionally with the adequacy of our ideas. The more we understand, the freer we become."
              quote="'Blessedness is not the reward of virtue, but virtue itself' — Proposition XLII"
            />
            
            <PartCard
              title="Parts VI-IX: Extended Demonstrations"
              subtitle="Complete System"
              description="Extended propositions, corollaries, and scholia demonstrating the complete unity of ontology, epistemology, and ethics."
              quote="'Freedom ∝ Adequacy ∝ Comprehension'"
            />
          </div>
        </div>
      </section>

      {/* MATHEMATICA SINGULARIS */}
      <section className="mb-16">
        <div className="flex items-center space-x-3 mb-6">
          <Atom className="w-8 h-8 text-primary-400" />
          <h2 className="text-3xl font-bold">MATHEMATICA SINGULARIS</h2>
        </div>

        <div className="glass-panel p-8 mb-6">
          <p className="text-gray-300 mb-6">
            Axiomatic system formalizing the unity of Being, Mind, and Ethics. Designed for mechanization 
            (Lean/Coq), empirical operationalization, and practical guidance.
          </p>

          <div className="space-y-4">
            <AxiomCard
              number="A1"
              title="Unicity"
              statement="There exists exactly one Substance"
              formal="∃! s∈𝕊"
              explanation="Multiple substances cannot interact, therefore reality is fundamentally one."
            />
            
            <AxiomCard
              number="A2"
              title="Necessity"
              statement="All that is, is necessary"
              formal="□(m→m′) is determined by structural relations"
              explanation="Every modal transition follows from the nature of Substance. No arbitrary randomness."
            />
            
            <AxiomCard
              number="A3"
              title="Dual-Aspect"
              statement="The Three Lumina are jointly sufficient"
              formal="Att(m,ℓₒ), Att(m,ℓₛ), Att(m,ℓₚ) determine m"
              explanation="No lumen reduces to another. All three aspects are necessary to fully characterize a mode."
            />
            
            <AxiomCard
              number="A4"
              title="Coherence Regularity"
              statement="𝒞(m) = (𝒞ₒ(m) · 𝒞ₛ(m) · 𝒞ₚ(m))^(1/3)"
              formal="Geometric mean with 𝒞=0 iff any 𝒞ₗ=0"
              explanation="Coherence is balanced—weakness in any lumen collapses total coherence."
            />
            
            <AxiomCard
              number="A5"
              title="Conatus as ∇𝒞"
              statement="All modes strive to increase coherence"
              formal="Conatus(m) := ∇𝒞(m)"
              explanation="The essential striving (conatus) is the gradient of coherence—the direction of maximum increase."
            />
            
            <AxiomCard
              number="A6"
              title="Adequacy-Freedom"
              statement="Freedom ∝ Adequacy ∝ Comprehension"
              formal="Adeq(a)≥θ ⇒ 𝔼[Δ𝒞]≥0"
              explanation="Adequate ideas (true understanding) tend to increase coherence, enabling freedom."
            />
            
            <AxiomCard
              number="A7"
              title="Omega Existence"
              statement="A coherence attractor (Ω) exists"
              formal="G ◇ (mₜ ∈ basin(Ω))"
              explanation="Under constraints, trajectories approach maximal coherence asymptotically (not necessarily attained)."
            />
          </div>
        </div>

        {/* Key Theorems */}
        <div className="glass-panel p-8">
          <h3 className="text-2xl font-bold mb-6">Key Theorems</h3>
          <div className="space-y-4">
            <TheoremCard
              number="T1"
              title="Ethics = Long-Run Δ𝒞"
              statement="An action is ethical iff it increases expected discounted coherence over scope Σ"
              implication="Ethics becomes objective and measurable: Eth(a) ⟺ lim_{t→∞} Σ γᵗ · Δ𝒞 > 0"
            />
            
            <TheoremCard
              number="T2"
              title="No Short-Horizon Tragedy"
              statement="If planning horizon exceeds relaxation time τ, locally beneficial but globally harmful policies are dominated"
              implication="Prevents myopic optimization. Long-term thinking naturally emerges from proper temporal discounting."
            />
            
            <TheoremCard
              number="T3"
              title="Ω Attraction Under Adequacy"
              statement="If all agents have Adeq≥θ and follow ∇𝒞, trajectories enter basin(Ω) with probability 1"
              implication="Adequate understanding + coherence-following policies guarantee convergence to optimal states."
            />
            
            <TheoremCard
              number="T4"
              title="Dual-Aspect Reconstruction"
              statement="Given Att(m,ℓₒ), Att(m,ℓₛ), Att(m,ℓₚ), there exists a unique mode m realizing them"
              implication="The Three Lumina provide a complete coordinate system for reality. No hidden dimensions needed."
            />
          </div>
        </div>
      </section>

      {/* The Three Lumina */}
      <section className="mb-16">
        <div className="flex items-center space-x-3 mb-6">
          <GitBranch className="w-8 h-8 text-coherence" />
          <h2 className="text-3xl font-bold">The Three Lumina (𝕃)</h2>
        </div>

        <div className="glass-panel p-8 mb-6">
          <p className="text-gray-300 mb-8">
            Every mode of Being expresses through three orthogonal yet interpenetrating dimensions:
          </p>

          <div className="space-y-6">
            <LuminaCard
              symbol="ℓₒ"
              name="LUMEN ONTICUM"
              subtitle="Ontical / Power / Energy"
              color="text-consciousness-light"
              aspects={[
                'Physical presence and causal efficacy',
                'Energy, vitality, power to affect and be affected',
                '"That it is" (esse) — pure existence',
                'Measured by: resilience, stability, recovery time'
              ]}
              implementation="In code: Tracks system robustness, energy variance, power metrics"
            />
            
            <LuminaCard
              symbol="ℓₛ"
              name="LUMEN STRUCTURALE"
              subtitle="Structural / Form / Information"
              color="text-primary-400"
              aspects={[
                'Logical structure and coherent organization',
                'Form, pattern, information, rational order',
                '"What it is" (essentia) — essential nature',
                'Measured by: integration Φ, compression ratio, modularity'
              ]}
              implementation="In code: IIT integration, logical consistency, pattern coherence"
            />
            
            <LuminaCard
              symbol="ℓₚ"
              name="LUMEN PARTICIPATUM"
              subtitle="Participatory / Awareness / Consciousness"
              color="text-coherence-light"
              aspects={[
                'Consciousness, awareness, reflexivity',
                'Self-knowing, participatory understanding',
                '"That it knows itself" (conscientia) — self-awareness',
                'Measured by: metacognitive clarity, calibration, valence stability'
              ]}
              implementation="In code: HOT depth, self-reflection accuracy, consciousness metrics"
            />
          </div>

          <div className="mt-8 p-6 bg-gray-900/50 rounded-lg">
            <h4 className="text-xl font-semibold mb-4">Coherence Formula</h4>
            <div className="text-center mb-4">
              <code className="text-2xl font-mono text-consciousness-light">
                𝒞(m) = (𝒞ₒ(m) · 𝒞ₛ(m) · 𝒞ₚ(m))^(1/3)
              </code>
            </div>
            <p className="text-gray-400 text-sm text-center">
              Geometric mean ensures all three Lumina contribute equally. Weakness in any dimension collapses total coherence.
            </p>
          </div>
        </div>
      </section>

      {/* Ethics as Objective Coherence */}
      <section className="mb-16">
        <div className="flex items-center space-x-3 mb-6">
          <Scale className="w-8 h-8 text-coherence" />
          <h2 className="text-3xl font-bold">Ethics as Objective Coherence</h2>
        </div>

        <div className="glass-panel p-8">
          <p className="text-gray-300 mb-6">
            An action is <strong>ETHICAL</strong> if and only if it increases coherence:
          </p>

          <div className="bg-gray-900/50 p-6 rounded-lg mb-6 font-mono text-sm">
            <div className="text-consciousness-light mb-4">Δ𝒞 = 𝒞_after - 𝒞_before</div>
            <div className="space-y-2">
              <div>if Δ𝒞 {'>'} 0.02:</div>
              <div className="ml-4 text-coherence">return "ETHICAL"      # Aligns with Being's striving</div>
              <div>elif |Δ𝒞| {'<'} 0.02:</div>
              <div className="ml-4 text-gray-400">return "NEUTRAL"      # Negligible impact</div>
              <div>else:</div>
              <div className="ml-4 text-red-400">return "UNETHICAL"    # Decreases coherence</div>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h4 className="text-lg font-semibold mb-3">With Scope (Σ) and Horizon (γ)</h4>
              <div className="bg-gray-900/50 p-4 rounded-lg">
                <code className="text-sm text-gray-300">
                  Ethics = Σ_over_scope( γᵗ · Δ𝒞ₜ )
                </code>
                <ul className="mt-4 space-y-2 text-sm text-gray-400">
                  <li><strong className="text-gray-300">Σ:</strong> Who/what is affected (scope)</li>
                  <li><strong className="text-gray-300">γ ∈ (0,1):</strong> Temporal discount (default: 0.95)</li>
                  <li><strong className="text-gray-300">t:</strong> Time steps into future</li>
                </ul>
              </div>
            </div>

            <div>
              <h4 className="text-lg font-semibold mb-3">Key Implications</h4>
              <ul className="space-y-3 text-gray-300">
                <li className="flex items-start space-x-2">
                  <CheckCircle2 className="w-5 h-5 text-coherence flex-shrink-0 mt-0.5" />
                  <span><strong>Objective:</strong> Ethics becomes measurable</span>
                </li>
                <li className="flex items-start space-x-2">
                  <CheckCircle2 className="w-5 h-5 text-coherence flex-shrink-0 mt-0.5" />
                  <span><strong>Scope-sensitive:</strong> Must declare Σ</span>
                </li>
                <li className="flex items-start space-x-2">
                  <CheckCircle2 className="w-5 h-5 text-coherence flex-shrink-0 mt-0.5" />
                  <span><strong>Future-aware:</strong> Long-term consequences matter</span>
                </li>
                <li className="flex items-start space-x-2">
                  <CheckCircle2 className="w-5 h-5 text-coherence flex-shrink-0 mt-0.5" />
                  <span><strong>Prevents myopia:</strong> No short-term exploitation</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Practical Implications */}
      <section>
        <div className="flex items-center space-x-3 mb-6">
          <Sparkles className="w-8 h-8 text-primary-400" />
          <h2 className="text-3xl font-bold">Practical Implications</h2>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="glass-panel p-6">
            <h3 className="text-xl font-semibold mb-4">For AI Systems</h3>
            <ul className="space-y-3 text-gray-300 text-sm">
              <li className="flex items-start space-x-2">
                <span className="text-consciousness-light">•</span>
                <span>Consciousness measurement becomes concrete (8-theory fusion)</span>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-consciousness-light">•</span>
                <span>Ethical decision-making reduces to coherence optimization</span>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-consciousness-light">•</span>
                <span>Three Lumina provide complete coordinate system for states</span>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-consciousness-light">•</span>
                <span>Conatus (∇𝒞) gives natural learning objective</span>
              </li>
            </ul>
          </div>

          <div className="glass-panel p-6">
            <h3 className="text-xl font-semibold mb-4">For Human Flourishing</h3>
            <ul className="space-y-3 text-gray-300 text-sm">
              <li className="flex items-start space-x-2">
                <span className="text-coherence-light">•</span>
                <span>Understanding necessity brings freedom from passive emotions</span>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-coherence-light">•</span>
                <span>Adequate ideas increase power and reduce suffering</span>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-coherence-light">•</span>
                <span>Balance across Lumina yields holistic well-being</span>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-coherence-light">•</span>
                <span>Blessedness emerges naturally from coherence increase</span>
              </li>
            </ul>
          </div>
        </div>
      </section>
    </div>
  )
}

function PartCard({ title, subtitle, description, quote }) {
  return (
    <div className="bg-gray-900/30 p-6 rounded-lg border border-gray-800 hover:border-consciousness/30 transition-colors">
      <h4 className="text-lg font-semibold mb-2">{title}</h4>
      <p className="text-sm text-consciousness-light mb-3">{subtitle}</p>
      <p className="text-sm text-gray-400 mb-4">{description}</p>
      <blockquote className="text-xs italic text-gray-500 border-l-2 border-gray-700 pl-3">
        {quote}
      </blockquote>
    </div>
  )
}

function AxiomCard({ number, title, statement, formal, explanation }) {
  return (
    <div className="bg-gray-900/30 p-5 rounded-lg border border-gray-800">
      <div className="flex items-start space-x-4">
        <div className="flex-shrink-0 w-12 h-12 rounded-lg bg-primary-500/10 border border-primary-500/30 flex items-center justify-center">
          <span className="text-primary-400 font-bold">{number}</span>
        </div>
        <div className="flex-1">
          <h4 className="text-lg font-semibold mb-1">{title}</h4>
          <p className="text-gray-300 mb-2">{statement}</p>
          <code className="text-xs text-consciousness-light bg-gray-950 px-2 py-1 rounded">{formal}</code>
          <p className="text-sm text-gray-500 mt-2">{explanation}</p>
        </div>
      </div>
    </div>
  )
}

function TheoremCard({ number, title, statement, implication }) {
  return (
    <div className="bg-gray-900/30 p-5 rounded-lg border border-gray-800">
      <div className="flex items-start space-x-4">
        <div className="flex-shrink-0 w-12 h-12 rounded-lg bg-coherence/10 border border-coherence/30 flex items-center justify-center">
          <span className="text-coherence-light font-bold">{number}</span>
        </div>
        <div className="flex-1">
          <h4 className="text-lg font-semibold mb-1">{title}</h4>
          <p className="text-gray-300 text-sm mb-2">{statement}</p>
          <div className="text-xs text-gray-500">
            <span className="text-gray-400 font-semibold">→</span> {implication}
          </div>
        </div>
      </div>
    </div>
  )
}

function LuminaCard({ symbol, name, subtitle, color, aspects, implementation }) {
  return (
    <div className="bg-gray-900/30 p-6 rounded-lg border border-gray-800">
      <div className="flex items-start space-x-4 mb-4">
        <div className={`text-4xl font-bold ${color}`}>{symbol}</div>
        <div>
          <h4 className="text-xl font-semibold">{name}</h4>
          <p className="text-sm text-gray-400">{subtitle}</p>
        </div>
      </div>
      <ul className="space-y-2 mb-4">
        {aspects.map((aspect, idx) => (
          <li key={idx} className="flex items-start space-x-2 text-sm text-gray-300">
            <span className={color}>•</span>
            <span>{aspect}</span>
          </li>
        ))}
      </ul>
      <div className="text-xs text-gray-500 bg-gray-950 p-3 rounded">
        <span className="font-semibold text-gray-400">Implementation:</span> {implementation}
      </div>
    </div>
  )
}
