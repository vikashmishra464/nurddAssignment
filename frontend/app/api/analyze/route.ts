import { type NextRequest, NextResponse } from "next/server"

// This is a mock implementation - replace with your actual backend API endpoint
const BACKEND_API_URL = process.env.BACKEND_API_URL || "http://localhost:8000"

export async function POST(request: NextRequest) {
  try {
    const { url } = await request.json()

    if (!url) {
      return NextResponse.json({ error: "URL is required" }, { status: 400 })
    }

    // Call your backend API
    const response = await fetch(`${BACKEND_API_URL}/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }),
    })

    if (!response.ok) {
      throw new Error(`Backend API error: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error("Analyze API error:", error)
    return NextResponse.json({ error: "Failed to analyze website" }, { status: 500 })
  }
}
