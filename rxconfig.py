import reflex as rx

# Reflex configuration for CodeChronOS
config = rx.Config(
    app_name="codechronos",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
    frontend_packages=[
        "lucide-react",
        "framer-motion",
        "@emotion/react",
        "@emotion/styled"
    ],
    tailwind={
        "theme": {
            "extend": {
                "fontFamily": {
                    "retro": ["'Press Start 2P'", "monospace"],
                    "mac": ["'VT323'", "monospace"],
                    "modern": ["'JetBrains Mono'", "monospace"]
                },
                "colors": {
                    "mac": {
                        "beige": "#F2F2F2",
                        "gray": "#C0C0C0",
                        "dark": "#808080"
                    },
                    "block": {
                        "blue": "#3B82F6",
                        "green": "#10B981",
                        "orange": "#F59E0B",
                        "red": "#EF4444"
                    },
                    "vibe": {
                        "purple": "#7C3AED",
                        "cyan": "#06B6D4",
                        "dark": "#0A0A0F"
                    }
                }
            }
        }
    },
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"]
)
