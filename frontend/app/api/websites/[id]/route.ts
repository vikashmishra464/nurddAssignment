import { type NextRequest, NextResponse } from "next/server"

// This is a mock implementation - replace with your actual backend API endpoint
const BACKEND_API_URL = process.env.BACKEND_API_URL || "http://localhost:8000"

export async function PUT(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const { description } = await request.json()
    const { id } = params

    if (!description) {
      return NextResponse.json({ error: "Description is required" }, { status: 400 })
    }

    // Call your backend API
    const response = await fetch(`${BACKEND_API_URL}/websites/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ description }),
    })

    if (!response.ok) {
      throw new Error(`Backend API error: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error("Update website API error:", error)
    return NextResponse.json({ error: "Failed to update website" }, { status: 500 })
  }
}

export async function DELETE(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const { id } = params

    // Call your backend API
    const response = await fetch(`${BACKEND_API_URL}/websites/${id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    })

    if (!response.ok) {
      throw new Error(`Backend API error: ${response.status}`)
    }

    return NextResponse.json({ success: true })
  } catch (error) {
    console.error("Delete website API error:", error)
    return NextResponse.json({ error: "Failed to delete website" }, { status: 500 })
  }
}
