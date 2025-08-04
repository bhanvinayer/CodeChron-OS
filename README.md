
# CodeChron-OS 🖥️

CodeChron-OS is a modern, modular productivity and creativity suite inspired by the evolution of software from 1984 to 2025. It combines retro aesthetics with cutting-edge AI, providing a playground of essential apps, a block-based editor, and seamless integration of utilities—all in a beautiful, responsive web UI.

---

## 🌟 Features by Era

### 🖥️ MacCode 1984
- Pixel-perfect Macintosh 1984 simulator
- Retro UI with authentic grayscale visuals
- Draggable windows: Calculator, Notepad, MacCode, MacDraw, Breakout
- Classic interface builder with form elements

### 🧱 BlockCode 2015
- Colorful drag-and-drop block editor (Scratch-like)
- Logic blocks: loops, conditions, variables
- UI blocks: buttons, inputs, canvas
- Export to Python code
- Dark-themed, modernized block editor

### 🧞 VibeCode 2025
- GPT-4-powered natural language interface
- Prompt-to-code generation
- Live code injection and preview
- Creativity level slider
- AI-powered translation and utilities

### 🏠 Playground (Modern Hub)
- 2x4 grid of 8 main apps: Text Editor, QR Generator, Password Generator, Calculator, Notepad, Translator, Block Editor, MacDraw
- Consistent, retro-modern styling and easy navigation
- Modern text editor, QR/password generator, and more

---

## 🛠️ Tech Stack

- **Python** (3.10+)
- **Reflex** (Python web framework)
- **FastAPI** (backend)
- **Modern frontend** (via Reflex)
- **OpenAI API** (for AI-powered features)

All web server logic and routing is handled by Reflex and FastAPI. The main entrypoint is managed by Reflex, which binds to the port specified by the `PORT` environment variable (default: 3000).

---

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bhanvinayer/CodeChron-OS
   cd CodeChron-OS
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Copy `.env.example` to `.env`
   - Add your own OpenAI API key and other settings in `.env`

4. **Run locally:**
   ```bash
   bash start.sh
   ```
   - Or run directly:
   ```bash
   reflex run 
   ```

5. **Deploy on Render:**
   - Set the start command to:
     ```bash
     bash start.sh
     ```
   - Add all environment variables from your `.env` file in the Render dashboard

---

## 🖼️ Screenshots

<!--
Add screenshots here:
![Playground Home](../screenshots/python.jpg)
![Mac 1984](../screenshots/mac.jpg)
-->

---

## 📁 Project Structure

- `codechronos/` — Main app code (components, pages, assets, backend)
- `backend/` — Core backend utilities (sandbox, GPT, mutation engine)
- `components/` — Shared UI components
- `data/` — Example data and saved apps
- `utils/` — Utility modules
- `start.sh` — Entrypoint script (uses Reflex, binds to `$PORT`)
- `requirements.txt` — Python dependencies
- `.env.example` — Template for environment variables

---

## 📝 Notes

- Uses Python-focused web frameworks (Reflex, FastAPI)
- All server-side logic is handled by Python; no Node.js or Bun required
- The app listens on the port specified by the `PORT` environment variable (as required by Render and other PaaS)
- For AI features, you must provide your own OpenAI API key in `.env`

---

## 🤝 Contributing

Pull requests and suggestions are welcome! Please open an issue or PR to discuss improvements or new features.

---


