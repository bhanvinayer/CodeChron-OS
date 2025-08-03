"""
Translator App - Multi-language Translation for Playground 202X
"""

import reflex as rx
from typing import Dict, List
import openai
import os

class TranslatorState(rx.State):
    """State for Translator App"""
    input_text: str = ""
    translated_text: str = ""
    source_language: str = "en"
    target_language: str = "es"
    translation_history: List[Dict[str, str]] = []
    is_translating: bool = False
    
    # Supported languages
    languages = {
        "en": "🇺🇸 English",
        "es": "🇪🇸 Spanish", 
        "fr": "🇫🇷 French",
        "de": "🇩🇪 German",
        "it": "🇮🇹 Italian",
        "pt": "🇵🇹 Portuguese",
        "zh": "🇨🇳 Chinese",
        "ja": "🇯🇵 Japanese",
        "ko": "🇰🇷 Korean",
        "ru": "🇷🇺 Russian",
        "ar": "🇸🇦 Arabic",
        "hi": "🇮🇳 Hindi"
    }
    
    # Simple word translations for demo (in real app, would use translation API)
    demo_translations = {
        "en_es": {
            "hello": "hola",
            "goodbye": "adiós", 
            "thank you": "gracias",
            "please": "por favor",
            "yes": "sí",
            "no": "no",
            "water": "agua",
            "food": "comida",
            "house": "casa",
            "car": "coche",
            "friend": "amigo",
            "family": "familia",
            "love": "amor",
            "time": "tiempo",
            "money": "dinero"
        },
        "en_fr": {
            "hello": "bonjour",
            "goodbye": "au revoir",
            "thank you": "merci",
            "please": "s'il vous plaît",
            "yes": "oui",
            "no": "non",
            "water": "eau",
            "food": "nourriture",
            "house": "maison",
            "car": "voiture",
            "friend": "ami",
            "family": "famille",
            "love": "amour",
            "time": "temps",
            "money": "argent"
        },
        "en_de": {
            "hello": "hallo",
            "goodbye": "auf wiedersehen",
            "thank you": "danke",
            "please": "bitte", 
            "yes": "ja",
            "no": "nein",
            "water": "wasser",
            "food": "essen",
            "house": "haus",
            "car": "auto",
            "friend": "freund",
            "family": "familie",
            "love": "liebe",
            "time": "zeit",
            "money": "geld"
        }
    }
    
    def set_source_language(self, lang: str):
        """Set source language"""
        self.source_language = lang
    
    def set_target_language(self, lang: str):
        """Set target language"""
        self.target_language = lang
    
    def set_input_text(self, text: str):
        """Set input text"""
        self.input_text = text
    
    def set_input_text(self, text: str):
        """Set input text"""
        self.input_text = text
    
    def swap_languages(self):
        """Swap source and target languages"""
        temp = self.source_language
        self.source_language = self.target_language
        self.target_language = temp
        
        # Also swap the texts
        temp_text = self.input_text
        self.input_text = self.translated_text
        self.translated_text = temp_text
    
    async def translate_text(self):
        """Translate the input text using OpenAI API with fallback to demo"""
        if not self.input_text.strip():
            return
        
        self.is_translating = True
        
        try:
            # Try OpenAI translation first
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                from openai import AsyncOpenAI
                client = AsyncOpenAI(api_key=api_key)
                
                source_lang_name = self.languages[self.source_language].split()[1]
                target_lang_name = self.languages[self.target_language].split()[1]
                
                prompt = f"Translate the following text from {source_lang_name} to {target_lang_name}. Only provide the translation, no additional text:\n\n{self.input_text}"
                
                response = await client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a professional translator. Provide accurate translations without additional commentary."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.3
                )
                
                self.translated_text = response.choices[0].message.content.strip()
            else:
                # Fallback to demo translation
                await self._demo_translate()
                
        except Exception as e:
            # Fallback to demo translation on error
            await self._demo_translate()
        
        # Add to history
        self.translation_history.insert(0, {
            "input": self.input_text,
            "output": self.translated_text,
            "from_lang": self.languages[self.source_language],
            "to_lang": self.languages[self.target_language],
            "timestamp": "now"
        })
        
        # Keep only last 10 translations
        if len(self.translation_history) > 10:
            self.translation_history = self.translation_history[:10]
        
        self.is_translating = False
    
    async def _demo_translate(self):
        """Demo translation fallback"""
        # Simulate API delay
        import asyncio
        await asyncio.sleep(1)
        
        # Simple demo translation
        text_lower = self.input_text.lower().strip()
        translation_key = f"{self.source_language}_{self.target_language}"
        
        if translation_key in self.demo_translations:
            translation_dict = self.demo_translations[translation_key]
            if text_lower in translation_dict:
                self.translated_text = translation_dict[text_lower]
            else:
                # Try to find partial matches
                found = False
                for key, value in translation_dict.items():
                    if key in text_lower:
                        self.translated_text = text_lower.replace(key, value)
                        found = True
                        break
                
                if not found:
                    self.translated_text = f"[Translation for '{self.input_text}' not available in demo mode]"
        else:
            self.translated_text = f"[{self.languages[self.source_language].split()[1]} to {self.languages[self.target_language].split()[1]} translation not available in demo]"
    
    def clear_translation(self):
        """Clear current translation"""
        self.input_text = ""
        self.translated_text = ""
    
    def clear_history(self):
        """Clear translation history"""
        self.translation_history = []
    
    @rx.var
    def language_keys(self) -> List[str]:
        """Get list of available language keys"""
        return list(self.languages.keys())

