// src/services/geminiService.js (CORRIGIDO E FINAL)

export async function callGemini(prompt, schema) {
    //
    // Certifique-se de que a sua chave de API está colada aqui
    //
    const apiKey = "AIzaSyDfP9J9VfBqjiJvgtNvjl4d3Bh3ElUc6Yc";
    //
    //

    if (!apiKey || apiKey === "AIzaSyDfP9J9VfBqjiJvgtNvjl4d3Bh3ElUc6Yc") {
        console.error("A chave da API da Gemini não foi definida em geminiService.js.");
        // Rejeita a promessa para que o componente possa apanhar o erro
        return Promise.reject("A chave da API da Gemini não está configurada.");
    }

    // URL CORRIGIDA com o modelo "gemini-1.5-flash-latest"
    const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=${apiKey}`;

    const payload = {
        contents: [{ role: "user", parts: [{ text: prompt }] }],
        generationConfig: {
            responseMimeType: "application/json",
            responseSchema: schema
        }
    };

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorBody = await response.json();
            // Lança um erro mais detalhado com a mensagem da API
            throw new Error(`A API retornou um erro: ${errorBody.error.message}`);
        }
        
        const result = await response.json();
        
        if (result.candidates && result.candidates[0].content.parts.length > 0) {
            // A resposta da API está dentro de `parts[0].text`
            return JSON.parse(result.candidates[0].content.parts[0].text);
        } else {
            throw new Error("Estrutura de resposta inválida da API Gemini.");
        }
    } catch (error) {
        console.error('Erro ao chamar a API Gemini:', error);
        // Rejeita a promessa com a mensagem de erro para que o componente a possa exibir
        return Promise.reject(error.message);
    }
}