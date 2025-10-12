# OpenAI Agent API

REST API szolgáltatás Docker-ben, amely okosotthon parancsokat elemez OpenAI agent segítségével és JSON választ ad vissza.

## 🚀 Funkciók

- ✅ REST API endpoint
- ✅ OpenAI agent integráció
- ✅ JSON válasz formátum
- ✅ Docker containerizáció
- ✅ Health check endpoint
- ✅ CORS támogatás
- ✅ Gunicorn production server
- ✅ Kívülről elérhető port

## 📋 Előfeltételek

- Docker és Docker Compose
- OpenAI API kulcs

## 🔧 Telepítés

### 1. Környezeti változók beállítása

Másold át a példa fájlt és töltsd ki az API kulcsot:

```bash
cp .env.example .env
```

Szerkeszd a `.env` fájlt:

```bash
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
PORT=5000
DEBUG=False
```

### 2. Docker image build és indítás

```bash
# Build és indítás egyetlen paranccsal
docker-compose up -d --build

# Vagy lépésenként:
docker-compose build
docker-compose up -d
```

### 3. Ellenőrzés

```bash
# Logok megtekintése
docker-compose logs -f

# Státusz ellenőrzése
docker-compose ps

# Health check
curl http://localhost:5000/health
```

## 📡 API Használat

### Endpoint: POST /analyze

Okosotthon parancs elemzése.

**Request:**
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "kapcsold be a nappaliban a lámpát"
  }'
```

**Response:**
```json
{
  "success": true,
  "result": {
    "helyiség": "nappali",
    "eszköz": "lámpa",
    "parancs": "bekapcsol"
  },
  "raw_json": "{\"helyiség\":\"nappali\",\"eszköz\":\"lámpa\",\"parancs\":\"bekapcsol\"}"
}
```

### Endpoint: GET /health

Health check endpoint.

**Request:**
```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "openai-agent-api"
}
```

### Endpoint: GET /

API dokumentáció.

**Request:**
```bash
curl http://localhost:5000/
```

## 🧪 Tesztelés

### Példa parancsok

```bash
# Lámpa bekapcsolás
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "kapcsold be a nappaliban a lámpát"}'

# Fűtés beállítás
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "állítsd 22 fokra a fűtést a hálószobában"}'

# Redőny vezérlés
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "nyisd ki a nappali redőnyöket"}'

# Minden lámpa kikapcsolás
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "kapcsold ki az összes lámpát"}'
```

### Python példa

```python
import requests

url = "http://localhost:5000/analyze"
data = {
    "text": "kapcsold be a nappaliban a lámpát"
}

response = requests.post(url, json=data)
print(response.json())
```

### Android (Kotlin) példa

```kotlin
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject

fun analyzeCommand(text: String) {
    val client = OkHttpClient()
    val url = "http://your-server:5000/analyze"
    
    val jsonBody = JSONObject().apply {
        put("text", text)
    }
    
    val requestBody = jsonBody.toString()
        .toRequestBody("application/json; charset=utf-8".toMediaType())
    
    val request = Request.Builder()
        .url(url)
        .post(requestBody)
        .build()
    
    val response = client.newCall(request).execute()
    val responseBody = response.body?.string()
    
    println("Response: $responseBody")
}
```

## 🛠️ Fejlesztés

### Lokális futtatás (Docker nélkül)

```bash
# Virtual environment létrehozása
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependenciák telepítése
pip install -r requirements.txt

# Környezeti változók beállítása
export OPENAI_API_KEY=your-api-key-here

# Alkalmazás indítása
python app.py
```

### Logok megtekintése

```bash
# Összes log
docker-compose logs -f

# Csak az utolsó 100 sor
docker-compose logs --tail=100 -f

# Keresés a logokban
docker-compose logs | grep "Analyzing command"
```

### Újraindítás

```bash
# Szolgáltatás újraindítása
docker-compose restart

# Újra build és indítás
docker-compose up -d --build
```

### Leállítás

```bash
# Leállítás (konténerek megmaradnak)
docker-compose stop

# Leállítás és törlés
docker-compose down

# Leállítás, törlés és volumes törlése
docker-compose down -v
```

## 🌐 Hálózati konfiguráció

### Port módosítása

A `docker-compose.yml` fájlban:

```yaml
ports:
  - "8080:5000"  # Külső port:Belső port
