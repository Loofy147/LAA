
import sys
import os
sys.path.append(os.path.abspath('laa_core/target/release'))
import laa_core

# Test SkiRental
ski_rental = laa_core.SkiRental(100.0)
decision = ski_rental.decide(1, 120.0, 0.5)
print(f"Ski Rental Decision: {decision}")

# Test Caching
predictions = {1: 10, 2: 5, 3: 12}
caching = laa_core.Caching(2, predictions)
cache = [1, 2]
decision, new_cache = caching.decide(3, cache)
print(f"Caching Decision: {decision}, New Cache: {new_cache}")

# Test OnewayTrading
oneway_trading = laa_core.OnewayTrading(100.0)
decision = oneway_trading.decide(110.0, 120.0, 0.5)
print(f"Oneway Trading Decision: {decision}")
