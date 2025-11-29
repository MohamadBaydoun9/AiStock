import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const image = formData.get('image') as File

    if (!image) {
      return NextResponse.json(
        { error: 'No image provided' },
        { status: 400 }
      )
    }

    // TODO: Replace with actual FastAPI endpoint
    // const apiFormData = new FormData()
    // apiFormData.append('image', image)
    // const response = await fetch('YOUR_FASTAPI_URL/api/classify', {
    //   method: 'POST',
    //   body: apiFormData,
    // })
    // const result = await response.json()

    // Mock response for demonstration
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    const mockResults = [
      { productType: 'Fruit', productName: 'Red Apple', predictedPrice: 2.49 },
      { productType: 'Vegetable', productName: 'Organic Carrot', predictedPrice: 1.99 },
      { productType: 'Electronics', productName: 'Wireless Mouse', predictedPrice: 24.99 },
      { productType: 'Beverage', productName: 'Orange Juice', predictedPrice: 4.99 },
    ]
    
    const randomResult = mockResults[Math.floor(Math.random() * mockResults.length)]

    return NextResponse.json(randomResult)
  } catch (error) {
    console.error('Classification error:', error)
    return NextResponse.json(
      { error: 'Classification failed' },
      { status: 500 }
    )
  }
}
