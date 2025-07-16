import type { NextApiRequest, NextApiResponse } from "next";
import axios from "axios";
const backendUrl = `${process.env.NEXT_PUBLIC_BACKEND_URL}/chat`;

type Data = {
    response?: string;
    error?: string;
};

export default async function handler(
    req: NextApiRequest,
    res: NextApiResponse<Data>
) {
    if (req.method !== "POST") {
        return res.status(405).json({ error: "Method not allowed" });
    }

    const { message, mode } = req.body;

    if (!message || !mode) {
        return res.status(400).json({ error: 'Message and mode are required' });
    }

    try {
        const response = await axios.post(backendUrl, { message, mode });
        return res.status(200).json({ response: response.data.response });
    } catch (error) {
        console.error("Error in chatbot API:", error);

        // Extract error message
        let errorMessage = "Failed to fetch response from AI";
        if (axios.isAxiosError(error)) {
            errorMessage = error.response?.data?.error || error.message;
        } else if (error instanceof Error) {
            errorMessage = error.message;
        }

        return res.status(500).json({ error: errorMessage });
    }
}
