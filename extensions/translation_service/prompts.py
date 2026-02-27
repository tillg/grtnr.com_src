"""
Translation Service Prompts

Engineered prompts for high-quality translation using OpenAI's GPT API.
"""

from typing import Dict, List


class TranslationPrompts:
    """Collection of translation prompts and prompt engineering utilities"""

    # Language code to full name mapping
    LANGUAGE_NAMES = {
        "en": "English",
        "de": "German",
        "fr": "French",
        "es": "Spanish",
        "it": "Italian",
        "pt": "Portuguese",
        "ru": "Russian",
        "ja": "Japanese",
        "ko": "Korean",
        "zh": "Chinese",
        "ar": "Arabic",
        "hi": "Hindi",
        "nl": "Dutch",
        "sv": "Swedish",
        "no": "Norwegian",
        "da": "Danish",
        "fi": "Finnish",
        "pl": "Polish",
        "cs": "Czech",
        "tr": "Turkish",
    }

    # Base translation prompt
    BASE_TRANSLATION_PROMPT = """You are a professional translator specializing in technical content and markdown documents.

TASK: Translate the following markdown content from {source_lang} to {target_lang}.

CRITICAL REQUIREMENTS:
1. Preserve ALL markdown formatting exactly (headers, links, code blocks, lists, tables, etc.)
2. NEVER translate WikiLink targets. Keep the original page name: [[Page Name]] stays [[Page Name]], or use display text syntax: [[Page Name|Translated Display Text]]
3. Keep code blocks and technical terms untranslated unless they are comments
4. Translate alt text in images: ![description](image.jpg) -> ![translated description](image.jpg)
5. Preserve metadata sections (YAML front matter) completely untranslated
6. Maintain the tone and style appropriate for technical/blog content
7. Use native language conventions and idiomatic expressions for the target language
8. Translate headers, body text, and comments, but preserve code syntax
9. Keep URLs and file paths unchanged
10. Preserve HTML tags and attributes

OUTPUT FORMAT REQUIREMENTS:
- Return ONLY the translated markdown content
- Do NOT wrap the output in markdown code blocks (```markdown)
- Do NOT add any explanations or prefixes
- The response should be the raw translated markdown that can be directly written to a file

CONTENT TO TRANSLATE:
{content}

TRANSLATION:"""

    # Language detection prompt
    LANGUAGE_DETECTION_PROMPT = """You are a language detection specialist.

TASK: Detect the primary language of the following text content.

INSTRUCTIONS:
1. Analyze the text and determine the primary language
2. Respond with ONLY the two-letter ISO 639-1 language code
3. Do not include quotes, punctuation, or any other text
4. Valid codes: en, de, fr, es, it, pt, ru, ja, ko, zh, ar, hi, nl, sv, no, da, fi, pl, cs, tr
5. If uncertain, respond with: en

CONTENT:
{content}

LANGUAGE CODE:"""

    # Language-specific adaptations
    LANGUAGE_ADAPTATIONS = {
        "de": {
            "style_notes": "Use formal German (Sie form) for technical content. Compound words should be properly formed.",
            "technical_terms": "Keep English technical terms when they are commonly used in German tech contexts.",
        },
        "fr": {
            "style_notes": "Use formal French register. Maintain proper accent marks and French typography conventions.",
            "technical_terms": "Translate technical terms to French equivalents when available, otherwise keep English terms.",
        },
        "es": {
            "style_notes": "Use neutral Spanish suitable for international audience. Avoid regional slang.",
            "technical_terms": "Use established Spanish technical terms when available.",
        },
        "it": {
            "style_notes": "Use formal Italian register appropriate for technical documentation.",
            "technical_terms": "Keep commonly used English technical terms in Italian tech contexts.",
        },
        "pt": {
            "style_notes": "Use Brazilian Portuguese unless specified otherwise.",
            "technical_terms": "Use Portuguese technical terms when established, otherwise keep English.",
        },
        "ru": {
            "style_notes": "Use formal Russian register. Maintain proper Cyrillic typography.",
            "technical_terms": "Translate technical terms to Russian when established equivalents exist.",
        },
        "ja": {
            "style_notes": "Use appropriate Japanese honorific levels. Mix hiragana, katakana, and kanji appropriately.",
            "technical_terms": "Use katakana for foreign technical terms, Japanese terms when available.",
        },
        "ko": {
            "style_notes": "Use formal Korean register (formal speech level).",
            "technical_terms": "Use Korean technical terms when available, otherwise keep English in parentheses.",
        },
        "zh": {
            "style_notes": "Use simplified Chinese unless specified otherwise. Maintain proper Chinese punctuation.",
            "technical_terms": "Use established Chinese technical terms when available.",
        },
    }

    @classmethod
    def get_language_name(cls, language_code: str) -> str:
        """Get full language name from language code"""
        return cls.LANGUAGE_NAMES.get(language_code.lower(), language_code.upper())

    @classmethod
    def build_translation_prompt(
        cls, content: str, source_lang: str, target_lang: str
    ) -> str:
        """Build a customized translation prompt"""

        # Get language names
        source_name = cls.get_language_name(source_lang)
        target_name = cls.get_language_name(target_lang)

        # Base prompt
        prompt = cls.BASE_TRANSLATION_PROMPT.format(
            source_lang=source_name, target_lang=target_name, content=content
        )

        # Add language-specific adaptations
        if target_lang.lower() in cls.LANGUAGE_ADAPTATIONS:
            adaptations = cls.LANGUAGE_ADAPTATIONS[target_lang.lower()]

            additional_notes = []
            if "style_notes" in adaptations:
                additional_notes.append(f"STYLE: {adaptations['style_notes']}")
            if "technical_terms" in adaptations:
                additional_notes.append(
                    f"TECHNICAL TERMS: {adaptations['technical_terms']}"
                )

            if additional_notes:
                # Insert additional notes before the content
                insertion_point = prompt.find("CONTENT TO TRANSLATE:")
                if insertion_point != -1:
                    notes_text = "\n".join(additional_notes) + "\n\n"
                    prompt = (
                        prompt[:insertion_point] + notes_text + prompt[insertion_point:]
                    )

        return prompt

    @classmethod
    def build_language_detection_prompt(cls, content: str) -> str:
        """Build a language detection prompt"""
        # Truncate content for language detection (first 1000 chars usually sufficient)
        truncated_content = content[:1000] if len(content) > 1000 else content

        return cls.LANGUAGE_DETECTION_PROMPT.format(content=truncated_content)

    @classmethod
    def get_supported_languages(cls) -> List[str]:
        """Get list of supported language codes"""
        return list(cls.LANGUAGE_NAMES.keys())

    @classmethod
    def is_language_supported(cls, language_code: str) -> bool:
        """Check if a language code is supported"""
        return language_code.lower() in cls.LANGUAGE_NAMES

    @classmethod
    def get_system_prompt(cls) -> str:
        """Get system prompt for translation assistant"""
        return """You are a professional translator with expertise in technical documentation, markdown formatting, and multiple programming languages. You maintain perfect formatting while providing natural, idiomatic translations."""

    @classmethod
    def validate_translation_response(
        cls, response: str, original_content: str
    ) -> Dict[str, bool]:
        """Validate translation response for common issues"""

        validation_results = {
            "has_content": len(response.strip()) > 0,
            "preserves_markdown_headers": original_content.count("#")
            == response.count("#"),
            "preserves_code_blocks": original_content.count("```")
            == response.count("```"),
            "preserves_wikilinks": original_content.count("[[") == response.count("[["),
            "preserves_images": original_content.count("![") == response.count("!["),
            "preserves_links": original_content.count("](") == response.count("]("),
            "reasonable_length": 0.3 <= len(response) / len(original_content) <= 3.0,
        }

        return validation_results

    @classmethod
    def suggest_prompt_improvements(
        cls, validation_results: Dict[str, bool]
    ) -> List[str]:
        """Suggest prompt improvements based on validation results"""

        suggestions = []

        if not validation_results.get("preserves_markdown_headers", True):
            suggestions.append("Emphasize header preservation in prompt")

        if not validation_results.get("preserves_code_blocks", True):
            suggestions.append("Strengthen code block preservation instructions")

        if not validation_results.get("preserves_wikilinks", True):
            suggestions.append("Improve WikiLinks handling instructions")

        if not validation_results.get("reasonable_length", True):
            suggestions.append(
                "Review translation length - may be too short or too long"
            )

        if not validation_results.get("has_content", True):
            suggestions.append("Response is empty - check API response handling")

        return suggestions
