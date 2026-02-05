"""
File organization system for translation extensions.
Handles creation and management of the extensions directory structure.
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

# Import centralized logging
sys.path.insert(0, os.path.dirname(__file__))
from logger_config import get_logger

logger = get_logger("file_organization")


class ExtensionFileManager:
    """Manages the file organization for translation extensions."""

    EXTENSIONS_DIR = "extensions"

    def __init__(self, content_root: str = "content"):
        self.content_root = content_root

    def get_content_dir(self, file_path: str) -> str:
        """Get the directory containing the content file."""
        return os.path.dirname(file_path)

    def get_extensions_dir(self, file_path: str) -> str:
        """Get the extensions directory for a content file."""
        content_dir = self.get_content_dir(file_path)
        return os.path.join(content_dir, self.EXTENSIONS_DIR)

    def ensure_extensions_dir(self, file_path: str) -> str:
        """Ensure the extensions directory exists and return its path."""
        extensions_dir = self.get_extensions_dir(file_path)
        os.makedirs(extensions_dir, exist_ok=True)
        logger.debug(f"Ensured extensions directory exists: {extensions_dir}")
        return extensions_dir

    def get_base_filename(self, file_path: str) -> str:
        """Get the base filename without extension."""
        filename = os.path.basename(file_path)
        return os.path.splitext(filename)[0]

    def get_translation_filename(self, file_path: str, target_language: str) -> str:
        """Generate filename for translation file."""
        base_filename = self.get_base_filename(file_path)
        return f"{base_filename}-{target_language.upper()}.md"

    def get_translation_file_path(self, file_path: str, target_language: str) -> str:
        """Get the full path for a translation file."""
        extensions_dir = self.get_extensions_dir(file_path)
        filename = self.get_translation_filename(file_path, target_language)
        return os.path.join(extensions_dir, filename)

    def write_translation_file(
        self,
        source_file_path: str,
        target_language: str,
        translated_content: str,
        source_language: str,
        file_hash: str,
    ):
        """
        Write a translation file with proper frontmatter.

        Args:
            source_file_path: Path to the original file
            target_language: Target language code
            translated_content: The translated content
            source_language: Source language code
            file_hash: Hash of the source file
        """
        # Ensure extensions directory exists
        self.ensure_extensions_dir(source_file_path)

        # Generate translation file path
        translation_file_path = self.get_translation_file_path(
            source_file_path, target_language
        )

        # Create frontmatter
        frontmatter = self._create_frontmatter(
            source_language, target_language, file_hash
        )

        # Write the file
        full_content = frontmatter + translated_content

        try:
            with open(translation_file_path, "w", encoding="utf-8") as f:
                f.write(full_content)
            logger.info(f"Created translation file: {translation_file_path}")
        except Exception as e:
            logger.error(
                f"Failed to write translation file " f"{translation_file_path}: {e}"
            )
            raise

    def _create_frontmatter(
        self, source_language: str, target_language: str, file_hash: str
    ) -> str:
        """Create frontmatter for translation file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        frontmatter = f"""---
source-language: {source_language}
target-language: {target_language}
last-created: {timestamp}
hash-on-last-created: {file_hash}
translation-type: automatic
---

"""
        return frontmatter

    def get_existing_translations(self, file_path: str) -> List[str]:
        """Get list of existing translation language codes for a file."""
        extensions_dir = self.get_extensions_dir(file_path)

        if not os.path.exists(extensions_dir):
            return []

        base_filename = self.get_base_filename(file_path)
        translations = []

        try:
            for filename in os.listdir(extensions_dir):
                if filename.startswith(base_filename) and filename.endswith(".md"):
                    # Extract language code from filename
                    # (e.g., "article-DE.md" -> "DE")
                    if "-" in filename:
                        lang_part = filename.split("-")[-1]  # Get last part
                        lang_code = lang_part.split(".")[0]  # Remove .md
                        if len(lang_code) == 2:  # Valid language code
                            translations.append(lang_code.lower())
        except Exception as e:
            logger.warning(
                f"Failed to read extensions directory " f"{extensions_dir}: {e}"
            )

        return translations

    def is_translation_current(
        self, source_file_path: str, target_language: str, source_file_hash: str
    ) -> bool:
        """Check if an existing translation file is current."""
        translation_file_path = self.get_translation_file_path(
            source_file_path, target_language
        )

        if not os.path.exists(translation_file_path):
            return False

        try:
            with open(translation_file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract hash from frontmatter
            lines = content.split("\n")
            for line in lines:
                if line.startswith("hash-on-last-created:"):
                    stored_hash = line.split(":", 1)[1].strip()
                    return stored_hash == source_file_hash

            return False
        except Exception as e:
            logger.warning(
                f"Failed to check translation file " f"{translation_file_path}: {e}"
            )
            return False

    def get_translation_metadata(
        self, source_file_path: str, target_language: str
    ) -> Optional[Dict]:
        """Get metadata from an existing translation file."""
        translation_file_path = self.get_translation_file_path(
            source_file_path, target_language
        )

        if not os.path.exists(translation_file_path):
            return None

        try:
            with open(translation_file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse frontmatter
            if not content.startswith("---"):
                return None

            # Find the end of frontmatter
            lines = content.split("\n")
            frontmatter_end = -1
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == "---":
                    frontmatter_end = i
                    break

            if frontmatter_end == -1:
                return None

            # Parse frontmatter
            metadata = {}
            for line in lines[1:frontmatter_end]:
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip()

            return metadata
        except Exception as e:
            logger.warning(
                f"Failed to read translation metadata from "
                f"{translation_file_path}: {e}"
            )
            return None

    def cleanup_old_translations(
        self, source_file_path: str, keep_languages: List[str]
    ):
        """Remove translation files for languages not in the keep list."""
        extensions_dir = self.get_extensions_dir(source_file_path)

        if not os.path.exists(extensions_dir):
            return

        base_filename = self.get_base_filename(source_file_path)
        keep_languages_upper = [lang.upper() for lang in keep_languages]

        try:
            for filename in os.listdir(extensions_dir):
                if filename.startswith(base_filename) and filename.endswith(".md"):
                    # Extract language code
                    if "-" in filename:
                        lang_part = filename.split("-")[-1]
                        lang_code = lang_part.split(".")[0]

                        if (
                            len(lang_code) == 2
                            and lang_code not in keep_languages_upper
                        ):
                            file_path = os.path.join(extensions_dir, filename)
                            os.remove(file_path)
                            logger.info(
                                f"Removed outdated translation file: " f"{file_path}"
                            )
        except Exception as e:
            logger.warning(
                f"Failed to cleanup old translations in " f"{extensions_dir}: {e}"
            )

    def remove_all_translations(self, source_file_path: str):
        """Remove all translation files for a specific source file."""
        extensions_dir = self.get_extensions_dir(source_file_path)

        if not os.path.exists(extensions_dir):
            logger.debug(f"No extensions directory found for {source_file_path}")
            return

        base_filename = self.get_base_filename(source_file_path)
        removed_count = 0

        try:
            for filename in os.listdir(extensions_dir):
                if filename.startswith(base_filename) and filename.endswith(".md"):
                    file_path = os.path.join(extensions_dir, filename)
                    os.remove(file_path)
                    removed_count += 1
                    logger.debug(f"Removed translation file: {file_path}")

            # Remove extensions directory if it's empty
            if removed_count > 0 and not os.listdir(extensions_dir):
                os.rmdir(extensions_dir)
                logger.debug(
                    f"Removed empty extensions directory: " f"{extensions_dir}"
                )

            if removed_count > 0:
                logger.info(
                    f"Removed {removed_count} translation files for "
                    f"{source_file_path}"
                )

        except Exception as e:
            logger.error(
                f"Failed to remove translations for " f"{source_file_path}: {e}"
            )

    def remove_all_translations_global(self, content_root: Optional[str] = None):
        """
        Remove all translation files across the entire project.

        Args:
            content_root: Root directory to search (defaults to self.content_root)
        """
        search_root = content_root or self.content_root
        removed_count = 0
        extensions_dirs_removed = 0

        logger.info(
            f"Starting global cleanup of translation files in " f"{search_root}"
        )

        try:
            for root, dirs, files in os.walk(search_root):
                if "extensions" in dirs:
                    extensions_path = os.path.join(root, "extensions")

                    # Count and remove all .md files in extensions directory
                    try:
                        translation_files = [
                            f for f in os.listdir(extensions_path) if f.endswith(".md")
                        ]

                        for filename in translation_files:
                            file_path = os.path.join(extensions_path, filename)
                            os.remove(file_path)
                            removed_count += 1
                            logger.debug(f"Removed translation file: {file_path}")

                        # Remove the extensions directory if it's empty
                        if not os.listdir(extensions_path):
                            os.rmdir(extensions_path)
                            extensions_dirs_removed += 1
                            logger.debug(
                                f"Removed empty extensions directory: "
                                f"{extensions_path}"
                            )

                    except Exception as e:
                        logger.warning(
                            f"Failed to process extensions directory "
                            f"{extensions_path}: {e}"
                        )

            logger.info(
                f"Global cleanup completed: removed {removed_count} "
                f"translation files and {extensions_dirs_removed} "
                f"empty directories"
            )

        except Exception as e:
            logger.error(f"Failed during global translation cleanup: {e}")

        return removed_count, extensions_dirs_removed
