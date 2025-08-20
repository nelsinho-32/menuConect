// src/services/geminiService.js (CORRIGIDO E FINAL)

export async function callGemini(prompt, schema) {
    //
    // Certifique-se de que a sua chave de API está colada aqui
    //
    const apiKey = import.meta.env.VITE_GEMINI_API_KEY;
    //
    //

    if (!apiKey || apiKey === "AIzaSyDpP6keoBAQ00zgopadEBXv_QzgOZOCPeY") {
        console.error("A chave da API da Gemini não foi definida em geminiService.js.");
        // Rejeita a promessa para que o componente possa apanhar o erro
        return Promise.reject("A chave da API da Gemini não está configurada.");
    }

    // URL CORRIGIDA com o modelo "gemini-2.5-flash-latest"
    const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-latest:generateContent?key=${apiKey}`;

    const payload = {
        contents: [{ role: "user", parts: [{ text: prompt }] }],
        generationConfig: {
            responseMimeType: "application/json",
            responseSchema: schema
        }
    };

    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 segundos

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
            signal: controller.signal
        });
        clearTimeout(timeoutId);

        if (!response.ok) {
            const errorBody = await response.json();
            // Lança um erro mais detalhado com a mensagem da API
            throw new Error(`A API retornou um erro: ${errorBody.error.message}`);
        }
        
        const result = await response.json();
        
        if (!result.candidates || !result.candidates[0]?.content?.parts?.length) {
            throw new Error("Estrutura de resposta inválida da API Gemini.");
        }

        // A resposta da API está dentro de `parts[0].text`
        return JSON.parse(result.candidates[0].content.parts[0].text);
        
    } catch (error) {
        console.error('Erro ao chamar a API Gemini:', error);
        // Rejeita a promessa com a mensagem de erro para que o componente a possa exibir
        return Promise.reject({ message: error.message, status: response.status });
    }
}