import { NextRequest, NextResponse } from 'next/server'
import type { Product } from '@/lib/types'

// Import the mock storage (in real app, this would be MongoDB)
// This is a workaround for the mock - in production use a database
const getProducts = (): Product[] => {
  if (typeof window === 'undefined') {
    // Server-side: use a global variable
    if (!(global as any).mockProducts) {
      (global as any).mockProducts = []
    }
    return (global as any).mockProducts
  }
  return []
}

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params
    const products = getProducts()
    
    // TODO: Replace with actual MongoDB query
    // const db = await connectToDatabase()
    // const product = await db.collection('products').findOne({ _id: new ObjectId(id) })

    const product = products.find(p => p._id === id)

    if (!product) {
      return NextResponse.json(
        { error: 'Product not found' },
        { status: 404 }
      )
    }

    return NextResponse.json(product)
  } catch (error) {
    console.error('Get product error:', error)
    return NextResponse.json(
      { error: 'Failed to fetch product' },
      { status: 500 }
    )
  }
}

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params
    const body = await request.json()
    const products = getProducts()

    // TODO: Replace with actual MongoDB update
    // const db = await connectToDatabase()
    // const result = await db.collection('products').updateOne(
    //   { _id: new ObjectId(id) },
    //   { $set: body }
    // )

    const index = products.findIndex(p => p._id === id)
    if (index === -1) {
      return NextResponse.json(
        { error: 'Product not found' },
        { status: 404 }
      )
    }

    products[index] = { ...products[index], ...body }

    return NextResponse.json(products[index])
  } catch (error) {
    console.error('Update product error:', error)
    return NextResponse.json(
      { error: 'Failed to update product' },
      { status: 500 }
    )
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params
    const products = getProducts()

    // TODO: Replace with actual MongoDB delete
    // const db = await connectToDatabase()
    // const result = await db.collection('products').deleteOne({ _id: new ObjectId(id) })

    const index = products.findIndex(p => p._id === id)
    if (index === -1) {
      return NextResponse.json(
        { error: 'Product not found' },
        { status: 404 }
      )
    }

    products.splice(index, 1)

    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('Delete product error:', error)
    return NextResponse.json(
      { error: 'Failed to delete product' },
      { status: 500 }
    )
  }
}
