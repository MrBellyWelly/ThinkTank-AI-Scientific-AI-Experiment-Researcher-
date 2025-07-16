import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import styles from './Home.module.css';

export default function Home() {
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [mode, setMode] = useState<'general' | 'scientific_idea'>('general');
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);

    // Auto-scroll to bottom when messages change
    useEffect(() => {
        scrollToBottom();
    }, [messages, loading]);

    // Focus input on load
    useEffect(() => {
        if (inputRef.current) {
            inputRef.current.focus();
        }
    }, []);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const formatMessage = (content: string) => {
        return content.split("\n").map((line, index) => {
            if (line.startsWith("### ")) {
                return <h3 key={index} className={styles.h3}>{line.replace("### ", "")}</h3>;
            } else if (line.startsWith("## ")) {
                return <h2 key={index} className={styles.h2}>{line.replace("## ", "")}</h2>;
            } else if (line.startsWith("# ")) {
                return <h1 key={index} className={styles.h1}>{line.replace("# ", "")}</h1>;
            } else if (line.startsWith("* ")) {
                return <li key={index} className={styles.bullet}>{line.replace("* ", "")}</li>;
            } else if (/\*\*(.*?)\*\*/.test(line)) {
                // Convert **bold** to <strong>bold</strong>
                const formattedText = line.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
                return <p key={index} dangerouslySetInnerHTML={{ __html: formattedText }} />;
            } else {
                return <p key={index} className={styles.text}>{line}</p>;
            }
        });
    };

    const sendMessage = async () => {
        if (!input.trim()) return;
        setError(null);

        setMessages((prev) => [...prev, { role: 'user', content: input }]);
        setInput('');
        setLoading(true);

        try {
            const response = await axios.post('/api/chat', { message: input, mode: mode });
            setMessages((prev) => [
                ...prev,
                { role: 'bot', content: response.data.response },
            ]);
            // console.log(response.data.evaluation);
        } catch (err) {
            console.error(err);
            setError('Failed to get a response from the server. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h1 className={styles.title}>Welcome to ThinkTank AI 🧠</h1>
            </div>

            <div className={styles.chatBox}>
                <div className={styles.modeSelector}>
                    <label className={`${styles.modeButton} ${mode === 'general' ? styles.activeModeButton : ''}`}>
                        <input
                            type="radio"
                            name="chatMode"
                            value="general"
                            checked={mode === "general"}
                            onChange={() => setMode("general")}
                            className={styles.modeRadio}
                        />
                        General Chat
                    </label>
                    <label className={`${styles.modeButton} ${mode === 'scientific_idea' ? styles.activeModeButton : ''}`}>
                        <input
                            type="radio"
                            name="chatMode"
                            value="scientific_idea"
                            checked={mode === "scientific_idea"}
                            onChange={() => setMode("scientific_idea")}
                            className={styles.modeRadio}
                        />
                        Scientific Idea
                    </label>
                </div>

                {messages.length === 0 ? (
                    <div className={styles.emptyState}>
                        <div className={styles.emptyStateIcon}>💬</div>
                        <h2>Start a conversation</h2>
                        <p>Ask a question to begin chatting with the AI assistant</p>
                    </div>
                ) : (
                    <div className={styles.messages}>
                        {messages.map((msg, index) => (
                            <div
                                key={index}
                                className={`${styles.message} ${msg.role === 'user' ? styles.userMessage : styles.botMessage}`}
                            >
                                <div className={styles.messageAvatar}>
                                    {msg.role === 'user' ? '👤' : '🤖'}
                                </div>
                                <div className={styles.messageContent}>
                                    {formatMessage(msg.content)}
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className={`${styles.message} ${styles.botMessage}`}>
                                <div className={styles.messageAvatar}>🤖</div>
                                <div className={styles.loadingIndicator}>
                                    <div className={styles.loadingDot}></div>
                                    <div className={styles.loadingDot}></div>
                                    <div className={styles.loadingDot}></div>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>
                )}

                {error && (
                    <div className={styles.errorContainer}>
                        <div className={styles.error}>
                            <span className={styles.errorIcon}>⚠️</span> {error}
                        </div>
                    </div>
                )}

                <div className={styles.inputContainer}>
                    <textarea
                        ref={inputRef}
                        className={styles.input}
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Type your message here..."
                        rows={1}
                    />
                    <button
                        onClick={sendMessage}
                        disabled={loading || !input.trim()}
                        className={`${styles.sendButton} ${loading || !input.trim() ? styles.disabledButton : ''}`}
                        aria-label="Send message"
                    >
                        <span className={styles.buttonIcon}>↑</span>
                    </button>
                </div>
            </div>

            <div className={styles.footer}>
                <p>Press Enter to send, Shift+Enter for new line</p>
            </div>
        </div>
    );
}