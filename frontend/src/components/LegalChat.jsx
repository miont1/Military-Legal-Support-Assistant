import React, { useState } from 'react';
import { sendMessage } from '../services/api';

const LegalChat = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sources, setSources] = useState([]);

  // New state for query tags
  const [issueCategory, setIssueCategory] = useState('');
  const [documentStatus, setDocumentStatus] = useState('');
  const [situationStage, setSituationStage] = useState('');

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: 'User', text: input };
    setMessages([...messages, userMessage]);
    setLoading(true);
    setSources([]);

    const metadata = {
      issue_category: issueCategory,
      document_status: documentStatus,
      situation_stage: situationStage
    };

    try {
      const response = await sendMessage(input, metadata);
      const botMessage = { sender: 'AI', text: response.answer };
      setMessages(prev => [...prev, botMessage]);
      setSources(response.sources);
    } catch (error) {
      setMessages(prev => [...prev, { sender: 'System', text: 'Error getting response.' }]);
    } finally {
      setLoading(false);
      setInput('');
    }
  };

  return (
    <div className="chat-container" style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h2>Legal Support Assistant</h2>

      <div className="chat-history" style={{ border: '1px solid #ccc', padding: '10px', height: '400px', overflowY: 'scroll', marginBottom: '10px' }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{ textAlign: msg.sender === 'User' ? 'right' : 'left', margin: '5px 0' }}>
            <strong>{msg.sender}:</strong> {msg.text}
          </div>
        ))}
        {loading && <div><em>Thinking...</em></div>}
      </div>

      <div className="filters" style={{ display: 'flex', gap: '10px', marginBottom: '10px', flexWrap: 'wrap' }}>
        <input
          type="text"
          placeholder="Category (e.g. Payments)"
          value={issueCategory}
          onChange={(e) => setIssueCategory(e.target.value)}
          style={{ padding: '5px' }}
        />
        <select value={documentStatus} onChange={(e) => setDocumentStatus(e.target.value)} style={{ padding: '5px' }}>
          <option value="">-- Document Status --</option>
          <option value="Є всі документи">Є всі документи</option>
          <option value="Документи відсутні">Документи відсутні</option>
          <option value="Є лише рапорт">Є лише рапорт</option>
          <option value="Часткові документи">Часткові документи</option>
          <option value="Є висновок ВЛК">Є висновок ВЛК</option>
          <option value="Є наказ">Є наказ</option>
        </select>
        <select value={situationStage} onChange={(e) => setSituationStage(e.target.value)} style={{ padding: '5px' }}>
          <option value="">-- Situation Stage --</option>
          <option value="Ситуація тільки виникла">Ситуація тільки виникла</option>
          <option value="Рапорт подано">Рапорт подано</option>
          <option value="Отримано відмову">Отримано відмову</option>
          <option value="Службове розслідування">Службове розслідування</option>
          <option value="Досудовий етап">Досудовий етап</option>
          <option value="Судовий розгляд">Судовий розгляд</option>
        </select>
      </div>

      <div className="input-area" style={{ display: 'flex', gap: '10px' }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask a legal question..."
          style={{ flex: 1, padding: '10px' }}
        />
        <button onClick={handleSend} disabled={loading} style={{ padding: '10px 20px' }}>Send</button>
      </div>

      {sources.length > 0 && (
        <div className="sources-section" style={{ marginTop: '20px', borderTop: '1px solid #eee', paddingTop: '10px' }}>
          <h3>Sources:</h3>
          <ul>
            {sources.map((source, idx) => (
              <li key={idx}>
                <a href={source.url} target="_blank" rel="noopener noreferrer">{source.title}</a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default LegalChat;
