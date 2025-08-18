import { NextResponse } from "next/server"

// This is a mock implementation - replace with your actual backend API endpoint
const BACKEND_API_URL = process.env.BACKEND_API_URL || "http://localhost:8000"

export async function GET() {
  try {
    // Call your backend API
    const response = await fetch(`${BACKEND_API_URL}/websites`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })

    if (!response.ok) {
      throw new Error(`Backend API error: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error("Websites API error:", error)
    return NextResponse.json({ error: "Failed to fetch websites" }, { status: 500 })
  }
}
