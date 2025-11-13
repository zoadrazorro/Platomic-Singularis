"""
STUCK Recovery Tracking System

Monitors whether unstick actions actually work by tracking visual similarity
before and after recovery attempts.

Problem:
User's session log showed: "STUCK detection (similarity=1.000) ignored"
System detected stuck but didn't verify if recovery actions worked.

Solution:
Track each STUCK recovery attempt:
1. Detect STUCK (visual similarity ≈ 1.0)
2. Try recovery action
3. Measure if visual similarity decreased
4. Log success/failure rate
5. Adapt strategy based on what works
"""

from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum
import time
import numpy as np


class RecoveryStatus(Enum):
    """Status of a recovery attempt."""
    PENDING = "pending"          # Recovery action issued, waiting to verify
    SUCCESS = "success"          # Visual state changed significantly
    PARTIAL = "partial"          # Small change, might need more attempts
    FAILED = "failed"            # No change, recovery action didn't work
    TIMEOUT = "timeout"          # Took too long to verify


@dataclass
class StuckDetection:
    """A detected stuck state."""
    timestamp: float
    visual_similarity: float  # How similar (0-1, 1.0 = identical)
    repeated_action: str
    repeat_count: int
    coherence: float
    location: str


@dataclass
class RecoveryAttempt:
    """A single recovery attempt."""
    stuck_detection: StuckDetection
    recovery_action: str
    action_timestamp: float
    
    # Visual state tracking
    visual_before: Optional[np.ndarray] = None
    visual_after: Optional[np.ndarray] = None
    similarity_before: float = 0.0
    similarity_after: float = 0.0
    
    # Results
    status: RecoveryStatus = RecoveryStatus.PENDING
    cycles_to_verify: int = 0
    improvement: float = 0.0  # How much similarity decreased
    
    def compute_success(self):
        """Compute whether recovery was successful based on visual change."""
        if self.visual_before is None or self.visual_after is None:
            self.status = RecoveryStatus.TIMEOUT
            return
        
        # Compute new similarity
        self.similarity_after = np.dot(
            self.visual_before.flatten(),
            self.visual_after.flatten()
        ) / (
            np.linalg.norm(self.visual_before) * np.linalg.norm(self.visual_after) + 1e-8
        )
        
        # Improvement is reduction in similarity (lower = more change)
        self.improvement = self.similarity_before - self.similarity_after
        
        # Classify success
        if self.improvement >= 0.15:
            self.status = RecoveryStatus.SUCCESS
        elif self.improvement >= 0.05:
            self.status = RecoveryStatus.PARTIAL
        else:
            self.status = RecoveryStatus.FAILED


