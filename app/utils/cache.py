"""
Simple caching utility
In-memory cache with TTL support
"""

from datetime import datetime, timedelta
from typing import Any, Optional
import json


class SimpleCache:
    """Simple in-memory cache with TTL"""
    
    def __init__(self):
        self.cache = {}
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if expired/not found
        """
        if key not in self.cache:
            self.misses += 1
            return None
        
        entry = self.cache[key]
        
        # Check if expired
        if datetime.now() > entry['expires_at']:
            del self.cache[key]
            self.misses += 1
            return None
        
        self.hits += 1
        return entry['value']
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (default: 1 hour)
        """
        expires_at = datetime.now() + timedelta(seconds=ttl)
        
        self.cache[key] = {
            'value': value,
            'expires_at': expires_at,
            'created_at': datetime.now()
        }
    
    def delete(self, key: str):
        """Delete key from cache"""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self):
        """Clear all cache"""
        self.cache = {}
        self.hits = 0
        self.misses = 0
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'hits': self.hits,
            'misses': self.misses,
            'total_requests': total_requests,
            'hit_rate': round(hit_rate, 2),
            'cached_items': len(self.cache)
        }
    
    def stats(self) -> dict:
        """Alias for get_stats()"""
        return self.get_stats()
    
    def cleanup_expired(self):
        """Remove expired entries"""
        now = datetime.now()
        expired_keys = [
            key for key, entry in self.cache.items()
            if now > entry['expires_at']
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        return len(expired_keys)


# Global cache instance
cache = SimpleCache()


def cached(ttl: int = 3600):
    """
    Decorator for caching function results
    
    Args:
        ttl: Time to live in seconds
        
    Usage:
        @cached(ttl=1800)
        def expensive_function(arg1, arg2):
            # ... expensive operation
            return result
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            key_parts = [func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = ":".join(key_parts)
            
            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl=ttl)
            
            return result
        
        return wrapper
    return decorator

