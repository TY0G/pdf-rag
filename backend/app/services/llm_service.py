import json

import httpx

from app.core.config import settings


class LLMService:
    async def generate_answer(self, question: str, evidence: list[dict]) -> str:
        if settings.openai_base_url and settings.openai_api_key and settings.openai_model:
            return await self._call_openai_compatible(question=question, evidence=evidence)
        return self._fallback_answer(question=question, evidence=evidence)

    async def _call_openai_compatible(self, question: str, evidence: list[dict]) -> str:
        system_prompt = (
            "你是一个基于文档证据回答问题的助手。"
            "只能依据提供的证据回答，若证据不足请明确说明。"
        )
        evidence_text = "\n\n".join(
            [
                f"[证据{i+1}] 文档：{item['document_name']} 页码：{item['page_number']}\n{item['content']}"
                for i, item in enumerate(evidence)
            ]
        )
        payload = {
            "model": settings.openai_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"问题：{question}\n\n证据：\n{evidence_text}\n\n请用中文回答，并先给结论，再给依据。",
                },
            ],
            "temperature": 0.2,
        }
        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        }
        url = settings.openai_base_url.rstrip("/") + "/chat/completions"
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

    def _fallback_answer(self, question: str, evidence: list[dict]) -> str:
        if not evidence:
            return "当前没有检索到足够证据，无法准确回答该问题。"

        intro = f"根据当前检索到的文档内容，关于“{question}”的回答如下："
        bullets = []
        for item in evidence[:3]:
            snippet = item["content"].replace("\n", " ").strip()
            bullets.append(
                f"- 在《{item['document_name']}》第 {item['page_number']} 页提到：{snippet[:160]}"
            )
        outro = "以上内容基于检索证据自动整理；如需更自然的生成式回答，可在 .env 中接入 Ollama / OpenAI 兼容模型。"
        return "\n".join([intro, *bullets, outro])
