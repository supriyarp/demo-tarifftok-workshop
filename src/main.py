"""
FastAPI server for the TariffTok AI system.
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from src.core.models import ChatRequest, ChatResponse
import requests
import json
from src.core.dynamic_pipeline import run_tariff_analysis, get_graph_visualization
from src.core.config import settings
from src.core.data_loader import data_loader


# Initialize FastAPI app
app = FastAPI(
    title="TariffTok AI",
    description="AI-powered tariff analysis system using LangGraph",
    version="1.0.0",
    debug=settings.debug
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve a simple HTML interface."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>TariffTok AI - Advanced Tariff Analysis</title>
        <link rel="icon" type="image/png" href="/static/images/icon.png">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns/dist/chartjs-adapter-date-fns.bundle.min.js"></script>
        <style>
            * { box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; padding: 0; 
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.8) 0%, rgba(118, 75, 162, 0.8) 100%), 
                            url('/static/images/background-image.jpg');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                min-height: 100vh;
            }
            .container { 
                max-width: 1200px; margin: 0 auto; padding: 20px; 
            }
            .header { 
                background: white; padding: 20px; border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 20px;
                display: flex; justify-content: space-between; align-items: center;
            }
            h1 { 
                color: #2c3e50; margin: 0; font-size: 2.2em; 
                background: linear-gradient(45deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .subtitle { color: #7f8c8d; margin: 10px 0; font-size: 1em; }
            .built-by { 
                color: #95a5a6; margin: 5px 0 0 0; font-size: 0.9em; 
                font-style: italic;
            }
            .built-by a:hover { 
                color: #764ba2; text-decoration: underline; 
                transition: color 0.3s ease;
            }
            
            .header-left { 
                display: flex; flex-direction: column; align-items: flex-start;
            }
            
            .header-right { 
                display: flex; align-items: center;
            }
            
            .women-who-code { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 8px 16px; border-radius: 20px; 
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                display: flex; align-items: center; justify-content: center;
            }
            
            .chat-container { 
                background: white; border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2); 
                height: 70vh; display: flex; flex-direction: column;
                overflow: hidden;
            }
            
            .chat-header { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; padding: 15px 20px; text-align: center;
                font-weight: bold; font-size: 1.1em;
            }
            
            .chat-messages { 
                flex: 1; padding: 20px; overflow-y: auto; 
                background: #f8f9fa;
            }
            
            .message { 
                margin: 15px 0; display: flex; align-items: flex-start;
            }
            
            .message.user { justify-content: flex-end; }
            .message.bot { justify-content: flex-start; }
            
            .message-content { 
                max-width: 70%; padding: 12px 16px; border-radius: 18px;
                word-wrap: break-word;
            }
            
            .message.user .message-content { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; border-bottom-right-radius: 5px;
            }
            
            .message.bot .message-content { 
                background: white; color: #2c3e50; 
                border: 1px solid #e9ecef; border-bottom-left-radius: 5px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            
            .message-avatar { 
                width: 32px; height: 32px; border-radius: 50%; 
                margin: 0 10px; display: flex; align-items: center; 
                justify-content: center; font-size: 16px; font-weight: bold;
            }
            
            .message.user .message-avatar { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; order: 1;
            }
            
            .message.bot .message-avatar { 
                background: #f8f9fa; color: #667eea; border: 2px solid #667eea;
            }
            
            .chat-input-container { 
                padding: 20px; background: white; border-top: 1px solid #e9ecef;
                display: flex; gap: 10px; align-items: center;
            }
            
            .chat-input { 
                flex: 1; padding: 12px 16px; border: 2px solid #e9ecef; 
                border-radius: 25px; font-size: 14px; outline: none;
                transition: border-color 0.3s;
            }
            .chat-input:focus { border-color: #667eea; }
            
            .send-btn { 
                width: 45px; height: 45px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; border: none; border-radius: 50%; 
                cursor: pointer; font-size: 18px; display: flex;
                align-items: center; justify-content: center;
                transition: transform 0.2s;
            }
            .send-btn:hover { transform: scale(1.05); }
            .send-btn:active { transform: scale(0.95); }
            
            .slack-btn { 
                background: #4A154B; 
                color: white; border: none; border-radius: 6px; 
                cursor: pointer; font-size: 14px; display: flex;
                align-items: center; justify-content: center;
                transition: all 0.2s; margin-left: 8px;
                padding: 10px 12px; gap: 6px;
                min-width: auto; height: auto;
            }
            .slack-btn:hover:not(:disabled) { 
                background: #611f69; transform: translateY(-1px);
            }
            .slack-btn:active { transform: scale(0.95); }
            .slack-btn:disabled { 
                background: #ccc; cursor: not-allowed; 
                transform: none;
            }
            .slack-text {
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }
            
            .graph-btn { 
                background: #2E7D32; 
                color: white; border: none; border-radius: 6px; 
                cursor: pointer; font-size: 14px; display: flex;
                align-items: center; justify-content: center;
                transition: all 0.2s; margin-left: 8px;
                padding: 10px 12px; gap: 6px;
                min-width: auto; height: auto;
            }
            .graph-btn:hover:not(:disabled) { 
                background: #388E3C; transform: translateY(-1px);
            }
            .graph-btn:active { transform: scale(0.95); }
            .graph-text {
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }
            
            .contact-btn { 
                background: #FF6B35; 
                color: white; border: none; border-radius: 6px; 
                cursor: pointer; font-size: 14px; display: flex;
                align-items: center; justify-content: center;
                transition: all 0.2s; margin-left: 8px;
                padding: 10px 12px; gap: 6px;
                min-width: auto; height: auto;
            }
            .contact-btn:hover:not(:disabled) { 
                background: #E55A2B; transform: translateY(-1px);
            }
            .contact-btn:active { transform: scale(0.95); }
            .contact-text {
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }
            
            .examples { 
                background: #f8f9fa; padding: 15px; border-radius: 10px; 
                margin: 10px 0; border-left: 4px solid #667eea;
            }
            .examples h4 { color: #2c3e50; margin: 0 0 10px 0; font-size: 0.9em; }
            .example-question { 
                background: white; padding: 8px 12px; margin: 5px 0; 
                border-radius: 15px; cursor: pointer; transition: all 0.2s;
                border: 1px solid #e9ecef; font-size: 0.85em;
                color: #667eea; border-color: #667eea;
            }
            .example-question:hover { 
                background: #667eea; color: white; transform: translateX(5px);
            }
            
            .response { 
                background: white; padding: 25px; border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-top: 20px;
                border-left: 5px solid #3498db;
            }
            .response.error { border-left-color: #e74c3c; }
            
            .comparison-grid { 
                display: grid; grid-template-columns: 1fr 1fr; gap: 20px; 
                margin: 20px 0;
            }
            .country-card { 
                background: #f8f9fa; padding: 20px; border-radius: 10px; 
                border: 2px solid #e9ecef; text-align: center;
            }
            .country-card.china { border-color: #e74c3c; }
            .country-card.vietnam { border-color: #27ae60; }
            .country-card.india { border-color: #f39c12; }
            .country-card.mexico { border-color: #9b59b6; }
            .country-card.usa { border-color: #3498db; }
            
            .rate-display { 
                font-size: 2.5em; font-weight: bold; margin: 10px 0;
                color: #2c3e50;
            }
            .trend-up { color: #e74c3c; }
            .trend-down { color: #27ae60; }
            .trend-neutral { color: #95a5a6; }
            
            .chart-container { 
                background: #f8f9fa; padding: 20px; border-radius: 10px; 
                margin: 20px 0; position: relative; height: 400px;
            }
            
            .insights { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; padding: 20px; border-radius: 10px; 
                margin: 20px 0;
            }
            .insights h3 { margin-top: 0; }
            
            .loading { 
                text-align: center; padding: 40px; color: #7f8c8d;
                font-size: 1.1em;
            }
            .spinner { 
                border: 3px solid #f3f3f3; border-top: 3px solid #3498db; 
                border-radius: 50%; width: 30px; height: 30px; 
                animation: spin 1s linear infinite; margin: 0 auto 15px;
            }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            
            .hidden { display: none; }
            
            @media (max-width: 768px) {
                .comparison-grid { grid-template-columns: 1fr; }
                .query-box { width: 100%; margin-bottom: 10px; }
                .submit-btn { width: 100%; margin-left: 0; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="header-left">
                    <h1><img src="/static/images/icon.png" alt="TariffTok AI" style="width: 40px; height: 40px; border-radius: 8px; vertical-align: middle; margin-right: 10px;">TariffTok AI</h1>
                    <p class="subtitle">Your AI Assistant for Tariff Analysis</p>
                    <p class="built-by">Built by <a href="https://www.linkedin.com/in/supriya-rp/" target="_blank" style="color: #667eea; text-decoration: none; font-weight: 500;">Supriya Ramarao Prasanna</a></p>
                </div>
                <div class="header-right">
                    <div class="women-who-code">
                        <a href="https://events.techfutures.com/2025/agenda/speakers/3778652" target="_blank" style="text-decoration: none;">
                            <img src="/static/images/womenwhocode-right-corner.webp" alt="Women Who Code" style="width: 150px; height: 90px; border-radius: 8px;">
                        </a>
                    </div>
                </div>
            </div>
            
            <div class="chat-container">
                <div class="chat-header">
                    💬 Chat with TariffTok AI
                </div>
                
                <div class="chat-messages" id="chatMessages">
                    <div class="message bot">
                        <div class="message-avatar">🤖</div>
                        <div class="message-content">
                            <p>Hello! I'm your TariffTok AI assistant. I can help you analyze tariff rates for different countries and products.</p>
                            
                            <div class="examples">
                                <h4>💡 Try asking me:</h4>
                                <div class="example-question" onclick="sendExampleQuestion('What is the tariff rate for Electronics from China?')">
                                    What's the tariff rate for Electronics from China?
                                </div>
                                <div class="example-question" onclick="sendExampleQuestion('How much tariff is charged on Toys from Vietnam?')">
                                    How much tariff is charged on Toys from Vietnam?
                                </div>
                                <div class="example-question" onclick="sendExampleQuestion('Compare tariff rates for Electronics between China and Vietnam')">
                                    Compare tariff rates for Electronics between China and Vietnam
                                </div>
                                <div class="example-question" onclick="sendExampleQuestion('What data do you have available?')">
                                    What data do you have available?
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="chat-input-container">
                    <input type="text" id="chatInput" class="chat-input" placeholder="Ask me about tariff rates..." autocomplete="off">
                    <button class="send-btn" onclick="sendMessage()">➤</button>
                    <button class="slack-btn" id="slackBtn" onclick="sendToSlack()" title="Send to Slack" disabled>
                        <span>💬</span>
                        <span class="slack-text">Slack me</span>
                    </button>
                    <button class="graph-btn" onclick="showGraph()" title="View Execution Graph">
                        <span>🔄</span>
                        <span class="graph-text">Graph</span>
                    </button>
                    <button class="contact-btn" onclick="showContact()" title="Contact & Community">
                        <span>📞</span>
                        <span class="contact-text">Contact</span>
                    </button>
                </div>
            </div>
        </div>
        
        <script>
            let currentChart = null;
            
            function addMessage(content, isUser = false, dataAttributes = {}) {
                const chatMessages = document.getElementById('chatMessages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
                
                // Add data attributes for execution tracking
                for (const [key, value] of Object.entries(dataAttributes)) {
                    messageDiv.dataset[key] = value;
                }
                
                const avatar = document.createElement('div');
                avatar.className = 'message-avatar';
                avatar.textContent = isUser ? '👤' : '🤖';
                
                const messageContent = document.createElement('div');
                messageContent.className = 'message-content';
                messageContent.innerHTML = content;
                
                messageDiv.appendChild(avatar);
                messageDiv.appendChild(messageContent);
                chatMessages.appendChild(messageDiv);
                
                chatMessages.scrollTop = chatMessages.scrollHeight;
                return messageContent;
            }
            
            async function showGraph() {
                try {
                    // Get execution path from the most recent message with execution data
                    let executionPath = null;
                    
                    // Find all bot messages and look for the most recent one with execution data
                    const botMessages = document.querySelectorAll('.message.bot');
                    console.log('Found bot messages:', botMessages.length);
                    
                    // Start from the most recent and work backwards
                    for (let i = botMessages.length - 1; i >= 0; i--) {
                        const message = botMessages[i];
                        console.log(`Message ${i}:`, message.dataset);
                        if (message.dataset.executionPath && message.dataset.executionPath.length > 0) {
                            executionPath = message.dataset.executionPath;
                            console.log(`Found execution path in message ${i}:`, executionPath);
                            break;
                        }
                    }
                    
                    console.log('Using execution path:', executionPath);
                    
                    // Build URL with execution path parameter
                    let url = '/api/graph';
                    if (executionPath) {
                        url += `?execution_path=${encodeURIComponent(executionPath)}`;
                    }
                    
                    console.log('Graph URL:', url);
                    
                    const response = await fetch(url);
                    const data = await response.json();
                    
                    if (data.success) {
                        // Create a modal to display the graph
                        const modal = document.createElement('div');
                        modal.style.cssText = `
                            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                            background: rgba(0,0,0,0.8); z-index: 1000; display: flex;
                            align-items: center; justify-content: center;
                        `;
                        
                        const content = document.createElement('div');
                        content.style.cssText = `
                            background: white; padding: 30px; border-radius: 15px;
                            max-width: 90%; max-height: 90%; overflow: auto;
                            position: relative;
                        `;
                        
                        content.innerHTML = `
                            <h2 style="margin-top: 0; color: #2c3e50;">🔄 TariffTok AI Execution Graph</h2>
                            <p style="color: #666; margin-bottom: 20px;">
                                This shows the dynamic LangGraph execution flow:
                            </p>
                            <div class="dot-content" style="background: #f8f9fa; padding: 20px; border-radius: 10px; font-family: monospace; white-space: pre-wrap; overflow-x: auto;">
                                ${data.dot_content}
                            </div>
                            <div style="margin-top: 20px; padding: 15px; background: #e3f2fd; border-radius: 8px;">
                                <strong>💡 How to visualize:</strong><br>
                                • Copy the DOT content above<br>
                                • Paste it into <a href="https://dreampuf.github.io/GraphvizOnline/" target="_blank">GraphvizOnline</a><br>
                                • Or use Graphviz tools locally: <code>dot -Tpng graph.dot -o graph.png</code>
                            </div>
                            <button onclick="copyDOTContent()" class="copy-btn" title="Copy DOT content" style="
                                position: absolute; top: 15px; right: 50px; background: #4CAF50;
                                color: white; border: none; border-radius: 4px; padding: 8px 12px;
                                cursor: pointer; font-size: 12px; transition: all 0.2s;
                                z-index: 1001;
                            ">📋 Copy</button>
                            <button onclick="this.closest('div').parentNode.remove()" style="
                                position: absolute; top: 15px; right: 15px; background: #e74c3c;
                                color: white; border: none; border-radius: 50%; width: 30px; height: 30px;
                                cursor: pointer; font-size: 16px;
                            ">×</button>
                        `;
                        
                        modal.appendChild(content);
                        document.body.appendChild(modal);
                        
                        // Close modal when clicking outside
                        modal.addEventListener('click', (e) => {
                            if (e.target === modal) {
                                modal.remove();
                            }
                        });
                    } else {
                        alert('Failed to load graph: ' + data.error);
                    }
                } catch (error) {
                    alert('Error loading graph: ' + error.message);
                }
            }
            
            async function copyDOTContent() {
                try {
                    const dotContentElement = document.querySelector('.dot-content');
                    if (!dotContentElement) {
                        alert('DOT content not found');
                        return;
                    }
                    
                    const dotContent = dotContentElement.textContent;
                    const copyBtn = document.querySelector('.copy-btn');
                    
                    // Try modern clipboard API first
                    if (navigator.clipboard && window.isSecureContext) {
                        await navigator.clipboard.writeText(dotContent);
                        showCopyFeedback(copyBtn, '✅ Copied!', '#4CAF50');
                    } else {
                        // Fallback for older browsers or non-secure contexts
                        const textArea = document.createElement('textarea');
                        textArea.value = dotContent;
                        textArea.style.position = 'fixed';
                        textArea.style.left = '-999999px';
                        textArea.style.top = '-999999px';
                        document.body.appendChild(textArea);
                        textArea.focus();
                        textArea.select();
                        
                        const successful = document.execCommand('copy');
                        document.body.removeChild(textArea);
                        
                        if (successful) {
                            showCopyFeedback(copyBtn, '✅ Copied!', '#4CAF50');
                        } else {
                            showCopyFeedback(copyBtn, '❌ Failed', '#f44336');
                        }
                    }
                } catch (error) {
                    const copyBtn = document.querySelector('.copy-btn');
                    showCopyFeedback(copyBtn, '❌ Failed', '#f44336');
                }
            }
            
            function showCopyFeedback(button, text, color) {
                if (!button) return;
                
                const originalText = button.innerHTML;
                const originalColor = button.style.backgroundColor;
                
                button.innerHTML = text;
                button.style.backgroundColor = color;
                button.style.transform = 'scale(1.05)';
                
                setTimeout(() => {
                    button.innerHTML = originalText;
                    button.style.backgroundColor = originalColor;
                    button.style.transform = 'scale(1)';
                }, 2000);
            }
            
            function addTypingIndicator() {
                const chatMessages = document.getElementById('chatMessages');
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message bot';
                messageDiv.id = 'typing-indicator';
                
                const avatar = document.createElement('div');
                avatar.className = 'message-avatar';
                avatar.textContent = '🤖';
                
                const messageContent = document.createElement('div');
                messageContent.className = 'message-content';
                messageContent.innerHTML = '<div class="typing-dots"><span></span><span></span><span></span></div>';
                
                messageDiv.appendChild(avatar);
                messageDiv.appendChild(messageContent);
                chatMessages.appendChild(messageDiv);
                
                chatMessages.scrollTop = chatMessages.scrollHeight;
                return messageDiv;
            }
            
            function removeTypingIndicator() {
                const typingIndicator = document.getElementById('typing-indicator');
                if (typingIndicator) {
                    typingIndicator.remove();
                }
            }
            
            function sendExampleQuestion(question) {
                document.getElementById('chatInput').value = question;
                sendMessage();
            }
            
            function sendMessage() {
                const chatInput = document.getElementById('chatInput');
                const query = chatInput.value.trim();
                
                if (!query) return;
                
                // Add user message
                addMessage(query, true);
                
                // Clear input
                chatInput.value = '';
                
                // Add typing indicator
                const typingIndicator = addTypingIndicator();
                
                // Send request
                fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: query })
                })
                .then(response => response.json())
                .then(data => {
                    removeTypingIndicator();
                    
                    if (data.error) {
                        addMessage(`❌ <strong>Error:</strong> ${data.error}`);
                    } else {
                        let responseContent = '';
                        
                        // Check if this is a comparison query
                        if (query.toLowerCase().includes('compare') && data.comparison_data && data.comparison_data.length > 0) {
                            responseContent = formatComparisonResponse(data);
                        } else {
                            responseContent = formatSingleTariffResponse(data);
                        }
                        
                        // Store execution metadata for graph visualization
                        const executionMetadata = {
                            executionPath: data.execution_path ? data.execution_path.join(',') : '',
                            executionTime: data.execution_time || 0,
                            currentNode: data.current_node || '',
                            nodeTimings: data.node_timings ? JSON.stringify(data.node_timings) : ''
                        };
                        
                        const messageContent = addMessage(responseContent, false, executionMetadata);
                        
                        // Create charts if it's a comparison
                        if (query.toLowerCase().includes('compare') && data.comparison_data && data.comparison_data.length > 0) {
                            setTimeout(() => {
                                createComparisonChart(messageContent, data);
                            }, 100);
                        }
                        
                        // Enable Slack button after successful response
                        setTimeout(() => updateSlackButton(), 100);
                    }
                })
                .catch(error => {
                    removeTypingIndicator();
                    addMessage(`❌ <strong>Error:</strong> Could not get a response. ${error.message}`);
                });
            }
            
            function formatSingleTariffResponse(data) {
                const info = data.tariff_info;
                if (!info || !info.found) {
                    return data.response;
                }
                
                const trendClass = info.trend === 'increased' ? 'trend-up' : 
                                 info.trend === 'decreased' ? 'trend-down' : 'trend-neutral';
                const trendIcon = info.trend === 'increased' ? '⬆️' : 
                                info.trend === 'decreased' ? '⬇️' : '➡️';
                
                return `
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 10px 0;">
                        <h4 style="margin: 0 0 10px 0; color: #2c3e50;">${getCountryFlag(info.country)} ${info.country} - ${info.product_type}</h4>
                        <div style="font-size: 2em; font-weight: bold; color: #667eea; margin: 10px 0;">${info.tariff_percentage}%</div>
                        <p style="margin: 5px 0;"><strong>Effective:</strong> ${info.effective_date || 'Not specified'}</p>
                        ${info.trend ? `<p style="margin: 5px 0; color: ${trendClass === 'trend-up' ? '#e74c3c' : trendClass === 'trend-down' ? '#27ae60' : '#95a5a6'};">${trendIcon} ${info.trend} from ${info.previous_percentage}%</p>` : ''}
                    </div>
                    <div style="margin-top: 15px;">
                        ${data.response}
                    </div>
                `;
            }
            
            function formatComparisonResponse(data) {
                let content = `
                    <h4 style="color: #2c3e50; margin-bottom: 15px;">📊 Comparison Analysis</h4>
                    <div style="margin-bottom: 15px;">
                        ${data.response.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}
                    </div>
                `;
                
                if (data.comparison_data) {
                    content += '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 15px 0;">';
                    
                    data.comparison_data.forEach(item => {
                        if (item.found) {
                            const trendClass = item.trend === 'increased' ? 'trend-up' : 
                                             item.trend === 'decreased' ? 'trend-down' : 'trend-neutral';
                            const trendIcon = item.trend === 'increased' ? '⬆️' : 
                                            item.trend === 'decreased' ? '⬇️' : '➡️';
                            
                            content += `
                                <div style="background: #f8f9fa; padding: 12px; border-radius: 8px; text-align: center; border-left: 4px solid ${getCountryColor(item.country)};">
                                    <h5 style="margin: 0 0 8px 0;">${getCountryFlag(item.country)} ${item.country}</h5>
                                    <div style="font-size: 1.5em; font-weight: bold; color: #667eea; margin: 5px 0;">${item.tariff_percentage}%</div>
                                    <p style="margin: 3px 0; font-size: 0.9em;">${item.product_type}</p>
                                    ${item.trend ? `<p style="margin: 3px 0; font-size: 0.8em; color: ${trendClass === 'trend-up' ? '#e74c3c' : trendClass === 'trend-down' ? '#27ae60' : '#95a5a6'};">${trendIcon} ${item.trend}</p>` : ''}
                                </div>
                            `;
                        }
                    });
                    
                    content += '</div>';
                    content += '<div style="margin: 20px 0;"><canvas id="comparisonChart" style="max-height: 300px;"></canvas></div>';
                }
                
                return content;
            }
            
            function getCountryFlag(country) {
                const flags = {
                    'China': '🇨🇳',
                    'Vietnam': '🇻🇳',
                    'India': '🇮🇳',
                    'Mexico': '🇲🇽',
                    'USA': '🇺🇸'
                };
                return flags[country] || '🌍';
            }
            
            function getCountryColor(country) {
                const colors = {
                    'China': '#e74c3c',
                    'Vietnam': '#27ae60',
                    'India': '#f39c12',
                    'Mexico': '#9b59b6',
                    'USA': '#3498db'
                };
                return colors[country] || '#95a5a6';
            }
            
            function createComparisonChart(messageElement, data) {
                const canvas = messageElement.querySelector('#comparisonChart');
                if (!canvas || !data.comparison_data) return;
                
                if (currentChart) {
                    currentChart.destroy();
                }
                
                const chartData = data.comparison_data.filter(item => item.found);
                if (chartData.length === 0) return;
                
                const labels = chartData.map(item => item.country);
                const rates = chartData.map(item => item.tariff_percentage);
                const colors = chartData.map(item => getCountryColor(item.country));
                
                currentChart = new Chart(canvas, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Tariff Rate (%)',
                            data: rates,
                            backgroundColor: colors.map(color => color + '80'),
                            borderColor: colors,
                            borderWidth: 2
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            title: {
                                display: true,
                                text: `${chartData[0]?.product_type || 'Product'} Tariff Comparison`,
                                font: { size: 14, weight: 'bold' }
                            },
                            legend: { display: false }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: { display: true, text: 'Tariff Rate (%)' }
                            }
                        }
                    }
                });
            }
            
            function sendToSlack() {
                const slackBtn = document.getElementById('slackBtn');
                if (slackBtn.disabled) return;
                
                const chatMessages = document.getElementById('chatMessages');
                const lastBotMessage = chatMessages.querySelector('.message.bot:last-child');
                
                if (!lastBotMessage) {
                    alert('No message to send to Slack!');
                    return;
                }
                
                const messageContent = lastBotMessage.querySelector('.message-content').textContent;
                const userQuery = lastBotMessage.previousElementSibling?.querySelector('.message-content')?.textContent || 'Tariff Analysis';
                
                // Add loading state
                slackBtn.disabled = true;
                slackBtn.innerHTML = '<span>⏳</span>';
                
                fetch('/api/slack/send', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        message: messageContent,
                        query: userQuery
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Show success feedback
                        slackBtn.innerHTML = '<span>✅</span>';
                        setTimeout(() => {
                            slackBtn.innerHTML = '<span>💬</span>';
                            slackBtn.disabled = false;
                        }, 2000);
                    } else {
                        throw new Error(data.error || 'Failed to send to Slack');
                    }
                })
                .catch(error => {
                    console.error('Slack send error:', error);
                    slackBtn.innerHTML = '<span>❌</span>';
                    setTimeout(() => {
                        slackBtn.innerHTML = '<span>💬</span>';
                        slackBtn.disabled = false;
                    }, 2000);
                    alert('Failed to send to Slack: ' + error.message);
                });
            }
            
            function updateSlackButton() {
                const slackBtn = document.getElementById('slackBtn');
                const chatMessages = document.getElementById('chatMessages');
                const lastBotMessage = chatMessages.querySelector('.message.bot:last-child');
                
                // Enable Slack button if there's a recent bot message
                if (lastBotMessage && !lastBotMessage.querySelector('.examples')) {
                    slackBtn.disabled = false;
                    slackBtn.title = 'Send latest analysis to Slack';
                } else {
                    slackBtn.disabled = true;
                    slackBtn.title = 'Send to Slack (no message to send)';
                }
            }
            
            function showContact() {
                // Create a modal to display contact information
                const modal = document.createElement('div');
                modal.style.cssText = `
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    background: rgba(0,0,0,0.8); z-index: 1000; display: flex;
                    align-items: center; justify-content: center;
                `;
                
                const content = document.createElement('div');
                content.style.cssText = `
                    background: white; padding: 30px; border-radius: 15px;
                    max-width: 500px; max-height: 80%; overflow: auto;
                    position: relative; box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                `;
                
                content.innerHTML = `
                    <h2 style="margin-top: 0; color: #2c3e50; text-align: center;">📞 Contact & Community</h2>
                    
                    <div style="text-align: center; margin-bottom: 25px;">
                        <h3 style="color: #667eea; margin: 0 0 10px 0;">Supriya Ramarao Prasanna</h3>
                        <p style="color: #7f8c8d; margin: 0; font-style: italic;">Creator of TariffTok AI</p>
                    </div>
                    
                    <div style="display: grid; gap: 15px;">
                        <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 4px solid #667eea;">
                            <strong style="color: #2c3e50;">🐙 GitHub</strong><br>
                            <a href="https://github.com/supriyarp" target="_blank" style="color: #667eea; text-decoration: none;">
                                @supriyarp
                            </a>
                        </div>
                        
                        <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 4px solid #0077b5;">
                            <strong style="color: #2c3e50;">💼 LinkedIn</strong><br>
                            <a href="https://www.linkedin.com/in/supriya-rp/" target="_blank" style="color: #0077b5; text-decoration: none;">
                                Connect with Supriya
                            </a>
                        </div>
                        
                        <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 4px solid #ff6b35;">
                            <strong style="color: #2c3e50;">🎤 Conference</strong><br>
                            <a href="https://events.techfutures.com/2025/agenda/speakers/3778652" target="_blank" style="color: #ff6b35; text-decoration: none;">
                                Women Who Code TechFutures 2025
                            </a>
                        </div>
                        
                        <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 4px solid #28a745;">
                            <strong style="color: #2c3e50;">📁 Repository</strong><br>
                            <a href="https://github.com/supriyarp/demo-tarifftok-workshop" target="_blank" style="color: #28a745; text-decoration: none;">
                                TariffTok AI Project
                            </a>
                        </div>
                    </div>
                    
                    <div style="margin-top: 25px; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; text-align: center;">
                        <p style="margin: 0; font-size: 14px;">
                            <strong>🌟 Built with ❤️ for the Women Who Code community</strong><br>
                            <span style="font-size: 12px; opacity: 0.9;">Demonstrating advanced agentic AI orchestration patterns</span>
                        </p>
                    </div>
                    
                    <button onclick="this.closest('div').parentNode.remove()" style="
                        position: absolute; top: 15px; right: 15px; background: #e74c3c;
                        color: white; border: none; border-radius: 50%; width: 30px; height: 30px;
                        cursor: pointer; font-size: 16px; display: flex; align-items: center; justify-content: center;
                    ">×</button>
                `;
                
                modal.appendChild(content);
                document.body.appendChild(modal);
                
                // Close modal when clicking outside
                modal.addEventListener('click', (e) => {
                    if (e.target === modal) {
                        modal.remove();
                    }
                });
            }
            
            // Event listeners
            document.getElementById('chatInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
            
            // Add typing animation CSS
            const style = document.createElement('style');
            style.textContent = `
                .typing-dots {
                    display: inline-flex;
                    align-items: center;
                    gap: 4px;
                }
                .typing-dots span {
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    background-color: #667eea;
                    animation: typing 1.4s infinite ease-in-out;
                }
                .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
                .typing-dots span:nth-child(2) { animation-delay: -0.16s; }
                @keyframes typing {
                    0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
                    40% { transform: scale(1); opacity: 1; }
                }
            `;
            document.head.appendChild(style);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint for tariff analysis.
    
    Args:
        request: Chat request with user message
        
    Returns:
        Chat response with analysis results
    """
    try:
        # Run the tariff analysis pipeline
        result = run_tariff_analysis(request.message)
        
        return ChatResponse(
            response=result["response"] or "Analysis completed successfully.",
            tariff_info=result["tariff_info"],
            comparison_data=result["comparison_data"],
            error=result["error"],
            execution_path=result["execution_path"],
            execution_time=result["execution_time"],
            current_node=result["current_node"],
            node_timings=result.get("node_timings"),
            execution_summary=result.get("execution_summary")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Test data loader
        summary = data_loader.get_data_summary()
        return {
            "status": "healthy",
            "data_summary": summary,
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "version": "1.0.0"
        }


@app.get("/api/data/summary")
async def data_summary():
    """Get summary of available tariff data."""
    try:
        return data_loader.get_data_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load data summary: {str(e)}")


@app.get("/api/graph")
async def get_graph(execution_path: str = None):
    """
    Get the LangGraph visualization with optional execution path highlighting.
    
    Args:
        execution_path: Comma-separated list of executed nodes (optional)
        
    Returns:
        Graph visualization data
    """
    try:
        # Parse execution path if provided
        path_list = None
        if execution_path:
            path_list = [node.strip() for node in execution_path.split(',')]
        
        dot_content = get_graph_visualization(path_list)
        return {
            "success": True,
            "dot_content": dot_content,
            "format": "graphviz_dot",
            "execution_path": path_list
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.post("/api/slack/send")
async def send_to_slack(request: dict):
    """
    Send tariff analysis to Slack.
    
    Args:
        request: Dictionary containing 'message' and 'query' fields
    
    Returns:
        Success/failure status
    """
    try:
        # Get Slack webhook URL from environment
        slack_webhook_url = settings.slack_webhook_url if hasattr(settings, 'slack_webhook_url') else None
        
        if not slack_webhook_url:
            return {
                "success": False,
                "error": "Slack webhook URL not configured. Please set SLACK_WEBHOOK_URL environment variable."
            }
        
        # Format the message for Slack
        query = request.get('query', 'Tariff Analysis')
        message = request.get('message', '')
        
        # Create Slack message payload
        slack_payload = {
            "text": f"🏭 *TariffTok AI Analysis*",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🏭 TariffTok AI Analysis"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Query:*\n{query}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Analysis:*\n{message[:1000]}{'...' if len(message) > 1000 else ''}"
                        }
                    ]
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"Generated by TariffTok AI at {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        }
                    ]
                }
            ]
        }
        
        # Send to Slack
        response = requests.post(
            slack_webhook_url,
            json=slack_payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            return {"success": True, "message": "Successfully sent to Slack"}
        else:
            return {
                "success": False,
                "error": f"Slack API returned status {response.status_code}: {response.text}"
            }
            
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Timeout sending to Slack"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