```

### Külső hozzáférés engedélyezése

Ha szeretnéd, hogy más gépek is elérjék:

1. **Tűzfal beállítás:**
```bash
sudo ufw allow 5000/tcp
```

2. **Router port forward** (ha szükséges)
   - Állítsd be a routereden a port forwarding-ot

3. **Publikus IP vagy domain használata:**
```bash
curl -X POST http://your-public-ip:5000/analyze -H "Content-Type: application/json" -d '{"text":"teszt"}'
```

## 📊 Monitorozás

### Health check

```bash
# Docker compose beépített health check
docker-compose ps

# Manual health check
watch -n 5 'curl -s http://localhost:5000/health'
```

### Resource használat

```bash
# Container stats
docker stats openai-agent-api

# Részletes info
docker inspect openai-agent-api
```

## ⚙️ Konfiguráció

### Environment Variables

| Változó | Leírás | Default | Kötelező |
|---------|--------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API kulcs | - | ✅ Igen |
| `PORT` | API port | 5000 | ❌ Nem |
| `DEBUG` | Debug mód | False | ❌ Nem |

### Gunicorn beállítások

A `Dockerfile`-ban módosítható:

```dockerfile
CMD ["gunicorn", 
     "--bind", "0.0.0.0:5000",
     "--workers", "4",           # Worker processes
     "--timeout", "120",         # Request timeout
     "--worker-class", "sync",   # Worker type
     "app:app"]
```

## 🐛 Hibaelhárítás

### 1. Port már használatban van

```bash
# Ellenőrizd melyik process használja
sudo lsof -i :5000

# Vagy változtasd meg a portot
# docker-compose.yml: "8080:5000"
```

### 2. OpenAI API hiba

```bash
# Ellenőrizd az API kulcsot
docker-compose exec openai-agent-api env | grep OPENAI_API_KEY

# Nézd meg a logokat
docker-compose logs | grep -i error
```

### 3. Container nem indul

```bash
# Részletes logok
docker-compose logs openai-agent-api

# Container újraépítése
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 4. Timeout hibák

Növeld a timeout értéket a `Dockerfile`-ban:
```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "300", "app:app"]
```

## 📈 Teljesítmény

**Becsült válaszidők:**
- Health check: < 10ms
- Parancs elemzés: 2-5 sec (OpenAI API függő)

**Ajánlott konfiguráció:**
- Workers: 2-4 (CPU magok száma alapján)
- Timeout: 120 sec
- Memory limit: 512MB

## 🔒 Biztonság

### Production ajánlások:

1. **API kulcs biztonság:**
   - Használj Docker secrets-et
   - Ne commitold a `.env` fájlt

2. **Rate limiting:**
   - Implementálj rate limiting-et (pl. Flask-Limiter)

3. **HTTPS:**
   - Használj reverse proxy-t (nginx, traefik)
   - SSL certificate (Let's Encrypt)

4. **Authentication:**
   - API key vagy JWT token
   - IP whitelist

## 📝 Changelog

**v1.0.0** (2024.10.12)
- ✅ Kezdeti verzió
- ✅ REST API endpoints
- ✅ Docker support
- ✅ OpenAI agent integráció
- ✅ JSON response formátum

## 🤝 Integráció Android app-pal

Az Android mobilapp használhatja ezt az API-t:

**OpenAiWorkflowService.kt módosítás:**
```kotlin
private val apiUrl = "http://your-server-ip:5000/analyze"

suspend fun sendMessageToWorkflow(userMessage: String): String {
    val jsonBody = JSONObject().apply {
        put("text", userMessage)
    }
    
    val request = Request.Builder()
        .url(apiUrl)
        .post(jsonBody.toString().toRequestBody("application/json".toMediaType()))
        .build()
    
    val response = client.newCall(request).execute()
    val responseBody = response.body?.string()
    val json = JSONObject(responseBody)
    
    return json.getJSONObject("result").toString()
}
```

## 📞 Support

Ha bármilyen problémád van:
1. Nézd meg a logokat: `docker-compose logs -f`
2. Ellenőrizd a health endpoint-ot: `curl http://localhost:5000/health`
3. Teszteld az API-t közvetlenül: `curl -X POST http://localhost:5000/analyze -d '{"text":"teszt"}'`

---

**Készítve:** 2024.10.12  
**Szerző:** AI Assistant  
**Licence:** Private Project

