"""
llm_client.py — Cliente LLM unificado para Groq y Ollama
"""
import json
import sys
import os

# Añadir el directorio padre al path para importar config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import requests
except ImportError:
    print("Error: instala 'requests' con: pip install requests")
    sys.exit(1)

try:
    from fase3_prompts.config import (
        LLM_PROVIDER, GROQ_API_KEY, GROQ_MODEL, GROQ_API_URL,
        OLLAMA_API_URL, OLLAMA_MODEL, MAX_TOKENS, TEMPERATURE
    )
except ImportError:
    from config import (
        LLM_PROVIDER, GROQ_API_KEY, GROQ_MODEL, GROQ_API_URL,
        OLLAMA_API_URL, OLLAMA_MODEL, MAX_TOKENS, TEMPERATURE
    )


class LLMClient:
    """Cliente unificado que soporta Groq API y Ollama local."""

    def __init__(self):
        self.provider = LLM_PROVIDER
        self._validate_config()

    def _validate_config(self):
        if self.provider == "groq" and not GROQ_API_KEY:
            print("\n⚠️  GROQ_API_KEY no configurada.")
            print("   Crea un archivo .env con tu API key (ver .env.example)")
            print("   O cámbia LLM_PROVIDER=ollama para uso local\n")

    def chat(self, system_prompt: str, user_message: str) -> str:
        """
        Envía una conversación al LLM y devuelve la respuesta.

        Args:
            system_prompt: Instrucciones base del agente.
            user_message: Mensaje del usuario con el contexto inyectado.

        Returns:
            Respuesta generada por el modelo.
        """
        if self.provider == "groq":
            return self._call_groq(system_prompt, user_message)
        elif self.provider == "ollama":
            return self._call_ollama(system_prompt, user_message)
        else:
            raise ValueError(f"Proveedor LLM no soportado: {self.provider}")

    def _call_groq(self, system_prompt: str, user_message: str) -> str:
        """Llama a la API de Groq (compatible con formato OpenAI)."""
        if not GROQ_API_KEY:
            return ("❌ Error: GROQ_API_KEY no configurada. "
                    "Agrega tu API key en el archivo .env")

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE
        }

        try:
            response = requests.post(
                GROQ_API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

        except requests.exceptions.ConnectionError:
            return "❌ Error de conexión. Verifica tu conexión a internet."
        except requests.exceptions.Timeout:
            return "❌ Tiempo de espera agotado. Intenta de nuevo."
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                return "❌ API Key inválida. Verifica tu GROQ_API_KEY en .env"
            return f"❌ Error HTTP {response.status_code}: {str(e)}"
        except (KeyError, json.JSONDecodeError) as e:
            return f"❌ Error al procesar la respuesta del modelo: {str(e)}"

    def _call_ollama(self, system_prompt: str, user_message: str) -> str:
        """Llama a Ollama local."""
        payload = {
            "model": OLLAMA_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "stream": False,
            "options": {
                "temperature": TEMPERATURE,
                "num_predict": MAX_TOKENS
            }
        }

        try:
            response = requests.post(
                OLLAMA_API_URL,
                json=payload,
                timeout=120  # Ollama puede ser más lento localmente
            )
            response.raise_for_status()
            data = response.json()
            return data["message"]["content"].strip()

        except requests.exceptions.ConnectionError:
            return ("❌ No se puede conectar a Ollama. "
                    "¿Está ejecutándose? Prueba: ollama serve")
        except requests.exceptions.Timeout:
            return "❌ Tiempo de espera agotado. El modelo puede estar cargando."
        except (KeyError, json.JSONDecodeError) as e:
            return f"❌ Error al procesar la respuesta de Ollama: {str(e)}"
