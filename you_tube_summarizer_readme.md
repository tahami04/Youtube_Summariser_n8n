# 🎮 YouTube Video Summarizer with n8n, Python, and OpenAI

This project is a **no-cost, open-source YouTube video summarizer** powered by:

- **n8n** (workflow automation)
- **Python** (for transcript extraction)
- **OpenAI GPT** (for summarizing)
- **Frontend HTML/JS** (to interact via browser)

---

## ✅ Features

- Input any YouTube video URL
- Extract the transcript using `youtube-transcript-api`
- Summarize into:
  - 📜 Short paragraph
  - 🔑 5 bullet points
- Fully local, no paid dependencies (uses your own OpenAI API key)
- Frontend interface

---

## 📦 Requirements

- [x] Docker + Docker Compose (for n8n setup)
- [x] Python 3 (inside Docker or mounted from host)
- [x] `youtube-transcript-api` Python package
- [x] OpenAI API key (ChatGPT Plus users already have access)
- [x] Basic HTML/CSS/JS for the frontend

---

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/youtube-summarizer-n8n.git
cd youtube-summarizer-n8n
```

### 2. Identify Your Docker Container Name
Run this to list containers:
```bash
docker ps
```
Look for the container running the `n8nio/n8n` image. Note the **name** — replace it with `your-container-name` below.

### 3. Start n8n via Docker
```bash
docker run -it --rm \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -v $PWD:/data \
  --name your-container-name \
  n8nio/n8n
```

### 4. Enter Docker & Setup Python Environment
```bash
# Replace "your-container-name" with actual name

docker exec -u 0 -it your-container-name sh

apk update
apk add python3 py3-pip
pip3 install youtube-transcript-api

# Create a virtual environment
python3 -m venv /tmp/venv

# Activate the venv
. /tmp/venv/bin/activate

# Install the package inside the venv
pip install youtube-transcript-api
```

✅ **Note**: Use the path `/tmp/venv/bin/python` inside **Execute Command** node in n8n.

You can also mount your `.py` file from your host into the Docker container (e.g. `/data/scripts/YoutubeSummariser/get_transcript.py`) for easy access.

---

## 🧠 n8n Workflow Summary

### ♻️ Workflow Nodes:

1. **Webhook Node** (POST `/summarize-youtube`)

2. **Code Node** to extract `video_id` from URL
```js
const url = new URL($json["body"]["video_url"]);
const videoId = url.searchParams.get("v");

if (!videoId) throw new Error("Invalid YouTube URL");

return [{ video_id: videoId }];
```

3. **Execute Command Node**
```bash
/tmp/venv/bin/python /data/scripts/YoutubeSummariser/get_transcript.py {{$json.video_id}}
```

4. **OpenAI Node** (e.g., `gpt-3.5-turbo` or `gpt-4o`)
```json
[
  { "role": "system", "content": "You are an assistant that summarizes YouTube transcripts into 5 concise bullet points." },
  { "role": "user", "content": "Summarize the following transcript:\n\n{{$json[\"stdout\"]}}" }
]
```

5. **Set Node**
   - Purpose: Extract and format the OpenAI summary content before sending it to response node.
   - Example: `summary = $json["message"]["content"]`

6. **Respond to Webhook Node**
```json
{
  "message": $json["summary"]
}
```

> Connect all nodes linearly: Webhook → Code → Execute → OpenAI → Set → Webhook Response

---

## 🌐 Frontend (index.html)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>YouTube Video Summarizer</title>
</head>
<body>
  <h1>YouTube Video Summarizer</h1>
  <input type="text" id="videoUrl" placeholder="Enter YouTube video URL...">
  <button onclick="summarizeVideo()">Summarize</button>
  <div id="output"></div>

  <script>
    async function summarizeVideo() {
      const videoUrl = document.getElementById('videoUrl').value;
      const output = document.getElementById('output');
      output.innerText = '⏳ Summarizing...';

      try {
        const response = await fetch('http://127.0.0.1:5678/webhook-test/summarize-youtube', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ video_url: videoUrl })
        });

        const data = await response.json();
        const summaryField = data?.message?.content?.summary;
        const keyPoints = data?.message?.content?.key_points;

        let summary = '';
        if (typeof summaryField === 'string') {
          summary = summaryField;
        } else if (typeof summaryField === 'object') {
          summary = JSON.stringify(summaryField, null, 2);
        }

        let html = '';
        if (summary) html += `<p><strong>Summary:</strong> ${summary}</p>`;
        if (Array.isArray(keyPoints)) {
          html += `<strong>Key Points:</strong><ul>${keyPoints.map(p => `<li>${p}</li>`).join('')}</ul>`;
        }

        output.innerHTML = html || '⚠️ No summary found.';
      } catch (error) {
        output.innerText = `❌ Error: ${error.message}`;
      }
    }
  </script>
</body>
</html>
```

### 💻 Run Frontend Locally
In the same folder as `index.html`, run:
```bash
python3 -m http.server 8000
```
Then go to: [http://localhost:8000](http://localhost:8000)

---

## 🔍 Test Your Workflow (cURL)
You can test your n8n workflow directly using:

```bash
curl -X POST http://localhost:5678/webhook-test/summarize-youtube \
  -H "Content-Type: application/json" \
  -d '{"video_url": "https://www.youtube.com/watch?v=Ks-_Mh1QhMc"}'
```

👉 Replace the video URL with any valid YouTube video link **that has subtitles/captions**.

---

## 🛠 Troubleshooting

- **Permission Denied on Docker Volumes:**
  Mount properly using `-v $PWD:/data`

- **Transcript Errors:**
  Not all YouTube videos support transcripts (music videos, ads, private videos, etc.)

- **OpenAI Errors:**
  "Insufficient quota" means you’ve hit your usage limit or API key is invalid. Get a new key from [OpenAI dashboard](https://platform.openai.com/account/api-keys).

- **Python Not Found Errors:**
  Ensure you've installed Python inside the Docker container and are referencing the correct virtual environment path.

---

## 🙌 Contributing
PRs welcome — especially for:
- Adding YouTube title/thumbnail preview
- Multi-language transcript support
- Exporting summaries (PDF, copy, share link)

---

## 📄 License
[MIT](LICENSE)

---

## 💡 Credits
Built by [@YourName](https://github.com/your-username) using:
- OpenAI GPT
- youtube-transcript-api
- n8n.io

