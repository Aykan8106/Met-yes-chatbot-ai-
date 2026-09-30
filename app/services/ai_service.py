# app/services/ai_service.py - Yapay zeka cagrilari SADECE burada bulunur
# Bu dosya Flask, HTTP rotalari veya veritabani bilmez; sadece AI ile konusur.
import requests
from config import Config


class AIServiceError(Exception):
    """AI servisine ozel hata; rotalar bunu yakalayip kibar JSON dondurecek."""
    pass


class AIService:
    GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
    MODEL = "openai/gpt-oss-20b"
    TIMEOUT = 30  # saniye; cevap gelmezse sonsuza kadar beklemesin

    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.provider = Config.AI_PROVIDER

    def _sistem_talimati(self):
        """Yapay zekanin kisiligini config'den okur."""
        return Config.BUSINESS_CONTEXT

    def _mesajlari_hazirla(self, mesaj, gecmis):
        """Sira: once sistem talimati, sonra gecmis, en sonda yeni mesaj."""
        mesajlar = [{"role": "system", "content": self._sistem_talimati()}]

        for eski in gecmis or []:
            # Sadece beklenen rolleri ve dolu icerigi kabul ediyoruz
            if eski.get("role") in ("user", "assistant") and eski.get("content"):
                mesajlar.append({"role": eski["role"], "content": eski["content"]})

        mesajlar.append({"role": "user", "content": mesaj})
        return mesajlar

    def _groq_istegi(self, mesajlar):
        """Groq API'sine istek atar ve yanit metnini dondurur."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.MODEL,
            "messages": mesajlar,
            "temperature": 0.5,
            "max_tokens": 800,
            "reasoning_effort": "low",
        }
        try:
            yanit = requests.post(
                self.GROQ_URL, headers=headers, json=payload, timeout=self.TIMEOUT
            )
            yanit.raise_for_status()  # 4xx/5xx durumlarinda hata firlatir
            return yanit.json()["choices"][0]["message"]["content"].strip()
        except requests.exceptions.RequestException as hata:
            # Groq'un gonderdigi ayrintili hata metnini de ekle
            detay = hata.response.text if hata.response is not None else ""
            raise AIServiceError(f"AI servisine ulasilamadi: {hata} {detay}") from hata
        except (KeyError, IndexError, ValueError, AttributeError) as hata:
            raise AIServiceError("AI yaniti beklenen formatta degil.") from hata

    def yanit_uret(self, mesaj, gecmis=None):
        """Kullanici mesajina yanit uretir."""
        # Anahtar yoksa cokmek yerine demo modu mesaji dondur
        if not self.api_key:
            return "Demo modu: Yapay zeka anahtari tanimli degil. Lutfen daha sonra tekrar deneyin."

        mesajlar = self._mesajlari_hazirla(mesaj, gecmis)
        return self._groq_istegi(mesajlar)


# Tek ornek: diger dosyalar "from app.services.ai_service import ai_service" ile kullanir
ai_service = AIService()
