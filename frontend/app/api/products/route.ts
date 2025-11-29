import { NextRequest, NextResponse } from 'next/server'
import type { Product } from '@/lib/types'

// Mock storage using global variable (replace with MongoDB)
const getProducts = (): Product[] => {
  if (typeof window === 'undefined') {
    if (!(global as any).mockProducts) {
      (global as any).mockProducts = []
    }
    return (global as any).mockProducts
  }
  return []
}

export async function GET(request: NextRequest) {
  try {
    const products = getProducts()
    return NextResponse.json(products)
  } catch (error) {
    console.error('Get products error:', error)
    return NextResponse.json(
      { error: 'Failed to fetch products' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const products = getProducts()

    const newProduct: Product = {
      _id: Date.now().toString(),
      ...body,
    }

    products.push(newProduct)

    return NextResponse.json(newProduct, { status: 201 })
  } catch (error) {
    console.error('Create product error:', error)
    return NextResponse.json(
      { error: 'Failed to create product' },
      { status: 500 }
    )
  }
}
