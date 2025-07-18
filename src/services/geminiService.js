export async function callGemini(prompt, schema) {
    const apiKey = ""; // Será fornecida pelo ambiente
    const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
    
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

        if (!response.ok) throw new Error(`API request failed with status ${response.status}`);
        
        const result = await response.json();
        
        if (result.candidates && result.candidates[0].content.parts.length > 0) {
            return JSON.parse(result.candidates[0].content.parts[0].text);
        } else {
            throw new Error("Invalid response structure from Gemini API");
        }
    } catch (error) {
        console.error('Error calling Gemini API:', error);
        return null;
    }
}