class StuckRecoveryTracker:
    """
    Tracks STUCK detection and recovery attempts.
    
    Monitors:
    - Detection rate (how often we detect stuck)
    - Recovery success rate (% of recoveries that work)
    - Which actions work best for recovery
    - Typical time to recover
    """
    
    def __init__(
        self,
        verification_cycles: int = 3,
        max_history: int = 100
    ):
        """
        Initialize tracker.
        
        Args:
            verification_cycles: How many cycles after recovery to check
            max_history: Maximum recovery attempts to remember
        """
        self.verification_cycles = verification_cycles
        self.max_history = max_history
        
        # Current tracking
        self.detections: List[StuckDetection] = []
        self.recovery_attempts: List[RecoveryAttempt] = []
        self.pending_verifications: List[RecoveryAttempt] = []
        
        # Statistics
        self.total_detections = 0
        self.total_recoveries = 0
        self.successful_recoveries = 0
        self.failed_recoveries = 0
        
        # Recovery action effectiveness
        self.action_success_rates: dict[str, tuple[int, int]] = {}  # action -> (successes, attempts)
    
    def detect_stuck(
        self,
        visual_similarity: float,
        repeated_action: str,
        repeat_count: int,
        coherence: float,
        location: str
    ) -> StuckDetection:
        """
        Record a STUCK detection.
        
        Args:
            visual_similarity: Visual similarity score (0-1)
            repeated_action: Action being repeated
            repeat_count: How many times repeated
            coherence: Current consciousness coherence
            location: Current location
            
        Returns:
            StuckDetection object
        """
        detection = StuckDetection(
            timestamp=time.time(),
            visual_similarity=visual_similarity,
            repeated_action=repeated_action,
            repeat_count=repeat_count,
            coherence=coherence,
            location=location
        )
        
        self.detections.append(detection)
        self.total_detections += 1
        
        # Keep history bounded
        if len(self.detections) > self.max_history:
            self.detections.pop(0)
        
        print(f"\n[STUCK-TRACKER] DETECTION #{self.total_detections}:")
        print(f"   Visual Similarity: {visual_similarity:.3f}")
        print(f"   Repeated Action: {repeated_action} x{repeat_count}")
        print(f"   Coherence: {coherence:.3f}")
        print(f"   Location: {location}")
        
        return detection
    
    def attempt_recovery(
        self,
        detection: StuckDetection,
        recovery_action: str,
        visual_before: np.ndarray
    ) -> RecoveryAttempt:
        """
        Record a recovery attempt.
        
        Args:
            detection: The stuck detection this is recovering from
            recovery_action: Action being taken to recover
            visual_before: Visual embedding before recovery
            
        Returns:
            RecoveryAttempt object
        """
        attempt = RecoveryAttempt(
            stuck_detection=detection,
            recovery_action=recovery_action,
            action_timestamp=time.time(),
            visual_before=visual_before,
            similarity_before=detection.visual_similarity
        )
        
        self.recovery_attempts.append(attempt)
        self.pending_verifications.append(attempt)
        self.total_recoveries += 1
        
        # Keep history bounded
        if len(self.recovery_attempts) > self.max_history:
            self.recovery_attempts.pop(0)
        
        print(f"\n[STUCK-TRACKER] RECOVERY ATTEMPT #{self.total_recoveries}:")
        print(f"   Action: {recovery_action}")
        print(f"   From: {detection.repeated_action} x{detection.repeat_count}")
        print(f"   Similarity Before: {detection.visual_similarity:.3f}")
        print(f"   Status: PENDING (verifying in {self.verification_cycles} cycles)")
        
        return attempt
    
    def verify_recovery(
        self,
        attempt: RecoveryAttempt,
        visual_after: np.ndarray
    ):
        """
        Verify if a recovery attempt succeeded.
        
        Args:
            attempt: The recovery attempt to verify
            visual_after: Visual embedding after recovery
        """
        attempt.visual_after = visual_after
        attempt.compute_success()
        
        # Update statistics
        if attempt.status == RecoveryStatus.SUCCESS:
            self.successful_recoveries += 1
        elif attempt.status == RecoveryStatus.FAILED:
            self.failed_recoveries += 1
        
        # Update action effectiveness
        action = attempt.recovery_action
        if action not in self.action_success_rates:
            self.action_success_rates[action] = (0, 0)
        
        successes, attempts = self.action_success_rates[action]
        if attempt.status == RecoveryStatus.SUCCESS:
            successes += 1
        self.action_success_rates[action] = (successes, attempts + 1)
        
        # Remove from pending
        if attempt in self.pending_verifications:
            self.pending_verifications.remove(attempt)
        
        # Log result
        print(f"\n[STUCK-TRACKER] RECOVERY VERIFICATION:")
        print(f"   Action: {attempt.recovery_action}")
        print(f"   Status: {attempt.status.value.upper()}")
        print(f"   Similarity: {attempt.similarity_before:.3f} → {attempt.similarity_after:.3f}")
        print(f"   Improvement: {attempt.improvement:+.3f}")
        print(f"   Cycles: {attempt.cycles_to_verify}")
    
    def tick_cycle(self, current_visual: Optional[np.ndarray] = None):
        """
        Advance cycle counter and verify pending recoveries.
        
        Args:
            current_visual: Current visual embedding
        """
        if current_visual is None:
            return
        
        completed = []
        
        for attempt in self.pending_verifications:
            attempt.cycles_to_verify += 1
            
            # Time to verify?
            if attempt.cycles_to_verify >= self.verification_cycles:
                self.verify_recovery(attempt, current_visual)
                completed.append(attempt)
        
        # Remove completed from pending
        for attempt in completed:
            if attempt in self.pending_verifications:
                self.pending_verifications.remove(attempt)
    
    def get_best_recovery_action(self) -> Optional[str]:
        """
        Get the recovery action with highest success rate.
        
        Returns:
            Best recovery action, or None if no data
        """
        if not self.action_success_rates:
            return None
        
        best_action = None
        best_rate = 0.0
        
        for action, (successes, attempts) in self.action_success_rates.items():
            if attempts > 0:
                rate = successes / attempts
                if rate > best_rate:
                    best_rate = rate
                    best_action = action
        
        return best_action
    
    def get_stats(self) -> dict:
        """Get recovery statistics."""
        return {
            'total_detections': self.total_detections,
            'total_recoveries': self.total_recoveries,
            'successful_recoveries': self.successful_recoveries,
            'failed_recoveries': self.failed_recoveries,
            'success_rate': self.successful_recoveries / max(self.total_recoveries, 1),
            'pending_verifications': len(self.pending_verifications),
            'action_success_rates': {
                action: {'successes': s, 'attempts': a, 'rate': s/a if a > 0 else 0}
                for action, (s, a) in self.action_success_rates.items()
            },
            'best_recovery_action': self.get_best_recovery_action()
        }
    
    def print_summary(self):
        """Print a summary of recovery tracking."""
        stats = self.get_stats()
        
        print("\n" + "=" * 70)
        print("STUCK RECOVERY TRACKING SUMMARY")
        print("=" * 70)
        print(f"Total STUCK Detections: {stats['total_detections']}")
        print(f"Total Recovery Attempts: {stats['total_recoveries']}")
        print(f"Successful: {stats['successful_recoveries']} ({stats['success_rate']:.1%})")
        print(f"Failed: {stats['failed_recoveries']}")
        print(f"Pending Verification: {stats['pending_verifications']}")
        
        if stats['action_success_rates']:
            print("\nRecovery Action Effectiveness:")
            for action, data in sorted(
                stats['action_success_rates'].items(),
                key=lambda x: x[1]['rate'],
                reverse=True
            ):
                print(f"  {action}: {data['successes']}/{data['attempts']} ({data['rate']:.1%})")
        
        if stats['best_recovery_action']:
            print(f"\nBest Recovery Action: {stats['best_recovery_action']}")
        
        print("=" * 70 + "\n")