def language_selector(current_lang: str, on_change, label: str) -> rx.Component:
    """Language selector component"""
    return rx.vstack(
        rx.text(label, font_weight="bold", color="#1976D2"),
        rx.select(
            TranslatorState.language_keys,
            value=current_lang,
            placeholder="Select language",
            on_change=on_change,
            size="3"
        ),
        rx.text(
            TranslatorState.languages.get(current_lang, ""),
            font_size="0.9rem",
            color="#666"
        ),
        align="center",
        spacing="2"
    )

def translation_history_item(item: Dict[str, str]) -> rx.Component:
    """Translation history item"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(item["from_lang"], font_size="0.8rem", color="#666"),
                rx.text("→", color="#999"),
                rx.text(item["to_lang"], font_size="0.8rem", color="#666"),
                spacing="2"
            ),
            rx.hstack(
                rx.text(item["input"], font_weight="bold"),
                rx.text("→", color="#1976D2"),
                rx.text(item["output"], color="#1976D2"),
                spacing="3"
            ),
            align="start",
            spacing="1"
        ),
        bg="white",
        border="1px solid #e0e0e0",
        border_radius="8px",
        padding="1rem",
        margin_bottom="0.5rem",
        _hover={"box_shadow": "0 2px 4px rgba(0,0,0,0.1)"}
    )

def translator_app() -> rx.Component:
    """Translator application"""
    return rx.vstack(
        # Header
        rx.text(
            "🌐 Universal Translator",
            font_size="2.5rem",
            font_weight="bold",
            color="#1976D2",
            text_align="center",
            margin_bottom="2rem"
        ),
        
        # Main translation interface
        rx.box(
            rx.vstack(
                # Language selectors
                rx.hstack(
                    language_selector(
                        TranslatorState.source_language,
                        TranslatorState.set_source_language,
                        "From"
                    ),
                    rx.button(
                        "⇄",
                        on_click=TranslatorState.swap_languages,
                        variant="outline",
                        size="3",
                        color_scheme="blue",
                        font_size="1.5rem",
                        align_self="center",
                        margin_top="2rem"
                    ),
                    language_selector(
                        TranslatorState.target_language,
                        TranslatorState.set_target_language,
                        "To"
                    ),
                    justify="between",
                    width="100%",
                    margin_bottom="2rem"
                ),
                
                # Text input and output
                rx.hstack(
                    # Input side
                    rx.vstack(
                        rx.text("Enter text to translate:", font_weight="bold"),
                        rx.text_area(
                            placeholder="Type your text here...",
                            value=TranslatorState.input_text,
                            on_change=TranslatorState.set_input_text,
                            height="150px",
                            resize="none"
                        ),
                        width="45%"
                    ),
                    
                    # Translation arrow
                    rx.center(
                        rx.text("→", font_size="2rem", color="#1976D2"),
                        width="10%"
                    ),
                    
                    # Output side
                    rx.vstack(
                        rx.text("Translation:", font_weight="bold"),
                        rx.text_area(
                            value=TranslatorState.translated_text,
                            height="150px",
                            is_read_only=True,
                            bg="#f8f9fa",
                            placeholder="Translation will appear here..."
                        ),
                        width="45%"
                    ),
                    
                    width="100%",
                    margin_bottom="2rem"
                ),
                
                # Action buttons
                rx.hstack(
                    rx.button(
                        "Translate",
                        on_click=TranslatorState.translate_text,
                        loading=TranslatorState.is_translating,
                        color_scheme="blue",
                        size="3"
                    ),
                    rx.button(
                        "Clear",
                        on_click=TranslatorState.clear_translation,
                        variant="outline",
                        size="3"
                    ),
                    spacing="4",
                    justify="center",
                    margin_bottom="2rem"
                ),
                
                # Demo notice
                rx.box(
                    rx.hstack(
                        rx.text("ℹ️", font_size="1.2rem"),
                        rx.vstack(
                            rx.text("AI Translation", font_weight="bold", color="#1976D2"),
                            rx.text(
                                "Uses OpenAI API when available (set OPENAI_API_KEY environment variable). Falls back to demo mode with limited vocabulary: hello, goodbye, thank you, water, house, friend, etc.",
                                font_size="0.9rem",
                                color="#666"
                            ),
                            align="start"
                        ),
                        align="start",
                        spacing="3"
                    ),
                    bg="#E3F2FD",
                    border="1px solid #BBDEFB",
                    border_radius="8px",
                    padding="1rem",
                    margin_bottom="2rem"
                ),
                
                width="100%"
            ),
            bg="white",
            border_radius="12px",
            padding="2rem",
            box_shadow="0 4px 6px rgba(0,0,0,0.1)",
            margin_bottom="2rem"
        ),
        
        # Translation History
        rx.cond(
            TranslatorState.translation_history.length() > 0,
            rx.box(
                rx.hstack(
                    rx.text(
                        "📜 Translation History",
                        font_size="1.5rem",
                        font_weight="bold",
                        color="#1976D2"
                    ),
                    rx.spacer(),
                    rx.button(
                        "Clear History",
                        on_click=TranslatorState.clear_history,
                        variant="outline",
                        color_scheme="red",
                        size="1"
                    ),
                    width="100%",
                    margin_bottom="1rem"
                ),
                rx.vstack(
                    rx.foreach(
                        TranslatorState.translation_history,
                        translation_history_item
                    ),
                    width="100%"
                ),
                bg="white",
                border_radius="12px",
                padding="2rem",
                box_shadow="0 4px 6px rgba(0,0,0,0.1)"
            ),
            rx.box()
        ),
        
        width="100%",
        max_width="1000px",
        margin="0 auto",
        padding="2rem",
        bg="linear-gradient(135deg, #F0F4F8 0%, #E8F5E8 100%)",
        min_height="100vh"
    )
