import json
import os
import time
import hashlib
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    """Manage caching of crawl results"""
    
    def __init__(self, cache_dir: str = "cache", ttl: int = 3600):
        """
        Initialize the cache manager
        
        Args:
            cache_dir: Directory to store cache files
            ttl: Time to live in seconds (default 1 hour)
        """
        self.cache_dir = cache_dir
        self.ttl = ttl
        
        # Create cache directory if it doesn't exist
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def _get_cache_key(self, key: str) -> str:
        """
        Generate a cache key/filename from a string
        
        Args:
            key: String to hash
            
        Returns:
            Hashed filename
        """
        hash_obj = hashlib.md5(key.encode('utf-8'))
        return hash_obj.hexdigest()
    
    def _get_cache_path(self, key: str) -> str:
        """
        Get the full path to a cache file
        
        Args:
            key: Cache key
            
        Returns:
            Full path to cache file
        """
        return os.path.join(self.cache_dir, f"{self._get_cache_key(key)}.json")
    
    def get(self, key: str) -> Optional[Dict]:
        """
        Get item from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached data or None if not found or expired
        """
        cache_path = self._get_cache_path(key)
        
        # Check if cache file exists
        if not os.path.exists(cache_path):
            return None
        
        try:
            # Read cache file
            with open(cache_path, 'r') as f:
                cache_data = json.load(f)
            
            # Check if cache is expired
            if time.time() - cache_data.get('timestamp', 0) > self.ttl:
                logger.debug(f"Cache expired for {key}")
                return None
            
            logger.debug(f"Cache hit for {key}")
            return cache_data.get('data')
            
        except Exception as e:
            logger.error(f"Error reading cache: {str(e)}")
            return None
    
    def set(self, key: str, data: Any) -> bool:
        """
        Set item in cache
        
        Args:
            key: Cache key
            data: Data to cache
            
        Returns:
            True if successful, False otherwise
        """
        cache_path = self._get_cache_path(key)
        
        try:
            # Prepare cache data
            cache_data = {
                'timestamp': time.time(),
                'data': data
            }
            
            # Write to cache file
            with open(cache_path, 'w') as f:
                json.dump(cache_data, f)
            
            logger.debug(f"Cached data for {key}")
            return True
            
        except Exception as e:
            logger.error(f"Error writing to cache: {str(e)}")
            return False
    
    def clear(self, key: Optional[str] = None) -> bool:
        """
        Clear cache
        
        Args:
            key: Specific key to clear, or None to clear all
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if key:
                # Clear specific cache item
                cache_path = self._get_cache_path(key)
                if os.path.exists(cache_path):
                    os.remove(cache_path)
                    logger.debug(f"Cleared cache for {key}")
            else:
                # Clear all cache items
                for filename in os.listdir(self.cache_dir):
                    if filename.endswith('.json'):
                        os.remove(os.path.join(self.cache_dir, filename))
                logger.debug("Cleared all cache")
            
            return True
            
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
            return False
