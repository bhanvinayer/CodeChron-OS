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
        rx.text(
            label, 
            font_weight="600", 
            color="#1F2937",
            font_size="1.1rem",
            margin_bottom="0.5rem"
        ),
        rx.select(
            TranslatorState.language_keys,
            value=current_lang,
            placeholder="Select language",
            on_change=on_change,
            size="3",
            width="100%",
            min_height="3rem",
            font_size="1rem",
            border_radius="12px",
            border="2px solid #BFDBFE",
            _hover={"border_color": "#2563EB"},
            _focus={"border_color": "#2563EB", "box_shadow": "0 0 0 3px rgba(37, 99, 235, 0.1)"}
        ),
        rx.text(
            TranslatorState.languages.get(current_lang, ""),
            font_size="1rem",
            color="#1F2937",
            font_weight="500"
        ),
        align="center",
        spacing="3",
        width="100%"
    )

def translation_history_item(item: Dict[str, str]) -> rx.Component:
    """Translation history item"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    item["from_lang"], 
                    font_size="1rem", 
                    color="#059669",
                    font_weight="500"
                ),
                rx.text(
                    "→", 
                    color="#2563EB",
                    font_size="1.2rem",
                    font_weight="600"
                ),
                rx.text(
                    item["to_lang"], 
                    font_size="1rem", 
                    color="#DC2626",
                    font_weight="500"
                ),
                spacing="3",
                align="center"
            ),
            rx.divider(color="#BFDBFE", margin="0.5rem 0"),
            rx.vstack(
                rx.hstack(
                    rx.text(
                        "Original:",
                        font_size="0.95rem",
                        color="#059669",
                        font_weight="600"
                    ),
                    rx.text(
                        item["input"], 
                        font_weight="500",
                        font_size="1.1rem",
                        color="#1F2937"
                    ),
                    spacing="2",
                    align="center"
                ),
                rx.hstack(
                    rx.text(
                        "Translation:",
                        font_size="0.95rem",
                        color="#DC2626",
                        font_weight="600"
                    ),
                    rx.text(
                        item["output"], 
                        color="#2563EB",
                        font_weight="600",
                        font_size="1.1rem"
                    ),
                    spacing="2",
                    align="center"
                ),
                spacing="2",
                align="start",
                width="100%"
            ),
            align="start",
            spacing="3",
            width="100%"
        ),
        bg="white",
        border="2px solid #DBEAFE",
        border_radius="16px",
        padding="1.5rem",
        margin_bottom="1rem",
        box_shadow="0 4px 6px rgba(37, 99, 235, 0.1)",
        _hover={
            "box_shadow": "0 8px 25px rgba(37, 99, 235, 0.2)",
            "border_color": "#BFDBFE",
            "transform": "translateY(-2px)"
        },
        transition="all 0.2s ease-in-out",
        width="100%"
    )

def translator_app() -> rx.Component:
    """Translator application"""
    return rx.container(
        rx.vstack(
            # Header
            rx.center(
                rx.vstack(
                    rx.text(
                        "🌐",
                        font_size="4rem",
                        margin_bottom="0.5rem"
                    ),
                    rx.text(
                        "Universal Translator",
                        font_size="3.5rem",
                        font_weight="700",
                        color="#BFC6D0",
                        text_align="center",
                        letter_spacing="-0.025em"
                    ),
                    rx.text(
                        "Translate text between multiple languages with AI precision",
                        font_size="1.3rem",
                        color="#7C3AED",
                        text_align="center",
                        font_weight="400"
                    ),
                    align="center",
                    spacing="4"
                ),
                width="100%",
                margin_bottom="3rem"
            ),
            
            # Main translation interface
            rx.box(
                rx.vstack(
                    # Language selectors
                    rx.hstack(
                        language_selector(
                            TranslatorState.source_language,
                            TranslatorState.set_source_language,
                            "Translate From"
                        ),
                        rx.center(
                            rx.button(
                                "⇄",
                                on_click=TranslatorState.swap_languages,
                                variant="outline",
                                size="4",
                                color_scheme="blue",
                                font_size="2rem",
                                height="4rem",
                                width="4rem",
                                border_radius="50%",
                                border="2px solid #BFDBFE",
                                _hover={
                                    "border_color": "#2563EB",
                                    "bg": "#EFF6FF",
                                    "transform": "rotate(180deg)"
                                },
                                transition="all 0.3s ease"
                            ),
                            width="auto"
                        ),
                        language_selector(
                            TranslatorState.target_language,
                            TranslatorState.set_target_language,
                            "Translate To"
                        ),
                        justify="between",
                        align="center",
                        width="100%",
                        margin_bottom="3rem",
                        spacing="6"
                    ),
                    
                    # Text input and output
                    rx.hstack(
                        # Input side
                        rx.vstack(
                            rx.text(
                                "Enter text to translate:", 
                                font_weight="600",
                                font_size="1.2rem",
                                color="#1F2937",
                                margin_bottom="0.75rem"
                            ),
                            rx.text_area(
                                placeholder="Type your text here...",
                                value=TranslatorState.input_text,
                                on_change=TranslatorState.set_input_text,
                                bg="#EFF6EE",
                                height="180px",
                                resize="none",
                                font_size="1.8rem",
                                border_radius="16px",
                                border="2px solid #BFDBFE",
                                padding="1.25rem",
                                color="#000000",
                                _hover={"border_color": "#059669"},
                                _focus={
                                    "border_color": "#059669", 
                                    "box_shadow": "0 0 0 3px rgba(5, 150, 105, 0.1)"
                                },
                                line_height="1.6"
                            ),
                            width="48%",
                            align="center"
                        ),
                        
                        # Translation arrow
                        rx.center(
                            rx.text(
                                "→", 
                                font_size="3rem", 
                                color="#2563EB",
                                font_weight="300"
                            ),
                            width="4%"
                        ),
                        
                        # Output side
                        rx.vstack(
                            rx.text(
                                "Translation:", 
                                font_weight="600",
                                font_size="1.2rem",
                                color="#1F2937",
                                margin_bottom="0.75rem"
                            ),
                            rx.text_area(
                                value=TranslatorState.translated_text,
                                height="180px",
                                is_read_only=True,
                                bg="#FEF3F2",
                                placeholder="Translation will appear here...",
                                font_size="1.8rem",
                                border_radius="16px",
                                border="2px solid #FECACA",
                                padding="1.25rem",
                                line_height="1.6",
                                color="#000000"
                            ),
                            width="48%",
                            align="center"
                        ),
                        
                        width="100%",
                        margin_bottom="3rem",
                        justify="between",
                        align="start"
                    ),
                    
                    # Action buttons
                    rx.center(
                        rx.hstack(
                            rx.button(
                                rx.cond(
                                    TranslatorState.is_translating,
                                    rx.hstack(
                                        rx.spinner(size="1"),
                                        rx.text("Translating...", font_size="1.1rem", font_weight="500"),
                                        spacing="2"
                                    ),
                                    rx.text("Translate", font_size="1.1rem", font_weight="600")
                                ),
                                on_click=TranslatorState.translate_text,
                                color_scheme="blue",
                                size="4",
                                height="3.5rem",
                                padding="0 2rem",
                                border_radius="12px",
                                box_shadow="0 4px 6px rgba(37, 99, 235, 0.2)",
                                _hover={"box_shadow": "0 6px 20px rgba(37, 99, 235, 0.3)"}
                            ),
                            rx.button(
                                "Clear All",
                                on_click=TranslatorState.clear_translation,
                                variant="outline",
                                size="4",
                                height="3.5rem",
                                padding="0 2rem",
                                border_radius="12px",
                                font_size="1.1rem",
                                font_weight="500",
                                border="2px solid #BFDBFE",
                                _hover={"border_color": "#DC2626", "color": "#DC2626"}
                            ),
                            spacing="4"
                        ),
                        width="100%",
                        margin_bottom="3rem"
                    ),
                    
                    # Demo notice
                    rx.box(
                        rx.hstack(
                            rx.text("ℹ️", font_size="1.5rem"),
                            rx.vstack(
                                rx.text(
                                    "AI-Powered Translation", 
                                    font_weight="700", 
                                    color="#2563EB",
                                    font_size="1.2rem"
                                ),
                                rx.text(
                                    "Uses OpenAI API when available (set OPENAI_API_KEY environment variable). Falls back to demo mode with common words: hello, goodbye, thank you, water, house, friend, and more.",
                                    font_size="1rem",
                                    color="#4B5563",
                                    line_height="1.5"
                                ),
                                align="start",
                                spacing="2"
                            ),
                            align="start",
                            spacing="4"
                        ),
                        bg="linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%)",
                        border="2px solid #BFDBFE",
                        border_radius="16px",
                        padding="1.5rem",
                        margin_bottom="3rem"
                    ),
                    
                    width="100%",
                    spacing="0"
                ),
                bg="white",
                border_radius="24px",
                padding="3rem",
                box_shadow="0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
                margin_bottom="3rem",
                border="1px solid #F3F4F6"
            ),
            
            # Translation History
            rx.cond(
                TranslatorState.translation_history.length() > 0,
                rx.box(
                    rx.hstack(
                        rx.hstack(
                            rx.text("📜", font_size="2rem"),
                            rx.text(
                                "Translation History",
                                font_size="2rem",
                                font_weight="700",
                                color="#1F2937"
                            ),
                            spacing="3",
                            align="center"
                        ),
                        rx.spacer(),
                        rx.button(
                            "Clear History",
                            on_click=TranslatorState.clear_history,
                            variant="outline",
                            color_scheme="red",
                            size="3",
                            font_size="1rem",
                            font_weight="500",
                            border_radius="10px",
                            padding="0.75rem 1.5rem"
                        ),
                        width="100%",
                        margin_bottom="2rem",
                        align="center"
                    ),
                    rx.vstack(
                        rx.foreach(
                            TranslatorState.translation_history,
                            translation_history_item
                        ),
                        width="100%",
                        spacing="0"
                    ),
                    bg="white",
                    border_radius="24px",
                    padding="3rem",
                    box_shadow="0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
                    border="1px solid #F3F4F6"
                ),
                rx.box()
            ),
            
            width="100%",
            spacing="0"
        ),
        max_width="1200px",
        margin="0 auto",
        padding="3rem 2rem",
        bg="linear-gradient(135deg, #1F2937 0%, #374151 50%, #4B5563 100%)",
        min_height="100vh"
    )
