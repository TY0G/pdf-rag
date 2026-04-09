import { http } from './http'

export const chatApi = {
  async ask(payload: { question: string; document_ids: number[]; conversation_id?: number | null }) {
    const { data } = await http.post('/chat/ask', payload)
    return data
  },
  async listConversations() {
    const { data } = await http.get('/chat/conversations')
    return data
  },
  async getConversation(id: number) {
    const { data } = await http.get(`/chat/conversations/${id}`)
    return data
  }
}
