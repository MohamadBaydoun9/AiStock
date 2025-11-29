"use client"

import { useState, useEffect, use } from "react"
import { useRouter } from 'next/navigation'
import Image from "next/image"
import { ArrowLeft, Save, DollarSign, Hash, Package, Calendar, Heart, Syringe } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { useToast } from "@/hooks/use-toast"
import { api, Product } from "@/lib/api"
import AuthGuard from "@/components/auth-guard"

export default function EditProductPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = use(params)
  const router = useRouter()
  const { toast } = useToast()
  const [product, setProduct] = useState<Product | null>(null)
  const [price, setPrice] = useState<string>("")
  const [quantity, setQuantity] = useState<string>("")

  // Metadata fields
  const [ageMonths, setAgeMonths] = useState<string>("")
  const [weightKg, setWeightKg] = useState<string>("")
  const [healthStatus, setHealthStatus] = useState<string>("1")
  const [vaccinated, setVaccinated] = useState<boolean>(true)
  const [country, setCountry] = useState<string>("USA")

  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)

  useEffect(() => {
    fetchProduct()
  }, [id])

  const fetchProduct = async () => {
    try {
      const data = await api.getProduct(id)
      setProduct(data)
      setPrice((data.price_modified ?? data.price_predicted).toString())
      setQuantity(data.quantity.toString())

      // Set metadata if available (check for both null and undefined)
      if (data.age_months != null) setAgeMonths(data.age_months.toString())
      if (data.weight_kg != null) setWeightKg(data.weight_kg.toString())
      if (data.health_status != null) setHealthStatus(data.health_status.toString())
      if (data.vaccinated != null) setVaccinated(data.vaccinated)
      if (data.country) setCountry(data.country)
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load product",
        variant: "destructive"
      })
      console.error('Fetch error:', error)
      router.push('/dashboard')
    } finally {
      setIsLoading(false)
    }
  }

  const handleSave = async () => {
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
      const token = localStorage.getItem('token')

      // Build update payload
      const updateData: any = {
        price_modified: priceNum,
        quantity: quantityNum,
      }

      // Add metadata if provided
      if (ageMonths) {
        const age = parseInt(ageMonths)
        if (!isNaN(age) && age > 0) updateData.age_months = age
      }
      if (weightKg) {
        const weight = parseFloat(weightKg)
        if (!isNaN(weight) && weight > 0) updateData.weight_kg = weight
      }
      if (healthStatus) {
        updateData.health_status = parseInt(healthStatus)
      }
      updateData.vaccinated = vaccinated
      updateData.country = country

      const response = await fetch(`http://localhost:8000/products/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(updateData),
      })

      if (!response.ok) throw new Error('Failed to update product')

      toast({
        title: "Changes Saved",
        description: "Product has been updated successfully",
      })

      router.push('/dashboard')
    } catch (error) {
      toast({
        title: "Save Failed",
        description: "Unable to save changes",
        variant: "destructive"
      })
      console.error('Update error:', error)
    } finally {
      setIsSaving(false)
    }
  }

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center py-12 text-muted-foreground">
          Loading product...
        </div>
      </div>
    )
  }

  if (!product) {
    return null
  }

  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <Button
          variant="ghost"
          onClick={() => router.push(`/products/${id}`)}
          className="mb-6"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Product Details
        </Button>

        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold mb-3 text-balance">Edit Product</h1>
          <p className="text-muted-foreground text-lg text-pretty">
            Update pricing, inventory, and metadata information
          </p>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          {/* Product Preview */}
          <Card className="border-2">
            <CardHeader>
              <CardTitle>Product Information</CardTitle>
              <CardDescription>
                Read-only product details
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="relative w-full aspect-square rounded-lg overflow-hidden border-2 border-border bg-muted">
                {product.has_image ? (
                  <img
                    src={`http://localhost:8000/products/${product.product_id}/image`}
                    alt={product.product_name}
                    className="object-cover w-full h-full"
                  />
                ) : (
                  <div className="flex items-center justify-center h-full bg-muted text-muted-foreground">
                    <Package className="h-16 w-16" />
                  </div>
                )}
              </div>

              <div className="space-y-3">
                <div className="flex flex-col gap-1.5 p-3 rounded-lg bg-muted">
                  <span className="text-xs font-medium text-muted-foreground">Product Name</span>
                  <span className="font-semibold">{product.product_name}</span>
                </div>

                <div className="flex flex-col gap-1.5 p-3 rounded-lg bg-muted">
                  <span className="text-xs font-medium text-muted-foreground">Product Type</span>
                  <span className="font-semibold">{product.product_type}</span>
                </div>

                <div className="flex flex-col gap-1.5 p-3 rounded-lg bg-primary/10 border border-primary/20">
                  <span className="text-xs font-medium text-muted-foreground">AI Predicted Price</span>
                  <span className="text-xl font-bold text-primary">
                    ${product.price_predicted.toFixed(2)}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Edit Form */}
          <Card className="border-2">
            <CardHeader>
              <CardTitle>Editable Fields</CardTitle>
              <CardDescription>
                Modify price, quantity, and metadata
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Price */}
              <div className="space-y-2">
                <Label htmlFor="price" className="flex items-center gap-2">
                  <DollarSign className="h-4 w-4 text-muted-foreground" />
                  Price
                </Label>
                <Input
                  id="price"
                  type="number"
                  step="0.01"
                  min="0"
                  placeholder="0.00"
                  value={price}
                  onChange={(e) => setPrice(e.target.value)}
                />
              </div>

              {/* Quantity */}
              <div className="space-y-2">
                <Label htmlFor="quantity" className="flex items-center gap-2">
                  <Hash className="h-4 w-4 text-muted-foreground" />
                  Quantity
                </Label>
                <Input
                  id="quantity"
                  type="number"
                  min="1"
                  placeholder="0"
                  value={quantity}
                  onChange={(e) => setQuantity(e.target.value)}
                />
              </div>

              <div className="pt-2 border-t">
                <h3 className="font-semibold mb-3 text-sm text-muted-foreground">Metadata (Optional)</h3>

                {/* Age */}
                <div className="space-y-2 mb-3">
                  <Label htmlFor="age" className="flex items-center gap-2">
                    <Calendar className="h-4 w-4 text-muted-foreground" />
                    Age (months)
                  </Label>
                  <Input
                    id="age"
                    type="number"
                    min="1"
                    max="120"
                    placeholder="e.g., 6"
                    value={ageMonths}
                    onChange={(e) => setAgeMonths(e.target.value)}
                  />
                </div>

                {/* Weight */}
                <div className="space-y-2 mb-3">
                  <Label htmlFor="weight" className="flex items-center gap-2">
                    <Package className="h-4 w-4 text-muted-foreground" />
                    Weight (kg)
                  </Label>
                  <Input
                    id="weight"
                    type="number"
                    step="0.1"
                    min="0.1"
                    max="200"
                    placeholder="e.g., 10.5"
                    value={weightKg}
                    onChange={(e) => setWeightKg(e.target.value)}
                  />
                </div>

                {/* Health Status */}
                <div className="space-y-2 mb-3">
                  <Label htmlFor="health" className="flex items-center gap-2">
                    <Heart className="h-4 w-4 text-muted-foreground" />
                    Health Status
                  </Label>
                  <Select value={healthStatus} onValueChange={setHealthStatus}>
                    <SelectTrigger id="health">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="0">Normal</SelectItem>
                      <SelectItem value="1">Good</SelectItem>
                      <SelectItem value="2">Excellent</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* Vaccinated */}
                <div className="flex items-center space-x-2 mb-3">
                  <input
                    type="checkbox"
                    id="vaccinated"
                    checked={vaccinated}
                    onChange={(e) => setVaccinated(e.target.checked)}
                    className="h-4 w-4 rounded border-gray-300"
                  />
                  <Label htmlFor="vaccinated" className="flex items-center gap-2 cursor-pointer">
                    <Syringe className="h-4 w-4 text-muted-foreground" />
                    Vaccinated
                  </Label>
                </div>

                {/* Country */}
                <div className="space-y-2">
                  <Label htmlFor="country">Country of Origin</Label>
                  <Select value={country} onValueChange={setCountry}>
                    <SelectTrigger id="country">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="USA">USA</SelectItem>
                      <SelectItem value="Canada">Canada</SelectItem>
                      <SelectItem value="England">England</SelectItem>
                      <SelectItem value="Scotland">Scotland</SelectItem>
                      <SelectItem value="France">France</SelectItem>
                      <SelectItem value="Germany">Germany</SelectItem>
                      <SelectItem value="Iran">Iran</SelectItem>
                      <SelectItem value="Thailand">Thailand</SelectItem>
                      <SelectItem value="Russia">Russia</SelectItem>
                      <SelectItem value="Afghanistan">Afghanistan</SelectItem>
                      <SelectItem value="Ethiopia">Ethiopia</SelectItem>
                      <SelectItem value="Africa">Africa</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="pt-4 border-t border-border">
                <div className="flex items-center justify-between text-sm mb-4">
                  <span className="text-muted-foreground">Estimated Total Value</span>
                  <span className="text-xl font-bold text-primary">
                    ${((parseFloat(price) || 0) * (parseInt(quantity) || 0)).toFixed(2)}
                  </span>
                </div>

                <div className="space-y-3">
                  <Button
                    onClick={handleSave}
                    disabled={isSaving || !price || !quantity}
                    size="lg"
                    className="w-full"
                  >
                    <Save className="mr-2 h-4 w-4" />
                    {isSaving ? 'Saving Changes...' : 'Save Changes'}
                  </Button>

                  <Button
                    onClick={() => router.push(`/products/${id}`)}
                    variant="outline"
                    size="lg"
                    className="w-full"
                  >
                    Cancel
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </AuthGuard>
  )
}
