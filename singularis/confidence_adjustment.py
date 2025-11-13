"""
Coherence-Based Confidence Adjustment

When the system has low consciousness coherence (𝒞 < 0.5), it should be less
confident in its actions. This prevents the system from acting boldly when it's
confused or uncertain about its state.

Example:
- Base confidence: 0.84 (from logic system)
- Coherence: 0.31 (low - system is confused)
- Adjusted confidence: 0.52 (dampened by low coherence)

This addresses the problem where the system acts with high confidence (0.84)
even when coherence is only 0.31-0.42.
"""

from typing import Tuple


def adjust_confidence(
    base_confidence: float,
    coherence: float,
    coherence_threshold: float = 0.5,
    min_confidence: float = 0.3,
    dampening_strength: float = 0.7
) -> Tuple[float, str]:
    """
    Adjust action confidence based on system coherence.
    
    When coherence is below threshold, confidence is dampened to reflect
    the system's uncertainty.
    
    Args:
        base_confidence: Original confidence score (0-1)
        coherence: Current consciousness coherence 𝒞 (0-1)
        coherence_threshold: Below this, confidence is dampened (default: 0.5)
        min_confidence: Minimum allowed confidence (default: 0.3)
        dampening_strength: How strongly to dampen (0=no dampening, 1=full dampening)
        
    Returns:
        Tuple of (adjusted_confidence, explanation)
    """
    # No adjustment needed if coherence is good
    if coherence >= coherence_threshold:
        return (
            base_confidence,
            f"No adjustment (coherence {coherence:.3f} ≥ threshold {coherence_threshold:.3f})"
        )
    
    # Compute dampening factor based on how far below threshold
    coherence_deficit = coherence_threshold - coherence
    dampening_factor = 1.0 - (coherence_deficit * dampening_strength)
    dampening_factor = max(dampening_factor, 0.0)
    
    # Apply dampening
    adjusted = base_confidence * dampening_factor
    adjusted = max(adjusted, min_confidence)  # Floor at minimum
    
    change = adjusted - base_confidence
    
    explanation = (
        f"Dampened due to low coherence: "
        f"{base_confidence:.3f} → {adjusted:.3f} "
        f"(𝒞={coherence:.3f}, Δ={change:+.3f})"
    )
    
    return adjusted, explanation


def compute_confidence_multiplier(coherence: float) -> float:
    """
    Compute a multiplier for confidence based on coherence.
    
    This can be used to scale multiple confidence scores at once.
    
    Coherence ranges:
    - 0.7-1.0: Full confidence (1.0x multiplier)
    - 0.5-0.7: Moderate confidence (0.7-1.0x)
    - 0.3-0.5: Low confidence (0.4-0.7x)
    - 0.0-0.3: Very low confidence (0.3-0.4x)
    
    Args:
        coherence: Current consciousness coherence 𝒞 (0-1)
        
    Returns:
        Confidence multiplier (0.3-1.0)
    """
    if coherence >= 0.7:
        return 1.0
    elif coherence >= 0.5:
        # Linear interpolation: 0.7 @ coherence=0.7, 0.7 @ coherence=0.5
        return 0.7 + (coherence - 0.5) * 1.5
    elif coherence >= 0.3:
        # Linear interpolation: 0.4 @ coherence=0.5, 0.4 @ coherence=0.3
        return 0.4 + (coherence - 0.3) * 1.5
    else:
        # Very low coherence
        return 0.3 + coherence


def should_delay_action(
    adjusted_confidence: float,
    coherence: float,
    confidence_threshold: float = 0.5
) -> Tuple[bool, str]:
    """
    Determine if an action should be delayed due to low confidence/coherence.
    
    When both confidence and coherence are low, the system should wait
    for more information rather than acting rashly.
    
    Args:
        adjusted_confidence: Confidence after coherence adjustment
        coherence: Current consciousness coherence
        confidence_threshold: Minimum confidence to act
        
    Returns:
        Tuple of (should_delay, reason)
    """
    if adjusted_confidence < confidence_threshold and coherence < 0.4:
        return (
            True,
            f"Low confidence ({adjusted_confidence:.3f}) AND low coherence ({coherence:.3f})"
        )
    
    if adjusted_confidence < confidence_threshold * 0.7:
        return (
            True,
            f"Very low confidence ({adjusted_confidence:.3f}) after dampening"
        )
    
    return False, "Sufficient confidence to act"


# Example usage:
if __name__ == "__main__":
    print("Coherence-Based Confidence Adjustment Examples\n")
    print("=" * 60)
    
    test_cases = [
        (0.84, 0.31, "High base confidence, very low coherence"),
        (0.84, 0.42, "High base confidence, low coherence"),
        (0.84, 0.55, "High base confidence, moderate coherence"),
        (0.84, 0.75, "High base confidence, high coherence"),
        (0.60, 0.31, "Moderate base confidence, very low coherence"),
        (0.45, 0.40, "Low base confidence, low coherence"),
    ]
    
    for base_conf, coh, description in test_cases:
        adjusted, explanation = adjust_confidence(base_conf, coh)
        multiplier = compute_confidence_multiplier(coh)
        delay, delay_reason = should_delay_action(adjusted, coh)
        
        print(f"\n{description}:")
        print(f"  Base: {base_conf:.3f}, Coherence: {coh:.3f}")
        print(f"  Adjusted: {adjusted:.3f}")
        print(f"  Multiplier: {multiplier:.3f}")
        print(f"  Delay Action: {'YES' if delay else 'NO'}")
        if delay:
            print(f"    Reason: {delay_reason}")
    
    print("\n" + "=" * 60)
