"""
Translation Cache Implementation

Hash-based caching system for translations.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from .exceptions import CacheError


class TranslationCache:
    """Content hash-based caching system for translations"""
    
    def __init__(self, cache_dir: str, ttl_hours: int = 24 * 30):  # 30 days default TTL
        self.cache_dir = Path(cache_dir)
        self.ttl_hours = ttl_hours
        
        # Create cache directory if it doesn't exist
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_path(self, content_hash: str, target_lang: str) -> Path:
        """Get cache file path for a content hash and target language"""
        filename = f"{content_hash}_{target_lang}.json"
        return self.cache_dir / filename
    
    def _generate_content_hash(self, content: str) -> str:
        """Generate SHA-256 hash of content"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def _is_cache_valid(self, cache_data: Dict[str, Any]) -> bool:
        """Check if cached data is still valid (not expired)"""
        if 'timestamp' not in cache_data:
            return False
        
        try:
            cached_time = datetime.fromisoformat(cache_data['timestamp'])
            expiry_time = cached_time + timedelta(hours=self.ttl_hours)
            return datetime.now() < expiry_time
        except (ValueError, KeyError):
            return False
    
    def get_cached_translation(self, content: str, target_lang: str) -> Optional[str]:
        """Retrieve cached translation if available and valid"""
        
        content_hash = self._generate_content_hash(content)
        cache_path = self._get_cache_path(content_hash, target_lang)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # Check if cache is still valid
            if not self._is_cache_valid(cache_data):
                # Remove expired cache
                self._remove_cache_file(cache_path)
                return None
            
            # Verify content hash matches
            if cache_data.get('content_hash') != content_hash:
                # Hash mismatch, remove invalid cache
                self._remove_cache_file(cache_path)
                return None
            
            return cache_data.get('translation')
            
        except (json.JSONDecodeError, KeyError, OSError) as e:
            # Cache file is corrupted or unreadable, remove it
            self._remove_cache_file(cache_path)
            return None
    
    def cache_translation(self, content: str, target_lang: str, translation: str, 
                         source_lang: str = None, metadata: Dict[str, Any] = None) -> None:
        """Store translation in cache with metadata"""
        
        content_hash = self._generate_content_hash(content)
        cache_path = self._get_cache_path(content_hash, target_lang)
        
        cache_data = {
            'content_hash': content_hash,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'translation': translation,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
        except OSError as e:
            raise CacheError(f"Failed to write cache file: {e}")
    
    def invalidate_cache(self, content: str, target_lang: str = None) -> None:
        """Remove cached translations for specific content"""
        
        content_hash = self._generate_content_hash(content)
        
        if target_lang:
            # Remove specific language cache
            cache_path = self._get_cache_path(content_hash, target_lang)
            self._remove_cache_file(cache_path)
        else:
            # Remove all language caches for this content
            for cache_file in self.cache_dir.glob(f"{content_hash}_*.json"):
                self._remove_cache_file(cache_file)
    
    def _remove_cache_file(self, cache_path: Path) -> None:
        """Safely remove cache file"""
        try:
            if cache_path.exists():
                cache_path.unlink()
        except OSError:
            # Ignore errors when removing cache files
            pass
    
    def clear_cache(self) -> None:
        """Clear all cached translations"""
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                self._remove_cache_file(cache_file)
        except OSError as e:
            raise CacheError(f"Failed to clear cache: {e}")
    
    def cleanup_expired_cache(self) -> int:
        """Remove expired cache entries and return count of removed files"""
        removed_count = 0
        
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                
                if not self._is_cache_valid(cache_data):
                    self._remove_cache_file(cache_file)
                    removed_count += 1
                    
            except (json.JSONDecodeError, OSError):
                # Remove corrupted cache files
                self._remove_cache_file(cache_file)
                removed_count += 1
        
        return removed_count
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        cache_files = list(self.cache_dir.glob("*.json"))
        
        stats = {
            'total_cached_translations': len(cache_files),
            'cache_size_mb': sum(f.stat().st_size for f in cache_files) / (1024 * 1024),
            'cache_directory': str(self.cache_dir),
            'languages': set(),
            'oldest_cache': None,
            'newest_cache': None
        }
        
        timestamps = []
        
        for cache_file in cache_files:
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                
                # Collect language codes
                if 'target_lang' in cache_data:
                    stats['languages'].add(cache_data['target_lang'])
                
                # Collect timestamps
                if 'timestamp' in cache_data:
                    timestamps.append(cache_data['timestamp'])
                    
            except (json.JSONDecodeError, OSError):
                continue
        
        stats['languages'] = sorted(list(stats['languages']))
        
        if timestamps:
            timestamps.sort()
            stats['oldest_cache'] = timestamps[0]
            stats['newest_cache'] = timestamps[-1]
        
        return stats
    
    def get_cached_languages(self, content: str) -> List[str]:
        """Get list of languages for which content is cached"""
        content_hash = self._generate_content_hash(content)
        languages = []
        
        for cache_file in self.cache_dir.glob(f"{content_hash}_*.json"):
            try:
                # Extract language from filename
                filename = cache_file.stem
                if '_' in filename:
                    lang = filename.split('_')[-1]
                    languages.append(lang)
            except Exception:
                continue
        
        return sorted(languages)
    
    def __repr__(self) -> str:
        """String representation of cache"""
        stats = self.get_cache_stats()
        return (
            f"TranslationCache("
            f"dir='{self.cache_dir}', "
            f"cached={stats['total_cached_translations']}, "
            f"size={stats['cache_size_mb']:.1f}MB, "
            f"languages={len(stats['languages'])}"
            f")"
        )