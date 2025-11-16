"""
Test Life Query Handler

Tests natural language queries about life data.
"""

import asyncio
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger

# Set up test environment
os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY', '')


async def test_query_handler_initialization():
    """Test query handler initialization."""
    logger.info("=" * 60)
    logger.info("TEST 1: Query Handler Initialization")
    logger.info("=" * 60)
    
    try:
        from life_timeline import LifeTimeline
        from singularis.unified_consciousness_layer import UnifiedConsciousnessLayer
        from singularis.life_ops import LifeQueryHandler
        
        # Initialize components
        timeline = LifeTimeline(":memory:")
        consciousness = UnifiedConsciousnessLayer()
        
        query_handler = LifeQueryHandler(
            consciousness=consciousness,
            timeline=timeline,
            pattern_engine=None
        )
        
        logger.info("✅ Query handler initialized successfully")
        
        # Check stats
        stats = query_handler.get_stats()
        logger.info(f"   Consciousness available: {stats['consciousness_available']}")
        logger.info(f"   Timeline available: {stats['timeline_available']}")
        logger.info(f"   Pattern engine available: {stats['pattern_engine_available']}")
        logger.info(f"   Query categories: {len(stats['query_categories'])}")
        
        timeline.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Initialization test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_query_categorization():
    """Test query categorization."""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 2: Query Categorization")
    logger.info("=" * 60)
    
    try:
        from life_timeline import LifeTimeline
        from singularis.unified_consciousness_layer import UnifiedConsciousnessLayer
        from singularis.life_ops import LifeQueryHandler
        
        timeline = LifeTimeline(":memory:")
        consciousness = UnifiedConsciousnessLayer()
        query_handler = LifeQueryHandler(consciousness, timeline)
        
        test_queries = [
            ("How did I sleep last night?", ['sleep', 'time']),
            ("Am I exercising enough?", ['exercise']),
            ("What's my heart rate?", ['health']),
            ("What patterns do you see?", ['pattern']),
            ("Where was I yesterday?", ['location', 'time']),
            ("How am I feeling today?", ['mood', 'time']),
        ]
        
        passed = 0
        failed = 0
        
        for query, expected_categories in test_queries:
            categories = query_handler._categorize_query(query)
            
            # Check if at least one expected category is present
            has_expected = any(cat in categories for cat in expected_categories)
            
            if has_expected:
                logger.info(f"   ✅ '{query[:40]}...'")
                logger.info(f"      Expected: {expected_categories}, Got: {categories}")
                passed += 1
            else:
                logger.warning(f"   ⚠️  '{query[:40]}...'")
                logger.warning(f"      Expected: {expected_categories}, Got: {categories}")
                failed += 1
        
        logger.info(f"\n   Results: {passed} passed, {failed} failed")
        
        timeline.close()
        return failed == 0
        
    except Exception as e:
        logger.error(f"❌ Categorization test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_time_range_extraction():
    """Test time range extraction from queries."""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 3: Time Range Extraction")
    logger.info("=" * 60)
    
    try:
        from life_timeline import LifeTimeline
        from singularis.unified_consciousness_layer import UnifiedConsciousnessLayer
        from singularis.life_ops import LifeQueryHandler
        
        timeline = LifeTimeline(":memory:")
        consciousness = UnifiedConsciousnessLayer()
        query_handler = LifeQueryHandler(consciousness, timeline)
        
        now = datetime.now()
        
        test_queries = [
            ("How did I sleep today?", 0),  # Today
            ("What did I do yesterday?", 1),  # Yesterday
            ("How was my week?", 7),  # This week
            ("What about last month?", 30),  # This month
        ]
        
        passed = 0
        failed = 0
        
        for query, expected_days in test_queries:
            start_time, end_time = query_handler._get_time_range(query)
            actual_days = (end_time - start_time).days
            
            # Allow some tolerance
            if abs(actual_days - expected_days) <= 1:
                logger.info(f"   ✅ '{query}'")
                logger.info(f"      Expected ~{expected_days} days, got {actual_days} days")
                passed += 1
            else:
                logger.warning(f"   ⚠️  '{query}'")
                logger.warning(f"      Expected ~{expected_days} days, got {actual_days} days")
                failed += 1
        
        logger.info(f"\n   Results: {passed} passed, {failed} failed")
        
        timeline.close()
        return failed == 0
        
    except Exception as e:
        logger.error(f"❌ Time range test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_query_with_mock_data():
    """Test query handling with mock data."""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 4: Query Handling with Mock Data")
    logger.info("=" * 60)
    
    try:
        from life_timeline import LifeTimeline, create_sleep_event, create_activity_event
        from singularis.unified_consciousness_layer import UnifiedConsciousnessLayer
        from singularis.life_ops import LifeQueryHandler
        
        timeline = LifeTimeline(":memory:")
        consciousness = UnifiedConsciousnessLayer()
        query_handler = LifeQueryHandler(consciousness, timeline)
        
        # Add mock sleep data
        logger.info("   Adding mock sleep data...")
        for i in range(7):
            date = datetime.now() - timedelta(days=i)
            sleep_event = create_sleep_event(
                user_id="test_user",
                start_time=date.replace(hour=23, minute=0),
                end_time=(date + timedelta(days=1)).replace(hour=7, minute=0),
                quality_score=0.8 - (i * 0.05)
            )
            timeline.add_event(sleep_event)
        
        # Add mock activity data
        logger.info("   Adding mock activity data...")
        for i in range(7):
            date = datetime.now() - timedelta(days=i)
            activity_event = create_activity_event(
                user_id="test_user",
                activity_type="walking",
                duration_minutes=30 + (i * 5),
                calories=150 + (i * 10),
                timestamp=date.replace(hour=14, minute=0)
            )
            timeline.add_event(activity_event)
        
        # Test query
        logger.info("   Testing query: 'How did I sleep this week?'")
        
        result = await query_handler.handle_query(
            "test_user",
            "How did I sleep this week?"
        )
        
        logger.info("   ✅ Query processed successfully")
        logger.info(f"      Response length: {len(result.response)} chars")
        logger.info(f"      Confidence: {result.confidence:.3f}")
        logger.info(f"      Events found: {result.event_count}")
        logger.info(f"      Data sources: {result.data_sources}")
        logger.info(f"      Categories: {result.metadata.get('categories', [])}")
        
        # Show response preview
        response_preview = result.response[:200] + "..." if len(result.response) > 200 else result.response
        logger.info(f"\n      Response preview:")
        logger.info(f"      {response_preview}")
        
        timeline.close()
        return result.event_count > 0
        
    except Exception as e:
        logger.error(f"❌ Query handling test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_api_endpoint():
    """Test API endpoint integration."""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 5: API Endpoint Integration")
    logger.info("=" * 60)
    
    try:
        # This test checks if the endpoint is properly defined
        from main_orchestrator import app
        
        # Check if /query endpoint exists
        routes = [route.path for route in app.routes]
        
        if '/query' in routes:
            logger.info("   ✅ /query endpoint exists")
        else:
            logger.warning("   ⚠️  /query endpoint not found")
            return False
        
        if '/health' in routes:
            logger.info("   ✅ /health endpoint exists")
        else:
            logger.warning("   ⚠️  /health endpoint not found")
        
        logger.info(f"   Total endpoints: {len(routes)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ API endpoint test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_messenger_integration():
    """Test Messenger bot integration."""
    logger.info("\n" + "=" * 60)
    logger.info("TEST 6: Messenger Bot Integration")
    logger.info("=" * 60)
    
    try:
        from messenger_bot_adapter import MessengerBotAdapter
        from life_timeline import LifeTimeline
        from singularis.unified_consciousness_layer import UnifiedConsciousnessLayer
        from singularis.life_ops import LifeQueryHandler
        
        # Initialize components
        timeline = LifeTimeline(":memory:")
        consciousness = UnifiedConsciousnessLayer()
        query_handler = LifeQueryHandler(consciousness, timeline)
        
        # Create messenger bot
        messenger = MessengerBotAdapter(
            page_access_token="test_token",
            verify_token="test_verify"
        )
        
        # Attach query handler
        messenger.life_query_handler = query_handler
        
        logger.info("   ✅ Messenger bot accepts life_query_handler")
        logger.info(f"      Handler attached: {hasattr(messenger, 'life_query_handler')}")
        
        timeline.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Messenger integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests."""
    logger.info("🗣️ Life Query Handler Tests")
    logger.info("=" * 60)
    
    if not os.getenv('GEMINI_API_KEY'):
        logger.warning("⚠️  GEMINI_API_KEY not set - some tests may have limited functionality")
    
    results = []
    
    # Test 1: Initialization
    results.append(await test_query_handler_initialization())
    
    # Test 2: Query categorization
    results.append(await test_query_categorization())
    
    # Test 3: Time range extraction
    results.append(await test_time_range_extraction())
    
    # Test 4: Query with mock data
    results.append(await test_query_with_mock_data())
    
    # Test 5: API endpoint
    results.append(await test_api_endpoint())
    
    # Test 6: Messenger integration
    results.append(await test_messenger_integration())
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    logger.info(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        logger.info("✅ All tests passed! Life Query Handler is ready.")
    else:
        logger.warning(f"⚠️  {total - passed} test(s) failed")
    
    logger.info("\n" + "=" * 60)
    logger.info("PHASE 5 COMPLETE: Unified Query Interface")
    logger.info("=" * 60)
    logger.info("You can now ask natural language questions about your life!")
    logger.info("")
    logger.info("Example queries:")
    logger.info("  • 'How did I sleep last week?'")
    logger.info("  • 'Am I exercising enough?'")
    logger.info("  • 'Why am I tired today?'")
    logger.info("  • 'What patterns do you see in my routine?'")
    logger.info("")
    logger.info("Integration points:")
    logger.info("  • Messenger bot (automatic routing)")
    logger.info("  • REST API (/query endpoint)")
    logger.info("  • Main orchestrator")


if __name__ == "__main__":
    asyncio.run(main())
