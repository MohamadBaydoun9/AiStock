"use client"

import { useState, useEffect } from "react"
import { useRouter } from 'next/navigation'
import Image from "next/image"
import { Package, DollarSign, Hash, Save, X } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useToast } from "@/hooks/use-toast"
import type { ClassificationResult } from "@/lib/types"
import { api } from "@/lib/api"
import AuthGuard from "@/components/auth-guard"

export default function AddProductPage() {
  const router = useRouter()
  const { toast } = useToast()
  const [classificationData, setClassificationData] = useState<ClassificationResult | null>(null)
  const [price, setPrice] = useState<string>("")
  const [quantity, setQuantity] = useState<string>("")
  const [isSaving, setIsSaving] = useState(false)

  useEffect(() => {
    // Retrieve classification result from sessionStorage
    const storedData = sessionStorage.getItem('classificationResult')
    if (storedData) {
      const data: ClassificationResult = JSON.parse(storedData)
      setClassificationData(data)
      setPrice(data.predictedPrice.toString())
    } else {
      // If no data, redirect back to upload
      toast({
        title: "No product data found",
        description: "Please upload a product image first",
        variant: "destructive"
      })
      router.push('/upload')
    }
  }, [router, toast])

  const handleSave = async () => {
    if (!classificationData) return

    const priceNum = parseFloat(price)
    const quantityNum = parseInt(quantity)

    // Validation
    if (isNaN(priceNum) || priceNum <= 0) {
      toast({
        title: "Invalid Price",
        description: "Please enter a valid price greater than 0",
        variant: "destructive"
      })
      return
    }

    if (isNaN(quantityNum) || quantityNum <= 0) {
      toast({
        title: "Invalid Quantity",
        description: "Please enter a valid quantity greater than 0",
        variant: "destructive"
      })
      return
    }

    setIsSaving(true)

    try {
      const formData = new FormData()
      formData.append('product_type', classificationData.productType)
      formData.append('product_name', classificationData.productName)
      formData.append('price_predicted', classificationData.predictedPrice.toString())
      formData.append('price_modified', priceNum.toString())
      formData.append('quantity', quantityNum.toString())

      // Add metadata if available
      if (classificationData.metadata) {
        if (classificationData.metadata.age_months !== undefined) {
          formData.append('age_months', classificationData.metadata.age_months.toString())
        }
        if (classificationData.metadata.weight_kg !== undefined) {
          formData.append('weight_kg', classificationData.metadata.weight_kg.toString())
        }
        if (classificationData.metadata.health_status !== undefined) {
          formData.append('health_status', classificationData.metadata.health_status.toString())
        }
        if (classificationData.metadata.vaccinated !== undefined) {
          formData.append('vaccinated', classificationData.metadata.vaccinated.toString())
        }
        if (classificationData.metadata.country) {
          formData.append('country', classificationData.metadata.country)
        }
      }

      if (classificationData.predictedBreed) {
        formData.append('predicted_breed', classificationData.predictedBreed)
      }
      if (classificationData.predictionConfidence) {
        formData.append('prediction_confidence', classificationData.predictionConfidence.toString())
      }

      if (classificationData.imageUrl) {
        const response = await fetch(classificationData.imageUrl);
        const blob = await response.blob();
        formData.append('image', blob, 'product_image.jpg');
      }

      await api.createProduct(formData)

      // Clear sessionStorage
      sessionStorage.removeItem('classificationResult')

      toast({
        title: "Product Saved",
        description: "Product has been added to your inventory",
      })

      router.push('/dashboard')
    } catch (error) {
      toast({
        title: "Save Failed",
        description: "Unable to save product. Please try again.",
        variant: "destructive"
      })
      console.error('Save error:', error)
    } finally {
      setIsSaving(false)
    }
  }

  const handleCancel = () => {
    sessionStorage.removeItem('classificationResult')
    router.push('/dashboard')
  }

  if (!classificationData) {
    return null
  }

  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold mb-3 text-balance">Add Product to Inventory</h1>
          <p className="text-muted-foreground text-lg text-pretty">
            Review and adjust product details before saving
          </p>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          {/* Product Preview */}
          <Card className="border-2">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Package className="h-5 w-5 text-primary" />
                Product Preview
              </CardTitle>
              <CardDescription>
                AI-detected product information
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="relative w-full aspect-square rounded-lg overflow-hidden border-2 border-border bg-muted">
                <Image
                  src={classificationData.imageUrl || "/placeholder.svg"}
                  alt={classificationData.productName}
                  fill
                  className="object-cover"
                />
              </div>

              <div className="space-y-3">
                <div className="flex flex-col gap-1.5 p-3 rounded-lg bg-muted">
                  <span className="text-xs font-medium text-muted-foreground">Product Type</span>
                  <span className="font-semibold">{classificationData.productType}</span>
                </div>

                <div className="flex flex-col gap-1.5 p-3 rounded-lg bg-muted">
                  <span className="text-xs font-medium text-muted-foreground">Product Name</span>
                  <span className="font-semibold">{classificationData.productName}</span>
                </div>

                <div className="flex flex-col gap-1.5 p-3 rounded-lg bg-primary/10 border border-primary/20">
                  <span className="text-xs font-medium text-muted-foreground">AI Predicted Price</span>
                  <span className="text-xl font-bold text-primary">
                    ${classificationData.predictedPrice.toFixed(2)}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Product Details Form */}
          <Card className="border-2">
            <CardHeader>
              <CardTitle>Product Details</CardTitle>
              <CardDescription>
                Enter pricing and inventory information
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="price" className="flex items-center gap-2">
                  <DollarSign className="h-4 w-4 text-muted-foreground" />
                  Selling Price
                </Label>
                <Input
                  id="price"
                  type="number"
                  step="0.01"
                  min="0"
                  placeholder="0.00"
                  value={price}
                  onChange={(e) => setPrice(e.target.value)}
                  className="text-lg"
                />
                <p className="text-xs text-muted-foreground">
                  You can adjust the AI-predicted price
                </p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="quantity" className="flex items-center gap-2">
                  <Hash className="h-4 w-4 text-muted-foreground" />
                  Quantity in Stock
                </Label>
                <Input
                  id="quantity"
                  type="number"
                  min="1"
                  placeholder="0"
                  value={quantity}
                  onChange={(e) => setQuantity(e.target.value)}
                  className="text-lg"
                />
                <p className="text-xs text-muted-foreground">
                  How many units do you have available?
                </p>
              </div>

              <div className="pt-4 space-y-3">
                <Button
                  onClick={handleSave}
                  disabled={isSaving || !price || !quantity}
                  size="lg"
                  className="w-full"
                >
                  <Save className="mr-2 h-4 w-4" />
                  {isSaving ? 'Saving...' : 'Save to Inventory'}
                </Button>

                <Button
                  onClick={handleCancel}
                  variant="outline"
                  size="lg"
                  className="w-full"
                >
                  <X className="mr-2 h-4 w-4" />
                  Cancel
                </Button>
              </div>

              <div className="pt-4 border-t border-border">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Product Type:</span>
                  <span className="font-medium">{classificationData.productType}</span>
                </div>
                <div className="flex items-center justify-between text-sm mt-2">
                  <span className="text-muted-foreground">Product Name:</span>
                  <span className="font-medium">{classificationData.productName}</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </AuthGuard>
  )
}
